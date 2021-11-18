import re
import sys

class Model():

    def __init__(self, W, R, V):
        self.W = W
        self.R = R
        self.V = V

    def get_reachable(self, state, agent):

        # Build dictionary of neighbor states
        r = dict()
        for (s,d) in self.R[agent]:
            if s not in r:
                r[s] = set([d])
            else: 
                r[s].add(d)
            if d not in r:
                r[d] = set([s])
            else: 
                r[d].add(s)
        
        if state not in r:
            return set()

        reachable = r[state]
        check = r[state]
        while len(check) != 0:
            s = next(iter(check))
            reachable = reachable.union(r[s])
            check.remove(s)
        
        return reachable

def parse_model(content):

    content = content.replace(" ", "")
    lines = content.split("\n")

    V_pattern = "^(\w+):(\w(,\w)*)$"
    R_pattern = "^(\w+):(\(\w+->\w+\)(,\(\w+->\w+\))*)$"

    W = set(lines[0].split(","))
    R = dict()
    V = dict()

    for line in lines:

        # R lines
        match = re.match(R_pattern, line)
        if match is not None:
            agent = match.group(1)
            trans_s = match.group(2)
            trans_s = trans_s.replace("(", "")
            trans_s = trans_s.replace(")", "")
            transitions = [s.split("->") for s in trans_s.split(",")]
            R[agent] = transitions

        # V lines
        match = re.match(V_pattern, line)
        if match is not None:
            state = match.group(1)
            props = set(match.group(2).split(","))
            V[state] = props

    # Add empty sets for state with no propositions
    for state in W:
        if state not in V:
            V[state] = set()

    return Model(W, R, V)

def main():
    file_path = sys.argv[1]
    with open(file_path, 'r') as fd:
        content = fd.read()
    model = parse_model(content)
    print(model.W)
    print(model.R)
    print(model.V)

    print(model.get_reachable('s0', 'a'))

if __name__ == "__main__":
    main()