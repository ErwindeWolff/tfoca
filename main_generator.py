from variables import *
from variableElimination import * 
from sampler import *
from agents import *
from predProc import *
from tqdm import *

import os
import matplotlib.pyplot as plt

# Specific Model imports
from babybot import *
from coinflip import *
from die import *

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
	for influence in tqdm(context):
	
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




def saveImage(name, x, y, nr_hypo_samples, nr_samples, use_sampling, use_weighting):

	plt.figure()
	plt.axis([-2, epochs+2, -0.01, 15.51])
	plt.plot(x, y)

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
	Function to run multiple simulations and plot them all
'''
def runAllCombinations(name, network, context, epochs, nr_samples, nr_hypo_samples):

	# Plot Figure
	x = [i for i in range(epochs)]

	for samples in nr_samples:
		for hypotheses in nr_hypo_samples:

			err = runSimulation(name, network, context,
							epochs, samples, hypotheses, True, True)
							
			saveImage(name, x, err, hypotheses, samples, True, True)


			err = runSimulation(name, network, context,
							epochs, samples, hypotheses, True, False)
			saveImage(name, x, err, hypotheses, samples, True, False)
				
				
	err = runSimulation(name, network, context,
							epochs, 0, 0, False, True)
	saveImage(name, x, err, hypotheses, samples, False, True)
	
							
	err = runSimulation(name, network, context,
							epochs, 0, 0, False, False)
	saveImage(name, x, err, hypotheses, samples, False, False)



# Save name
#name = "coinflip_with_world"
#name = "babybot"
name = "Dice_test2"

# Define network
#network = CoinflipModel()
#network = BabybotModel()
network = DieModel()

# Set numbers of epochs
epochs = 100

# Set data style
#style = "homogenous"
style = "sorted"
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
nr_hypo_samples = [5, 10, 100]
nr_samples = [5, 10, 100]

runAllCombinations(name, network, context, epochs, nr_samples, nr_hypo_samples)



