from variables import *
from variableElimination import * 

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


# Bayesian Variable
var = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
                 parentValues = [["Fair", "Unfair"], ["Light", "Dark"], ["Erwin", "Wouter"]]) 

# Factor, triple with   f[0] = variable names
#                       f[1] = variable & parent values
#                       f[2] = probabilities
f1 = var.getProbabilityTable()
f1 = (var.names, f1[0], f1[1])
f2 = applyEvidence(f1, "Brightness", "Light")
f3 = sumOut(f2, "Fairness")

printFactor(f1)
printFactor(f2)
printFactor(f3)
