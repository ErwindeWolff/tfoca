from variables import *

class BabybotModel():

	def __init__(self):
		self.model = []
		self.hypothesisNodes = []
		self.predictionNodes = []
	
		self.createModel()
		
	def createModel(self):
		# Define motor signal variables
		MS_LL = FixedVariable(names = ['MS_LL'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		MS_RL = FixedVariable(names = ['MS_RL'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		MS_LA = FixedVariable(names = ['MS_LA'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		MS_RA = FixedVariable(names = ['MS_RA'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		# Define previous limb positions

		prev_LL = FixedVariable(names = ['prev_LL'], values=['High', 'Middle', 'Low'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		prev_RL = FixedVariable(names = ['prev_RL'], values=['High', 'Middle', 'Low'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		prev_LA = FixedVariable(names = ['prev_LA'], values=['High', 'Middle', 'Low'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])

		prev_RA = FixedVariable(names = ['prev_RA'], values=['High', 'Middle', 'Low'], value_row_table=[[]], 
										prob_table = [[0.33, 0.33, 0.34]])


		# Define current limb positions
		cur_LL = FixedVariable(names = ['cur_LL', 'prev_LL', 'MS_LL'], values=['High', 'Middle', 'Low'], 
								value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Low', 'Up'],
												 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
												 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
								prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
											  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
											  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

		cur_RL = FixedVariable(names = ['cur_RL', 'prev_RL', 'MS_RL'], values=['High', 'Middle', 'Low'], 
								value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Low', 'Up'],
												 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
												 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
								prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
											  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
											  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

		cur_LA = FixedVariable(names = ['cur_LA', 'prev_LA', 'MS_LA'], values=['High', 'Middle', 'Low'], 
								value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Low', 'Up'],
												 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
												 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
								prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
											  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
											  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

		cur_RA = FixedVariable(names = ['cur_RA', 'prev_RA', 'MS_RA'], values=['High', 'Middle', 'Low'], 
								value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Low', 'Up'],
												 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
												 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
								prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
											  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
											  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])


		mobile = HyperpriorVariable(names = ['Mobile_movement', 'prev_LL', 'cur_LL', 'prev_RL', 'cur_RL', 
											'prev_LA', 'cur_LA', 'prev_RA', 'cur_RA'], values=['True', 'False'],
											parentValues=[prev_LL.values, cur_LL.values, prev_RL.values, cur_RL.values,
														  prev_LA.values, cur_LA.values, prev_RA.values, cur_RA.values])

		# Define model of agent
		self.model = [MS_LL, MS_RL, MS_LA, MS_RA, prev_LL, prev_RL, prev_LA, prev_RA, cur_LL, cur_RL, cur_LA, cur_RA, mobile]
		self.hypothesisNodes = [MS_LL, MS_RL, MS_LA, MS_RA]
		self.predictionNodes = [mobile]



