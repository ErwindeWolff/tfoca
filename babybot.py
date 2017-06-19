from variables import *
from agents import *
from predProc import *

# Define motor signal variables
MS_LL = FixedVariable(names = ['MS_LL'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
								prob_table = [[0.5, 0.5]])

MS_RL = FixedVariable(names = ['MS_RL'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
								prob_table = [[0.5, 0.5]])

MS_LA = FixedVariable(names = ['MS_LA'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
								prob_table = [[0.5, 0.5]])

MS_RA = FixedVariable(names = ['MS_RA'], values=['Up', 'Still', 'Down'], value_row_table=[[]], 
								prob_table = [[0.5, 0.5]])

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
						value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Down', 'Up'],
										 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
										 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
						prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
									  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
									  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

cur_RL = FixedVariable(names = ['cur_RL', 'prev_RL', 'MS_RL'], values=['High', 'Middle', 'Low'], 
						value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Down', 'Up'],
										 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
										 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
						prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
									  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
									  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

cur_LA = FixedVariable(names = ['cur_LA', 'prev_LA', 'MS_LA'], values=['High', 'Middle', 'Low'], 
						value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Down', 'Up'],
										 ['High', 'Still'], ['Middle', 'Still'], ['Low', 'Still'],
										 ['High', 'Down'], ['Middle', 'Down'], ['Low', 'Down']], 
						prob_table = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
									  [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
									  [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

cur_RA = FixedVariable(names = ['cur_RA', 'prev_RA', 'MS_RA'], values=['High', 'Middle', 'Low'], 
						value_row_table=[['High', 'Up'], ['Middle', 'Up'], ['Down', 'Up'],
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
model = [MS_LL, MS_RL, MS_LA, MS_RA, prev_LL, prev_RL, prev_LA, prev_RA, cur_LL, cur_RL, cur_LA, cur_RA, mobile]
hypothesisNodes = [MS_LL, MS_RL, MS_LA, MS_RA]
predictionNodes = [mobile]

a = DeterministicAgent(model, hypothesisNodes, predictionNodes, use_weighting=True)

err = []
epochs = 20
for i in range(epochs):
	print(i)

	(full_table, small_table, hypothesis) = a.makePrediction(["Mobile_movement"], ["True"], [])

	#printFactor(full_table)
	print(small_table)

# SOMETHING WITH GETTING OBSERVATION FROM WORLD GIVEN HYPOTHESIS AGENT

	prediction_error = KLD(observation, small_table[2])
	err.append(prediction_error)

	for value_row, prob_row in zip(full_table[1], full_table[2]):

		update = [prob_row * obs for obs in observation]

		a.updateModel("Mobile_movement", value_row[1:], update, prediction_error)

	print ""

x = [i for i in range(epochs)]

plt.figure()
plt.plot(x, err)
plt.show()


