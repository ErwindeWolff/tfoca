from math import log

# Returns kullback-leiber divergence between prediction and observed
# Where in the definition, P = obs ad Q = pred
def KLD (obs, pred):
    return sum([x1 * log((x1/x2), 2) for x1, x2 in zip(obs, pred) if x1 != 0.0])


def simulation( agent_model, world_model, nr_iterations, sampling=False, weighting = False):

    hypo_nodes = agent_model.getHypothesisNodes()    

    pred_errors = list() 

    for _ in range(nr_iterations):

        hypo_truth = world_model.observe(hypo_nodes)

        pred =  agent_model.getPrediction(hypo_truth, sampling)
        obs = world_model.getPrediction(hypo_truth, sampling)

        pred_error = KLD(obs, pred)

        agent_model.update(obs, pred_error, weighting)
