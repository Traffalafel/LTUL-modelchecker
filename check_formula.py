import re

def get_sets(f_parsed, model):

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

    # Safe belief
    if f_parsed[0] == "S":
        agent = f_parsed[1]
        subformula = f_parsed[2]
        states = set()
        satisfying = get_sets(subformula, model)
        for w in model.W:
            post = model.get_post(agent, w)
            if len(satisfying.intersection(post)) == len(post):
                states.add(w)
        return states

    # Weakly safe belief
    if f_parsed[0] == "W":
        agent = f_parsed[1]
        subformula = f_parsed[2]
        states = set()
        satisfying = get_sets(subformula, model)
        for w in model.W:
            if w not in satisfying:
                continue
            post = model.get_strict_post(agent, w)
            if len(satisfying.intersection(post)) == len(post):
                states.add(w)
        return states

    # Strong belief
    if f_parsed[0] == "T":
        agent = f_parsed[1]
        sub = f_parsed[2]
        f_new = ["/\\", ["B", agent, sub], ["K", agent, ["=>", sub, ["S", agent, sub]]]]
        return get_sets(f_new, model)

    # Ignorance
    if f_parsed[0] == "I":
        agent = f_parsed[1]
        sub = f_parsed[2]
        f_new = ["/\\", ["~", ["K", agent, sub]], ["~", ["K", agent, ["~", sub]]]]
        return get_sets(f_new, model)
    
    # Doubt
    if f_parsed[0] == "D":
        agent = f_parsed[1]
        sub = f_parsed[2]
        f_new = ["/\\", ["~", ["B", agent, sub]], ["~", ["B", agent, ["~", sub]]]]
        return get_sets(f_new, model)

    # Announcement
    if f_parsed[0] == "!":
        f_announcement = f_parsed[1]
        f_consequence = f_parsed[2]

        satisfying_before = get_sets(f_announcement, model)

        model_new = model.announce(f_announcement)
        satisfying_after = get_sets(f_consequence, model_new)
        return model_new.W.difference(satisfying_before).union(satisfying_after)
