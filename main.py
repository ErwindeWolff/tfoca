from hypers import *

var = PredictionNode(values=["Heads", "Tails"] , parentValues =[["Fair", "Unfair"], ["Dark", "Light"], ["Wouter", "Erwin"]]) 

(foo, bar) = var.getProbabilityTable()
for i in range(len(foo)):
    print foo[i], bar[i]
print ""

#(foo, bar) = var.getProbabilities(["Fair"])
#for i in range(len(foo)):
#    print foo[i], bar[i]
#print ""

#print var.getProbability("Heads", ["Fair"])
