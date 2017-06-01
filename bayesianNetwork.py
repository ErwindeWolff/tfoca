

class BayesianNetwork():
    def __init__(self, pred_nodes, inter_nodes, hypo_nodes):
        self.pred_nodes = pred_nodes
        self.inter_nodes = inter_nodes
        self.hypo_nodes = hypo_nodes

    def getVariables(self):
        return self.pred_nodes + self.inter_nodes + self.hypo_nodes

    


class WorldNetwork(BayesianNetwork):
    def __init__(self, pred_nodes, inter_ndoes, hypo_nodes, extra_nodes, extra_cycles):
    
        self.pred_nodes = pred_nodes
        self.inter_nodes = inter_nodes
        self.hypo_nodes = hypo_nodes

        self.extra_nodes = extra_nodes
        self.extra_cycles = extra_cycles

        self.counter = 0

    def observe(self, hypo_nodes):
        

        self.counter += 1
        
