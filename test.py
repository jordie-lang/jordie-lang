import interp
import os
import subprocess

def test_lexer():
    print("#################### Testing Lexer ####################")
    lex_dir = "tests/lexer"
    for fn in os.listdir(lex_dir + "/test_cases"):
        if fn.endswith(".txt"):
            test_case_file = lex_dir + "/test_cases/" + fn
            solution_file = lex_dir + "/solutions/" + fn

            with open(test_case_file, "r") as tf:
                with open(solution_file, "r") as sf:
                    print("##### Test case {} #####".format(fn))
                    test_case_source = tf.read()
                    tokens = interp.lexer.lex(test_case_source)
                    test_string = interp.lexer.format_token_output(tokens).rstrip().replace("\r", "")
                    solution_string = sf.read().rstrip().replace("\r", "")

                    if test_string == solution_string:
                        print("Test case {} PASSED.".format(fn))
                        print("\n")
                    else:
                        print("Test case {} FAILED.".format(fn))
                        print("\n### Expected Output ###")
                        print(solution_string)
                        print("\n### Generated Output ###")
                        print(test_string)
                        print("")

def test_parser():
    print("#################### Testing Parser ####################")
    lex_dir = "tests/parser"
    for fn in os.listdir(lex_dir + "/test_cases"):
        if fn.endswith(".txt"):
            test_case_file = lex_dir + "/test_cases/" + fn
            solution_file = lex_dir + "/solutions/" + fn

            with open(test_case_file, "r") as tf:
                with open(solution_file, "r") as sf:
                    print("##### Test case {} #####".format(fn))
                    test_case_source = tf.read()
                    tokens = interp.lexer.lex(test_case_source)
                    ast = interp.parser.parse(tokens)

                    test_string = ast.get_tree_str().rstrip().replace("\r", "")

                    solution_string = sf.read().rstrip().replace("\r", "")

                    if test_string == solution_string:
                        print("Test case {} PASSED.".format(fn))
                        print("\n")
                    else:
                        print("Test case {} FAILED.".format(fn))
                        print("\n### Expected Output ###")
                        print(solution_string)
                        print("\n### Generated Output ###")
                        print(test_string)
                        print("")

def test_execution():
    print("#################### Testing Execution ####################")
    lex_dir = "tests/execution"
    for fn in os.listdir(lex_dir + "/test_cases"):
        if "06" in fn:
            exit(0)
        elif "01" in fn:
            continue
        if fn.endswith(".txt"):
            test_case_file = lex_dir + "/test_cases/" + fn
            solution_file = lex_dir + "/solutions/" + fn

            with open(test_case_file, "r") as tf:
                with open(solution_file, "r") as sf:
                    print("##### Test case {} #####".format(fn))
                    test_case_source = tf.read()
                    tokens = interp.lexer.lex(test_case_source)
                    ast = interp.parser.parse(tokens)
                    """
                    print("*********************** TMP *************************")
                    ast.execute()
                    print("*********************** TMP *************************")
                    """

                    test_exec = subprocess.Popen(["python", "jordie.py", test_case_file], stdout=subprocess.PIPE)
                    test_string = test_exec.communicate()[0]

                    solution_string = sf.read().rstrip().replace("\r", "")

                    if test_string == solution_string:
                        print("Test case {} PASSED.".format(fn))
                        print("\n")
                    else:
                        print("Test case {} FAILED.".format(fn))
                        print("\n### Expected Output ###")
                        print(solution_string)
                        print("\n### Generated Output ###")
                        print(test_string)
                        print("")


if __name__ == "__main__":
    test_lexer()
    test_parser()
    test_execution()