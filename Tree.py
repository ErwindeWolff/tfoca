# -*- coding: utf-8 -*-
from variables import *

class TreeModel():
	def __init__(self, tree_depth=4, num_children=2):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
	
		self.makeTreeNetwork(tree_depth, num_children)
		
		self.query = ['Layer_{0}_Node_1'.format(tree_depth)]
		self.goal = ['True']
		
	def makeTreeNetwork(self, tree_depth, num_children = 2):
		depth = 0
		    
		# Make the uppermost node, and add it to the network
		node = Variable(names = ["Layer_{0}_Node_{1}".format(depth+1, 1)], values=["True", "False"], parentValues=[])
		self.model.append(node)
		self.hypothesisNodes.append(node)
		    
		# Recursively add children to the current uppermost node
		self.makeChildren([node], depth+1, tree_depth, num_children, 1, prediction) 
		

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
				self.makeChildren([node], depth+1, tree_depth, num_children, pos, prediction)