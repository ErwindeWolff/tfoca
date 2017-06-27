from variables import *
from variableElimination import * 
from sampler import *
from agents import *
from predProc import *
from tqdm import *

import os

# Specific Model imports
from babybot import *
from coinflip import *

import matplotlib.pyplot as plt

# Define network

#network = CoinflipModel()
network = BabybotModel()

model = network.model
hypo = network.hypothesisNodes
pred = network.predictionNodes

# Save name
#name = "coinflip_other_test"
name = "babybot_test"

#query = ["Coin Outcome"]
#goal = ["Heads"]

query = ["Mobile_movement"]
goal = ['True']

# Methods for creating agent title in plot
use_sampling = True
use_weighting = True

# Parameters for sampling
nr_hypo_samples = 10
nr_samples = 10

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
epochs = 1000
for i in tqdm(range(epochs)):

	(full_table, small_table, hypothesis) = a.makePrediction(query, goal, [])

	if (i % 2 == 0):
		observation = [1.0, 0.0]
	else:
		observation = [1.0, 0.0]

	# Calculate and save prediction error
	prediction_error = KLD(observation, small_table[2])
	err.append(prediction_error)
	

	for value_row, prob_row in zip(full_table[1], full_table[2]):
	
		if (type(value_row) is list):
			key = "_"
			for v in value_row[1:]:
				key += v + "_"
			value_row = key

		#print(value_row)
		
		update = [ob * prob_row for ob in observation]
		a.updateModel(query, value_row, update, prediction_error)


# Plot Figure
x = [i for i in range(epochs)]

plt.figure()
plt.plot(x, err)
plt.axis([-2, epochs+2, -0.01, 1.01])

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


