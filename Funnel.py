# -*- coding: utf-8 -*-
from variables import *

class TreeModel():
	def __init__(self, funnel_depth=4, num_parents=2):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
	
		self.makeFunnelNetwork(funnel_depth, num_parents)
		
		self.query = ['Layer_{0}_Node_1'.format(funnel_depth)]
		self.goal = ['True']
		
	def makeFunnelNetwork(self,funnel_depth, num_parents):

		depth = funnel_depth
		# recursively make parents for current node
		parents = self.makeParents(depth-1, num_parents, 1)
		    
		# make parameters for current node
		names = list()
		parentValues = list()
		values = ["True","False"]
		    
		# append the node's own name to the list of names
		names.append("Layer_{0}_Node_{1}".format(depth, 1))
		    
		# extract parent values and names from this node's parents
		if len(parents)>0:    
			for parent in parents:
				parentValues.append(parent.values)
				names.append(parent.names[0])
            
		node = HyperpriorVariable(names=names, values=values, parentValues=parentValues)
		self.model.append(node)
		    
		self.predictionNodes.append(node)
    
	def makeParents(self,network, depth, num_parents, current_width):
		current_parents = list()
		# If the funnel has not reached its maximum depth:
		if depth > 0:        
			# make list of node numbers for all parents
			cur_positions = [(current_width*num_parents)-i for i in range(num_parents)[::-1]]
			# for each parent we make for the current child:
			for pos in cur_positions:
				# recursively make parents for current node
				parents = self.makeParents(network, depth-1, num_parents, pos,)
				names = list()
				parentValues = list()
				            
				# append the node's own name to the list of names
				names.append("Layer_{0}_Node_{1}".format(depth, pos))
				            
				# make list of values for this variable
				values = ["True","False"]
				            
				# extract parent values and names from this node's parents
				if len(parents)>0:
					for parent in parents:
						parentValues.append(parent.values)
						names.append(parent.names[0])
            
				# make the parent and add it to the network
				parent = Variable(names = names, values = values, parentValues = parentValues)
				current_parents.append(parent)
				self.model.append(parent)
				            
				# if we're at the uppermost layer, indicate the current node as a hypothesis node
				if depth == 1:
					self.hypothesisNodes.append(parent)
		return current_parents
    