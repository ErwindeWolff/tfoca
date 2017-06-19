from variables import *
from variableElimination import * 
from factory import *
from sampler import *

from agents import *
from predProc import *

from tqdm import *

import matplotlib.pyplot as plt

# Define network

v1 = FixedVariable(names = ['Person'], values=['Erwin', 'Wouter'], value_row_table=[[]], prob_table=[[0.5, 0.5]])

v2 = FixedVariable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], value_row_table = [["Erwin"], ["Wouter"]], prob_table = [[0.5,0.5],[0.8,0.2]])


#v1 = Variable(names = ["Person"], values=["Erwin", "Wouter"], parentValues=[])

#v2 = Variable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], parentValues=[v1.values]) 

v3 = Variable(names = ["Brightness"], values=["Light", "Dark"], parentValues=[])
                    
v4 = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
                 parentValues = [v2.values, v3.values, v1.values])


# Methods for creating agent title in plot
use_sampling = False
use_weighting = False

# Define network for agents
model = [v1, v2, v3, v4]
hypo = [v1]
pred = [v4]

# Parameters for sampling
nr_hypo_samples = 10
nr_samples = 100

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
epochs = 250
for i in tqdm(range(epochs)):

	(full_table, small_table, hypothesis) = a.makePrediction(["Coin Outcome"], ["Heads"], [])

	if (i % 2 == 0):
		observation = [1.0, 0.0]
	else:
		observation = [1.0, 0.0]

	# Calculate and save prediction error
	prediction_error = KLD(observation, small_table[2])
	err.append(prediction_error)

	for value_row, prob_row in zip(full_table[1], full_table[2]):
		update = [prob_row * obs for obs in observation]
		a.updateModel("Coin Outcome", value_row[1:], update, prediction_error)


# Plot Figure

x = [i for i in range(epochs)]

plt.figure()

if use_sampling:
	if use_weighting:
		plt.title("Sampling with weighting")
	else:
		plt.title("Sampling without weighting")
else:
	if use_weighting:
		plt.title("Normative with weighting")
	else:
		plt.title("Normative without weighting")

plt.plot(x, err)
plt.show()



