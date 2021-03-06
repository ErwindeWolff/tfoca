from variables import *
from random import shuffle

class CoinflipModel():

	def __init__(self):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
		self.world = [] 
	
		self.createModel()
		self.createWorld()
		
		self.query = ['Coin Outcome']
		self.goal = ['Heads']
		
		
	def createModel(self):
	
		v1 = FixedVariable(names = ['Person'], values=['Erwin', 'Wouter'], 
									value_row_table=[[]], prob_table=[[0.5, 0.5]])
		v2 = FixedVariable(names = ["Fairness", "Person"], values=["Fair", "Unfair"], 
									value_row_table = [["Erwin"], ["Wouter"]], prob_table = [[0.5,0.5],[0.8,0.2]])
		v3 = Variable(names = ["Brightness"], values=["Light", "Dark"], parentValues=[])        
		v4 = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], 
									values=["Heads", "Tails"], parentValues = [v2.values, v3.values, v1.values])

		# Define network for agents
		self.model = [v1, v2, v3, v4]
		self.hypothesisNodes = [v1]
		self.predictionNodes = [v4]
		
		
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
		
		
		
				
				
				
