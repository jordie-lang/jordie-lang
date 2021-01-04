from . import lexer
from . import parser
from pprint import pprint
import json

def run(soure_string, fn, path, verbose=False):
    token_list = lexer.lex(soure_string)

    if verbose:
        print("Tokens:")
        for token in token_list:
            print(token)
        print()
    
    ast = parser.parse(token_list, fn, path)

    if verbose:
        ast.print_tree()
        print("### BEGIN SCRIPT STANDARD OUT ###")
    
    env = ast.execute()

    if verbose:
        print("#### END SCRIPT STANDARD OUT ####")
        print()
        pprint(env)
