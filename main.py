from variables import *


def printVar(var):
    
    if (len(var.names) > 1):
        print var.names[0] + " given " + str(var.names[1::]) + "\n"
    else:
        print var.names[0]

    (foo, bar) = var.getProbabilityTable()
    for i in range(len(foo)):
        print foo[i], bar[i]
    print ""

#var = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"],values=["Heads", "Tails"] ,
#                 parentValues =[["Fair", "Unfair"], ["Dark", "Light"], ["Wouter", "Erwin"]]) 



var = HyperpriorVariable(names = ["Coin Outcome", "Fairness"],values=["Heads", "Tails"] ,
                 parentValues =[["Fair", "Unfair"]]) 

var.updateHyperprior([3.0, 0], ["Unfair"])

var2 = Variable(names = ["Fairness"], values=["Fair", "Unfair"], parentValues=[])

printVar(var2)
printVar(var)

