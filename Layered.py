# -*- coding: utf-8 -*-
from variables import *

class LayeredModel():
	def __init__(self, layers):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
	
		self.makeLayerNetwork(layers)
		
		self.query = ['Layer_{0}_Node_1'.format(len(layers))]
		self.goal = ['True']
	
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
