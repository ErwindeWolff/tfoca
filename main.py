from variables import *
from variableElimination import * 
from factory import *
from sampler import *

from agents import *
from predProc import *

import matplotlib.pyplot as plt

# Function to print variable table
def printVar(var):
    
    if (len(var.names) > 1):
        print(var.names[0] + " given " + str(var.names[1::]) + "\n")
    else:
        print( var.names[0])

    (foo, bar) = var.getProbabilityTable()
    for i in range(len(foo)):
        print( foo[i], bar[i])
    print("")

# Function to print factor
def printFactor(f):

    print(f[0])
    (foo, bar) = (f[1], f[2])
    for i in range(len(foo)):
        print(foo[i], bar[i])
    print("")




v1 = FixedVariable(names = ['Person'], values=['Erwin', 'Wouter'], value_row_table=[[]], prob_table=[[0.5, 0.5]])

v2 = FixedVariable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], value_row_table = [["Erwin"], ["Wouter"]], prob_table = [[0.5,0.5],[0.8,0.2]])


#v1 = Variable(names = ["Person"], values=["Erwin", "Wouter"], parentValues=[])

#v2 = Variable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], parentValues=[v1.values]) 

v3 = Variable(names = ["Brightness"], values=["Light", "Dark"], parentValues=[])
                    
v4 = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
                 parentValues = [v2.values, v3.values, v1.values])


#full_factor = VE( [v1, v2, v3, v4], v4.names, [])

#printFactor(full_factor)

#factor = VE([v1,v2,v3,v4], ["Coin Outcome"], [])
#printFactor(factor)

#(full_factor, small_factor) = getPredictionTables( [v1, v2, v3, v4], ["Coin Outcome"], [])

#printFactor(full_factor)
#printFactor(small_factor)

#rejectionSampling([v1, v2, v3, v4], ["Coin Outcome"], [], 1000, bias=0.1)


a = DeterministicAgent([v1,v2,v3,v4], [v1], [v4], use_weighting=False)

err = []
epochs = 20
for i in range(epochs):

	(full_table, small_table, hypothesis) = a.makePrediction(["Coin Outcome"], ["Heads"], [])

	#printFactor(full_table)
	#printFactor(small_table)

	if (i % 2 == 0):
		observation = [1.0, 0.0]
	else:
		observation = [1.0, 0.0]

	prediction_error = KLD(observation, small_table[2])
	err.append(prediction_error)

	for value_row, prob_row in zip(full_table[1], full_table[2]):

		update = [prob_row * obs for obs in observation]

		a.updateModel("Coin Outcome", value_row[1:], update, prediction_error)

	print ""

x = [i for i in range(epochs)]

plt.figure()
plt.plot(x, err)
plt.show()



