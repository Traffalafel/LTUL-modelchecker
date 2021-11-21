import re
from parse_model import Model

def get_sets(f_parsed, model:Model):

    n_args = len(f_parsed)

    # Propositional atom
    if n_args == 1:
        p = f_parsed[0]
        states = set()
        for s in model.W:
            if p in model.V[s]:
                states.add(s)
        return states

    # Negation
    if f_parsed[0] == "~":
        states_sub = get_sets(f_parsed[1], model)
        return model.W.difference(states_sub)

    # AND
    if f_parsed[0] == "/\\":
        states_sub = [get_sets(f, model) for f in f_parsed[1:]]
        return set.intersection(*states_sub)
    
    # OR
    if f_parsed[0] == "\\/":
        states_sub = [get_sets(f, model) for f in f_parsed[1:]]
        return set.union(*states_sub)

    # Implication
    if f_parsed[0] == "=>":
        sub1 = get_sets(f_parsed[1], model)
        sub2 = get_sets(f_parsed[2], model)
        subs = [sub2, model.W.difference(sub1)]
        return set.union(*subs) # p => q === ~p \/ q

    # Knowledge 
    if f_parsed[0] == "K":
        agent = f_parsed[1]
        subformula = f_parsed[2]
        states = set()
        for w in model.W:
            possible = model.get_possible(agent, w)
            if len(possible) == 0:
                continue
            s = get_sets(subformula, model)
            satisfying = [v for v in possible if v in s]
            if len(possible) == len(satisfying):
                states.add(w)
        return states

    # Belief
    if f_parsed[0] == "B":
        agent = f_parsed[1]
        subformula = f_parsed[2]
        states = set()
        for w in model.W:
            possible_w = model.get_possible(agent, w)
            maxes = model.get_max(agent, possible_w)
            s = get_sets(subformula, model)
            satisfying = [v for v in maxes if v in s]
            if len(maxes) == len(satisfying):
                states.add(w)
        return states