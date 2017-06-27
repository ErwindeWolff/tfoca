import matplotlib.pyplot as plt

from math import log
from random import random

################################################################################################

def dirichlet(alfas, steps=100):

	values = list()
	probabilities = list()
	
	dirichlet_recur(alfas, values, probabilities, [], 0, steps)
	
	sum_probs = sum([p * (1.0/len(probabilities)) for p in probabilities])
	probabilities = [prob/sum_probs for prob in probabilities]
	
	return (values, probabilities)
	

def dirichlet_recur(alfas, values, probabilities, cur_values, index, steps=100):

	if index == len(alfas)-1:
	
		cur_values.append(1.0 - sum(cur_values))
		
		prob = 1.0
		for x, alfa in zip(cur_values, alfas):
			prob = prob * x**(alfa-1.0)
		
		values.append(cur_values)
		probabilities.append(prob)
		
	else:
		end = steps - int(steps*sum(cur_values))
		for i in range(end+1):
			x = (i*1.0)/steps
			dirichlet_recur(alfas, values, probabilities, cur_values + [x], index+1, steps)

################################################################################################

def update_dirichlet(values, probabilities, update):

	new_probabilities = list()
	for value, prob in zip(values, probabilities):
		new_prob = prob
		for x, c in zip(value, update):
			new_prob = new_prob * x**c
		new_probabilities.append(new_prob)
		
	sum_new_probs = sum([p * (1.0/len(new_probabilities)) for p in new_probabilities])
	new_probabilities = [prob/sum_new_probs for prob in new_probabilities]
	
	return new_probabilities

################################################################################################

def entropy(probabilities):
	width = 1.0/len(probabilities)
	return -sum([p*width * log(p*width, 2) for p in probabilities if p != 0])

################################################################################################

def sampleHyperprior(values, probabilities):
	
	choice = random() * sum(probabilities)
	
	for v, p in zip(values, probabilities):
	
		#print(choice, p)
	
		if choice <= p:
			return v
		choice -= p
	
	return values[-1]


################################################################################################

steps = 100
(v, p) = dirichlet([1.0, 1.0], steps)

#for x in p:
#	print(x)


#x = [0]
#e = [entropy(p)]

plt.figure(0)
plt.plot(range(len(p)), p)
for i in range(5):
	p = update_dirichlet(v, p, [0.0, 1.0])	

	#x.append(i+1)
	#e.append(entropy(p))

	#plt.plot(range(len(p)), p)
#plt.show()

#plt.figure(1)
#plt.plot(x, e)
#plt.show()

foo = 0.0
samples = 10
for _ in range(samples):
	foo += sampleHyperprior(v, p)[0]

print(foo/samples)


#plt.plot(x, probabilities)
#plt.plot(x, p)
#plt.legend(['Dirichlet (3,3) Instant', 'Dirichlet (3,3) Iterative'])
#plt.show()



