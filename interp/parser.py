"""
jordie-lang parser

"""

from .jordie_std import *
from . import lexer
from copy import deepcopy
from num2words import num2words
from pprint import pprint

import os


# operators
# operator precedence from lowest to highest
op_prec_list = [
    ["or"],
    ["and"],
    ["not"],
    ["is greater than", "is equal to", "is less than"],
    ["minus", "plus"],
    ["divides", "times"]
]

def parse_error(pos, error_msg):
    ln, ecc = pos.split(",")
    print(f"parse error ({ln},{ecc}): {error_msg}.")
    exit(0)

def execute_error(error_msg):
    print(error_msg)
    exit(0)

def exec_error(pos, error_msg):
    ln, ecc = pos.split(",")
    return f"execution error ({ln},{ecc}): {error_msg}."

def parse_operator_tokens(op, token_list, index, pos):
    if op == "times":
        return MultExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "divides":
        return DivExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "plus":
        return AddExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "minus":
        return SubExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "is equal to":
        return EqualExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "is greater than":
        return GreaterExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "is less than":
        return LessExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "not":
        return NotExp(parse_value_tokens(token_list[index+1:]), pos)
    elif op == "and":
        return AndExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    elif op == "or":
        return OrExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]), pos)
    else:
        parse_error(pos, f"unexpected operator {op}")

def parse_value_tokens(token_list):
    # check if value contains an operator
    for ops in op_prec_list:
        for op in ops:
            # op = operator
            cnt = 0
            for token in token_list:
                if token[0] == "op" and token[1] == op:
                    return parse_operator_tokens(op, token_list, cnt, token[2])
                cnt += 1
    
    # if there are no operators, its either an id or a value
    if len(token_list) > 1:
        parse_error(token_list[0][2], f"no valid operator, expecting value or identifier")
    
    if token_list[0][0] == "id" or token_list[0][0] == "val":
        return ValExp(token_list[0], token_list[0][2])
    else:
        parse_error(token_list[0][2], f"unexpected value token {token_list[0][:2]}, expected an 'id' or 'val'")

def check_jordie_types(foo, f_type):
    if f_type == "integer":
        if type(foo) == int:
            return True
        else:
            return False
    elif f_type == "float":
        if type(foo) == float:
            return True
        else:
            return False
    elif f_type == "string":
        if type(foo) == str:
            return True
        else:
            return False
    elif f_type == "list":
        if type(foo) == list:
            return True
        else:
            return False
    elif f_type == "dictionary":
        if type(foo) == dict:
            return True
        else:
            return False
    elif f_type == "boolean":
        if type(foo) == bool:
            return True
        else:
            return False
    else:
        execute_error("unknown type 1")

def get_jordie_type(foo):
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
        execute_error("unknown type 2")

class Exp():
    def __init__(self):
        print("CREATE EXP")

    def print_exp(self):
        return "GET EXP STRING"

    def execute(self):
        exit(0)
        return "RUN EXP"

class ValExp(Exp): 
    def __init__(self, _data_token, _pos):
        if _data_token[0] == "id":
            self.is_id = True
        else:
            self.is_id = False
        self.data = _data_token[1]
        self.pos = _pos
    
    def get_pos(self):
        return self.pos
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ValExp:\n".format("  "*level)
        if self.is_id:
            exp_str += "{}id={}\n".format("  "*(level+1), self.data)
        else:
            exp_str += "{}val={}\n".format("  "*(level+1), self.data)
        return exp_str
    
    def execute(self, env):
        # check if expression is a value or a reference
        if self.is_id:
            # ensure variable exists in environment
            if not self.data in env["vars"].keys():
                return ("ERROR", exec_error(self.pos, f"unknown variable {self.data}"))
            
            # return value of variable
            return (env["vars"][self.data]["value"], env)
        else:
            # return value of ValExp
            return (self.data, env)

class MultExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}MultExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # ensure left value is either integer or float
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            exp_pos = self.left_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid multiplication input type {l_type}, expected integer or float"))

        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)

        # ensure right value is either integer or float
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            exp_pos = self.right_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid multiplication input type {r_type}, expected integer or float"))
        
        # return multiplication of left and right values
        return (l_val*r_val, env)

class DivExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}DivExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # ensure left value is either integer or float
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            exp_pos = self.left_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid division input type {l_type}, expected integer or float"))

        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure right value is either integer or float
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            exp_pos = self.right_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid division input type {r_type}, expected integer or float"))
        
        # return division of left and right values
        return (l_val/r_val, env)

class AddExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos

    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AddExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # ensure left value is either integer or float
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            exp_pos = self.left_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid addition input type {l_type}, expected integer or float"))

        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure right value is either integer or float
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            exp_pos = self.right_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid addition input type {r_type}, expected integer or float"))
        
        # return addition of left and right values
        return (l_val+r_val, env)

class SubExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}SubExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # ensure left value is either integer or float
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            exp_pos = self.left_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid subtraction input type {l_type}, expected integer or float"))

        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure right value is either integer or float
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            exp_pos = self.right_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid subtraction input type {r_type}, expected integer or float"))
        
        # return subtraction of left and right values
        return (l_val-r_val, env)

class EqualExp(Exp):
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}EqualExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure the left and right values are the same type
        l_type = get_jordie_type(l_val)
        r_type = get_jordie_type(r_val)
        if l_type != r_type:
            return ("ERROR", exec_error(self.pos, f"types must match for equivalence comparison, got types {l_type} and {r_type}"))
        
        # return equivalence comparison of left and right values
        return (l_val==r_val, env)

class GreaterExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}GreaterExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)

        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure the left and right values are the same type
        l_type = get_jordie_type(l_val)
        r_type = get_jordie_type(r_val)
        if l_type != r_type:
            return ("ERROR", exec_error(self.pos, f"types must match for greater than comparison, got types {l_type} and {r_type}"))
        
        # return greater comparison of left and right values
        return (l_val>r_val, env)

class LessExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}LessExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure the left and right values are the same type
        l_type = get_jordie_type(l_val)
        r_type = get_jordie_type(r_val)
        if l_type != r_type:
            return ("ERROR", exec_error(self.pos, f"types must match for less than comparison, got types {l_type} and {r_type}"))
        
        # return less comparison of left and right values
        return (l_val<r_val, env)

class NotExp(Exp): 
    def __init__(self, _right, _pos):
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}NotExp:\n".format("  "*level)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure right value is a boolean
        r_type = get_jordie_type(r_val)
        if r_type != "boolean":
            exp_pos = self.right_exp.get_pos()
            return ("ERROR", exec_error(exp_pos, f"invalid not input type {r_type}, expected boolean"))

        # return boolean not of right value
        return (not r_val, env)

class AndExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AndExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure left and right values are booleans
        l_type = get_jordie_type(l_val)
        r_type = get_jordie_type(r_val)
        if r_type != "boolean" or l_type != "boolean":
            return ("ERROR", exec_error(self.pos, f"invalid and input types {r_type} and {l_type}, expected booleans"))

        # return boolean and of left and right values
        return (l_val and r_val, env)

class OrExp(Exp): 
    def __init__(self, _left, _right, _pos):
        self.left_exp = _left
        self.right_exp = _right
        self.pos = _pos
    
    def get_pos(self):
        return self.pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}OrExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from left expression
        l_val, env = self.left_exp.execute(env)
        if l_val == "ERROR":
            return ("ERROR", env)
        
        # get value from right expression
        r_val, env = self.right_exp.execute(env)
        if r_val == "ERROR":
            return ("ERROR", env)
        
        # ensure left and right values are booleans
        l_type = get_jordie_type(l_val)
        r_type = get_jordie_type(r_val)
        if r_type != "boolean" or l_type != "boolean":
            return ("ERROR", exec_error(self.pos, f"invalid or input types {r_type} and {l_type}, expected booleans"))
        
        # return boolean or of right value
        return (l_val or r_val, env)

class BodyExp(Exp): 
    def __init__(self):
        self.exp_list = []

    def append(self, exp):
        self.exp_list.append(exp)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}BodyExp:\n".format("  "*level)
        for exp in self.exp_list:
            exp_str += exp.print_exp(level+1)
        return exp_str
    
    def get_exp_list(self):
        return self.exp_list
    
    def execute(self, env):
        # run each expression in the body expression
        for exp in self.exp_list:
            val, env = exp.execute(env)
            
            # check for an error or a break statement to stop loop execution
            if val == "EXIT":
                break
            elif val == "ERROR":
                return ("ERROR", env)

        return (None, env)

class StructExp(Exp): 
    def __init__(self, _id, _e_fields):
        self.e_id = _id
        self.e_fields = _e_fields

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}StructExp: id={}\n".format("  "*level, self.e_id)
        exp_str += "{}Fields:\n".format("  "*(level+1))
        for field in self.e_fields.keys():
            exp_str += "{}{}: {}\n".format("  "*(level+2), field, self.e_fields[field])
        return exp_str
    
    def execute(self, env):
        # create struct as new custom type or overwrite previous definition
        env["types"][self.e_id] = {}

        # add each field to the custom type
        for field in self.e_fields.keys():
            env["types"][self.e_id][field] = self.e_fields[field]
        
        return (None, env)

class RetrieveExp(Exp): 
    def __init__(self, _id, _path):
        self.e_id = _id
        self.s_path = _path
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}RetrieveExp: id={}\n".format("  "*level, self.e_id)
        return exp_str
    
    def execute(self, env):
        # string to hold module source string
        source_string = ""

        # add '.jordie' to module name if not present
        if self.e_id.endswith(".jordie"):
            fn = self.e_id
        else:
            fn = self.e_id + ".jordie"


        # check if filename is a filepath
        if self.e_id.startswith(".") or "/" in self.e_id:
            path = "/".join(fn.split("/")[:-1]) + "/"
            fn = fn.split("/")[-1]
        else:
            path = ""
        
        path = os.path.join(self.s_path, path)
        
        # check if file exists
        if fn in os.listdir(path) and os.path.isfile(path+fn):
            # get module source
            with open(path+fn, "r") as f:
                source_string = f.read()
        else:
            return ("ERROR", f"module {path+fn} doesn't exist")
        
        # run lexer and parser on source
        source_ast = parse(lexer.lex(source_string), path)

        # get source BodyExp
        body = source_ast.get_body()

        # run source BodyExp
        ret_val, env = body.execute(env)
        if ret_val == "ERROR":
            return ("ERROR", f"module {self.e_id}, {env}")
        
        return (None, env)

class DeclareExp(Exp): 
    def __init__(self, _id, _const, _type, _value=None):
        self.e_id = _id
        self.e_const = _const
        self.e_type = _type
        self.e_val = _value
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}DeclareExp: id={} const={} type={}\n".format("  "*level, self.e_id, self.e_const, self.e_type)
        exp_str += "{}value:\n".format("  "*(level+1))
        if self.e_val != None:
            exp_str += self.e_val.print_exp(level+2)
        else:
            exp_str += "{}{}\n".format("  "*(level+2), self.e_val)
        return exp_str
    
    def execute(self, env):
        # get value from value expression
        val, env = self.e_val.execute(env)
        if val == "ERROR":
            return ("ERROR", env)
        
        # save value to env
        if val != None:
            if type(val) is tuple:
                # create variable from a reference
                env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": env["vars"][val[1]]["value"]}
            else:
                # create variable from a value
                env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": val}
        else:
            if env["types"][self.e_type]:
                # its a struct
                struct_fields = { k:{"type": v, "value": None} for (k,v) in env["types"][self.e_type].items()}
                
                env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": struct_fields}
            else:
                env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": None}
        
        return (None, env)

class SetExp(Exp): 
    def __init__(self, _id, _val, _field_id, _id_pos, _field_pos):
        self.e_id = _id
        self.e_val = _val
        self.e_field_id = _field_id
        self.id_pos = _id_pos
        self.field_pos = _field_pos

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}SetExp: id={} field_id={}\n".format("  "*level, self.e_id, self.e_field_id)
        exp_str += "{}value:\n".format("  "*(level+1))
        exp_str += self.e_val.print_exp(level+2)
        return exp_str
    
    def execute(self, env):
        # ensure target id is in the environment
        if not self.e_id in env["vars"].keys():
            return ("ERROR", exec_error(self.id_pos, f"unknown variable {self.e_id}"))

        # get value from the value expression
        val, env = self.e_val.execute(env)
        if val == "ERROR":
            return ("ERROR", env)
        
        # check if target variable is a struct
        if self.e_field_id:
            # check that value is the correct type for the struct field
            f_type = env["types"][env["vars"][self.e_id]["type"]][self.e_field_id]
            if not check_jordie_types(val, f_type):
                return ("ERROR", exec_error(self.field_pos, f"invalid field type {f_type} for field {self.e_field_id}"))
            
            # store value in the struct field
            env["vars"][self.e_id]["value"][self.e_field_id]["value"] = val
        else:
            # check that value is the correct type for the variable
            v_type = env["vars"][self.e_id]["type"]
            if not check_jordie_types(val, v_type):
                return ("ERROR", exec_error(self.id_pos, f"invalid type for value {self.e_id}"))
            
            # store value in the variable
            env["vars"][self.e_id]["value"] = val
        
        return (None, env)

class WhileExp(Exp): 
    def __init__(self, _cond, _body):
        self.e_cond = _cond
        self.e_body = _body
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}WhileExp:\n".format("  "*level)
        exp_str += self.e_cond.print_exp(level+1)
        exp_str += self.e_body.print_exp(level+1)
        return exp_str

    def execute(self, env):
        # save copy of the environment
        envc = deepcopy(env)

        # get value from conditional expression
        cond_val, env = self.e_cond.execute(env)
        if cond_val == "ERROR":
            return ("ERROR", env)
        
        # run the body while the condition evaluates to true
        while cond_val:
            # get all expressions from the body
            for exp in self.e_body.get_exp_list():
                # run the expression
                tmp_val, env = exp.execute(env)

                # check for break, jump, exit, or error cases
                if tmp_val == "BREAK":
                    return (None, envc)
                elif tmp_val == "JUMP":
                    break
                elif tmp_val == "EXIT":
                    return ("EXIT", envc)
                elif tmp_val == "ERROR":
                    return ("ERROR", env)
                elif tmp_val == "RETURN":
                    ret_val = env
                    return ("RETURN", ret_val)
            
            # reevaluate the conditional expression
            cond_val, env = self.e_cond.execute(env)
            if cond_val == "ERROR":
                return ("ERROR", env)
        
        return (None, envc)

class CallExp(Exp): 
    def __init__(self, _f_id, _args, _ret_id, _f_id_pos, _args_pos, _ret_id_pos):
        self.f_id = _f_id
        self.f_args = _args
        self.f_ret = _ret_id
        self.f_id_pos = _f_id_pos
        self.f_args_pos = _args_pos
        self.f_ret_pos = _ret_id_pos
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}CallExp: func_id={} ret_id={}\n".format("  "*level, self.f_id, self.f_ret)
        exp_str += "{}Args:\n".format("  "*(level+1))
        if self.f_args:
            for arg in self.f_args.keys():
                exp_str += "{}Arg: {}\n".format("  "*(level+2), arg)
                exp_str += "{}value:\n".format("  "*(level+3))
                exp_str += self.f_args[arg].print_exp(level+4)
        else:
            exp_str += "{}None\n".format("  "*(level+2))
        return exp_str
    
    def execute(self, env):
        func_args_values = []

        # save copy of the environment
        envc = deepcopy(env)

        # ensure function exists
        if not self.f_id in env["funcs"].keys():
            return ("ERROR", exec_error(self.f_id_pos, f"unknown function {self.f_id}"))
        
        # check args are correct types and add then to the environment
        for arg in env["funcs"][self.f_id]["args"].keys():
            # get argument value expression from input args
            arg_exp = self.f_args[arg]
            arg_pos = self.f_args_pos[arg]

            # get value from the value expression
            arg_val, env = arg_exp.execute(env)
            if arg_val == "ERROR":
                return ("ERROR", env)
            
            # ensure argument is the correct type
            arg_type = get_jordie_type(arg_val)
            check_type = env["funcs"][self.f_id]["args"][arg]
            if arg_type != check_type and check_type != "any":
                return ("ERROR", exec_error(arg_pos, f"invalid argument type for argument {arg}"))

            # add args to the environment (args are constants)
            env["vars"][arg] = {"type": arg_type, "const": True, "value": arg_val}

            # add value to arg list for builtin functions
            func_args_values.append(arg_val)
        
        # ensure variable to store return value is in the environment
        if self.f_ret:
            if not self.f_ret in env["vars"].keys():
                return ("ERROR", exec_error(self.f_ret_pos, f"invalid return target {self.f_ret}"))

        # check if function is in the standard library or user defined
        if env["funcs"][self.f_id]["body"] != None:
            # run user defined function and return value
            # get all expressions from the body
            for exp in env["funcs"][self.f_id]["body"].get_exp_list():
                # run the expression
                tmp_val, env = exp.execute(env)

                # check for exit, error, or return cases
                if tmp_val == "EXIT":
                    return ("EXIT", envc)
                elif tmp_val == "ERROR":
                    return ("ERROR", env)
                elif tmp_val == "RETURN":
                    if self.f_ret:
                        # return value replaces environment
                        ret_val = env

                        # ensure return value is the correct type
                        ret_type = get_jordie_type(ret_val)
                        if ret_type != envc["vars"][self.f_ret]["type"]:
                            return ("ERROR", exec_error(self.f_id_pos, f"invalid return type {ret_type}"))
                        
                        # update variable that stores return value
                        envc["vars"][self.f_ret]["value"] = ret_val
            
            return (None, envc)
        else:
            # run standard library function
            ret_val = env["funcs"][self.f_id]["fnc"](*func_args_values)
            
            # check if the function should return a value
            if self.f_ret:
                # ensure return value is the correct type
                ret_type = get_jordie_type(ret_val)
                if ret_type != env["vars"][self.f_ret]["type"]:
                    return ("ERROR", exec_error(self.f_id_pos, f"invalid return type {ret_type}"))

                # update variable that stores return value
                envc["vars"][self.f_ret]["value"] = ret_val
        
            return (None, envc)

class BreakExp(Exp): 
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}BreakExp\n".format("  "*level)
        return exp_str
    
    def execute(self, env):
        return ("BREAK", env)

class JumpExp(Exp): 
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}JumpExp\n".format("  "*level)
        return exp_str
    
    def execute(self, env):
        return ("JUMP", env)

class ForExp(Exp): 
    def __init__(self, _id, _body, _id_pos):
        self.iter_id = _id
        self.e_body = _body
        self.iter_id_pos = _id_pos
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ForExp: id={}\n".format("  "*level, self.iter_id)
        exp_str += self.e_body.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # save copy of the environment
        envc = deepcopy (env)

        # get list value from the environment
        if not self.iter_id in env["vars"].keys():
            return ("ERROR", exec_error(self.iter_id_pos, f"unknown list {self.iter_id}"))
        iter_list = env["vars"][self.iter_id]["value"]

        # ensure that input is a list
        id_type = env["vars"][self.iter_id]["type"]
        if id_type != "list":
            return ("ERROR", exec_error(self.iter_id_pos, f"for loop input must be a list, recieved {id_type}"))

        # loop over input list
        for item in iter_list:
            # set item variable in environment
            env["vars"]["item"] = {"const": True, "type": get_jordie_type(item), "value": item}

            # get all expressions from the body
            for exp in self.e_body.get_exp_list():
                # run the expression
                tmp_val, env = exp.execute(env)

                # check for break, jump, exit, or error cases
                if tmp_val == "BREAK":
                    return (None, envc)
                elif tmp_val == "JUMP":
                    break
                elif tmp_val == "EXIT":
                    return ("EXIT", envc)
                elif tmp_val == "ERROR":
                    return ("ERROR", env)
                elif tmp_val == "RETURN":
                    ret_val = env
                    return ("RETURN", ret_val)

        return (None, envc)

class FuncExp(Exp): 
    def __init__(self, _id, _type, _args, _body):
        self.f_id = _id
        self.f_type = _type
        self.f_args = _args
        self.f_body = _body
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}FuncExp: id={} type={}\n".format("  "*level, self.f_id, self.f_type)
        exp_str += "{}Args:\n".format("  "*(level+1))
        if self.f_args:
            for arg in self.f_args.keys():
                exp_str += "{}Arg: {}={}\n".format("  "*(level+2), arg, self.f_args[arg])
        else:
            exp_str += "{}None\n".format("  "*(level+2))
        exp_str += self.f_body.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # add function to environment
        env["funcs"][self.f_id] = {"type": self.f_type, "args": self.f_args, "body": self.f_body, "fnc": None}
        
        return (None, env)

class RetExp(Exp): 
    def __init__(self, _val):
        self.r_val = _val
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}RetExp:\n".format("  "*level)
        exp_str += self.r_val.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # get value from the value expression
        val, env = self.r_val.execute(env)
        if val == "ERROR":
            return ("ERROR", env)
        
        # return value instead of environment
        return ("RETURN", val)

class IfExp(Exp): 
    def __init__(self, _conds, _bodys, _else):
        self.e_conds = _conds
        self.e_bodys = _bodys
        self.e_else = _else
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}IfExp:\n".format("  "*level)
        exp_str += self.e_conds[0].print_exp(level+1)
        exp_str += self.e_bodys[0].print_exp(level+1)
        cnt = 0
        while(cnt < len(self.e_conds)-1):
            exp_str += "{}Else If:\n".format("  "*level)
            exp_str += self.e_conds[cnt].print_exp(level+1)
            exp_str += self.e_bodys[cnt].print_exp(level+1)
            cnt += 1
        if self.e_else:
            exp_str += "{}Else:\n".format("  "*level)
            exp_str += self.e_bodys[-1].print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # save copy of the environment
        envc = deepcopy(env)

        # get the number of conditionals
        num_conds = len(self.e_conds)

        # execute each condition and block
        for i in range(num_conds):
            cond = self.e_conds[i]
            body = self.e_bodys[i]
            
            # get value from the conditional expression
            cond_val, env = cond.execute(env)
            if cond_val == "ERROR":
                return ("ERROR", env)
            
            # run the body if the condition evaluates to true
            if cond_val:
                # get all expressions from the body
                for exp in body.get_exp_list():
                    # run the expression
                    tmp_val, env = exp.execute(env)

                    # check for break, jump, exit, or error cases
                    if tmp_val == "BREAK":
                        return ("BREAK", envc)
                    elif tmp_val == "JUMP":
                        return ("JUMP", envc)
                    elif tmp_val == "EXIT":
                        return ("EXIT", envc)
                    elif tmp_val == "ERROR":
                        return ("ERROR", env)
                    elif tmp_val == "RETURN":
                        ret_val = env
                        return ("RETURN", ret_val)
                    
                return (None, envc)
        
        # if none of the conditions are true, check for an else case
        if self.e_else:
            body = self.e_bodys[-1]

            # get all expressions from the body
            for exp in body.get_exp_list():
                # run the expression
                tmp_val, env = exp.execute(env)
                
                # check for break, jump, exit, or error cases
                if tmp_val == "BREAK":
                    return ("BREAK", envc)
                elif tmp_val == "JUMP":
                    return ("JUMP", envc)
                elif tmp_val == "EXIT":
                    return ("EXIT", envc)
                elif tmp_val == "ERROR":
                    return ("ERROR", env)
                elif tmp_val == "RETURN":
                    ret_val = env
                    return ("RETURN", ret_val)

        return (None, envc)

class TryExp(Exp): 
    def __init__(self, _body, _err_id, _err_body):
        self.e_body = _body
        self.e_err_id = _err_id
        self.e_err_body = _err_body
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}TryExp:\n".format("  "*level)
        exp_str += self.e_body.print_exp(level+1)
        exp_str += "{}Catch: id={}\n".format("  "*(level+1), self.e_err_id)
        exp_str += self.e_err_body.print_exp(level+2)
        return exp_str
    
    def execute(self, env):
        # save copy of the environment
        envc = deepcopy(env)

        # run the expression
        val, _env = self.e_body.execute(env)
        if val == "ERROR":
            env["vars"][self.e_err_id] = {"const": True, "type": get_jordie_type(_env), "value": _env}
            val, env = self.e_err_body.execute(env)
            if val == "ERROR":
                return ("ERROR", env)

        return (None, envc)

class AssertExp(Exp): 
    def __init__(self, _cond, _cond_pos):
        self.e_cond = _cond
        self.e_cond_pos = _cond_pos
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AssertExp:\n".format("  "*level)
        exp_str += self.e_cond.print_exp(level+1)
        return exp_str

    def execute(self, env):
        # get value from conditional expression
        cond_val, env = self.e_cond.execute(env)

        # handle output cases
        if cond_val == False:
            return ("ERROR", exec_error(self.e_cond_pos, f"assertion failed"))
        elif cond_val == "ERROR":
            return ("ERROR", env)
        
        return(None, env)

class ExitExp(Exp): 
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ExitExp\n".format("  "*level)
        return exp_str
    
    def execute(self, env):
        return ("EXIT", env)

def pop_token(token_list):
    return (token_list[0], token_list[1:])

def parse_retrieve_exp(token_list, path):
    e_id = ""
    token, token_list = pop_token(token_list)
    if token[0] == "id":
        e_id = token[1]
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "semicolon"):
        return (RetrieveExp(e_id, path), token_list)
    else:
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon')")

def parse_declare_exp(token_list, path):
    t_id = ""
    t_const = False
    t_type = ""
    t_val = None
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "functional"):
        f_id = ""
        f_type = ""
        f_args = {}
        f_body = None
        
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            f_id = token[1]
        else:
            parse_error(token[2], f"unexpected token {token}, expected an 'id'")
        
        token, token_list = pop_token(token_list)
        if token[:2] == ("kw", "returns"):
            token, token_list = pop_token(token_list)
            if token[0] == "type":
                f_type = token[1]
            else:
                parse_error(token[2], f"unexpected token {token}, expected ('kw', 'returns')")
        else:
            parse_error(token[2], f"unexpected token {token}, expected ('kw', 'returns')")
        
        token, token_list = pop_token(token_list)
        if token[:2] == ("kw", "receives"):
            token, token_list = pop_token(token_list)
            if token[:2] == ("type", "nothing"):
                f_args = {}
                token, token_list = pop_token(token_list)
                if not token[:2] == ("kw", "open-curly-brace"):
                    parse_error(token[2], f"unexpected token {token}, expected ('kw', 'open-curly-brace')")
            else:
                cnt = 1
                while(not token[:2] == ("kw", "open-curly-brace")):
                    if token[0] == "type":
                        f_args["argument-{}".format(num2words(cnt))] = token[1]
                    elif token[:2] == ("kw", "and"):
                        # nop
                        _nop = "YEET"
                    else:
                        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'open-curly-brace') or ('kw', 'and')")
                    token, token_list = pop_token(token_list)
                    cnt += 1
        else:
            parse_error(token[2], f"unexpected token {token}, expected ('kw', 'receives')")
        
        f_body = BodyExp()
        while(not token[:2] == ("kw", "close-curly-brace")):
            tmp_exp, token_list = parse_next_exp(token_list, path)
            f_body.append(tmp_exp)
            if token_list[0][:2] == ("kw", "close-curly-brace"):
                break
        
        token, token_list = pop_token(token_list)
        return (FuncExp(f_id, f_type, f_args, f_body), token_list)
    elif token[:2] == ("kw", "changeable"):
        t_const = False
    elif token[:2] == ("kw", "nonchangeable"):
        t_const = True
    elif token[:2] == ("kw", "structure"):
        t_id = ""
        t_fields = {}
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            t_id = token[1]
        else:
            parse_error(token[2], f"unexpected token {token}, expected an 'id'")
        token, token_list = pop_token(token_list)
        if token[:2] == ("kw", "open-curly-brace"):
            while(not token[:2] == ("kw", "close-curly-brace")):
                f_id = ""
                f_type = ""
                token, token_list = pop_token(token_list)
                if token[:2] == ("kw", "field"):
                    token, token_list = pop_token(token_list)
                    if token[0] == "id":
                        f_id = token[1]
                    else:
                        parse_error(token[2], f"unexpected token {token}, expected an 'id'")
                    token, token_list = pop_token(token_list)
                    if token[0] == "type":
                        f_type = token[1]
                    else:
                        parse_error(token[2], f"unexpected token {token}, expected a 'type'")
                    token, token_list = pop_token(token_list)
                    if token[:2] == ("kw", "semicolon"):
                        t_fields[f_id] = f_type
                    else:
                        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon')")
                elif token[:2] == ("kw", "close-curly-brace"):
                    break
                else:
                    parse_error(token[2], f"unexpected token {token}, expected ('kw', 'field') or ('kw', 'close-curly-brace')")
            return (StructExp(t_id, t_fields), token_list)
        else:
            parse_error(token[2], f"unexpected token {token}, expected ('kw', 'open-curly-brace')")
    else:
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'functional') or ('kw', 'changeable') or ('kw', 'nonchangeable') or ('kw', 'structure')")
    token, token_list = pop_token(token_list)
    if token[0] == "id":
        t_id = token[1]
        t_id_pos = token[2]
    else:
        parse_error(token[2], f"unexpected token {token}, expected an 'id'")
    token, token_list = pop_token(token_list)
    if token[0] == "type":
        t_type = token[1]
    else:
        parse_error(token[2], f"unexpected token {token}, expected an 'type'")
    
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "semicolon"):
        t_val = ValExp(("val", None, t_id_pos), t_id_pos)
        return (DeclareExp(t_id, t_const, t_type, t_val), token_list)
    else:
        tmp_tokens = []
        while token[:2] != ("kw", "semicolon"):
            tmp_tokens.append(token)
            token, token_list = pop_token(token_list)
        t_val = parse_value_tokens(tmp_tokens)
        return (DeclareExp(t_id, t_const, t_type, t_val), token_list)

def parse_set_exp(token_list, path):
    t_id = ""
    t_val = None
    t_field_id = ""
    t_field_pos = "-1,-1"
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "field"):
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            t_field_id = token[1]
            t_field_pos = token[2]
            token, token_list = pop_token(token_list)
            if token[0] == "id":
                t_id = token[1]
                t_id_pos = token[2]
            else:
                parse_error(token[2], f"unexpected token {token}, expected an 'id'")
        else:
            parse_error(token[2], f"unexpected token {token}, expected an 'id'")
    elif token[0] == "id":
        t_id = token[1]
        t_id_pos = token[2]
    else:
        parse_error(token[2], f"unexpected token {token}, expected a 'field' or 'id'")

    token, token_list = pop_token(token_list)
    tmp_tokens = []
    while(not token[:2] == ("kw", "semicolon")):
        tmp_tokens.append(token)
        token, token_list = pop_token(token_list)
    
    t_val = parse_value_tokens(tmp_tokens)
    return (SetExp(t_id, t_val, t_field_id, t_id_pos, t_field_pos), token_list)

def parse_call_exp(token_list, path):
    func_id = None
    args = {}
    ret_id = None
    func_id_pos = "-1,-1"
    args_pos = {}
    ret_id_pos = "-1,-1"
    
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "functional"):
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            func_id = token[1]
            func_id_pos = token[2]
        else:
            parse_error(token[2], f"unexpected token {token}, expected an 'id'")

        token, token_list = pop_token(token_list)
        if token[:2] == ("kw", "semicolon"):
            return (CallExp(func_id, args, ret_id, func_id_pos, args_pos, ret_id_pos), token_list)
        elif token[:2] == ("kw", "pass"):
            token, token_list = pop_token(token_list)
            cnt = 1
            while(not (token[:2] == ("kw", "return") or token[:2] == ("kw", "semicolon"))):
                if token[:2] == ("kw", "and"):
                    token, token_list = pop_token(token_list)
                else:
                    # turn token into ValExp
                    tmp_val = ValExp(token, token[2])
                    args["argument-{}".format(num2words(cnt))] = tmp_val
                    args_pos["argument-{}".format(num2words(cnt))] = token[2]
                    token, token_list = pop_token(token_list)
                    cnt += 1
            if token[:2] == ("kw", "return"):
                token, token_list = pop_token(token_list)
                if token[0] == "id":
                    ret_id = token[1]
                    ret_id_pos = token[2]
                else:
                    parse_error(token[2], f"unexpected token {token}, expected an 'id'")
                token, token_list = pop_token(token_list)
                if token[:2] == ("kw", "semicolon"):
                    return (CallExp(func_id, args, ret_id, func_id_pos, args_pos, ret_id_pos), token_list)
                else:
                    parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon')")
            elif token[:2] == ("kw", "semicolon"):
                return (CallExp(func_id, args, ret_id, func_id_pos, args_pos, ret_id_pos), token_list)
            else:
                parse_error(token[2], f"unexpected token {token}, expected ('kw', 'return') or ('kw', 'semicolon')")
        elif token[:2] == ("kw", "return"):
            token, token_list = pop_token(token_list)
            if token[0] == "id":
                ret_id = token[1]
                ret_id_pos = token[2]
            else:
                parse_error(token[2], f"unexpected token {token}, expected an 'id'")
            token, token_list = pop_token(token_list)
            if token[:2] == ("kw", "semicolon"):
                return (CallExp(func_id, args, ret_id, func_id_pos, args_pos, ret_id_pos), token_list)
            else:
                parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon')")
        else:
            parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon') or ('kw', 'pass') or ('kw', 'return')")
    else:
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'functional')")

    return (CallExp(func_id, args, ret_id, func_id_pos, args_pos, ret_id_pos), token_list)

def parse_break_exp(token_list, path):
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "semicolon"):
        return (BreakExp(), token_list)
    else:
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon')")

def parse_jump_exp(token_list, path):
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "semicolon"):
        return (JumpExp(), token_list)
    else:
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'semicolon')")

def parse_for_exp(token_list, path):
    items = None
    body_exp = None

    token, token_list = pop_token(token_list)
    if token[0] == "id":
        items = token[1]
        items_pos = token[2]
    else:
        parse_error(token[2], f"unexpected token {token}, expected an 'id'")
    
    body_exp = BodyExp()
    token, token_list = pop_token(token_list)
    while(not token[:2] == ("kw", "close-curly-brace")):
        tmp_exp, token_list = parse_next_exp(token_list, path)
        body_exp.append(tmp_exp)

        if token_list[0][:2] == ("kw", "close-curly-brace"):
            break

    token, token_list = pop_token(token_list)
    return (ForExp(items, body_exp, items_pos), token_list)

def parse_while_exp(token_list, path):
    cond_exp = None
    body_exp = None

    cond_tokens = []
    token, token_list = pop_token(token_list)
    while token[:2] != ("kw", "open-curly-brace"):
        cond_tokens.append(token)
        token, token_list = pop_token(token_list)
    cond_exp = parse_value_tokens(cond_tokens)

    body_exp = BodyExp()
    while(not token[:2] == ("kw", "close-curly-brace")):
        tmp_exp, token_list = parse_next_exp(token_list, path)
        body_exp.append(tmp_exp)

        if token_list[0][:2] == ("kw", "close-curly-brace"):
            break

    token, token_list = pop_token(token_list)
    return (WhileExp(cond_exp, body_exp), token_list)

def parse_return_exp(token_list, path):
    val_tokens = []
    token, token_list = pop_token(token_list)
    while(not token[:2] == ("kw", "semicolon")):
        val_tokens.append(token)
        token, token_list = pop_token(token_list)
    
    r_val = parse_value_tokens(val_tokens)
    
    return (RetExp(r_val), token_list)

def parse_if_exp(token_list, path):
    conds = []
    bodys = []
    else_case = False

    cond_exp = None
    body_exp = None
    cond_tokens = []
    token, token_list = pop_token(token_list)
    while token[:2] != ("kw", "open-curly-brace"):
        cond_tokens.append(token)
        token, token_list = pop_token(token_list)
    cond_exp = parse_value_tokens(cond_tokens)

    body_exp = BodyExp()
    while(not token[:2] == ("kw", "close-curly-brace")):
        tmp_exp, token_list = parse_next_exp(token_list, path)
        body_exp.append(tmp_exp)

        if token_list[0][:2] == ("kw", "close-curly-brace"):
            break
    
    token, token_list = pop_token(token_list)

    conds.append(cond_exp)
    bodys.append(body_exp)

    while(token_list and token_list[0][:2] == ("kw", "or")):
        token, token_list = pop_token(token_list)
        if not token[:2] == ("kw", "or"):
            parse_error(token[2], f"unexpected token {token}, expected ('kw', 'or')")
        token, token_list = pop_token(token_list)
        if token[:2] == ("kw", "if"):
            cond_tokens = []
            token, token_list = pop_token(token_list)
            while token[:2] != ("kw", "open-curly-brace"):
                cond_tokens.append(token)
                token, token_list = pop_token(token_list)
            cond_exp = parse_value_tokens(cond_tokens)

            body_exp = BodyExp()
            while(not token[:2] == ("kw", "close-curly-brace")):
                tmp_exp, token_list = parse_next_exp(token_list, path)
                
                body_exp.append(tmp_exp)

                if token_list[0][:2] == ("kw", "close-curly-brace"):
                    break
            token, token_list = pop_token(token_list)
            conds.append(cond_exp)
            bodys.append(body_exp)
        elif token[:2] == ("kw", "open-curly-brace"):
            else_case = True
            body_exp = BodyExp()
            while(not token[:2] == ("kw", "close-curly-brace")):
                tmp_exp, token_list = parse_next_exp(token_list, path)
                body_exp.append(tmp_exp)

                if token_list[0][:2] == ("kw", "close-curly-brace"):
                    break
            token, token_list = pop_token(token_list)
            bodys.append(body_exp)
        else:
            parse_error(token[2], f"unexpected token {token}, expected ('kw', 'if') or ('kw', 'open-curly-brace')")
        if token_list == []:
            break
    return (IfExp(conds, bodys, else_case), token_list)

def parse_try_exp(token_list, path):
    body_exp = None
    error_id = None
    error_body = None

    token, token_list = pop_token(token_list)
    if not token[:2] == ("kw", "open-curly-brace"):
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'open-curly-brace')")

    body_exp = BodyExp()
    while(not token[:2] == ("kw", "close-curly-brace")):
        tmp_exp, token_list = parse_next_exp(token_list, path)
        body_exp.append(tmp_exp)

        if token_list[0][:2] == ("kw", "close-curly-brace"):
            break
    token, token_list = pop_token(token_list)
    
    token, token_list = pop_token(token_list)
    if token[:2] == ("kw", "catch"):
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            error_id = token[1]
        else:
            parse_error(token[2], f"unexpected token {token}, expected an 'id'")
    else:
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'catch')")
    
    token, token_list = pop_token(token_list)
    if not token[:2] == ("kw", "open-curly-brace"):
        parse_error(token[2], f"unexpected token {token}, expected ('kw', 'open-curly-brace')")

    error_body = BodyExp()
    while(not token[:2] == ("kw", "close-curly-brace")):
        tmp_exp, token_list = parse_next_exp(token_list, path)
        error_body.append(tmp_exp)

        if token_list[0][:2] == ("kw", "close-curly-brace"):
            break
    token, token_list = pop_token(token_list)
    return (TryExp(body_exp, error_id, error_body), token_list)

def parse_assert_exp(token_list, path):
    cond_tokens = []

    token, token_list = pop_token(token_list)
    cond_pos = token[2]
    while token[:2] != ("kw", "semicolon"):
        cond_tokens.append(token)
        token, token_list = pop_token(token_list)
    cond_exp = parse_value_tokens(cond_tokens)
    
    return (AssertExp(cond_exp, cond_pos), token_list)

def parse_exit_exp(token_list, path):
    return (ExitExp(), token_list)

def parse_next_exp(token_list, path):
    token, token_list = pop_token(token_list)
    tmp_exp = None
    if token[:2] == ("kw", "retrieve"):
        tmp_exp, token_list = parse_retrieve_exp(token_list, path)
    elif token[:2] == ("kw", "declare"):
        tmp_exp, token_list = parse_declare_exp(token_list, path)
    elif token[:2] == ("kw", "set"):
        tmp_exp, token_list = parse_set_exp(token_list, path)
    elif token[:2] == ("kw", "while"):
        tmp_exp, token_list = parse_while_exp(token_list, path)
    elif token[:2] == ("kw", "call"):
        tmp_exp, token_list = parse_call_exp(token_list, path)
    elif token[:2] == ("kw", "break"):
        tmp_exp, token_list = parse_break_exp(token_list, path)
    elif token[:2] == ("kw", "jump"):
        tmp_exp, token_list = parse_jump_exp(token_list, path)
    elif token[:2] == ("kw", "for"):
        tmp_exp, token_list = parse_for_exp(token_list, path)
    elif token[:2] == ("kw", "return"):
        tmp_exp, token_list = parse_return_exp(token_list, path)
    elif token[:2] == ("kw", "if"):
        tmp_exp, token_list = parse_if_exp(token_list, path)
    elif token[:2] == ("kw", "try"):
        tmp_exp, token_list = parse_try_exp(token_list, path)
    elif token[:2] == ("kw", "assert"):
        tmp_exp, token_list = parse_assert_exp(token_list, path)
    elif token[:2] == ("kw", "exit"):
        tmp_exp, token_list = parse_exit_exp(token_list, path)
    else:
        parse_error(token[2], f"unexpected token {token}, expected a keyword ['retrieve', 'declare', 'set', 'while', 'call', 'break', 'jump', 'for', 'return', 'if', 'try', 'assert', 'exit']")
    return (tmp_exp, token_list)

class AST:
    def __init__(self):
        self.head = BodyExp()
        self.env = {}

    def parse_tokens(self, token_list, path):
        while(token_list):
            token, token_list = pop_token(token_list)
            tmp_exp = None
            if token[:2] == ("kw", "retrieve"):
                tmp_exp, token_list = parse_retrieve_exp(token_list, path)
            elif token[:2] == ("kw", "declare"):
                tmp_exp, token_list = parse_declare_exp(token_list, path)
            elif token[:2] == ("kw", "set"):
                tmp_exp, token_list = parse_set_exp(token_list, path)
            elif token[:2] == ("kw", "while"):
                tmp_exp, token_list = parse_while_exp(token_list, path)
            elif token[:2] == ("kw", "call"):
                tmp_exp, token_list = parse_call_exp(token_list, path)
            elif token[:2] == ("kw", "break"):
                tmp_exp, token_list = parse_break_exp(token_list, path)
            elif token[:2] == ("kw", "jump"):
                tmp_exp, token_list = parse_jump_exp(token_list, path)
            elif token[:2] == ("kw", "for"):
                tmp_exp, token_list = parse_for_exp(token_list, path)
            elif token[:2] == ("kw", "return"):
                tmp_exp, token_list = parse_return_exp(token_list, path)
            elif token[:2] == ("kw", "if"):
                tmp_exp, token_list = parse_if_exp(token_list, path)
            elif token[:2] == ("kw", "try"):
                tmp_exp, token_list = parse_try_exp(token_list, path)
            elif token[:2] == ("kw", "assert"):
                tmp_exp, token_list = parse_assert_exp(token_list, path)
            elif token[:2] == ("kw", "exit"):
                tmp_exp, token_list = parse_exit_exp(token_list, path)
            else:
                parse_error(token[2], f"unexpected token {token}, expected a keyword ['retrieve', 'declare', 'set', 'while', 'call', 'break', 'jump', 'for', 'return', 'if', 'try', 'assert', 'exit']")
            self.head.append(tmp_exp)

    def print_tree(self):
        print(self.head.print_exp(0))
    
    def get_tree(self):
        return self.head.print_exp(0)
    
    def get_body(self):
        return self.head

    def create_env(self):
        self.env = {
            "vars": {
                "jordie-name": {"type": "string", "value": ""}
            },
            "funcs": {
                "print": {"args": {"argument-one": "any"}, "body": None, "fnc": jordie_print}
            },
            "types": {
                "integer": {},
                "float": {},
                "string": {},
                "list": {},
                "dictionary": {}
            },
            "cur_ret_id": ""
        }
        return self.env

    def execute(self):
        self.create_env()
        _ret_val, self.env = self.head.execute(self.env)
        if _ret_val == "ERROR":
            execute_error(self.env)
        return self.env
    
def parse(token_list, path):
    ast = AST()
    ast.parse_tokens(token_list, path)
    return ast
