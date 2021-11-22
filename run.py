import sys

from parse_formula import parse_formula
from parse_model import parse_model
from check_formula import get_sets

def main():
    
    if len(sys.argv) != 3:
        print("Usage: <model-path> <formula>")
        return

    model_path = sys.argv[1]
    formula = sys.argv[2]

    # Parse model
    file_path = sys.argv[1]
    with open(file_path, 'r') as fd:
        content = fd.read()
    model = parse_model(content)

    # Log model
    print()
    print(f"Model W: {model.W}")
    print(f"Model R: {model.R}")
    print(f"Model V: {model.V}")
    print()

    # Parse formula
    print(f"Formula: {formula}")
    f_parsed = parse_formula(formula)
    print(f"Parsed:  {f_parsed}")
    print()

    # Check formula on model
    sat = get_sets(f_parsed, model)
    if len(sat) == 0:
        print("None")
        return
        
    print(f"Satisfying states: {sat}")
    print()

if __name__ == "__main__":
    main()
