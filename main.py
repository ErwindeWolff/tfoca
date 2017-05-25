from variables import *


#var = PredictionNode(names = ["Coin Outcome", "Fairness", "Brightness", "Person"],values=["Heads", "Tails"] ,
#                 parentValues =[["Fair", "Unfair"], ["Dark", "Light"], ["Wouter", "Erwin"]]) 

var = HyperpriorVariable(names = ["Coin Outcome", "Fairness"],values=["Heads", "Tails"] ,
                 parentValues =[["Fair", "Unfair"]]) 

var2 = Variable(names = ["Fairness"], values=["Fair", "Unfair"], parentValues=[])

print var.names[0] + " given " + str(var.names[1::]) + "\n"
(foo, bar) = var.getProbabilityTable()
for i in range(len(foo)):
    print foo[i], bar[i]
print ""


print var2.names[0] + " given " + str(var2.names[1::]) + "\n"
(foo, bar) = var2.getProbabilityTable()
for i in range(len(foo)):
    print foo[i], bar[i]
print ""
