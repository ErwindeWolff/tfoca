from hypers import *

var = PredictionNode(names = ["Coin Outcome", "Fairness", "Brightness", "Person"],values=["Heads", "Tails"] ,
                 parentValues =[["Fair", "Unfair"], ["Dark", "Light"], ["Wouter", "Erwin"]]) 

#var = PredictionNode(names = ["Coin Outcome"],values=["Heads", "Tails"] ,
#                 parentValues =[]) 

print var.names[0] + " given " + str(var.names[1::]) + "\n"
(foo, bar) = var.getProbabilityTable()
for i in range(len(foo)):
    print foo[i], bar[i]
print ""

