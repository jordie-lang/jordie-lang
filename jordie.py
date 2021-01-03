import argparse
import interp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jordie-lang")
    parser.add_argument(dest="fn", help="jordie-lang file to execute")
    parser.add_argument("-v", action="store_true", help="show tokens, AST, and resulting env")
    args = parser.parse_args()

    # Get text from source file
    with open(args.fn, "r") as f:
        source_string = f.read()

    path = "/".join(args.fn.split("/")[:-1]) + "/"
    if path == "/":
        path = "."
    
    interp.run(source_string, path, verbose=args.v)
