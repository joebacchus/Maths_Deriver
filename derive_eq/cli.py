import argparse
from derive_eq.derive_equation import * # Import your backend function

def main():
    parser = argparse.ArgumentParser(
        description="Derive equations based on given arguments"
    )
    parser.add_argument(
        "arg1",
        help="First argument for equation derivation"
    )
    parser.add_argument(
        "arg2",
        help="Second argument for equation derivation"
    )

    args = parser.parse_args()
    
    # Call your backend function with the arguments
    result = derive_equation(args.arg1, args.arg2)
    print(result)

if __name__ == "__main__":
    main() 
