# -*- coding: utf-8 -*-
from variables import *
from bayesianNetwork import *
from variableElimination import * 
from factory import *

def makeTreeNetwork(tree_depth, num_children = 2):
    network = list()
    depth = 0
    # Make the uppermost node, and add it to the network
    node = Variable(names = ["Layer_{0}_Node_{1}".format(depth, 1)], values=["True", "False"], parentValues=[])
    network.append(node)
    # Recursively add children to the current uppermost node
    makeChildren(network, [node], depth+1, tree_depth, num_children, 1)   
    return network

def makeChildren(network, parents, depth, tree_depth, num_children, current_width):
    # If the tree has not reached its maximum depth:
    if depth < tree_depth:
        # make list of node numbers for all children
        cur_positions = [(current_width*num_children)-i for i in range(num_children)[::-1]]
        # For each child we make for the current parent:
        for pos in cur_positions:
            # make list of names for this variable; a list containing the current name, and the names of all recursive parents.
            names = []
            names.append("Layer_{0}_Node_{1}".format(depth, pos))
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
            # recursively make children to this node until the tree depth has been reached
            makeChildren(network, [node], depth+1, tree_depth, num_children, pos)
            
def makeFunnelNetwork(funnel_depth, num_parents = 2):
    network = list()
    depth = funnel_depth
    # recursively make parents for current node
    parents = makeParents(network, depth-1, num_parents, 1)
    # make parameters for current node
    names = list()
    parentValues = list()
    values = ["True","False"]
    # append the node's own name to the list of names
    names.append("Layer_{0}_Node_{1}".format(depth, 1))
    # extract parent values and names from this node's parents
    if len(parents)>1:    
        for parent in parents:
            parentValues.append(parent.values)
            names.append(parent.names[0])
    node = Variable(names=names, values=values, parentValues=parentValues)
    network.append(node)
    return network
    
def makeParents(network, depth, num_parents, current_width):
    current_parents = list()
    # If the funnel has not reached its maximum depth:
    if depth > 0:        
        # make list of node numbers for all parents
        cur_positions = [(current_width*num_parents)-i for i in range(num_parents)[::-1]]
        # for each parent we make for the current child:
        for pos in cur_positions:
            # recursively make parents for current node
            parents = makeParents(network, depth-1, num_parents, pos)
            names = list()
            parentValues = list()
            # append the node's own name to the list of names
            names.append("Layer_{0}_Node_{1}".format(depth, pos))
            # make list of values for this variable
            values = ["True","False"]
            # extract parent values and names from this node's parents
            if len(parents)>1:
                for parent in parents:
                    parentValues.append(parent.values)
                    names.append(parent.names[0])
            # make the parent and add it to the network
            parent = Variable(names = names, values = values, parentValues = parentValues)
            current_parents.append(parent)
            network.append(parent)
    return current_parents
    
myTree = makeFunnelNetwork(3, num_parents=3)

printFactor( VE( myTree, ["Layer_1_Node_9"], [("Layer_2_Node_3","True")]))