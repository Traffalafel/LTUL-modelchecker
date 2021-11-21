import re

def parse_formula(formula):

    formula = formula.replace(" ", "")

    # Atomic propositions
    proposition = r"^(\w)$"
    match = re.match(proposition, formula)
    if match is not None:
        p = match.group(1)
        return [p]

    negation = r"^~\((.+)\)$|^~(\w)$"
    match = re.match(negation, formula)
    if match is not None:
        sub = match.group(1) if match.group(1) is not None else match.group(2)
        return ["~", parse_formula(sub)]

    # Knowledge operator
    knowledge = r"^K_(\w)(\(?.+\)?)$"
    match = re.match(knowledge, formula)
    if match is not None:
        agent = match.group(1)
        sub = match.group(2)
        return ["K", agent, parse_formula(sub)]

    # Belief operator
    belief = r"^B_(\w)(\(?.+\)?)$"
    match = re.match(belief, formula)
    if match is not None:
        agent = match.group(1)
        sub = match.group(2)
        return ["B", agent, parse_formula(sub)]

    # Binary operators
    subs, op = get_multi_subformulas(formula)
    parsed = [parse_formula(sub) for sub in subs]
    return [op] + parsed

def get_multi_subformulas(formula):

    # Identify operators
    n_parens = 0
    operators = ["\\/", "/\\", "=>"]
    op_pos = []
    ops = []
    for idx in range(len(formula)):
        if formula[idx] == r"(":
            n_parens += 1
            continue
        if formula[idx] == r")":
            n_parens -= 1
            continue
        if formula[idx] == "!" and n_parens == 0:
            op_pos.append(idx)
            ops.append(formula[idx])
        if formula[idx:idx+2] in operators and n_parens == 0:
            op_pos.append(idx)
            ops.append(formula[idx:idx+2])

    if len(set(ops)) > 1:
        raise "Cannot mix operators"
    op = ops[0]

    # Identify subformulas
    n_subs = len(op_pos)
    idxs = []
    idxs.append((0, op_pos[0]))
    idxs += [(op_pos[i]+len(op), op_pos[i+1]) for i in range(n_subs-1)]
    idxs.append((op_pos[n_subs-1]+len(op), len(formula)))
    phis = [formula[i:j] for (i,j) in idxs]

    # Remove outermost parentheses
    for i,phi in enumerate(phis):
        if phi[0] == "(":
            phi = phi[1:]
        if phi[-1] == ")":
            phi = phi[:-1]
        phis[i] = phi

    return phis, op