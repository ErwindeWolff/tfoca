from variables import *
from variableElimination import * 
from factory import *

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
#var = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
#                 parentValues = [["Fair", "Unfair"], ["Light", "Dark"], ["Erwin", "Wouter"]]) 

# Factor, triple with   f[0] = variable names
#                       f[1] = variable & parent values
#                       f[2] = probabilities

#f1 = var.getProbabilityTable()
#f1 = (var.names, f1[0], f1[1])
#f2 = applyEvidence(f1, "Brightness", "Light")
#f3 = sumOut(f2, "Fairness")

#printFactor(f1)
#printFactor(f2)
#printFactor(f3)


v1 = FixedVariable(names = ['Person'], values=['Erwin', 'Wouter'], value_row_table=[[]], prob_table=[[0.5, 0.5]])

v2 = FixedVariable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], value_row_table = [["Erwin"], ["Wouter"]], prob_table = [[0.5,0.5],[0.8,0.2]])


#v1 = Variable(names = ["Person"], values=["Erwin", "Wouter"], parentValues=[])

#v2 = Variable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], parentValues=[v1.values]) 

v3 = Variable(names = ["Brightness"], values=["Light", "Dark"], parentValues=[])
                    
v4 = Variable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
                 parentValues = [v2.values, v3.values, v1.values])

factors = selectFactors( [v1, v2, v3, v4], ["Coin Outcome"], [])

for factor in factors:
    printFactor(factor)

f1 = multiplyFactors(factors[0], factors[1])

printFactor(f1)

print(factors[1][0][0])
f2 = sumOut(f1, factors[1][0][0])

printFactor(f2)






