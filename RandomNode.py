# -*- coding: utf-8 -*-

import random as r

# Class that makes a random probability distribution given a node and its required parents.
class RandomTable():
    def __init__(self, values, diff):
        self.values = values
        self.diff = diff
        
        # Create baseline for all values, and then normalize
        self.params = list()
        for param in range(len(values)):
            self.params.append(diff+r.uniform(0,1))
        paramSum = sum(self.params)
        self.params = [i/paramSum for i in self.params]
        
    # returns the probability of a given random value.
    def getProbability(self, value):
        index = self.values.index(value)
        return self.params[index]
        
    # returns a list of probabilities for given random values in a tuple
    def getProbabilities(self):
        probs = list()
        
        for param in self.params:
            probs.append(param)
            
        return (self.values, probs)


# Bayesian Variable class that uses hyperpriors instead of probability    
class RandomNode():
           
    # Save names and create probability table
    def __init__(self, names, values = ["True", "False"], parentValues = [], diff=0):
        self.names = names
        self.prob_table = dict()
        self.createValues(values, parentValues, [0 for _ in range(len(parentValues))], len(parentValues)-1)
        selfdiff = diff
    
    # Recursively creates hyperpriors for the variable      
    def createValues(self, values, parentValues, indices, pointer):
    
        if pointer < 0:
        
            vals = list()
            for i, index in enumerate(indices):
                vals.append(parentValues[i][index])
            self.prob_table[str(vals)] = RandomTable(values, self.diff)
            
        else:
            for i in range(len(parentValues[pointer])):
                indices[pointer] = i
                self.createValues(values, parentValues, indices, pointer - 1)
    

    # Return probability of a given value and parentValues
    # Parent values is empty by default for variables without parents
    def getProbability(self, value, parentValues = []):
        table = self.prob_table[str(parentValues)]
        return table.getProbability(value)


    # Return probabilities given parentValues
    # Parent values is empty by default for variables without parents        
    def getProbabilities(self, parentValues = []):
        table = self.prob_table[str(parentValues)]
        return table.getProbabilities()
    
    # Returns the whole probability table as a tuple of two lists
    # the first list contains labels, the second probabilities  
    def getProbabilityTable(self):
        
        labels = list()
        probas = list()
        
        for parentVals in self.prob_table.keys():
            (vals, probs) = self.getProbabilities(parentVals)
            
            for val, prob in zip(vals, probs):
            
                parentList = [x.strip() for x in parentVals.split("'") if len(x.strip()) > 1]
                labels.append([val] + parentList)
                probas.append(prob)
            
        return (labels, probas)
        