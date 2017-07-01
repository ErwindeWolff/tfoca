# -*- coding: utf-8 -*-
from variables import *
from random import shuffle

class FunnelModel():
	def __init__(self, funnel_depth=4, num_parents=2):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
		self.world = [] 
	
		self.makeFunnelNetwork(funnel_depth, num_parents)
		self.createWorld()
		
		self.query = [self.predictionNodes[0].names[0]]
		self.goal = [self.predictionNodes[0].values[0]]
		
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
    
	def makeParents(self, depth, num_parents, current_width):
		current_parents = list()
		# If the funnel has not reached its maximum depth:
		if depth > 0:        
			# make list of node numbers for all parents
			cur_positions = [(current_width*num_parents)-i for i in range(num_parents)[::-1]]
			# for each parent we make for the current child:
			for pos in cur_positions:
				# recursively make parents for current node
				parents = self.makeParents( depth-1, num_parents, pos,)
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
		
