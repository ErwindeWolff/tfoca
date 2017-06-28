# -*- coding: utf-8 -*-
from variables import *

class LayeredModel():
	def __init__(self, layers):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
		self.world = []
		
		self.makeLayerNetwork(layers)
		self.createWorld()
		
		self.query = [self.predictionNodes[0].names[0]]
		self.goal = [self.predictionNodes[0].values[0]]
	
	def makeLayerNetwork(self,layers):

		for i, layer in enumerate(layers):
			# Save the previous layer's size for use in getting the parents' names and values
			if i > 0:
				previous = layers[i-1]
			else:
				previous = 0
        
			# make a list for the current layer to be added to the network after each loop
			current_layer = list()
        
			for pos in range(layer):
				# make parameters for current node
				names = list()
				values = ["True","False"]
				parentValues = list()
				            
				# add the current node's name to the list of names
				names.append("Layer_{0}_Node_{1}".format(i+1,pos+1))
				            
				# if there is a previous layer:
				if previous > 0:
					for parent in self.model[-previous:]:
						# Add the parents' names to the current node's names
						names.append(parent.names[0])
						# Add the parents' values to the current node's parentValues
						parentValues.append(parent.values) 
            
				if i > len(layers)-1:
					node = HyperpriorVariable(names=names, values=values, parentValues=parentValues)
				else:
					node = Variable(names=names, values=values, parentValues=parentValues)
				current_layer.append(node)
            
			# Add all nodes in the current layer to the network, and if necessary to hypothesis or prediction
			for node in current_layer:
				self.model.append(node)
				if previous == 0:
					# node is a hypothesis node
					self.hypothesisNodes.append(node)
				elif i == len(layers)-1:
					# node is a prediction node
					self.predictionNodes.append(node)
					
					
	def createWorld(self):
	
		context = Variable(names = ["Context"], 
							values=self.predictionNodes[0].values, parentValues=[])
		self.world.append(context)
	
		for var in self.model:
			if var not in self.predictionNodes:
				self.world.append(var)
			else:
				new_var = Variable(names = var.names + ['Context'], values=var.values,
									parentValues=var.parentValues + [context.values])
						
				# Create weighting of context			
				for key in new_var.value_rows.keys():
				
					entry = [name for name in key.split("_") if len(name) > 1]
					
					for i in range(len(new_var.values)):
						value = new_var.values[i]
					
						if (entry[-1] == value):
							
							ideal_prob = [0.0 for x in new_var.values]
							ideal_prob[i] = 1.0
							
							real_prob = new_var.value_rows[key].getProbabilities()[1]
							
							new_probs = [0.5*real + 0.5*ideal for real, ideal in zip(real_prob, ideal_prob)]
							
							new_var.value_rows[key] = ProbTable(new_var.values, new_probs)

									
				self.world.append(new_var)
	
	
	'''
		Function to create evidence of context based on a given distribution
	'''		
	def getContext(self, epochs, distribution):
	
		values = self.predictionNodes[0].values
		
		# Create homogenous distribution
		if (distribution == 1):
			context = [x for i in range(int(epochs/len(values))) for x in values]
			
		# Create sorted distribution
		elif (distribution == 2):
			context = [x for x in values for i in range(int(epochs/len(values)))]
			
		# Create randomized distribution
		else:
			context = [x for i in range(int(epochs/len(values))) for x in values]
			shuffle(context)
		
		return context
		
