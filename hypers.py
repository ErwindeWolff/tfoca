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
        
        
        
        
        
        
        
        
# Bayesian Variable class that uses hyperpriors instead of probability    
class PredictionNode():
           
    # Save names and create probability table
    def __init__(self, names, values = ["True", "False"], parentValues = []):
        self.names = names
        self.prob_table = dict()
        self.createPriors(values, parentValues, [0 for _ in range(len(parentValues))], len(parentValues)-1)
    

    # Recursively creates hyperpriors for the variable      
    def createPriors(self, values, parentValues, indices, pointer):
    
        if pointer < 0:
        
            vals = list()
            for i, index in enumerate(indices):
                vals.append(parentValues[i][index])
            self.prob_table[str(vals)] = HyperPrior(values)
            
        else:
            for i in range(len(parentValues[pointer])):
                indices[pointer] = i
                self.createPriors(values, parentValues, indices, pointer - 1)
    

    # Return probability of a given value and parentValues
    # Parent values is empty by default for variables without parents
    def getProbability(self, value, parentValues = []):
        hyperprior = self.prob_table[str(parentValues)]
        return hyperprior.getProbability(value)


    # Return probabilities given parentValues
    # Parent values is empty by default for variables without parents        
    def getProbabilities(self, parentValues = []):
        hyperprior = self.prob_table[str(parentValues)]
        return hyperprior.getProbabilities()
    
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
        
        
        



