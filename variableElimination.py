from variables import *

def sumOut (factor, var_names, var):
    index = var_names.index(var)

    names = list()
    probs = [prob for prob in factor[1]]

    for row in factor[0]:
        new_row = [x for i,x in enumerate(row) if i != index]
        names.append(new_row)

    return (names, probs)


#var = HyperpriorVariable(names = ["Coin Outcome", "Fairness"],values=["Heads", "Tails"] ,
#                 parentValues =[["Fair", "Unfair"]]) 

var = HyperpriorVariable(names = ["Coin Outcome"],values=["Heads"] ,
                 parentValues =[]) 


f1 = var.getProbabilities()
f2 = sumOut(f1, ["Fairness", "Outcome"], "Fairness")

print f1
print f2
