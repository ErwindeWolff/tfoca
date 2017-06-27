# -*- coding: utf-8 -*-
from variables import *

class WorldModel():
	def __init__(self, network, hypothesis, prediction):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
	
		self.makeWorldetwork(network, hypothesis, prediction)
		
		self.query = [self.predictionNodes[0].names[0]]
		self.goal = [self.predictionNodes[0].values[0]]
	
	def makeWorldNetwork(self, network, hypothesis, prediction):
		    
		# make the unobserved world node, and add it to the world model
		unobserved = Variable(names=["Unobserved_Node"], values = ["True","False"], parentValues=[])
		self.model.append(unobserved)
		    
		# iterate over the observed variables we will add
		for var in network:
			# copy the current node's names, values and parentValues
			names = list(var.names)
			values = list(var.values)
			parentValues = [parent.values for parent in network if parent.names[0] in var.names[1:]]            
			        
			# If the current node is a prediction node, unobserved node's influences are added
			if var in prediction:
				# add the unobserved node's name and values to the names and parentValues
				names.append(unobserved.names[0])
				parentValues.append(unobserved.values)
				new_var = Variable(names=names, values=values, parentValues = parentValues)
			else:
				new_var = var
            
			# add node to the world model
			self.model.append(new_var)
			        
			if var in prediction:
				self.predictionNodes.append(new_var)
			elif var in hypothesis:
				self.hypothesisNodes.append(new_var)
