class Exp():
    def __init__(self):
        print("CREATE EXP")

    def print_exp(self):
        return "GET EXP STRING"

    def execute(self):
        return "RUN EXP"

class BodyExp(Exp):
    #exp_list = []

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

class DeclareExp(Exp):
    #e_id = ""
    #e_const = False
    #e_type = ""
    #e_val = None

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

class AST:
    head = None

    def __init__(self):
        self.head = BodyExp()

    def add_tokens(self, token_list):
        tmp_exp = DeclareExp("num", False, "int", 13)
        self.head.append(tmp_exp)
        tmp_exp = DeclareExp("num", False, "int", 15)
        self.head.append(tmp_exp)
        body_exp = BodyExp()
        cnt = 0
        while(cnt < 6):
            #id, const, type
            dec_exp = DeclareExp("num", False, "int")
            body_exp.append(dec_exp)
            cnt += 1
        self.head.append(body_exp)

    def print_tree(self):
        print(self.head.print_exp(0))
    
    def get_tree_str(self):
        return self.head.print_exp(0)

    def execute(self):
        return "EXECUTE THE TREE"

#ast = AST()
#ast.add_tokens([])
#ast.print_tree()


body1 = BodyExp()
print(body1.print_exp(0))

dec1 = DeclareExp("num1", False, "int", 1)
print(dec1.print_exp(0))

body1.append(dec1)
print(body1.print_exp(0))

dec2 = DeclareExp("num2", False, "int", 2)
print(dec2.print_exp(0))

dec3 = DeclareExp("num3", False, "int", 3)
print(dec3.print_exp(0))

body1.append(dec2)
body1.append(dec3)
print(body1.print_exp(0))

body2 = BodyExp()
print(body2.print_exp(0))

dec4 = DeclareExp("num4", False, "int", 4)
print(dec4.print_exp(0))

dec5 = DeclareExp("num5", False, "int", 5)
print(dec5.print_exp(0))

body2.append(dec4)
print(body2.print_exp(0))

body1.append(body2)
print(body1.print_exp(0))

body1.append(dec5)
print(body1.print_exp(0))
