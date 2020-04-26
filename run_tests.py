import os
import subprocess

from test_cases import *
from interp import lexer, parser

def run_test(test_case):
    variables = globals()
    test_case_source = variables["test_case_{}".format(test_case)]
    expected_lexer_output = variables["lexer_{}".format(test_case)].strip().replace("\r", "")
    expected_parser_output = variables["parser_{}".format(test_case)].strip().replace("\r", "")
    expected_exec_output = variables["exec_{}".format(test_case)].strip().replace("\r", "")

    # Test Lexer
    lexer_output = lexer.format_token_output(lexer.lex(test_case_source)).rstrip().replace("\r", "")
    #print(expected_lexer_output)
    #print(lexer_output)
    if expected_lexer_output == lexer_output:
        print("Lexer: test case named {} PASSED.".format(test_case))
        print("\n")
    else:
        print("Lexer: test case named {} FAILED.".format(test_case))
        print("\n### Expected Output ###")
        print(expected_lexer_output)
        print("\n### Generated Output ###")
        print(lexer_output)
        print("\n")

    # Test Parser
    parser_output = parser.parse(lexer.lex(test_case_source)).get_tree_str().rstrip().replace("\r", "")
    #print(expected_parser_output)
    #print(parser_output)
    if expected_parser_output == parser_output:
        print("Parser: test case named {} PASSED.".format(test_case))
        print("\n")
    else:
        print("Parser: test case named {} FAILED.".format(test_case))
        print("\n### Expected Output ###")
        print(expected_parser_output)
        print("\n### Generated Output ###")
        print(parser_output)
        print("\n")
    
    # Test Execution
    with open("tmp_test_case_file.jordie", "w") as f:
        f.write(test_case_source)
    exec_output = subprocess.Popen(["python", "jordie.py", "tmp_test_case_file.jordie"], stdout=subprocess.PIPE).communicate()[0].rstrip().replace("\r", "")
    os.remove("tmp_test_case_file.jordie")
    #print(expected_exec_output)
    #print(exec_output)
    if expected_exec_output == exec_output:
        print("Exec: test case named {} PASSED.".format(test_case))
        print("\n")
    else:
        print("Exec: test case named {} FAILED.".format(test_case))
        print("\n### Expected Output ###")
        print(expected_exec_output)
        print("\n### Generated Output ###")
        print(exec_output)
        print("\n")
    

map(run_test, ["_".join(a.split("_")[2:]) for a in dir() if a.startswith("test_case_")])