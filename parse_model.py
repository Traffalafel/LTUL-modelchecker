import re
import sys

class Model():

    def __init__(self, W, R, V):
        self.W = W
        self.R = R
        self.V = V

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

    return Model(W, R, V)


def main():
    file_path = sys.argv[1]
    with open(file_path, 'r') as fd:
        content = fd.read()
    
    parse_model(content)

if __name__ == "__main__":
    main()