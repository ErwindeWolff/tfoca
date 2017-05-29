from variables import *

# Factor, triple with   f[0] = variable names
#                       f[1] = variable & parent values
#                       f[2] = probabilities

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
    
    for value_row, prob_row in zip(value_rows, prob_rows):
        if (value_row[index] == evidence_value):
            new_value_rows.append(value_row)
            new_prob_rows.append(prob_row)

    return (new_var_names, new_value_rows, new_prob_rows)


var = HyperpriorVariable(names = ["Coin Outcome", "Fairness", "Brightness", "Person"], values=["Heads", "Tails"],
                 parentValues = [["Fair", "Unfair"], ["Light", "Dark"], ["Erwin", "Wouter"]]) 

f1 = var.getProbabilityTable()
f1 = (var.names, f1[0], f1[1])
f2 = applyEvidence(f1, "Brightness", "Light")
f3 = sumOut(f2, "Fairness")


def printFactor(f):

    print f[0]
    (foo, bar) = (f[1], f[2])
    for i in range(len(foo)):
        print foo[i], bar[i]
    print ""

printFactor(f1)
printFactor(f2)
printFactor(f3)


















