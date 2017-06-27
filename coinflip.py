from variables import *

class CoinflipModel():

	def __init__(self):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
	
		self.createModel()
		
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
