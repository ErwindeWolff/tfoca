# -*- coding: utf-8 -*-

import random as r

# Class that makes a random probability distribution given a node and its required parents.
class ProbTable():
	def __init__(self, values, params):
		self.values = values

		# Create baseline for all values, and then normalize
		self.params = params

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
	def __init__(self, values, steps):
		self.values = values

		# Create baseline for all values
		self.params = list()
		for param in range(len(values)):
			self.params.append(1.0)

		self.steps = steps			
		self.distribution = list()
		self.probabilities = list()

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

	# Simple reset function
	def reset(self):
		self.params = [1.0 for _ in self.params]
		self.distribution = list()
		self.probabilities = list()
		
		
	# Function to create probability density function values
	def createDistribution(self):

		# Create values recursively
		self.createDistributionRecur(self.distribution, self.probabilities, [], 0, self.steps)

		# Normalize to make AUC equal 1.0
		sum_probs = sum([p * (1.0/len(self.probabilities)) for p in self.probabilities])
		self.probabilities = [prob/sum_probs for prob in self.probabilities]
		
		
	# Recursive helper function to calculate distribution values	
	def createDistributionRecur(self, distribution, probabilities, cur_dist, index, steps):
		
		# If the final parameter x is chosen
		if index == len(self.params)-1:
			# Value is fixed since values sum to 1
			cur_dist.append(1.0 - sum(cur_dist))
			
			# Calculate probability that belongs to combinations of x_i
			prob = 1.0
			for x, alfa in zip(cur_dist, self.params):
				prob = prob * x**(alfa-1.0)
			
			# Remember these results
			distribution.append(cur_dist)
			probabilities.append(prob)
		
		else:
			# Determine maximum value this x_i can have (sum to 1.0 demand)
			end = steps - int(steps*sum(cur_dist))
			# Traverse all combinations
			for i in range(end+1):
				x = (i*1.0)/steps
				# Continue with this value of x_i
				self.createDistributionRecur(distribution, probabilities, 
											cur_dist + [x], index+1, steps)
		
	
	# Function to sample from hyperprior via Gibb's sampling	
	def getSampledProbabilities(self):
	
		# If distribution was not made yet, create it
		if (len(self.distribution) == 0):
			self.createDistribution()
	
		# Get random value sampled from distribution
		choice = r.random() * sum(self.probabilities)
		for v, p in zip(self.distribution, self.probabilities):
			if choice <= p:
				return (self.values, v)
			choice -= p
			
		# Catch default return of last element. Should never get here
		return (self.values, self.distribution[-1])
		
	
	# Function to update a hyperprior with new observations
	def updateDistribution(self, update):
	
		new_probabilities = list()
		for dist, prob in zip(self.distribution, self.probabilities):
			new_prob = prob
			for x, c in zip(dist, update):
				new_prob = new_prob * x**c
			new_probabilities.append(new_prob)
		
		sum_new_probs = sum([p * (1.0/len(new_probabilities)) for p in new_probabilities])
		new_probabilities = [prob/sum_new_probs for prob in new_probabilities]
	
		self.probabilities = new_probabilities	
	
	# Add the updates to the parameters
	def updateParams(self, updates):
		self.params = [x + y for x, y in zip(self.params, updates)]
		
		if (len(self.distribution) > 0):
			self.updateDistribution(updates)


########################################################################################################


# Bayesian Variable class that uses random probabilities
class FixedVariable():

	def __init__(self, names, values, value_row_table, prob_table):
 
		self.names = names
		self.values = values

		self.value_rows = dict()

		for values, probs in zip(value_row_table, prob_table):
			
			# Find table at proper key
			key = "_"
			for value in values:
				key += value + "_"
				
			self.value_rows[key] = probs
  
	# Return probability of a given value and parentValues
	# Parent values is empty by default for variables without parents
	def getProbability(self, value, parentValues = []):

		# Find table at proper key
		key = "_"
		for value in parentValues:
			key += value + "_"

		return self.value_rows[key]


	# Return probabilities given parentValues
	# Parent values is empty by default for variables without parents
	def getProbabilities(self, parentValues = [], sampling=False):

		# Find table at proper key
		key = "_"
		for value in parentValues:
			key += value + "_"

		table = self.value_rows[key]

		return (self.values, table)

	# Returns the whole probability table as a tuple of two lists
	# the first list contains labels, the second probabilities  
	def getProbabilityTable(self):

		labels = list()
		probas = list()

		#for parentVals in self.value_row_table:

			# Find table at proper key
			#key = "_"
			#for value in parentValues:
			#	key += value + "_"
			
		for key in self.value_rows.keys():
		
			table = self.value_rows[key]
			parentVals = [word for word in key.split("_") if len(word) > 0]		

			for val, prob in zip(self.values, table):

				labels.append([val] + parentVals)
				probas.append(prob)

		return (labels, probas)


#########################################################################################################


class Variable():
	# Save names and create probability table
	def __init__(self, names, values = ["True", "False"], parentValues = [], diff = 0):
		self.names = names
		self.values = values
		self.parentValues = parentValues

		self.diff = diff

		self.value_rows = dict()
		self.createValues(values, parentValues, [0 for _ in range(len(parentValues))], len(parentValues)-1)


	# Recursively creates random probabilities for the variable  
	def createValues(self, values, parentValues, row_values, pointer):

		# Basecase: traversed (backwards) through parentvalues
		# Create a new probability entry for this combination
		if pointer < 0:
			# Copy because it is a pointer otherwise
			vals = [value for value in row_values]

			# Create proper key
			key = "_"
			for value in vals:
				key += value + "_"

			# Create this row
			self.value_rows[key] = RandomTable(values, self.diff)

		# Not all parents have an assigned value yet,
		# recursively iterate to the next parents for all
		# values of current selected parent (will thus go through all 
		# complete permutations recursively)
		else:
			for value in parentValues[pointer]:
				row_values[pointer] = value
				self.createValues(values, parentValues, row_values, pointer - 1)

	# Return probability of a given value and parentValues
	# Parent values is empty by default for variables without parents
	def getProbability(self, value, parentValues = []):

		# Find table at proper key
		key = ""
		for value in parentValues:
			key += value + "_"

		return self.value_rows[key]


	# Return probabilities given parentValues
	# Parent values is empty by default for variables without parents
	def getProbabilities(self, parentValues = [], sampling=False):

		# Find table at proper key
		key = "_"
		for value in parentValues:
			key += value + "_"

		table = self.value_rows[key]

		return table.getProbabilities()

	# Returns the whole probability table as a tuple of two lists
	# the first list contains labels, the second probabilities  
	def getProbabilityTable(self):

		labels = list()
		probas = list()

		for key in self.value_rows.keys():

			table = self.value_rows[key]
			parentVals = [word for word in key.split("_") if len(word) > 0]		
			
			(values, probabilities) = table.getProbabilities()
			for val, prob in zip(values, probabilities):
			
				labels.append([val] + parentVals)
				probas.append(prob)

		return (labels, probas)

#########################################################################################################


# Bayesian Variable class that uses hyperpriors instead of probability
class HyperpriorVariable(Variable):

	 # Save names and create probability table
	def __init__(self, names, values = ["True", "False"], parentValues = [], steps=100):
		self.names = names
		self.values = values
		self.parentValues = parentValues
		
		self.value_rows = dict()

		self.createPriors(values, parentValues, [parent[0] for parent in parentValues], len(parentValues)-1, steps)

	# Recursively creates hyperpriors for the variable  
	def createPriors(self, values, parentValues, row_values, pointer, steps):

		# Basecase: traversed (backwards) through parentvalues
		# Create a new hyperprior for this combination
		if pointer < 0:
			# Copy because it is a pointer otherwise
			vals = [value for value in row_values]
			
			# Create proper key
			key = "_"
			for value in vals:
				key += value + "_"

			# Create this row
			self.value_rows[key] = HyperPrior(values, steps)

		# Not all parents have an assigned value yet,
		# recursively iterate to the next parents for all
		# values of current selected parent (will thus go through all 
		# complete permutations recursively)
		else:
			for value in parentValues[pointer]:
				row_values[pointer] = value
				self.createPriors(values, parentValues, row_values, pointer - 1, steps)


	# Return probabilities given parentValues
	# Parent values is empty by default for variables without parents
	def getProbabilities(self, parentValues = [], sampling=False):

		# Find table at proper key
		key = "_"
		for value in parentValues:
			key += value + "_"

		table = self.value_rows[key]
		
		if sampling:		
			return table.getSampledProbabilities()
		else:
			return table.getProbabilities()


	# Update specific hyperprior
	def updateHyperprior(self, values, key=[]):
		
		hyperprior = self.value_rows[key]
		hyperprior.updateParams(values)
		
	def reset(self):
		for hyperprior in self.value_rows.values():
			hyperprior.reset()






