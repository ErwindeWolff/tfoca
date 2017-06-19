from variables import *
from variableElimination import *
from factory import *

from random import *

class DeterministicAgent():

	def __init__(self, model, hypothesisNodes, predictionNodes, use_weighting = False):

		self.model = model
		self.hypothesisNodes = hypothesisNodes
		self.predictionNodes = predictionNodes

		self.use_weighting = use_weighting


	def makePrediction(self, query, query_value, evidence):
		
		# Tracking parameters for best hypothesis
		best_pred = 0.0
		best_full_table = []
		best_small_table = []
		best_hypothesis = []

		# Gather hypotheses and shuffle to get some randomness if all the same prob.
		hypotheses = self.getHypotheses()
		shuffle(hypotheses)

		for i, hypo in enumerate(hypotheses):

			# Get prediction over query
			(full_table, small_table) = getPredictionTables(self.model, query, evidence + hypo)
			
			# Extract prediction of desired value of query
			index = small_table[1].index(query_value)
			pred_query_value = small_table[2][index]

			# If highest prediction, save over other
			if pred_query_value > best_pred:
				best_pred = pred_query_value
				best_full_table = full_table
				best_small_table = small_table
				best_hypothesis = hypo

		return (best_full_table, best_small_table, best_hypothesis)

	
	# Changes the hyperpriors relevant to the prediction, 
	# observation and error if weighting
	def updateModel(self, query, parents, observation, prediction_error):

		if self.use_weighting:
			observation = [obs * prediction_error for obs in observation]

		for var in self.predictionNodes:
			if var.names[0] == query:
				var.updateHyperprior(observation, parents)


	# Creates list of possible hypotheses
	def getHypotheses(self):
		hypotheses = []
		self.getHypothesesRecur(hypotheses, [], self.hypothesisNodes, 0)
		return hypotheses


	# Recursive helper function for getHypotheses
	def getHypothesesRecur(self, hypotheses, cur_hypo, hypothesisNodes, index):

		if index >= len(hypothesisNodes):
			hypotheses.append( [value for value in cur_hypo])

		else:
			var = hypothesisNodes[index]
			name = var.names[0]
			for value in var.values:
				self.getHypothesesRecur(hypotheses, cur_hypo + [(name, value)], hypothesisNodes, index+1)



class SamplingAgent():

	def __init__(self, model, hypothesisNodes, predictionNodes, nr_samples use_weighting = False):

		self.model = model
		self.hypothesisNodes = hypothesisNodes
		self.predictionNodes = predictionNodes

		self.nr_samples = nr_samples
		self.use_weighting = use_weighting


	def makePrediction(self, query, query_value, evidence):
		
		# Tracking parameters for best hypothesis
		best_pred = 0.0
		best_full_table = []
		best_small_table = []
		best_hypothesis = []

		# Gather hypotheses and shuffle to get some randomness if all the same prob.
		hypotheses = self.getHypotheses()
		shuffle(hypotheses)

		for i, hypo in enumerate(hypotheses):
			print(hypo)

			# Get prediction over query
			(full_table, small_table) = getPredictionTables(self.model, query, evidence + hypo)
			
			# Extract prediction of desired value of query
			index = small_table[1].index(query_value)
			pred_query_value = small_table[2][index]

			# If highest prediction, save over other
			if pred_query_value > best_pred:
				best_pred = pred_query_value
				best_full_table = full_table
				best_small_table = small_table
				best_hypothesis = hypo

		return (best_full_table, best_small_table, best_hypothesis)

	
	# Changes the hyperpriors relevant to the prediction, 
	# observation and error if weighting
	def updateModel(self, query, parents, observation, prediction_error):

		if self.use_weighting:
			observation = [obs * prediction_error for obs in observation]

		for var in self.predictionNodes:
			if var.names[0] == query:
				var.updateHyperprior(observation, parents)


