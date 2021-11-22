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
    knowledge = r"^K_(\w+)\((.+)\)$|^K_(\w+)([a-z])$"
    match = re.match(knowledge, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["K", agent, parse_formula(sub)]

    # Belief operator
    belief = r"^B_(\w+)\((.+)\)$|^B_(\w+)([a-z])$"
    match = re.match(belief, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["B", agent, parse_formula(sub)]

    # Safe belief operator
    safebelief = r"^S_(\w+)\((.+)\)$|^S_(\w+)([a-z])$"
    match = re.match(safebelief, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["S", agent, parse_formula(sub)]

    # Weakly safe belief operator
    weaklysafebelief = r"^W_(\w+)\((.+)\)$|^W_(\w+)([a-z])$"
    match = re.match(weaklysafebelief, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["T", agent, parse_formula(sub)]

    # Strong belief operator
    strongbelief = r"^T_(\w+)\((.+)\)$|^T_(\w+)([a-z])$"
    match = re.match(strongbelief, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["T", agent, parse_formula(sub)]

    # Ignorance operator
    ignorance = r"^I_(\w+)\((.+)\)$|^I_(\w+)([a-z])$"
    match = re.match(ignorance, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["I", agent, parse_formula(sub)]
    
    # Doubt operator
    doubt = r"^D_(\w+)\((.+)\)$|^D_(\w+)([a-z])$"
    match = re.match(doubt, formula)
    if match is not None:
        agent = match.group(1) if match.group(1) is not None else match.group(3)
        sub = match.group(2) if match.group(2) is not None else match.group(4)
        return ["D", agent, parse_formula(sub)]

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

    # Check that there is just one operator type
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

    # Check that numbers of subformulas are valid
    if (op == "=>" or op == "!") and len(phis) > 2:
        raise "Cannot have more than 2 subformulas for operator"

    # Remove outermost parentheses
    for i,phi in enumerate(phis):
        if phi[0] == "(":
            phi = phi[1:]
        if phi[-1] == ")":
            phi = phi[:-1]
        phis[i] = phi

    return phis, op