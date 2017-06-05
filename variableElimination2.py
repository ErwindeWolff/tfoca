from variables import *
from factory import *
import numpy as np

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

    matching_indices = dict()
    for i, name1 in enumerate(var_names1):
        for j, name2 in enumerate(var_names2):
            if name1 == name2:
                matching_indices[j] = i

    # Create new variable names
    new_var_names = [name for name in var_names1]
    print new_var_names
    new_var_names.extend([name for name in var_names2 if name not in new_var_names])

    # Variables to fill
    new_value_rows = list()
    new_prob_rows = list()

    # Get each value row with associated probability
    for value_row1, prob1 in zip(value_rows1, prob_rows1):
    
        # Default is order of factor 1
        new_value_row = [val for val in value_row1]
        
        # Get each value row with associated probability
        for value_row2, prob2 in zip(value_rows2, prob_rows2):

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

# Function to print factor
def printFactor(f):

    print f[0]
    (foo, bar) = (f[1], f[2])
    for i in range(len(foo)):
        print foo[i], bar[i]
    print ""

        
def variableElimination(variables, queries, evidence=[]):
    # select factors from all the available variables and the queried variables
    factors = selectFactors(variables,queries,[])  
    for factor in factors:
        for evidenced in evidence:
            factor = applyEvidence(factor,evidenced[0],evidenced[1])
    
    # identify all variable names without duplicates
    var_names = [var_name for var_name in factors[0][0]]    
    var_names.extend([var_name for var_name in factor[0] if var_name not in var_names for factor in factors ])
    
    # iterate over each non-query variable
    for var_name in var_names:
        if var_name not in queries:
            # identify factors containing current non-query variable, and their indices
            factors_to_use = [factor for factor in factors if var_name in factor[0]]
            indices = list()
            for each in factors_to_use:
                indices.append(factors.index(each))
            
            # appoint 'origin factor' to multiply others with
            theFactor = factors_to_use[0]
            # multiply factors containing current non-query variable
            if np.shape(factors_to_use)[0] > 1:
                for each in factors_to_use[1:]:
                    print "current other factor:"
                    printFactor(each) 
                    print "and current thefactor:"
                    printFactor(theFactor) 
                    theFactor = multiplyFactors(each,theFactor)
                    printFactor(theFactor)

            # remove all factors used above from the current list of factors
            factors_copy = list(factors)
            factors = list()
            for i, factor in enumerate(factors_copy):
                if i not in indices:
                    factors.append(factor)
            
            
            theFactor = sumOut(theFactor, var_name)         
            # sum out the current non-query variable
            factors.append(theFactor)
    return factors
        
    










