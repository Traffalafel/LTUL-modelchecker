import sys

from parse_formula import parse_formula
from parse_model import parse_model
from check_formula import get_sets

def main():
    
    if len(sys.argv) != 4:
        print("Usage: <model-path> <formula> <state>")
        return

    model_path = sys.argv[1]
    formula = sys.argv[2]
    state = sys.argv[3]

    # Parse model
    file_path = sys.argv[1]
    with open(file_path, 'r') as fd:
        content = fd.read()
    model = parse_model(content)

    # Log model
    print("\nSuccessfully parsed model")
    print(f"Model W: {model.W}")
    print(f"Model R: {model.R}")
    print(f"Model V: {model.V}")
    print()

    # Parse formula
    print(f"Formula: {formula}")
    f_parsed = parse_formula(formula)
    print(f_parsed)
    print()

    # Check formula on model
    satisfying_sets = get_sets(f_parsed, model)
    print(satisfying_sets)

if __name__ == "__main__":
    main()
