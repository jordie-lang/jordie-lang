"""
jordie-lang parser

AST:


"""
from jordie_std import *
import lexer

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

def parse_error(error_msg):
    print(error_msg)
    exit(0)

def execute_error(error_msg):
    print("Execution Error: {}".format(error_msg))
    exit(0)

def deepcopy(foo):
    if type(foo) == "list":
        lst = []
        for i in foo:
            if type(i) == "list" or type(i) == "dict":
                lst.append(deepcopy(i))
            else:
                lst.append(i)
        return lst
    elif type(foo) == "dict":
        dct = {}
        for k in foo.keys():
            if type(foo[k]) == "list" or type(foo[k]) == "dict":
                dct[k] = deepcopy(foo[k])
            else:
                dct[k] = foo[k]
        return dct
    else:
        parse_error("")

def parse_operator_tokens(op, token_list, index):
    if op == "times":
        return MultExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "divides":
        return DivExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "plus":
        return AddExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "minus":
        return SubExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "is equal to":
        return EqualExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "is greater than":
        return GreaterExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "is less than":
        return LessExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "not":
        return NotExp(parse_value_tokens(token_list[index+1:]))
    elif op == "and":
        return AndExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    elif op == "or":
        return OrExp(parse_value_tokens(token_list[:index]), parse_value_tokens(token_list[index+1:]))
    else:
        parse_error("")

def parse_value_tokens(token_list):
    # check if value contains an operator
    for ops in op_prec_list:
        for op in ops:
            # op = operator
            cnt = 0
            for token in token_list:
                if token[0] == "op" and token[1] == op:
                    return parse_operator_tokens(op, token_list, cnt)
                cnt += 1
    
    # if there are no operators, its either an id or a value
    if len(token_list) > 1:
        parse_error("")
    
    if token_list[0][0] == "id" or token_list[0][0] == "val":
        return ValExp(token_list[0])
    else:
        parse_error("")

def get_next_val_exp(tok_list): # OLD
    #if there is an operator
    op_prec_list.reverse()
    for ops in op_prec_list:
        ops.reverse()
        for op in ops:
            #op = operator
            cnt = 0
            for token in tok_list:
                if token[0] == "op" and token[1] == op:
                    exp_val = make_op_exp(op, tok_list, cnt)
                    exp_val.build_tree()
                    return exp_val
                cnt += 1
    
    #if there are no operators, its either id or val
    if len(tok_list) > 1:
        parse_error("eeeeeeeeeeeeee")
    
    if tok_list[0][0] == "id":
        exp_val = ValExp([tok_list[0]])
        exp_val.build_tree()
        return exp_val
    elif tok_list[0][0] == "val":
        exp_val = ValExp([tok_list[0]])
        exp_val.build_tree()
        return exp_val
    else:
        parse_error("eeeeeeeeeeeeee")
    return exp_val

def get_next_cond_exp(tok_list):
    #if there is an operator
    if op_prec_list[0][0] != "or":
        op_prec_list.reverse()
    for ops in op_prec_list:
        for op in ops:
            cnt = 0
            for token in tok_list:
                if token[0] == "op" and token[1] == op:
                    exp_val = make_op_exp(op, tok_list, cnt)
                    exp_val.build_tree()
                    return exp_val
                cnt += 1
    
    #if there are no operators, its either id or val
    if len(tok_list) > 1:
        parse_error("eeeeeeeeeeeeee")
    
    if tok_list[0][0] == "id":
        exp_val = ValExp([tok_list[0]])
        exp_val.build_tree()
        return exp_val
    elif tok_list[0][0] == "val":
        exp_val = ValExp([tok_list[0]])
        exp_val.build_tree()
        return exp_val
    else:
        parse_error("eeeeeeeeeeeeee")

def make_op_exp(op, tokens, index): # OLD
    if op == "times":
        return MultExp(tokens[:index], tokens[index+1:])
    elif op == "divides":
        return DivExp(tokens[:index], tokens[index+1:])
    elif op == "plus":
        return AddExp(tokens[:index], tokens[index+1:])
    elif op == "minus":
        return SubExp(tokens[:index], tokens[index+1:])
    elif op == "is equal to":
        return EqualExp(tokens[:index], tokens[index+1:])
    elif op == "is greater than":
        return GreaterExp(tokens[:index], tokens[index+1:])
    elif op == "is less than":
        return LessExp(tokens[:index], tokens[index+1:])
    elif op == "not":
        return NotExp(tokens[index+1:])
    elif op == "and":
        return AndExp(tokens[:index], tokens[index+1:])
    elif op == "or":
        return OrExp(tokens[:index], tokens[index+1:])
    else:
        parse_error("Error: make_op_exp")

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
    else:
        execute_error("unknown type")

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
    else:
        execute_error("unknown type")

class Exp():
    def __init__(self):
        print("CREATE EXP")

    def print_exp(self):
        return "GET EXP STRING"

    def execute(self):
        exit(0)
        return "RUN EXP"

class ValExp(Exp):
    def __init__(self, _data_token):
        if _data_token[0] == "id":
            self.is_id = True
        else:
            self.is_id = False
        self.data = _data_token[1]
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ValExp:\n".format("  "*level)
        if self.is_id:
            exp_str += "{}id={}\n".format("  "*(level+1), self.data)
        else:
            exp_str += "{}val={}\n".format("  "*(level+1), self.data)
        return exp_str
    
    def execute(self, env):
        if self.is_id:
            if not self.data in env["vars"].keys():
                execute_error("")
            return (env["vars"][self.data]["value"], env)
        else:
            return (self.data, env)

class MultExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}MultExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        l_val, env = self.left_exp.execute(env)
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            execute_error("")

        r_val, env = self.right_exp.execute(env)
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            execute_error("")
        return (l_val*r_val, env)

class DivExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}DivExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        l_val, env = self.left_exp.execute(env)
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            execute_error("")

        r_val, env = self.right_exp.execute(env)
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            execute_error("")
        return (l_val/r_val, env)

class AddExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AddExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        l_val, env = self.left_exp.execute(env)
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            execute_error("")

        r_val, env = self.right_exp.execute(env)
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            execute_error("")
        return (l_val+r_val, env)

class SubExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}SubExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        l_val, env = self.left_exp.execute(env)
        l_type = get_jordie_type(l_val)
        if l_type != "integer" and l_type != "float":
            execute_error("")

        r_val, env = self.right_exp.execute(env)
        r_type = get_jordie_type(r_val)
        if r_type != "integer" and r_type != "float":
            execute_error("")
        return (l_val-r_val, env)

class EqualExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}EqualExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        l_val, env = self.left_exp.execute(env)
        r_val, env = self.right_exp.execute(env)
        return (l_val==r_val, env)

class GreaterExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        #print(self.left_exp)
        #print(self.right_exp)
        exp_str = ""
        exp_str += "{}GreaterExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        l_val, env = self.left_exp.execute(env)
        r_val, env = self.right_exp.execute(env)
        return (l_val>r_val, env)

class LessExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}LessExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        l_val, env = self.left_exp.execute(env)
        r_val, env = self.right_exp.execute(env)
        return (l_val<r_val, env)

class NotExp(Exp):
    def __init__(self, _right):
        self.right_exp = _right
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}NotExp:\n".format("  "*level)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        exit(0)
        return "RUN NOT EXP"

class AndExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AndExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        exit(0)
        return "RUN AND EXP"

class OrExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = _left
        self.right_exp = _right
        #self.left_tokens = _left
        #self.right_tokens = _right

    def build_tree(self): # OLD
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}OrExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        exit(0)
        return "RUN OR EXP"

class CondExp(Exp): # OLD
    def __init__(self, _cond):
        self.c_tokens = _cond
        self.c_exp = None
    
    def build_cond_tree(self):
        self.c_exp = get_next_cond_exp(self.c_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}CondExp:\n".format("  "*level)
        exp_str += self.c_exp.print_exp(level+1)
        return exp_str

    def execute(self):
        exit(0)
        return "RUN COND EXP"

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
    
    def execute(self, env):
        for exp in self.exp_list:
            val, env = exp.execute(env)
        return None, env

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
        env["types"][self.e_id] = {}
        for field in self.e_fields.keys():
            env["types"][self.e_id][field] = self.e_fields[field]
        return (None, env)

class RetrieveExp(Exp):
    def __init__(self, _id):
        self.e_id = _id
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}RetrieveExp: id={}\n".format("  "*level, self.e_id)
        return exp_str
    
    def execute(self, env):
        # get source from file
        with open(self.e_id + ".jordie", "r") as f:
            test_case_source = f.read()
        
        # run lexer and parser on source
        source_ast = parse(lexer.lex(test_case_source))

        # get source BodyExp
        body = source_ast.get_body()

        # run source BodyExp
        ret_val, env = body.execute(env)
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
        val, env = self.e_val.execute(env)
        if val != None:
            env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": val}
            #print("its not ya boi")
        else:
            #print("its ya boi")
            if env["types"][self.e_type]:
                # its a struct
                struct_fields = { k:{"type": v, "value": None} for (k,v) in env["types"][self.e_type].items()}
                #print("cc")
                #print(struct_fields)
                #print("dd")

                env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": struct_fields}
            else:
                env["vars"][self.e_id] = {"type": self.e_type, "const": self.e_const, "value": None}
        return (None, env)

class SetExp(Exp):
    def __init__(self, _id, _val, _field_id):
        self.e_id = _id
        self.e_val = _val
        self.e_field_id = _field_id

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}SetExp: id={} field_id={}\n".format("  "*level, self.e_id, self.e_field_id)
        exp_str += "{}value:\n".format("  "*(level+1))
        exp_str += self.e_val.print_exp(level+2)
        return exp_str
    
    def execute(self, env):
        # ensure target id is in env
        if not self.e_id in env["vars"].keys():
            execute_error("unknown construct: {}".format(self.e_id))

        # evaluate val exp
        #val, env = self.e_val.execute(env)  TOO MANY VALUES TO UNPACK, WUT?
        val = self.e_val.execute(env)
        env = val[1]
        val = val[0]
        if self.e_field_id:
            #set field of struct
            #f_type = env["vars"][self.e_id]["value"][self.e_field_id]["type"]
            f_type = env["types"][env["vars"][self.e_id]["type"]][self.e_field_id]
            if not check_jordie_types(val, f_type):
                execute_error("invalid type 1")
            else:
                #print("aa")
                #print(env)
                #print("bb")
                env["vars"][self.e_id]["value"][self.e_field_id]["value"] = val
        else:
            #set regular var
            v_type = env["vars"][self.e_id]["type"]
            if not check_jordie_types(val, v_type):
                execute_error("invalid type 2")
            else:
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

    def execute(self):
        print("WhileExp")

class CallExp(Exp):
    def __init__(self, _f_id, _args, _ret_id):
        self.f_id = _f_id
        self.f_args = _args #list of ValExps
        self.f_ret = _ret_id
    
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
        #print("Call")
        args_to_remove = []
        func_args_values = []

        # check function exists
        if not self.f_id in env["funcs"].keys():
            #invalid function identifier
            execute_error("invalid function name")
        
        # check args are correct types and add to env
        for arg in env["funcs"][self.f_id]["args"].keys():
            # arg = "argument-1"
            tmp_arg = self.f_args[arg]
            arg_val, env = tmp_arg.execute(env)
            arg_type = get_jordie_type(arg_val)
            check_type = env["funcs"][self.f_id]["args"][arg]

            if arg_type != check_type and check_type != "any":
                execute_error("invalid arg type")

            # add args to env, args are constants
            env["vars"][arg] = {"type": arg_type, "const": True, "value": arg_val}
            args_to_remove.append(arg)

            # add value to arg list for builtin functions
            func_args_values.append(arg_val)

        # check if function is in std lib or user defined
        if env["funcs"][self.f_id]["body"]:
            # ensure no ret id is set
            if env["cur_ret_id"]:
                execute_error("ret id already set")

            # add args to env
            for arg in self.f_args.keys():
                env["vars"][arg] = self.f_args[arg]

            # add ret id to env
            if self.f_ret:
                env["cur_ret_id"] = self.f_ret

            # run user function and return val
            tmp_ret_val, env = env["funcs"][self.f_id]["body"].execute(env)

            # remove ret id to env
            if self.f_ret:
                env["cur_ret_id"] = ""

            # return value
        else:
            # check that ret_id is set
            if self.f_ret:
                print("its ya boi")
                # check if ret_id is in env
                if not self.f_ret in env["vars"].keys():
                    execute_error("ret id doesn't exist")

                # run std lib function and return val
                ret_val = env["funcs"][self.f_id]["fnc"](func_args_values)
                env["vars"][self.f_ret]["value"] = ret_val
            else:
                # run std lib function
                ret_val = env["funcs"][self.f_id]["fnc"](*func_args_values)

        # remove args from env
        for arg in args_to_remove:
            env["vars"].pop(arg)
        
        return (None, env)

class BreakExp(Exp):
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}BreakExp\n".format("  "*level)
        return exp_str
    
    def execute(self):
        exit(0)
        return "RUN BREAK EXP"

class JumpExp(Exp):
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}JumpExp\n".format("  "*level)
        return exp_str
    
    def execute(self):
        exit(0)
        return "RUN JUMP EXP"

class ForExp(Exp):
    def __init__(self, _id, _body):
        self.iter_id = _id
        self.e_body = _body
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ForExp: id={}\n".format("  "*level, self.iter_id)
        exp_str += self.e_body.print_exp(level+1)
        return exp_str
    
    def execute(self, env):
        # check that iterable is a list
        id_type = env["vars"][self.iter_id]["type"]
        if id_type != "list":
            execute_error("")

        iter_list = env["vars"][self.iter_id]["value"]

        # loop over iterable _id
        for item in iter_list:
            # set item variable in environment
            env["vars"]["item"] = {"const": True, "type": get_jordie_type(item), "value": item}
            
            # run BodyExp
            ret_val, env = self.e_body.execute(env)

        return (None, env)

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
        #print("((((((((((((((((((((((((((((")
        #print(env)
        #print(self.f_id)
        #print(self.f_args)
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
        #print("RETRETRETRETRETRET")
        tmp_val = self.r_val.execute(env)
        #print(tmp_val)
        # check for cur ret id
        if not env["cur_ret_id"]:
            execute_error("no return id")
        
        env["vars"]["cur_ret_id"] = tmp_val
        return env

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
    
    def execute(self):
        exit(0)
        return "RUN IF EXP"

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
    
    def execute(self):
        exit(0)
        return "RUN TRY EXP"

class AssertExp(Exp):
    def __init__(self, _cond):
        self.e_cond = _cond
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AssertExp:\n".format("  "*level)
        exp_str += self.e_cond.print_exp(level+1)
        return exp_str

    def execute(self):
        exit(0)
        return "RUN ASSERT EXP"

class ExitExp(Exp):
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ExitExp\n".format("  "*level)
        return exp_str
    
    def execute(self):
        exit(0)
        return "RUN EXIT EXP"

def pop_token(token_list):
    return (token_list[0], token_list[1:])

def parse_retrieve_exp(token_list):
    #print("Retrieve")
    e_id = ""
    token, token_list = pop_token(token_list)
    if token[0] == "id":
        e_id = token[1]
    token, token_list = pop_token(token_list)
    if token == ("kw", "semicolon"):
        return (RetrieveExp(e_id), token_list)
    else:
        parse_error("eeeretrieve")

def parse_declare_exp(token_list):
    #print("Declare")
    #print(token_list[:token_list.index(("kw", "semicolon"))+1])
    t_id = ""
    t_const = False
    t_type = ""
    t_val = None
    token, token_list = pop_token(token_list)
    if token == ("kw", "functional"):
        #declare function
        f_id = ""
        f_type = ""
        f_args = {}
        f_body = None
        
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            f_id = token[1]
        else:
            parse_error("")
        
        token, token_list = pop_token(token_list)
        if token == ("kw", "returns"):
            token, token_list = pop_token(token_list)
            if token[0] == "type":
                f_type = token[1]
            else:
                parse_error("")
        else:
            parse_error("")

        token, token_list = pop_token(token_list)
        if token == ("kw", "receives"):
            token, token_list = pop_token(token_list)
            if token == ("type", "nothing"):
                f_args = {}
                token, token_list = pop_token(token_list)
                if not token == ("kw", "open-curly-brace"):
                    parse_error("")
            else:
                cnt = 1 # argument-1, change to be argument-one later
                while(not token == ("kw", "open-curly-brace")):
                    if token[0] == "type":
                        f_args["argument-{}".format(str(cnt))] = token[1]
                    else:
                        parse_error("")
                    token, token_list = pop_token(token_list)
                    cnt += 1
        else:
            parse_error("")
        
        f_body = BodyExp()
        while(not token == ("kw", "close-curly-brace")):
            tmp_exp, token_list = parse_next_exp(token_list)
            f_body.append(tmp_exp)
            if token_list[0] == ("kw", "close-curly-brace"):
                break

        token, token_list = pop_token(token_list)
        #print("FORTRAN")
        return (FuncExp(f_id, f_type, f_args, f_body), token_list)
    elif token == ("kw", "changeable"):
        t_const = False
    elif token == ("kw", "nonchangeable"):
        t_const = True
    elif token == ("kw", "structure"):
        t_id = ""
        t_fields = {}
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            t_id = token[1]
        else:
            parse_error("eee0.5")
        token, token_list = pop_token(token_list)
        if token == ("kw", "open-curly-brace"):
            while(not token == ("kw", "close-curly-brace")):
                f_id = ""
                f_type = ""
                token, token_list = pop_token(token_list)
                if token == ("kw", "field"):
                    token, token_list = pop_token(token_list)
                    if token[0] == "id":
                        f_id = token[1]
                    else:
                        parse_error("eee3.5")
                    token, token_list = pop_token(token_list)
                    if token[0] == "type":
                        f_type = token[1]
                    else:
                        parse_error("eee4.5")
                    token, token_list = pop_token(token_list)
                    if token == ("kw", "semicolon"):
                        t_fields[f_id] = f_type
                    else:
                        parse_error("eee5.5")
                elif token == ("kw", "close-curly-brace"):
                    break
                else:
                    parse_error("eee2.5")
            return (StructExp(t_id, t_fields), token_list)
        else:
            parse_error("eee1.5")
    else:
        parse_error("Declare: Unknown construct type.")
    token, token_list = pop_token(token_list)
    if token[0] == "id":
        t_id = token[1]
    else:
        parse_error("Declare: Construct ID not found.")
    token, token_list = pop_token(token_list)
    if token[0] == "type":
        t_type = token[1]
    else:
        parse_error("Declare: Construct type not found.")
    token, token_list = pop_token(token_list)
    if token == ("kw", "semicolon"):
        t_val = ValExp(("val", None))
        return (DeclareExp(t_id, t_const, t_type, t_val), token_list)
    else:
        tmp_tokens = []
        while token != ("kw", "semicolon"):
            tmp_tokens.append(token)
            token, token_list = pop_token(token_list)
        t_val = parse_value_tokens(tmp_tokens)
        #t_val = get_next_val_exp(tmp_tokens)
        return (DeclareExp(t_id, t_const, t_type, t_val), token_list)

def parse_set_exp(token_list):
    #print("Set")
    t_id = ""
    t_val = None
    t_field_id = ""
    token, token_list = pop_token(token_list)
    if token == ("kw", "field"):
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            t_field_id = token[1]
            token, token_list = pop_token(token_list)
        else:
            parse_error("eee9")
    if token[0] == "id":
        t_id = token[1]
    else:
        parse_error("eee5")

    token, token_list = pop_token(token_list)
    tmp_tokens = []
    while(not token == ("kw", "semicolon")):
        tmp_tokens.append(token)
        token, token_list = pop_token(token_list)
    #t_val = ValExp(val_tokens)
    t_val = parse_value_tokens(tmp_tokens)
    #t_val.build_tree()
    return (SetExp(t_id, t_val, t_field_id), token_list)

def parse_call_exp(token_list):
    #print("Call")
    #print("da boi")
    func_id = None
    args = {}
    ret_id = None
    
    token, token_list = pop_token(token_list)
    if token == ("kw", "functional"):
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            func_id = token[1]
        else:
            parse_error("")

        token, token_list = pop_token(token_list)
        if token == ("kw", "semicolon"):
            return (CallExp(func_id, args, ret_id), token_list)
        elif token == ("kw", "pass"):
            token, token_list = pop_token(token_list)
            cnt = 1 # another spot to update arg names
            while(not (token == ("kw", "return") or token == ("kw", "semicolon"))):
                #print("ya boi again")
                if token == ("kw", "and"):
                    # this is where i would make a change to allow expressions inside call params
                    # nop
                    token, token_list = pop_token(token_list)
                else:
                    #turn token into ValExp
                    tmp_val = ValExp(token)
                    args["argument-{}".format(str(cnt))] = tmp_val
                    token, token_list = pop_token(token_list)
                    cnt += 1
            if token == ("kw", "return"):
                token, token_list = pop_token(token_list)
                if token[0] == "id":
                    ret_id = token[1]
                else:
                    parse_error("")
                token, token_list = pop_token(token_list)
                if token == ("kw", "semicolon"):
                    return (CallExp(func_id, args, ret_id), token_list)
            elif token == ("kw", "semicolon"):
                return (CallExp(func_id, args, ret_id), token_list)
            else:
                parse_error("")
        elif token == ("kw", "return"):
            token, token_list = pop_token(token_list)
            if token[0] == "id":
                ret_id = token[1]
            else:
                parse_error("")
            token, token_list = pop_token(token_list)
            if token == ("kw", "semicolon"):
                return (CallExp(func_id, args, ret_id), token_list)
        else:
            parse_error("")
    else:
        parse_error("calleeeeeeeeee")

    return (CallExp(func_id, args, ret_id), token_list)

def parse_break_exp(token_list):
    #print("Break")
    token, token_list = pop_token(token_list)
    if token == ("kw", "semicolon"):
        return (BreakExp(), token_list)
    else:
        parse_error("breakeeeeee")

def parse_jump_exp(token_list):
    #print("Jump")
    token, token_list = pop_token(token_list)
    if token == ("kw", "semicolon"):
        return (JumpExp(), token_list)
    else:
        parse_error("breakeeeeee")

def parse_for_exp(token_list):
    #print("For")
    items = None
    body_exp = None

    token, token_list = pop_token(token_list)
    if token[0] == "id":
        items = token[1]
    else:
        parse_error("foreeeeeeee")
    
    body_exp = BodyExp()
    token, token_list = pop_token(token_list)
    while(not token == ("kw", "close-curly-brace")):
        tmp_exp, token_list = parse_next_exp(token_list)
        body_exp.append(tmp_exp)

        if token_list[0] == ("kw", "close-curly-brace"):
            break

    token, token_list = pop_token(token_list)
    return (ForExp(items, body_exp), token_list)

def parse_while_exp(token_list):
    #print("While")
    #print(token_list[:10])
    cond_exp = None
    body_exp = None

    cond_tokens = []
    token, token_list = pop_token(token_list)
    while token != ("kw", "open-curly-brace"):
        cond_tokens.append(token)
        token, token_list = pop_token(token_list)
    cond_exp = parse_value_tokens(cond_tokens)
    #cond_exp = CondExp(cond_tokens)
    #cond_exp.build_cond_tree()
    #print(cond_exp)
    #exit(0)

    body_exp = BodyExp()
    while(not token == ("kw", "close-curly-brace")):
        #next_exp, token_list = get_next_exp(token_list)
        #body_exp.append(next_exp)
        #token = token_list[0]
        tmp_exp, token_list = parse_next_exp(token_list)
        body_exp.append(tmp_exp)

        if token_list[0] == ("kw", "close-curly-brace"):
            break

    token, token_list = pop_token(token_list)
    return (WhileExp(cond_exp, body_exp), token_list)

def parse_return_exp(token_list):
    val_tokens = []
    token, token_list = pop_token(token_list)
    while(not token == ("kw", "semicolon")):
        val_tokens.append(token)
        token, token_list = pop_token(token_list)
    r_val = ValExp(val_tokens)
    r_val.build_tree()
    return (RetExp(r_val), token_list)

def parse_if_exp(token_list):
    #print("If")
    conds = []
    bodys = []
    else_case = False

    cond_exp = None
    body_exp = None
    cond_tokens = []
    token, token_list = pop_token(token_list)
    while(not token == ("kw", "open-curly-brace")):
        cond_tokens.append(token)
        token, token_list = pop_token(token_list)
    cond_exp = CondExp(cond_tokens)
    cond_exp.build_cond_tree()
    body_exp = BodyExp()
    while(not token == ("kw", "close-curly-brace")):
        next_exp, token_list = get_next_exp(token_list)
        body_exp.append(next_exp)
        token = token_list[0]
    token, token_list = pop_token(token_list)

    conds.append(cond_exp)
    bodys.append(body_exp)
    
    while(token_list[0] == ("kw", "or")):
        token, token_list = pop_token(token_list)
        if not token == ("kw", "or"):
            parse_error("")
        token, token_list = pop_token(token_list)
        if token == ("kw", "if"):
            cond_tokens = []
            token, token_list = pop_token(token_list)
            while(not token == ("kw", "open-curly-brace")):
                cond_tokens.append(token)
                token, token_list = pop_token(token_list)
            cond_exp = CondExp(cond_tokens)
            cond_exp.build_cond_tree()

            body_exp = BodyExp()
            while(not token == ("kw", "close-curly-brace")):
                next_exp, token_list = get_next_exp(token_list)
                body_exp.append(next_exp)
                token = token_list[0]
            token, token_list = pop_token(token_list)
            conds.append(cond_exp)
            bodys.append(body_exp)
        elif token == ("kw", "open-curly-brace"):
            else_case = True
            body_exp = BodyExp()
            while(not token == ("kw", "close-curly-brace")):
                next_exp, token_list = get_next_exp(token_list)
                body_exp.append(next_exp)
                token = token_list[0]
            token, token_list = pop_token(token_list)
            bodys.append(body_exp)
        else:
            parse_error("")
        if token_list == []:
            break
    return (IfExp(conds, bodys, else_case), token_list)

def parse_try_exp(token_list):
    #print("Try")
    body = None
    error_id = None
    error_body = None

    token, token_list = pop_token(token_list)
    if not token == ("kw", "open-curly-brace"):
        parse_error("")

    body = BodyExp()
    while(not token == ("kw", "close-curly-brace")):
        next_exp, token_list = get_next_exp(token_list)
        body.append(next_exp)
        token = token_list[0]
    token, token_list = pop_token(token_list)
    
    token, token_list = pop_token(token_list)
    if token == ("kw", "catch"):
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            error_id = token[1]
        else:
            parse_error("")
    else:
        parse_error("")
    
    token, token_list = pop_token(token_list)
    if not token == ("kw", "open-curly-brace"):
        parse_error("")

    error_body = BodyExp()
    while(not token == ("kw", "close-curly-brace")):
        next_exp, token_list = get_next_exp(token_list)
        error_body.append(next_exp)
        token = token_list[0]
    token, token_list = pop_token(token_list)
    return (TryExp(body, error_id, error_body), token_list)

def parse_exit_exp(token_list):
    #print("Exit")
    return (ExitExp(), token_list)

def parse_next_exp(token_list):
    token, token_list = pop_token(token_list)
    tmp_exp = None
    if token == ("kw", "retrieve"):
        tmp_exp, token_list = parse_retrieve_exp(token_list)
    elif token == ("kw", "declare"):
        tmp_exp, token_list = parse_declare_exp(token_list)
    elif token == ("kw", "set"):
        tmp_exp, token_list = parse_set_exp(token_list)
    elif token == ("kw", "while"):
        tmp_exp, token_list = parse_while_exp(token_list)
    elif token == ("kw", "call"):
        tmp_exp, token_list = parse_call_exp(token_list)
    elif token == ("kw", "break"):
        tmp_exp, token_list = parse_break_exp(token_list)
    elif token == ("kw", "jump"):
        tmp_exp, token_list = parse_jump_exp(token_list)
    elif token == ("kw", "for"):
        tmp_exp, token_list = parse_for_exp(token_list)
    elif token == ("kw", "return"):
        tmp_exp, token_list = parse_return_exp(token_list)
    elif token == ("kw", "if"):
        tmp_exp, token_list = parse_if_exp(token_list)
    elif token == ("kw", "try"):
        tmp_exp, token_list = parse_try_exp(token_list)
    elif token == ("kw", "exit"):
        tmp_exp, token_list = parse_exit_exp(token_list)
    else:
        print(token)
        parse_error("Unknown Exp: YEETO 2")
    return (tmp_exp, token_list)

class AST:
    def __init__(self):
        self.head = BodyExp()
        self.env = {}

    def parse_tokens(self, token_list):
        while(token_list):
            token, token_list = pop_token(token_list)
            tmp_exp = None
            if token == ("kw", "retrieve"):
                tmp_exp, token_list = parse_retrieve_exp(token_list)
            elif token == ("kw", "declare"):
                tmp_exp, token_list = parse_declare_exp(token_list)
            elif token == ("kw", "set"):
                tmp_exp, token_list = parse_set_exp(token_list)
            elif token == ("kw", "while"):
                tmp_exp, token_list = parse_while_exp(token_list)
            elif token == ("kw", "call"):
                tmp_exp, token_list = parse_call_exp(token_list)
            elif token == ("kw", "break"):
                tmp_exp, token_list = parse_break_exp(token_list)
            elif token == ("kw", "jump"):
                tmp_exp, token_list = parse_jump_exp(token_list)
            elif token == ("kw", "for"):
                tmp_exp, token_list = parse_for_exp(token_list)
            elif token == ("kw", "return"):
                tmp_exp, token_list = parse_return_exp(token_list)
            elif token == ("kw", "if"):
                tmp_exp, token_list = parse_if_exp(token_list)
            elif token == ("kw", "try"):
                tmp_exp, token_list = parse_try_exp(token_list)
            elif token == ("kw", "exit"):
                tmp_exp, token_list = parse_exit_exp(token_list)
            else:
                parse_error("Unknown Exp: YEETO 1")
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
                "print": {"args": {"argument-1": "any"}, "body": None, "fnc": jordie_print}
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
        print(self.env)
    

def parse(token_list):
    ast = AST()
    #print(ast)
    ast.parse_tokens(token_list)
    #print("aaaa")
    #print(ast)
    #print("bbbb")
    return ast

#parse = lambda token_list: AST().parse_tokens(token_list)