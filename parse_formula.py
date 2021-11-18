import re

def parse_formula(formula):

    formula = formula.replace(" ", "")

    # Atomic propositions
    proposition = r"^(\w)$"
    match = re.match(proposition, formula)
    if match is not None:
        p = match.group(1)
        return [p]

    # Parenthesis
    parenthesis = r"^\((.+)\)$"
    match = re.match(parenthesis, formula)
    if match is not None:
        sub = match.group(1)
        return parse_formula(sub)

    negation = r"^~\((.+)\)$|^~(\w)$"
    match = re.match(negation, formula)
    if match is not None:
        sub = match.group(1) if match.group(1) is not None else match.group(2)
        return ["~", parse_formula(sub)]

    # TODO: Epistemic operators

    # Binary operator
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
        if formula[idx:idx+2] in operators and n_parens == 0:
            op_pos.append(idx)
            ops.append(formula[idx:idx+2])

    if len(set(ops)) > 1:
        raise "Cannot mix operators"
    
    # Identify subformulas
    n_ops = len(op_pos)
    idxs = []
    idxs.append((0, op_pos[0]))
    idxs += [(op_pos[i]+2, op_pos[i+1]) for i in range(n_ops-1)]
    idxs.append((op_pos[n_ops-1]+2, len(formula)))
    phis = [formula[i:j] for (i,j) in idxs]

    return phis, ops[0]