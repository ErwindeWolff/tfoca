from variables import *
import numpy as np



def selectFactors(variables, queries, evidenced=[]):

    factors = list()
    
    # Go up from queried nodes
    for var in queries:
        addParentsRecur(variables, factors, var)
        
    # Go up from evidenced nodes
    for var, value in evidenced:
        addParentsRecur(variables, factors, var)
        
    return factors
        

def addParentsRecur (variables, factors, parentName):

    for var in variables:
        # If the parent...
        if var.names[0] == parentName:

            # Create factor
            (value_rows, prob_rows) = var.getProbabilityTable()
            factor = (var.names, value_rows, prob_rows)
            
            # If this factor was not in the factor list yet
            if factor not in factors:
                factors.append(factor)
            
                # Then, recursively add all parents
                for parent in factor[0][1::]:
                    addParentsRecur(variables, factors, parent)

# Function to print factor
def printFactor(f):

    print(f[0])
    (foo, bar) = (f[1], f[2])
    for i in range(len(foo)):
        print (foo[i], bar[i])
    print ("")


def applyEvidence(factor, var, evidence_value):
    # Unpack factor
    (var_names, value_rows, prob_rows) = factor

    # Get index of to-sum-out variable in table
    index = var_names.index(var)
    
    # Create new factor parameters
    new_var_names = [name for name in var_names]
    new_value_rows = list()
    new_prob_rows = list()
    
    # Iterate through the complete table
    for value_row, prob_row in zip(value_rows, prob_rows):

        # If the evidenced variable matches the evidence, save it
        if (value_row[index] == evidence_value):
            new_value_rows.append(value_row)
            new_prob_rows.append(prob_row)

    return (new_var_names, new_value_rows, new_prob_rows)


def multiplyFactors(factor1, factor2):

    # Unpack factors
    (var_names1, value_rows1, prob_rows1) = factor1
    (var_names2, value_rows2, prob_rows2) = factor2

    # Find indices where column i in factor 1 points to 
    # the same variable as a column j in factor 2
    matching_indices = dict()
    for i, name1 in enumerate(var_names1):
        for j, name2 in enumerate(var_names2):
            if name1 == name2:
                matching_indices[j] = i

    # Create new variable names
    new_var_names = [name for name in var_names1]
    new_var_names.extend([name for name in var_names2 if name not in new_var_names])

    # Variables to fill
    new_value_rows = list()
    new_prob_rows = list()

    # Get each value row with associated probability
    for value_row1, prob1 in zip(value_rows1, prob_rows1):
        
        # Get each value row with associated probability
        for value_row2, prob2 in zip(value_rows2, prob_rows2):

            # Default is order of factor 1
            new_value_row = [val for val in value_row1]

            # Traverse all values in value_row 2
            succesful = True
            for j, value in enumerate(value_row2):

                # If the value should match one in value row 1:
                if (j in matching_indices):
                    
                    # ...and this fails: stop
                    if value_row1[matching_indices[j]] != value:
                        succesful = False
                        break
                
                # If not, add value to current row
                else:
                    new_value_row.append(value)

            # If rows could be merged: add them (else do nothing)
            if succesful:
                new_value_rows.append(new_value_row)
                new_prob_row = prob1 * prob2
                new_prob_rows.append(new_prob_row)

    # Return new factors
    return (new_var_names, new_value_rows, new_prob_rows) 
        

def sumOut(factor, var):
    # Unpack factor
    (var_names, value_rows, prob_rows) = factor

    # Get index of to-sum-out variable in table
    index = var_names.index(var)
    
    # Create new factor parameters
    new_var_names = [name for i, name in enumerate(var_names) if i != index]
    new_value_rows = list()
    new_prob_rows = list()

    # Traverse each row of probability table
    for value_row, prob_row in zip(value_rows, prob_rows):
        # Remove to-sum-out variable from row
        new_value_row = [value for i, value in enumerate(value_row) if i != index]

        # If this combination was not yet added, add and save probability
        if (new_value_row not in new_value_rows):
            new_value_rows.append(new_value_row)
            new_prob_rows.append(prob_row)

        # else if if was added, just add this probability to existing one
        else:
            i = new_value_rows.index(new_value_row)
            new_prob_rows[i] += prob_row

    # Return new factor
    return (new_var_names, new_value_rows, new_prob_rows)


def VE (variables, query, evidence=[]):

    # Gather relevant factors
    factors = selectFactors(variables, query, evidence)  

    # Apply evidence to factors
    for evidenced in evidence:
        for i, factor in enumerate(factors):
            if (evidenced[0] in factor[0]):
                factors[i] = applyEvidence(factor,evidenced[0],evidenced[1])

    # Determine variable (names) to eliminate
    var_names = list()
    for factor in factors:
        name = factor[0][0]
        if (name not in query):
            var_names.append(name)

    for i, name in enumerate(var_names):

        # Gather factors to multiply then sumout
        process_factors = [factor for factor in factors if name in factor[0]]

        # Redefine factors to no longer contain to be processed factors
        factors = [factor for factor in factors if factor not in process_factors]

        # While there are at least two factors to multiply
        new_factor = process_factors[0]

        while (len(process_factors) > 1):
            
            # Multiply two factors
            new_factor = multiplyFactors(process_factors[0], process_factors[1])
        
            # Replace first factor with new one and pop last from list
            process_factors[0] = new_factor
            process_factors = [f for i, f in enumerate(process_factors) if i > 1]

        # Sum out the variable in question
        new_factor = sumOut(new_factor, name)

        # Append new factor
        factors.append(new_factor)


    # Multiply remaining factors
    factor = factors[0]
    while (len(factors) > 1):
        factor = multiplyFactors(factors[0], factors[-1])
        factors = factors[:-1]

    # Perform normalization
    sum_probs = sum(factor[2])
    factor = [factor[0], factor[1], [prob/sum_probs for prob in factor[2]]]

    return factor
        

def getPredictionTables (variables, query, evidence):

    # Create new query for full table
    for var in variables:
        if var.names[0] == query[0]:
            new_query = var.names

    # Find this full factor (for weighted updates)
    full_factor = VE(variables, new_query, evidence)

    # Sum out larger to smaller variable
    small_factor = full_factor
    for var_name in new_query:
        if var_name not in query:
            small_factor = sumOut(small_factor, var_name)

    # Return full table first, smaller one second
    return (full_factor, small_factor)




