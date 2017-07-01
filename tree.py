# -*- coding: utf-8 -*-
from variables import *
from random import shuffle

class TreeModel():
	def __init__(self, tree_depth=4, num_children=2):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
		self.world = []
	
		self.makeTreeNetwork(tree_depth, num_children)
		self.createWorld()
		
		self.query = [self.predictionNodes[0].names[0]]
		self.goal = [self.predictionNodes[0].values[0]]
		
	def makeTreeNetwork(self, tree_depth, num_children = 2):
		depth = 0
		    
		# Make the uppermost node, and add it to the network
		node = Variable(names = ["Layer_{0}_Node_{1}".format(depth+1, 1)], values=["True", "False"], parentValues=[])
		self.model.append(node)
		self.hypothesisNodes.append(node)
		    
		# Recursively add children to the current uppermost node
		self.makeChildren([node], depth+1, tree_depth, num_children, 1, self.predictionNodes) 
		

	def makeChildren(self, parents, depth, tree_depth, num_children, current_width, prediction):
		# If the tree has not reached its maximum depth:
		if depth < tree_depth:
			# make list of node numbers for all children
			cur_positions = [(current_width*num_children)-i for i in range(num_children)[::-1]]
			        
			# For each child we make for the current parent:
			for pos in cur_positions:
				# make list of names for this variable; a list containing the current name, and the names of all recursive parents.
				names = []
				names.append("Layer_{0}_Node_{1}".format(depth+1, pos))
				
				# make list of values for this variable
				values = ["True","False"]
				            
				# extract parent values from the child's parent
				parentValues = list()
				for parent in parents:
				                parentValues.append(parent.values)
				                names.append(parent.names[0])
				                 
				# Add the current node to prediction nodes if it is a prediction node
				if depth+1==tree_depth:
					#Make current child node...
					node = HyperpriorVariable(names=names, values=values, parentValues=parentValues)
					self.predictionNodes.append(node)
				else:
					#Make current child node...
					node = Variable(names=names, values=values, parentValues=parentValues)
				#and add to the network
				self.model.append(node)            
				            
				# recursively make children to this node until the tree depth has been reached
				self.makeChildren([node], depth+1, tree_depth, num_children, pos, self.predictionNodes)
				
	
					
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
		
