from random import random
from variables import *
from factory import *
from variableElimination import *



def rejectionSampling(variables, query, evidence, nr_samples, bias=0.1):

    small_table = []
    full_table = []

    for var in variables:
        if var.names[0] == query[0]:
            small_table = [[value for value in var.values], [bias for _ in var.values]]
            full_table = ["" for name in var.names]

    if (len(full_table) <= 0):
        print ("Query not in variable list: {0}".format(query))

    factors = selectFactors(variables, query, evidence)
    for _ in range(nr_samples):
        (small_table_entry, full_table_entry) = rejectionSample(factors, query[0], evidence)

        if len(small_table_entry) > 0:
            index = small_table[0].index(small_table_entry)
            small_table[1][index] += 1.0

        #print("{0} = {1}\n".format(query[0], small_table_entry))

    sum_counts = sum(small_table[1])
    small_table[1] = [count/sum_counts for count in small_table[1]]

    for x, y in zip(small_table[0], small_table[1]):
        print(x, y)


    #index = small_table[0].index(sampled_value) 
    #small_table[0][index] += 1.0


def rejectionSample(all_factors, query, evidence):

    # Make copy of all_factors
    factors = [factor for factor in all_factors]

    # Unpack evidence into names and values
    evidence_names = [name for (name, value) in evidence]
    evidence_values = [value for (name, value) in evidence]

    small_table_entry = ""
    full_table_entry = []

    query_parents = []
    for f in factors:
        if f[0][0] == query:
            query_parents = [name for name in f[0]]
            full_table_entry = ["" for _ in f[0]]

    while len(factors) > 0:
        
        # Split factor into to-sample and not-to-sample
        single_factors = []
        new_factors = []
   
        for factor in factors:

            # To sample
            if len(factor[0]) == 1:
                single_factors.append(factor)

            # Not-to-sample
            else:
                new_factors.append(factor)

        # Change pointer
        factors = new_factors

        for factor in single_factors:

            # Get random value from factor
            sampled_value = sampleFactor(factor)

            # Extract name from factor
            f_name = factor[0][0]

	        # If the query was sampled, save into tables.
            if f_name == query:

		        # Increment the small table at the proper index
                small_table_entry = sampled_value
		
		        # Increment the full table at the proper index
                full_table_entry[0] = sampled_value
		
	        # Else if the factor was one of the parents of the query
            elif f_name in query_parents:
	
                index = query_parents.index(f_name)
                full_table_entry[index] = sampled_value

            # Check if sample matches 
            if f_name in evidence_names:

                # Rejection check
                index = evidence_names.index(f_name)
                if (sampled_value != evidence_values[index]):
                    return ("", [])


            # Now update all further factors to sample over with this evidence
            new_factors = list()
            for f in factors:
                if (f_name in f[0]):
                    new_factor = applyEvidence(f, f_name, sampled_value)
                    new_factor = ([n for n in f[0] if n != f_name], new_factor[1], new_factor[2])
                    new_factors.append(new_factor)
                else:
                    new_factors.append(f)
            # Change pointer
            factors = new_factors        

    return (small_table_entry, full_table_entry)

            









#index = full_table[0].index(cur_table_entry)
#full_table[1][index] += 1.0


	# Sample through factors one by one.

	# If a parent of query: save sampled value
	
	# If query itself:
		# Add 1 counter to small_table where the value equals the sampled_value
		# Add 1 counter to full_table where the values of the parents and the sampled value of query match





























def getSampledProbability(variables, query, evidence, nr_samples, bias=0.1):


    count = []
    values = []

    # Find number of values to keep track of
    for var in variables:
        if var.names[0] == query[0]:
            count = [bias for i in range(len(var.values))]
            values = [value for value in var.values]

    if len(count) == 0:
        print("Query not existent among variables: {0}".format(query))
        return

    for i in range(nr_samples):
        value = getSampledPrediction(variables, query, evidence)
        count[values.index(value)] += 1.0

    sum_count = sum(count)

    return (query[0], [c/sum_count for c in count])


def getSampledPrediction(variables, query, evidence):

    # Select all factors
    factors = selectFactors(variables, query, evidence)


##################################
#TEST WITH EVIDENCE: PROBABLY NEED TO APPLY EVIDENCE STILL
##########################################


    # While list doesn't contain just query
    while len(factors) > 1:
        
        # Grab sampleable factors from list
        single_factors = [factor for factor in factors if len(factor[0]) == 1 and factor[0] != query[0]]

        # Remove those from the factors list
        factors = [factor for factor in factors if factor not in single_factors]

        # For each factor, determine value randomly
        for sf in single_factors:
            name = sf[0][0]

            sample_value = sampleFactor(sf)

            # Apply this evidence to each other factor if applicable
            new_factors = list()
            for f in factors:
                if (name in f[0]):
                    new_factor = applyEvidence(f, name, sample_value)
                    new_factor = ([n for n in f[0] if n != name], new_factor[1], new_factor[2])
                    new_factors.append(new_factor)
                else:
                    new_factors.append(f)

            factors = new_factors

    for f in factors:
        print(f[0], f[1])

    # Return the value of the query factor
    return sampleFactor(factors[0])
            


# Generates a number of hypotheses equal to nr_hypo
def generateHypotheses(hypothesisNodes, nr_hypo):
    
    # Create factors from hypothesisNodes
    factors = list()
    for var in hypothesisNodes:
        (value_rows, prob_rows) = var.getProbabilityTable()
        factors.append((var.names, value_rows, prob_rows))

    # Put them together in the hypothesis
    hypotheses = list()
    for i in range(nr_hypo):
        hypotheses.append([(factor[0][0], sampleFactor(factor)) for factor in factors])

    return hypotheses

# Samples the factor and returns the chosen value
def sampleFactor(factor):
    (names, values, probs) = factor

    choice = random()
    for value, prob in zip(values, probs):
        if (choice <= prob):
            return value[0]
        else:
            choice -= prob

    return values[-1]


