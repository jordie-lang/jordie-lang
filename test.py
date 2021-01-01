import interp
import os
import subprocess

def test_lexer():
    print("#################### Testing Lexer ####################")
    fns = os.listdir("tests/test_cases")
    fns.sort()
    for fn in fns:
        if fn.endswith(".txt"):
            test_case_file = "tests/test_cases/" + fn
            solution_file = "tests/solutions/lexer/" + fn

            with open(test_case_file, "r") as tf:
                with open(solution_file, "r") as sf:
                    print("##### Test case {} #####".format(fn))
                    test_case_source = tf.read()
                    tokens = interp.lexer.lex(test_case_source)
                    test_string = interp.lexer.format_token_output(tokens).rstrip().replace("\r", "")
                    solution_string = sf.read().rstrip().replace("\r", "")

                    if test_string == solution_string:
                        print("Test case {} PASSED.\n".format(fn))
                    else:
                        print("Test case {} FAILED.".format(fn))
                        print("\n### Expected Output ###")
                        print(solution_string)
                        print("\n### Generated Output ###")
                        print(test_string)
                        print("")

def test_parser():
    print("#################### Testing Parser ####################")
    fns = os.listdir("tests/test_cases")
    fns.sort()
    for fn in fns:
        if fn.endswith(".txt"):
            test_case_file = "tests/test_cases/" + fn
            solution_file = "tests/solutions/parser/" + fn

            with open(test_case_file, "r") as tf:
                with open(solution_file, "r") as sf:
                    print("##### Test case {} #####".format(fn))
                    test_case_source = tf.read()
                    tokens = interp.lexer.lex(test_case_source)
                    ast = interp.parser.parse(tokens)

                    test_string = ast.get_tree().rstrip().replace("\r", "")

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
    fns = os.listdir("tests/test_cases")
    fns.sort()
    for fn in fns:
        if fn.endswith(".txt"):
            test_case_file = "tests/test_cases/" + fn
            solution_file = "tests/solutions/execution/" + fn

            with open(solution_file, "r") as sf:
                print("##### Test case {} #####".format(fn))
                test_exec = subprocess.Popen(["python3", "jordie.py", test_case_file], stdout=subprocess.PIPE)
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
    #test_parser()
    #test_execution()