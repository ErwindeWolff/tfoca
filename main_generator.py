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

from random import shuffle




def runSimulation(name, network, context, epochs, nr_samples, nr_hypo_samples, use_sampling, use_weighting):
				
	# Unpack variables from network
	model = network.model
	hypo = network.hypothesisNodes
	pred = network.predictionNodes
	world = network.world
	query = network.query
	goal = network.goal
		
	# Reset hyperpriors		
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
	
		evidence = []
		
		evidence = evidence + [("Context", influence)]

		# Let agent make prediction
		(full_table, small_table, hypothesis) = a.makePrediction(query, goal, evidence)

		# Get observation from world (1 sample)
		(_, observation) = rejectionSampling(world, query, evidence + hypothesis, 1, bias=0.0)
		observation = observation[2]
			
		# Calculate and save prediction error
		prediction_error = KLD(observation, small_table[2])
		err.append(prediction_error)

		for value_row, prob_row in zip(full_table[1], full_table[2]):
		
			if (type(value_row) is list):
				key = "_"
				for v in value_row[1:]:
					key += v + "_"
				value_row = key
		
			update = [ob * prob_row for ob in observation]
			a.updateModel(query, value_row, update, prediction_error)

	# Plot Figure
	x = [i for i in range(epochs)]

	plt.figure()
	plt.plot(x, err)
	plt.axis([-2, epochs+2, -0.01, 2.51])

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


def runAllCombinations(name, network, context, epochs, nr_samples, nr_hypo_samples):

	for samples in nr_samples:
		for hypotheses in nr_hypo_samples:

			runSimulation(name, network, context,
							epochs, samples, hypotheses, True, True)
							
			runSimulation(name, network, context,
							epochs, samples, hypotheses, True, False)
						
	runSimulation(name, network, context,
							epochs, 0, 0, False, True)
							
	runSimulation(name, network, context,
							epochs, 0, 0, False, False)



# Save name
name = "coinflip_with_world_sorted"
#name = "babybot"

# Define network
network = CoinflipModel()
#network = BabybotModel()

# Set numbers of epochs
epochs = 250

# Define context: First is homogenous, second is sorted, third is shuffled
#context = [x for i in range(int(epochs/2)) for x in ['True', 'False']]
context = [x for x in ["True", "False"] for i in range(int(epochs/2))]
shuffle(context)

# Parameters for sampling
nr_hypo_samples = [5, 10, 100]
nr_samples = [5, 10, 100, 1000]

runAllCombinations(name, network, context, epochs, nr_samples, nr_hypo_samples)



