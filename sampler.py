from random import random
from variables import *
from variableElimination import *

################################
# CODE FOR TOPOLOGICAL SORTING #
################################

class Node:

	def __init__(self, name, value):
		self.name = name
		self.children = list()
		
		self.value = value
		
		self.marked = False
		self.markedTemp = False
		
	def addChild(self, child):
		self.children.append(child)
	
	
def toposort(graph):
	sort = list()
	while len(sort) < len(graph):
		for node in graph:
			if not node.marked:
				sort = visit(node, sort)
	return sort
	
				
def visit(node, sort):
	
	if node.markedTemp:
		print("Not a DAG")
	
	if not node.marked:
		node.markedTemp = True
		for child in node.children:
			sort = visit(child, sort)
		node.markedTemp = False
		node.marked = True
		sort = [node] + sort
	return sort

################################
# CODE FOR SELECTING VARIABLES #
################################
	
def selectVariables(variables, queries, evidenced=[]):

    var_selection = list()
    
    # Go up from queried nodes
    for var in queries:
        addParentsRecur(variables, var_selection, var)
        
    # Go up from evidenced nodes
    for var, value in evidenced:
        addParentsRecur(variables, var_selection, var)
        
    return var_selection
        

def addParentsRecur (variables, var_selection, targetName):

	for var in variables:
		# If the right variable
		if var.names[0] == targetName:

			# If this variable was not in the factor list yet
			if var not in var_selection:
				var_selection.append(var)
				
				# Then, recursively add all parents
				for parent in var.names[1:]:
					addParentsRecur(variables, var_selection, parent)	
		
		
def VariablesToGraph(variables):

	graph = dict()

	for var in variables:
		graph[var.names[0]] = Node(var.names[0], var)
		
	for var in variables:
		for father in var.names[1:]:
			graph[father].addChild(graph[var.names[0]])
			
	return list(graph.values())


###############################
# CODE FOR REJECTION SAMPLING #
###############################		

def rejectionSampling(variables, query, evidence, nr_samples, bias = 0.0001):
	
	# Create table to read probabilities from
	small_table = []
	full_table = []
	
	extended_query = []
	
	for var in variables:
		if var.names[0] == query[0]:
			# Define small table
			small_table = [query, [value for value in var.values], [bias for _ in var.values]]
			
			# Define full table via probability table
			table = var.value_rows
			
			diction = dict()
			for key in table.keys():			
				diction[key] = bias
			
			full_table = [var.names, diction]
			#full_table = [var.names, table[0], [bias for _ in table[1]]]
			
			# Define extended query (used later for sampling)
			extended_query = var.names

	# If table could not be created, report and return
	if (len(small_table) <= 0):
		print ("Query not in variable list: {0}".format(query))

	# Select factors
	var_selection = selectVariables(variables, query, evidence)

	# Create a graph from selected factors, then find topological ordering
	graph = VariablesToGraph(var_selection)
	graph = toposort(graph)

	# Unpack variables from graph again
	to_sample = [node.value for node in graph]
	
	# Perform samples
	count = 0
	attempts = 0
	while (count < nr_samples and attempts < 1000*nr_samples):
	
	#for i in range(nr_samples):
		
		attempts += 1
		
		# One sample cycle
		(full_table_entry, small_table_entry) = sampleVariables(to_sample, query, extended_query, evidence)
		
		# If sample was succesful, add info to table
		if len(small_table_entry) > 0:
		
			# Create proper key
			key = "_"
			for value in full_table_entry[1:]:
				key += value + "_"
		
			index = small_table[1].index(small_table_entry)
			small_table[2][index] += 1.0
		
			full_table[1][key] += 1.0
			
			# Indicate that a sample has been succesful
			count += 1
	
	#print("{0} samples rejected".format(attempts-count))
	
	# Normalize probabilities small table
	sum_counts = sum(small_table[2])
	small_table[2] = [count/sum_counts for count in small_table[2]]
	
	# Normalize probabilities full table
	
	probs = full_table[1].values()
	sum_counts = sum(probs)
	full_table = [full_table[0], full_table[1], [count/sum_counts for count in probs]]
	
	return (full_table, small_table)
	
	
def sampleVariables(variables, query, extended_query, evidence):
	
	# Unpack evidence into names and values
	evidence_names = [name for (name, value) in evidence]
	evidence_values = [value for (name, value) in evidence]
	
	# Dictionary to saved sampled values in
	sampled_values = dict()
	
	# Can go in this order because variables are ordered
	for var in variables:
		
		#print(var.names[0])
		
		# Create parent values from already sampled values
		parentValues = []
		for parent in var.names[1:]:
			parentValues.append(sampled_values[parent])
			
		# Get correct values given sampled values so far
		table = var.getProbabilities(parentValues, sampling=True)
		
		#print("TABLE", table)
		
		# Sample over this table
		sampled_value = sampleVariable(table)

		# Check if sampled variable was evidenced
		if var.names[0] in evidence_names:
			# Rejection check
			index = evidence_names.index(var.names[0])
			if (sampled_value != evidence_values[index]):
				return ("", [])
		
		sampled_values[var.names[0]] = sampled_value		
		
	# Create small table entry
	small_table_entry = sampled_values[query[0]]	
	
	# Create full table entry
	full_table_entry = list()
	for key in extended_query:
		full_table_entry.append(sampled_values[key])
		
	return (full_table_entry, small_table_entry)
	
		
'''
	Function to sample a (filtered) probability table.
	Returns the selected value (last by default).
''' 
def sampleVariable(table):	
	sample = random()
	for value, prob in zip(table[0], table[1]):
		if sample <= prob:
			return value
		else:
			sample = sample - prob
	return table[0][-1]


'''
	Generates a number of hypotheses equal to nr_hypo
'''
def generateHypotheses(hypothesisNodes, nr_hypo):

    # Put them together in the hypothesis
    hypotheses = list()
    for i in range(nr_hypo):
        hypotheses.append([(var.names[0], sampleVariable(var.getProbabilities())) for var in hypothesisNodes])

    return hypotheses



