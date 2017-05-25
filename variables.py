# -*- coding: utf-8 -*-

import random as r

# Class that makes a random probability distribution given a node and its required parents.
class RandomTable():
    def __init__(self, values, diff=0):
        self.values = values
        
        # Create baseline for all values, and then normalize
        self.params = list()
        for param in range(len(values)):
            self.params.append(diff + r.uniform(0,1))
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
        
########################################################################################################

# Class to represent dirichlet-based hyperpriors
class HyperPrior():

    # General Constructor for labelled values. Default value is True, False
    def __init__(self, values):
        self.values = values
        
        # Create baseline for all values
        self.params = list()
        for param in range(len(values)):
            self.params.append(1.0)
            
    # Returns probability as parameter divided by sum (dirichet average)
    def getProbability(self, value):
        index = self.values.index(value)
        
        return self.params[index] / sum(self.params)
    
    # Returns list of tuples of the form (value, probability), where a value can be true/false f.e.    
    def getProbabilities(self):
        probs = list()
        
        sum_params = sum(self.params)
        
        for param in self.params:
            probs.append(param/sum_params)
            
        return (self.values, probs)
        
    # Add the updates to the parameters
    def updateParams(self, updates):
        self.params = [x + y for x, y in zip(self.params, updates)]        



########################################################################################################

# Bayesian Variable class that uses random probabilities    
class Variable():
           
    # Save names and create probability table
    def __init__(self, names, values = ["True", "False"], parentValues = []):
        self.names = names
        self.prob_table = dict()
        self.createValues(values, parentValues, [0 for _ in range(len(parentValues))], len(parentValues)-1)
    
    # Recursively creates random probabilities for the variable      
    def createValues(self, values, parentValues, indices, pointer):
    
        if pointer < 0:
        
            vals = list()
            for i, index in enumerate(indices):
                vals.append(parentValues[i][index])
            self.prob_table[str(vals)] = RandomTable(values)
            
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
            
                # Turns list-string into a real list again
                parentList = parentVals.replace("[", "").replace("]", "")
                parentList = [x.strip() for x in parentList.split("'") if len(x.strip()) > 1]

                labels.append([val] + parentList)
                probas.append(prob)
            
        return (labels, probas)

#########################################################################################################
        

# Bayesian Variable class that uses hyperpriors instead of probability            
class HyperpriorVariable(Variable):

     # Save names and create probability table
    def __init__(self, names, values = ["True", "False"], parentValues = []):
        self.names = names
        self.prob_table = dict()
        self.createPriors(values, parentValues, [0 for _ in range(len(parentValues))], len(parentValues)-1)
        
    # Recursively creates hyperpriors for the variable      
    def createPriors(self, values, parentValues, indices, pointer):
    
        # Basecase: traversed (backwards) through parentvalues
        # Create a new hyperprior for this combination in the dictionary
        if pointer < 0:
        
            vals = list()
            for i, index in enumerate(indices):
                vals.append(parentValues[i][index])
            self.prob_table[str(vals)] = HyperPrior(values) # str() because lists cant be hashed
            
        # Not all parents have an assigned value yet,
        # recursively iterate to the next parents for all
        # values of current selected parent (will thus go through all 
        # complete permutations recursively)
        else:
            for i in range(len(parentValues[pointer])):
                indices[pointer] = i
                self.createPriors(values, parentValues, indices, pointer - 1)
        
        
