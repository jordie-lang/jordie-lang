import random
import os

# print value to stdout
def jordie_print(foo):
    print(foo)

# converts an integer to a float
def jordie_integer_to_float(foo):
    return float(foo)

# converts a float to an integer
def jordie_float_to_integer(foo):
    return int(foo)

# converts a string number into an integer
def jordie_string_to_integer(foo):
    return int(foo)

# converts a string into a list
def jordie_string_to_list(foo):
    return list(foo)

# get random float from 0 to 1
def jordie_get_random():
    return random.random()

# get random integer from a to b and step by c, a and b are integers, a < b
def jordie_get_random_range(a, b, c):
    return random.randrange(a, b, c)

# sort list of inputs alphanumerically in ascending order
def jordie_sort(foo):
    tmp = foo
    tmp.sort()
    return tmp

# listens for input from stdin
def jordie_listen(foo):
    return input(foo)

# gets construct type
def jordie_get_type(foo):
    if type(foo) == int:
        return "integer"
    elif type(foo) == float:
        return "float"
    elif type(foo) == str:
        return "string"
    elif type(foo) == list:
        return "list"
    elif type(foo) == dict:
        return "dictionary"
    elif type(foo) == bool:
        return "boolean"
    else:
        exit(1)

# get number of characters in strings, constructs in lists, and pairs in dictionaries
def jordie_get_length(foo):
    return len(foo)

# get minimum value of list
def jordie_get_min(foo):
    return min(foo)

# get maximum value of list
def jordie_get_max(foo):
    return max(foo)

# get data from file
def jordie_get_file(fn):
    with open(fn, "r") as f:
        return f.read()

# write string to a file
def jordie_write_file(fn, data):
    with open(fn, "w") as f:
        f.write(data)

# append string to a file
def jordie_append_file(fn, data):
    with open(fn, "a") as f:
        f.write(data)

# check if file exists
def jordie_check_file(fn):
    return os.path.exists(fn)

# delete file
def jordie_delete_file(fn):
    os.remove(fn)
