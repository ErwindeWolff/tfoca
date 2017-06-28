from variables import *
from variableElimination import * 
from sampler import *
from agents import *
from predProc import *
from tqdm import *

import os
import matplotlib.pyplot as plt
import numpy as np

# Specific Model imports
from babybot import *
from coinflip import *
from die import *
from funnel import *
from tree import *
from layered import *

from random import *



def getEvidence(model, hypo, pred, chance=0.1):

	evidence = list()

	variables = list()
	for var in model:
		if (var not in hypo) and (var not in pred):
			variables.append(var)
			
	for var in variables:
		if random() <= chance:
			value = var.values[randint(0, len(var.values)-1)]
			evidence.append( (var.names[0], value) ) 
			
	return evidence



'''
	Function to run multiple simulations and plot them all
'''
def runAllCombinations(name, network, context, epochs, nr_samples, nr_hypo_samples):

	# Plot Figure
	x = [i for i in range(len(context))]

	for samples in nr_samples:
		for hypo_samples in nr_hypo_samples:

			meanStdPlot(name, network, context, epochs, samples, hypo_samples, True, True, runs=10)
			meanStdPlot(name, network, context, epochs, samples, hypo_samples, True, False, runs=10)
	
	#meanStdPlot(name, network, context, epochs, samples, hypo_samples, False, True, runs=1)
	#meanStdPlot(name, network, context, epochs, samples, hypo_samples, False, False, runs=1)



def meanStdPlot(name, network, context, epochs, nr_samples, nr_hypo_samples, use_sampling, use_weighting, runs=10):
	
	errs = list()
	
	for _ in tqdm(range(runs)):
		err = runSimulation(name, network, context,
							epochs, nr_samples, nr_hypo_samples, use_sampling, use_weighting)
							
		errs.append(err)
		
	mean_err = list()
	std_err_high = list()
	std_err_low = list()
	
	for i in range(len(errs[0])):
	
		column = list()
		for j in range(len(errs)):
			column.append(errs[j][i])
		
		mean_column = np.asarray(column).mean()
		std_column = np.asarray(column).std()
		
		#print(mean_column, std_column)
		
		mean_err.append(mean_column)
		std_err_high.append(mean_column + 2*std_column)
		std_err_low.append(mean_column - 2*std_column)
	
	x = range(len(context))
	
	saveImage(name, x, [std_err_high, std_err_low, mean_err],
				nr_hypo_samples, nr_samples, use_sampling, use_weighting)



def runSimulation(name, network, context, epochs, nr_samples, nr_hypo_samples, use_sampling, use_weighting):
				
	# Unpack variables from network
	model = network.model
	hypo = network.hypothesisNodes
	pred = network.predictionNodes
	world = network.world
	query = network.query
	goal = network.goal
		
	# Reset hyperpriors (allows multiple subsequent runs)
	for var in pred:
		var.reset()
				
	# Make agent
	if use_sampling:
		if use_weighting:
			a = SamplingAgent(model, hypo, pred, nr_hypo_samples, nr_samples, use_weighting=True)
		else:
			a = SamplingAgent(model, hypo, pred, nr_hypo_samples, nr_samples, use_weighting=False)
	else:
		if use_weighting:
			a = DeterministicAgent(model, hypo, pred, use_weighting=True)
		else:
			a = DeterministicAgent(model, hypo, pred, use_weighting=False)

	err = []
	for influence in context:
	
		# Gather evidence for observation
		evidence = getEvidence(model, hypo, pred, chance=0.1)
		evidence = evidence + [("Context", influence)]

		# Let agent make prediction
		(full_table, small_table, hypothesis) = a.makePrediction(query, goal, evidence)

		# Get observation from world (1 sample)
		(_, observation) = rejectionSampling(world, query, evidence + hypothesis, 1, bias=0.0)
		observation = observation[2]
			
		# Calculate and save prediction error
		prediction_error = KLD(observation, small_table[2])
		err.append(prediction_error)

		# Update all hyperpriors
		for value_row, prob_row in zip(full_table[1], full_table[2]):
		
			# Create key
			if (type(value_row) is list):
				key = "_"
				for v in value_row[1:]:
					key += v + "_"
				value_row = key
		
			# Multiply observation with probability they influenced
			update = [ob * prob_row for ob in observation]
			a.updateModel(query, value_row, update, prediction_error)

	return err



def saveImage(name, x, ys, nr_hypo_samples, nr_samples, use_sampling, use_weighting):

	plt.figure()
	plt.axis([-2, epochs+2, -0.01, 10.01])
	
	plt.ylabel('Prediction Error (sum {0})'.format( int(100*sum(ys[-1]))/100.0))
	plt.xlabel('Nr Observations')
	
	for i, y in enumerate(ys):
		if (i == len(ys)-1):	
			plt.plot(x, y, color='OrangeRed')
		else:
			plt.plot(x, y, color='LightSalmon')

	if not os.path.isdir("Results/{0}".format(name)):
		os.makedirs("Results/{0}".format(name))

	if use_sampling:
		if use_weighting:
			plt.title("Sampling with weighting ({0} hypotheses, {1} samples)".format(nr_hypo_samples, nr_samples))
			plt.savefig('Results/{0}/sample_weight_{1}_hypotheses_{2}_samples.png'.format(name, nr_hypo_samples, nr_samples))
		else:
			plt.title("Sampling without weighting ({0} hypotheses, {1} samples)".format(nr_hypo_samples, nr_samples))

			plt.savefig('Results/{0}/sample_no_weight_{1}_hypotheses_{2}_samples.png'.format(name, nr_hypo_samples, nr_samples))
	else:
		if use_weighting:
			plt.title("Normative with weighting")
			plt.savefig('Results/{0}/normative_weight.png'.format(name))
		else:
			plt.title("Normative without weighting")
			plt.savefig('Results/{0}/normative_no_weight.png'.format(name))
	
	plt.close()



'''
	DEFINE EXPERIMENTAL VALUES
'''

# Save name
#name = "coinflip_with_world"
#name = "babybot"
#name = "Dice_test"
name = "Tree"

# Define network
#network = CoinflipModel()
#network = BabybotModel()
#network = DieModel()
network = TreeModel()

# Set numbers of epochs
epochs = 200

# Set data style
style = "homogenous"
#style = "sorted"
#style = "randomized"

# Define context: 1 is homogenous, 2 is sorted, 3 is randomized
if (style == "homogenous"):
	name += "_homogenous"
	context = network.getContext(epochs, distribution=1)
elif (style == "sorted"):
	name += "_sorted"
	context = network.getContext(epochs, distribution=2)
else:
	name += "_randomized"
	context = network.getContext(epochs, distribution=3)


# Parameters for sampling
nr_hypo_samples = [10]
nr_samples = [2, 8, 32, 128, 512]

runAllCombinations(name, network, context, epochs, nr_samples, nr_hypo_samples)

