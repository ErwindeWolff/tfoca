from variables import *

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


    

    
