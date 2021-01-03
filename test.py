import interp
import os
import subprocess

def test_lexer():
    print("####################### Testing  Lexer #######################")
    fns = os.listdir("tests/test_cases")
    fns.sort()

    total = 0
    succ = 0

    for fn in fns:
        total += 1
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
                        succ += 1
                        print("Test case {} PASSED.\n".format(fn))
                    else:
                        print("Test case {} FAILED.".format(fn))
                        print("\n### Expected Output ###")
                        print(solution_string)
                        print("\n### Generated Output ###")
                        print(test_string)
                        print("")
    
    return (total, succ)

def test_parser():
    print("####################### Testing Parser #######################")
    fns = os.listdir("tests/test_cases")
    fns.sort()

    total = 0
    succ = 0

    for fn in fns:
        total += 1
        if fn.endswith(".txt"):
            test_case_file = "tests/test_cases/" + fn
            solution_file = "tests/solutions/parser/" + fn

            with open(test_case_file, "r") as tf:
                with open(solution_file, "r") as sf:
                    print("##### Test case {} #####".format(fn))
                    test_case_source = tf.read()
                    tokens = interp.lexer.lex(test_case_source)
                    ast = interp.parser.parse(tokens, "tests/test_cases/")

                    test_string = ast.get_tree().rstrip().replace("\r", "")

                    solution_string = sf.read().rstrip().replace("\r", "")

                    if test_string == solution_string:
                        succ += 1
                        print("Test case {} PASSED.".format(fn))
                        print("\n")
                    else:
                        print("Test case {} FAILED.".format(fn))
                        print("\n### Expected Output ###")
                        print(solution_string)
                        print("\n### Generated Output ###")
                        print(test_string)
                        print("")
    
    return (total, succ)

def test_execution():
    print("##################### Testing  Execution #####################")
    fns = os.listdir("tests/test_cases")
    fns.sort()

    total = 0
    succ = 0

    for fn in fns:
        total += 1
        if fn.endswith(".txt"):
            test_case_file = "tests/test_cases/" + fn
            solution_file = "tests/solutions/execution/" + fn

            with open(solution_file, "r") as sf:
                print("##### Test case {} #####".format(fn))
                test_exec = subprocess.Popen(["python3", "jordie.py", test_case_file], stdout=subprocess.PIPE)
                test_string = test_exec.communicate()[0].decode("utf-8").rstrip().replace("\r", "")
                solution_string = sf.read().rstrip().replace("\r", "")

                if test_string == solution_string:
                    succ += 1
                    print("Test case {} PASSED.".format(fn))
                    print("\n")
                else:
                    print("Test case {} FAILED.".format(fn))
                    print("\n### Expected Output ###")
                    print(solution_string)
                    print("\n### Generated Output ###")
                    print(test_string)
                    print("")
    
    return (total, succ)


if __name__ == "__main__":
    print("#################### Testing  jordie-lang ####################\n")
    
    l_total, l_succ = test_lexer()
    p_total, p_succ = test_parser()
    e_total, e_succ = test_execution()

    print("###################### Testing  results ######################")

    print(f"\nLexer Result: {l_total} tests run, {l_succ} tests succeeded.")
    print(f"\nParser Result: {p_total} tests run, {p_succ} tests succeeded.")
    print(f"\nExecution Result: {e_total} tests run, {e_succ} tests succeeded.")

    if l_total == l_succ and p_total == p_succ and e_total == e_succ:
        print("\nAll Tests Successful.\n")
    
    print("#################### Testing  jordie-lang ####################")
