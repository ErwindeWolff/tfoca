from variables import *
from variableElimination import * 
from factory import *
from sampler import *

# Function to print variable table
def printVar(var):
    
    if (len(var.names) > 1):
        print var.names[0] + " given " + str(var.names[1::]) + "\n"
    else:
        print var.names[0]

    (foo, bar) = var.getProbabilityTable()
    for i in range(len(foo)):
        print foo[i], bar[i]
    print ""

# Function to print factor
def printFactor(f):

    print f[0]
    (foo, bar) = (f[1], f[2])
    for i in range(len(foo)):
        print foo[i], bar[i]
    print ""




v1 = FixedVariable(names = ['Person'], values=['Erwin', 'Wouter'], value_row_table=[[]], prob_table=[[0.5, 0.5]])

v2 = FixedVariable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], value_row_table = [["Erwin"], ["Wouter"]], prob_table = [[0.5,0.5],[0.8,0.2]])


#v1 = Variable(names = ["Person"], values=["Erwin", "Wouter"], parentValues=[])

#v2 = Variable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], parentValues=[v1.values]) 

v3 = Variable(names = ["Brightness"], values=["Light", "Dark"], parentValues=[])
                    
v4 = Variable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
                 parentValues = [v2.values, v3.values, v1.values])


#full_factor = VE( [v1, v2, v3, v4], v4.names, [])

#printFactor(full_factor)

#factor = VE([v1,v2,v3,v4], ["Coin Outcome"], [])
#printFactor(factor)

(full_factor, small_factor) = getPredictionTables( [v1, v2, v3, v4], ["Coin Outcome"], [])

printFactor(full_factor)
printFactor(small_factor)



#print getSampledProbability( [v1, v2, v3, v4], ["Person"], [("Coin Outcome", "Heads")], 100, 0.1)






