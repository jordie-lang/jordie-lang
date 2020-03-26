"""
jordie-lang parser

AST:


"""

test_tokens = [
    ('kw', 'declare'),
    ('kw', 'nonchangeable'),
    ('id', 'number_one'),
    ('type', 'integer'),
    ('val', 13),
    ('kw', 'semicolon'),
    ('kw', 'set'),
    ('id', 'number_one'),
    ('val', 31),
    ('kw', 'semicolon'),
]

op_prec_list = [
    ["times", "divides"],
    ["plus", "minus"],
    ["is equal to", "is greater than", "is less than"],
    ["not"],
    ["and"],
    ["or"]
]

class Exp():
    def __init__(self):
        print("CREATE EXP")

    def print_exp(self):
        return "GET EXP STRING"

    def execute(self):
        return "RUN EXP"

def get_next_val_exp(tok_list):
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

class ValExp(Exp):
    def __init__(self, _v_tokens):
        self.val_tokens = _v_tokens
        self.v_head = None
        self.is_id = False
        self.is_val = False

    def build_tree(self):
        if len(self.val_tokens) == 1:
            #only 1 token means val or id
            tok = self.val_tokens[0]
            if tok[0] == "val":
                self.is_val = True
                self.v_head = tok[1]
            elif tok[0] == "id":
                self.is_id = True
                self.v_head = tok[1]
        elif len(self.val_tokens) == 0:
            parse_error("")
        else:
            self.v_head = get_next_val_exp(self.val_tokens)
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ValExp:\n".format("  "*level)
        if self.is_val:
            exp_str += "{}val={}\n".format("  "*(level+1), self.v_head)
        elif self.is_id:
            exp_str += "{}id={}\n".format("  "*(level+1), self.v_head)
        else:
            exp_str += self.v_head.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN VAL EXP"

def get_next_cond_exp(tok_list):
    #if there is an operator
    op_prec_list.reverse()
    for ops in op_prec_list:
        ops.reverse()
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

def make_op_exp(op, tokens, index):
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

class MultExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}MultExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN MULT EXP"

class DivExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}DivExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN DIV EXP"

class AddExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AddExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN ADD EXP"

class SubExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}SubExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN SUB EXP"

class EqualExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}EqualExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN EQUAL EXP"

class GreaterExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}GreaterExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN GREATER EXP"

class LessExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}LessExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN LESS EXP"

class NotExp(Exp):
    def __init__(self, _right):
        self.right_exp = None
        self.right_tokens = _right

    def build_tree(self):
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}NotExp:\n".format("  "*level)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN NOT EXP"

class AndExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}AndExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN AND EXP"

class OrExp(Exp):
    def __init__(self, _left, _right):
        self.left_exp = None
        self.right_exp = None
        self.left_tokens = _left
        self.right_tokens = _right

    def build_tree(self):
        self.left_exp = get_next_cond_exp(self.left_tokens)
        self.right_exp = get_next_cond_exp(self.right_tokens)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}OrExp:\n".format("  "*level)
        exp_str += self.left_exp.print_exp(level+1)
        exp_str += self.right_exp.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN OR EXP"

class CondExp(Exp):
    def __init__(self, _cond):
        self.c_exp = _cond
        self.c_heaad = None
    
    def build_cond_tree(self):
        self.c_head = get_next_cond_exp(self.c_exp)

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}CondExp:\n".format("  "*level)
        exp_str += self.c_head.print_exp(level+1)
        return exp_str

    def execute(self):
        return "RUN COND EXP"

class BodyExp(Exp):  # DONE
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
    
    def execute(self):
        for exp in self.exp_list:
            exp.execute()

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
    
    def execute(self):
        return "RUN STRUCT EXP"

class RetrieveExp(Exp):
    def __init__(self, _id):
        self.e_id = _id
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}RetrieveExp: id={}\n".format("  "*level, self.e_id)
        return exp_str
    
    def execute(self):
        return "RUN RETRIEVE EXP"

class DeclareExp(Exp):
    def __init__(self, _id, _const, _type, _value=None):
        self.e_id = _id
        self.e_const = _const
        self.e_type = _type
        self.e_val = _value
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}DeclareExp: id={} const={} type={} value={}\n".format("  "*level, self.e_id, self.e_const, self.e_type, self.e_val)
        return exp_str
    
    def execute(self):
        return "RUN DECLARE EXP"

class SetExp(Exp):
    def __init__(self, _id, _val, _field_id):
        self.e_id = _id
        self.e_val = _val
        self.e_field_id = _field_id

    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}SetExp: id={} field_id={}\n".format("  "*level, self.e_id, self.e_field_id)
        exp_str += self.e_val.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "TODO"

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
        return "RUN WHILE EXP"

class CallExp(Exp):
    def __init__(self, _f_id, _args, _ret_id):
        self.f_id = _f_id
        self.f_args = _args
        self.f_ret = _ret_id
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}CallExp: func_id={} ret_id={}\n".format("  "*level, self.f_id, self.f_ret)
        exp_str += "{}Args:\n".format("  "*(level+1))
        for arg in self.f_args:
            exp_str += "{}Arg: {}={}\n".format("  "*(level+2), arg[0], arg[1])
        return exp_str
    
    def execute(self):
        return "RUN CALL EXP"

class BreakExp(Exp):
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}BreakExp\n".format("  "*level)
        return exp_str
    
    def execute(self):
        return "RUN BREAK EXP"

class JumpExp(Exp):
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}JumpExp\n".format("  "*level)
        return exp_str
    
    def execute(self):
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
    
    def execute(self):
        return "RUN FOR EXP"

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
        for arg in self.f_args:
            exp_str += "{}Arg: {}={}\n".format("  "*(level+2), arg[0], arg[1])
        exp_str += self.f_body.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN FUNC EXP"

class RetExp(Exp):
    def __init__(self, _val):
        self.r_val = _val
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}RetExp:\n".format("  "*level)
        exp_str += self.r_val.print_exp(level+1)
        return exp_str
    
    def execute(self):
        return "RUN FUNC EXP"

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
        return "RUN ASSERT EXP"

class ExitExp(Exp):
    def __init__(self):
        self.tmp_var = "TMP"
    
    def print_exp(self, level):
        exp_str = ""
        exp_str += "{}ExitExp\n".format("  "*level)
        return exp_str
    
    def execute(self):
        return "RUN EXIT EXP"

def pop_token(token_list):
    return (token_list[0], token_list[1:])

def get_next_exp(token_list):
    token, token_list = pop_token(token_list)
    if token == ("kw", "retrieve"):
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
    elif token == ("kw", "declare"):
        #print("Declare")
        t_id = ""
        t_type = ""
        t_const = False
        t_val = ""
        token, token_list = pop_token(token_list)
        if token == ("kw", "functional"):
            #declare function
            f_id = ""
            f_type = ""
            f_args = []
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
                while(not token == ("kw", "open-curly-brace")):
                    if token[0] == "type":
                        f_args.append(token)
                    else:
                        parse_error("")
                    token, token_list = pop_token(token_list)
            else:
                parse_error("")
            #print("$$$$$$$$")
            #print(f_args)
            #print("########")
            f_body = BodyExp()
            while(not token == ("kw", "close-curly-brace")):
                #print("another go around")
                #print(token)
                #print(token_list[:10])
                next_exp, token_list = get_next_exp(token_list)
                f_body.append(next_exp)
                if len(token_list) < 1:
                    #print("YOYOYEET")
                    return (FuncExp(f_id, f_type, f_args, f_body), token_list)
                token = token_list[0]
            token, token_list = pop_token(token_list)
            #print("FORTRAN")
            return (FuncExp(f_id, f_type, f_args, f_body), token_list)
        elif token == ("kw", "changeable"):
            t_const = True
        elif token == ("kw", "nonchangeable"):
            t_const = False
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
            parse_error("eee1")
        token, token_list = pop_token(token_list)
        if token[0] == "id":
            t_id = token[1]
        else:
            parse_error("eee2")
        token, token_list = pop_token(token_list)
        if token[0] == "type":
            t_type = token[1]
        else:
            parse_error("eee3")
        token, token_list = pop_token(token_list)
        if token == ("kw", "semicolon"):
            return (DeclareExp(t_id, t_const, t_type), token_list)
        elif token[0] == "val":
            t_val = token[1]
            token, token_list = pop_token(token_list)
            if token == ("kw", "semicolon"):
                return (DeclareExp(t_id, t_const, t_type, t_val), token_list)
            else:
                parse_error("eee3.5")
        else:
            parse_error("eee4")
    elif token == ("kw", "set"):
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

        val_tokens = []
        token, token_list = pop_token(token_list)
        while(not token == ("kw", "semicolon")):
            val_tokens.append(token)
            token, token_list = pop_token(token_list)
        t_val = ValExp(val_tokens)
        t_val.build_tree()

        if token == ("kw", "semicolon"):
            return (SetExp(t_id, t_val, t_field_id), token_list)
        else:
            parse_error("eee7")
    elif token == ("kw", "while"):
        #print("While")
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
        return (WhileExp(cond_exp, body_exp), token_list)
    elif token == ("kw", "call"):
        #print("Call")
        func_id = None
        args = []
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
                while(not (token == ("kw", "return") or token == ("kw", "semicolon"))):
                    args.append(token)
                    token, token_list = pop_token(token_list)
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
    elif token == ("kw", "break"):
        #print("Break")
        token, token_list = pop_token(token_list)
        if token == ("kw", "semicolon"):
            return (BreakExp(), token_list)
        else:
            parse_error("breakeeeeee")
    elif token == ("kw", "jump"):
        #print("Jump")
        token, token_list = pop_token(token_list)
        if token == ("kw", "semicolon"):
            return (JumpExp(), token_list)
        else:
            parse_error("breakeeeeee")
    elif token == ("kw", "for"):
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
            next_exp, token_list = get_next_exp(token_list)
            body_exp.append(next_exp)
            token = token_list[0]
        token, token_list = pop_token(token_list)
        return (ForExp(items, body_exp), token_list)
    elif token == ("kw", "return"):
        val_tokens = []
        token, token_list = pop_token(token_list)
        while(not token == ("kw", "semicolon")):
            val_tokens.append(token)
            token, token_list = pop_token(token_list)
        r_val = ValExp(val_tokens)
        r_val.build_tree()
        return (RetExp(r_val), token_list)
    elif token == ("kw", "if"):
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
    elif token == ("kw", "try"):
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
    elif token == ("kw", "assert"):
        #print("Assert")
        cond_exp = None

        cond_tokens = []
        token, token_list = pop_token(token_list)
        while(not token == ("kw", "semicolon")):
            cond_tokens.append(token)
            token, token_list = pop_token(token_list)
        cond_exp = CondExp(cond_tokens)
        cond_exp.build_cond_tree()
        return (AssertExp(cond_exp), token_list)
    elif token == ("kw", "exit"):
        #print("Exit")
        return (ExitExp(), token_list)
    else:
        #print(token)
        parse_error("Unknown Exp: YEETO")

class AST:
    def __init__(self):
        self.head = BodyExp()

    def add_tokens(self, token_list):
        while(token_list):
            #print("add tokens loop")
            tmp_exp, token_list = get_next_exp(token_list)
            #print(tmp_exp)
            #print(token_list[:10])
            self.head.append(tmp_exp)
            #print("add tokens end loop")

    def print_tree(self):
        print(self.head.print_exp(0))
    
    def get_tree_str(self):
        return self.head.print_exp(0)

    def execute(self):
        # probably need to setup environment for vars and builtins and such here before executing, maybe pass in the env and return the envs back as an execution stack
        print("***** AST *****")
        self.print_tree()
        print("***** RUN *****")
        self.head.execute()

def parse_error(error_msg):
    print(error_msg)
    exit(0)

def format_tree_output(ast):
    return "TODO"

def parse(token_list):
    ast = AST()
    ast.add_tokens(token_list)
    #ast.add_tokens(test_tokens)
    return ast