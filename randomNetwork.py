# -*- coding: utf-8 -*-
from variables import *
from bayesianNetwork import *
from variableElimination import VE, printFactor
from factory import *
import numpy as np

def makeTreeNetwork(tree_depth, num_children = 2):
    network = list()
    hypothesis = list()
    prediction = list()
    depth = 0
    
    # Make the uppermost node, and add it to the network
    node = Variable(names = ["Layer_{0}_Node_{1}".format(depth+1, 1)], values=["True", "False"], parentValues=[])
    network.append(node)
    hypothesis.append(node)
    
    # Recursively add children to the current uppermost node
    makeChildren(network, [node], depth+1, tree_depth, num_children, 1, prediction) 

    return network, hypothesis, prediction

def makeChildren(network, parents, depth, tree_depth, num_children, current_width, prediction):
    # If the tree has not reached its maximum depth:
    if depth < tree_depth:
        # make list of node numbers for all children
        cur_positions = [(current_width*num_children)-i for i in range(num_children)[::-1]]
        
        # For each child we make for the current parent:
        for pos in cur_positions:
            # make list of names for this variable; a list containing the current name, and the names of all recursive parents.
            names = []
            names.append("Layer_{0}_Node_{1}".format(depth+1, pos))
            # make list of values for this variable
            values = ["True","False"]
            
            # extract parent values from the child's parent
            parentValues = list()
            for parent in parents:
                parentValues.append(parent.values)
                names.append(parent.names[0])
                
            # Make current child node and add to the network
            node = Variable(names=names, values=values, parentValues=parentValues)
            network.append(node)
            
            # Add the current node's index to prediction nodes indices if it is a prediction node
            if depth+1==tree_depth:
                prediction.append(node)
            
            # recursively make children to this node until the tree depth has been reached
            makeChildren(network, [node], depth+1, tree_depth, num_children, pos, prediction)
            
def makeFunnelNetwork(funnel_depth, num_parents = 2):
    network = list()
    hypothesis = list()
    prediction = list()
    
    depth = funnel_depth
    # recursively make parents for current node
    parents = makeParents(network, depth-1, num_parents, 1, hypothesis)
    
    # make parameters for current node
    names = list()
    parentValues = list()
    values = ["True","False"]
    
    # append the node's own name to the list of names
    names.append("Layer_{0}_Node_{1}".format(depth, 1))
    
    # extract parent values and names from this node's parents
    if len(parents)>0:    
        for parent in parents:
            parentValues.append(parent.values)
            names.append(parent.names[0])
            
    node = Variable(names=names, values=values, parentValues=parentValues)
    network.append(node)
    
    prediction.append(node)
    
    return network, hypothesis, prediction
    
def makeParents(network, depth, num_parents, current_width, hypothesis):
    current_parents = list()
    # If the funnel has not reached its maximum depth:
    if depth > 0:        
        # make list of node numbers for all parents
        cur_positions = [(current_width*num_parents)-i for i in range(num_parents)[::-1]]
        # for each parent we make for the current child:
        for pos in cur_positions:
            # recursively make parents for current node
            parents = makeParents(network, depth-1, num_parents, pos, hypothesis)
            names = list()
            parentValues = list()
            
            # append the node's own name to the list of names
            names.append("Layer_{0}_Node_{1}".format(depth, pos))
            
            # make list of values for this variable
            values = ["True","False"]
            
            # extract parent values and names from this node's parents
            if len(parents)>0:
                for parent in parents:
                    parentValues.append(parent.values)
                    names.append(parent.names[0])
            
            # make the parent and add it to the network
            parent = Variable(names = names, values = values, parentValues = parentValues)
            current_parents.append(parent)
            network.append(parent)
            
            # if we're at the uppermost layer, indicate the current node as a hypothesis node
            if depth == 1:
                hypothesis.append(parent)
    return current_parents
    
def makeLayerNetwork(layers):
    network = list()
    hypothesis = list()
    prediction = list()
    for i, layer in enumerate(layers):
        # Save the previous layer's size for use in getting the parents' names and values
        if i > 0:
            previous = layers[i-1]
        else:
            previous = 0
        
        # make a list for the current layer to be added to the network after each loop
        current_layer = list()
        
        for pos in range(layer):
            # make parameters for current node
            names = list()
            values = ["True","False"]
            parentValues = list()
            
            # add the current node's name to the list of names
            names.append("Layer_{0}_Node_{1}".format(i+1,pos+1))
            
            # if there is a previous layer:
            if previous > 0:
                for parent in network[-previous:]:
                    # extend the current node's names with the parents' names
                    names.append(parent.names[0])
                    # extend the current node's parent values with the parents' values
                    parentValues.append(parent.values) 
                    
            node = Variable(names=names, values=values, parentValues=parentValues)
            current_layer.append(node)
            
        # Add all nodes in the current layer to the network, and if necessary to hypothesis or prediction
        for node in current_layer:
            network.append(node)
            if previous == 0:
                hypothesis.append(node)
            elif i == len(layers)-1:
                prediction.append(node)
    return network, hypothesis, prediction
    
def makeWorldNetwork(network, hypothesis, prediction):
    # copy the given model as the world to which we will add unobserved variables
    world = list()
    world_hypothesis = list()
    world_prediction = list()
    
    # make the unobserved world node, and add it to the world model
    unobserved = Variable(names=["Unobserved_Node"], values = ["True","False"], parentValues=[])
    world.append(unobserved)
    
    # iterate over the observed variables we will add
    for var in network:
        # copy the current node's names, values and parentValues
        names = list(var.names)
        values = list(var.values)
        parentValues = [parent.values for parent in network if parent.names[0] in var.names[1:]]            
        
        # If the current node is a prediction node, unobserved node's influences are added
        if var in prediction:
            # add the unobserved node's name and values to the names and parentValues
            names.append(unobserved.names[0])
            parentValues.append(unobserved.values)
            
        # make the node and add it to the world model
        new_var = Variable(names=names, values=values, parentValues = parentValues)
        world.append(new_var)
        
        if var in prediction:
            world_prediction.append(new_var)
        elif var in hypothesis:
            world_hypothesis.append(new_var)
    return world, world_hypothesis, world_prediction, unobserved 
    
myTree, hypotheses, predictions = makeTreeNetwork(4)#makeLayerNetwork([2,3,4,2])
print len(myTree)
world, world_hypotheses, world_predictions, unobserved = makeWorldNetwork(myTree, hypotheses, predictions)
print len(world)
factor = VE(world, [world_predictions[-1].names[0]], evidence=[])
printFactor(factor)