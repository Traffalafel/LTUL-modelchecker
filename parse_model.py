import re
import sys

class Model():

    def __init__(self, W, R, V):
        self.W = W
        self.R = R
        self.V = V

    def get_max(self, agent, S):
        output = S
        for (s,_) in self.R[agent]:
            if s in output:
                output.remove(s)
        return output

    def get_possible(self, agent, w):
        pre = set(s for (s,d) in self.R[agent] if d == w)
        post = set(d for (s,d) in self.R[agent] if s == w)
        return set.union(pre, post)

def parse_model(content):

    content = content.replace(" ", "")
    lines = content.split("\n")

    V_pattern = "^(\w+):(\w(,\w)*)$"
    R_pattern = "^(\w+):(\(\w+<=\w+\)(,\(\w+<=\w+\))*)$"

    W = set(lines[0].split(","))
    agents = set(lines[1].split(","))
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
            transitions = set([tuple(s.split("<=")) for s in trans_s.split(",")])
            R[agent] = transitions

        # V lines
        match = re.match(V_pattern, line)
        if match is not None:
            state = match.group(1)
            props = set(match.group(2).split(","))
            V[state] = props

    # Add empty sets for states with no propositions
    for state in W:
        if state not in V:
            V[state] = set()

    # Add empty lists for agents with no transitions
    for agent in agents:
        if agent not in R:
            R[agent] = set()

    # Make transition relations R reflexive
    for agent in agents:
        for state in W:
            R[agent].add((state,state))

    # Make transition relations R transitive
    for agent in agents:

        for origin in W:

            reachable = {origin}
            to_check = {origin}
            checked = set()

            while len(to_check) > 0:
                state = next(iter(to_check))

                # Compute immediately accessible states
                r = set([d for (s,d) in R[agent] if s == state])
                reachable = reachable.union(r)

                # Update which states to check for
                to_check.remove(state)
                checked.add(state)
                to_check = to_check.union(r.difference(checked))

            to_add = set([(origin,d) for d in reachable])
            R[agent] = R[agent].union(to_add)


    return Model(W, R, V)

def main():
    file_path = sys.argv[1]
    with open(file_path, 'r') as fd:
        content = fd.read()
    model = parse_model(content)
    print(model.W)
    print(model.R)
    print(model.V)

    print(model.get_possible('s0', 'a'))

if __name__ == "__main__":
    main()