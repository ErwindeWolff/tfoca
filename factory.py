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

# Function to print variable table
def printVar(var):
    
    if (len(var.names) > 1):
        print(var.names[0] + " given " + str(var.names[1::]) + "\n")
    else:
        print( var.names[0])

    (foo, bar) = var.getProbabilityTable()
    for i in range(len(foo)):
        print( foo[i], bar[i])
    print("")

# Function to print factor
def printFactor(f):

    print(f[0])
    (foo, bar) = (f[1], f[2])
    for i in range(len(foo)):
        print(foo[i], bar[i])
    print("")

