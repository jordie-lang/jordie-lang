# Test 0 - declaring variables
test_case_00_variables = """
declare changeable construct named sum of type integer semicolon
declare changeable construct named counter of type integer with value zero semicolon
comment
call functional construct named print and pass in sum semicolon
call functional construct named print and pass in counter semicolon
comment
"""
lexer_00_variables = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'sum')
('type', 'integer')
('kw', 'semicolon')
('kw', 'declare')
('kw', 'changeable')
('id', 'counter')
('type', 'integer')
('val', 0)
('kw', 'semicolon')
"""
parser_00_variables = """
BodyExp:
  DeclareExp: id=sum const=False type=integer
    value:
      ValExp:
        val=None
  DeclareExp: id=counter const=False type=integer
    value:
      ValExp:
        val=0
"""
exec_00_variables = """
"""

# Test 1 - declaring constant
test_case_01_constants = """
declare nonchangeable construct named number_one of type integer with value thirteen semicolon
declare nonchangeable construct named number_two of type integer with value four-thousand-eight-hundred-sixty-seven semicolon
"""
lexer_01_constants = """
Tokens:
('kw', 'declare')
('kw', 'nonchangeable')
('id', 'number_one')
('type', 'integer')
('val', 13)
('kw', 'semicolon')
('kw', 'declare')
('kw', 'nonchangeable')
('id', 'number_two')
('type', 'integer')
('val', 4867)
('kw', 'semicolon')
"""
parser_01_constants = """
BodyExp:
  DeclareExp: id=number_one const=True type=integer
    value:
      ValExp:
        val=13
  DeclareExp: id=number_two const=True type=integer
    value:
      ValExp:
        val=4867
"""
exec_01_constants = """
"""

# Test 2 - declaring integer
test_case_02_integers = """
declare changeable construct named int_one of type integer with value thirteen semicolon
declare changeable construct named int_two of type integer with value eight semicolon
"""
lexer_02_integers = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'int_one')
('type', 'integer')
('val', 13)
('kw', 'semicolon')
('kw', 'declare')
('kw', 'changeable')
('id', 'int_two')
('type', 'integer')
('val', 8)
('kw', 'semicolon')
"""
parser_02_integers = """
BodyExp:
  DeclareExp: id=int_one const=False type=integer
    value:
      ValExp:
        val=13
  DeclareExp: id=int_two const=False type=integer
    value:
      ValExp:
        val=8
"""
exec_02_integers = """
"""

# Test 3 - declaring float
test_case_03_floats = """
declare changeable construct named float_one of type float with value thirteen-dot-five semicolon
declare changeable construct named float_two of type float with value eighty-seven-dot-two-five semicolon
"""
lexer_03_floats = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'float_one')
('type', 'float')
('val', 13.5)
('kw', 'semicolon')
('kw', 'declare')
('kw', 'changeable')
('id', 'float_two')
('type', 'float')
('val', 87.25)
('kw', 'semicolon')
"""
parser_03_floats = """
BodyExp:
  DeclareExp: id=float_one const=False type=float
    value:
      ValExp:
        val=13.5
  DeclareExp: id=float_two const=False type=float
    value:
      ValExp:
        val=87.25
"""
exec_03_floats = """
"""

# Test 4 - declaring string
test_case_04_strings = """
declare changeable construct named message of type string with value double-quote Hello There! double-quote semicolon
declare changeable construct named empty of type string with value double-quote  double-quote semicolon
"""
lexer_04_strings = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'message')
('type', 'string')
('val', 'Hello There!')
('kw', 'semicolon')
('kw', 'declare')
('kw', 'changeable')
('id', 'empty')
('type', 'string')
('val', '')
('kw', 'semicolon')
"""
parser_04_strings = """
BodyExp:
  DeclareExp: id=message const=False type=string
    value:
      ValExp:
        val=Hello There!
  DeclareExp: id=empty const=False type=string
    value:
      ValExp:
        val=
"""
exec_04_strings = """
"""

# Test 5 - declaring list
test_case_05_lists = """
declare changeable construct named fruit of type list with value open-square-bracket double-quote mango double-quote double-quote banana double-quote close-square-bracket semicolon
declare changeable construct named lst of type list with value open-square-bracket double-quote word double-quote seven six-dot-five close-square-bracket semicolon
"""
lexer_05_lists = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'fruit')
('type', 'list')
('val', ['mango', 'banana'])
('kw', 'semicolon')
('kw', 'declare')
('kw', 'changeable')
('id', 'lst')
('type', 'list')
('val', ['word', 7, 6.5])
('kw', 'semicolon')
"""
parser_05_lists = """
BodyExp:
  DeclareExp: id=fruit const=False type=list
    value:
      ValExp:
        val=['mango', 'banana']
  DeclareExp: id=lst const=False type=list
    value:
      ValExp:
        val=['word', 7, 6.5]
"""
exec_05_lists = """
"""

# Test 6 - declaring dictionary
test_case_06_dictionaries = """
declare changeable construct named address of type dictionary with value open-curly-brace key double-quote city double-quote value double-quote Hoboken double-quote key double-quote street double-quote value double-quote Washington double-quote close-curly-brace semicolon
"""
lexer_06_dictionaries = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'address')
('type', 'dictionary')
('val', {'city': 'Hoboken', 'street': 'Washington'})
('kw', 'semicolon')
"""
parser_06_dictionaries = """
BodyExp:
  DeclareExp: id=address const=False type=dictionary
    value:
      ValExp:
        val={'city': 'Hoboken', 'street': 'Washington'}
"""
exec_06_dictionaries = """
"""

# Test 7 - declaring structs
test_case_07_structs = """
declare structure named address open-curly-brace
    field named name of type string semicolon
    field named street of type string semicolon
    field named city of type string semicolon
    field named state of type string semicolon
    field named zip of type integer semicolon
close-curly-brace
declare changeable construct named my_address of type address semicolon
"""
lexer_07_structs = """
Tokens:
('kw', 'declare')
('kw', 'structure')
('id', 'address')
('kw', 'open-curly-brace')
('kw', 'field')
('id', 'name')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'street')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'city')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'state')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'zip')
('type', 'integer')
('kw', 'semicolon')
('kw', 'close-curly-brace')
('kw', 'declare')
('kw', 'changeable')
('id', 'my_address')
('type', 'address')
('kw', 'semicolon')
"""
parser_07_structs = """
BodyExp:
  StructExp: id=address
    Fields:
      city: string
      state: string
      street: string
      name: string
      zip: integer
  DeclareExp: id=my_address const=False type=address
    value:
      ValExp:
        val=None
"""
exec_07_structs = """
"""

# Test 8 - setting variables
test_case_08_set = """
declare changeable construct named message of type string semicolon
set construct named message with value double-quote Hello World! double-quote semicolon
declare nonchangeable construct named number_one of type integer with value one semicolon
declare changeable construct named counter of type integer with value zero semicolon
set construct named counter with value number_one semicolon
declare structure named address open-curly-brace
    field named name of type string semicolon
    field named street of type string semicolon
    field named city of type string semicolon
    field named state of type string semicolon
    field named zip of type integer semicolon
close-curly-brace
declare changeable construct named my_address of type address semicolon
set field named city of construct named my_address with value double-quote Hoboken double-quote semicolon
"""
lexer_08_set = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'message')
('type', 'string')
('kw', 'semicolon')
('kw', 'set')
('id', 'message')
('val', 'Hello World!')
('kw', 'semicolon')
('kw', 'declare')
('kw', 'nonchangeable')
('id', 'number_one')
('type', 'integer')
('val', 1)
('kw', 'semicolon')
('kw', 'declare')
('kw', 'changeable')
('id', 'counter')
('type', 'integer')
('val', 0)
('kw', 'semicolon')
('kw', 'set')
('id', 'counter')
('id', 'number_one')
('kw', 'semicolon')
('kw', 'declare')
('kw', 'structure')
('id', 'address')
('kw', 'open-curly-brace')
('kw', 'field')
('id', 'name')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'street')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'city')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'state')
('type', 'string')
('kw', 'semicolon')
('kw', 'field')
('id', 'zip')
('type', 'integer')
('kw', 'semicolon')
('kw', 'close-curly-brace')
('kw', 'declare')
('kw', 'changeable')
('id', 'my_address')
('type', 'address')
('kw', 'semicolon')
('kw', 'set')
('kw', 'field')
('id', 'city')
('id', 'my_address')
('val', 'Hoboken')
('kw', 'semicolon')
"""
parser_08_set = """
BodyExp:
  DeclareExp: id=message const=False type=string
    value:
      ValExp:
        val=None
  SetExp: id=message field_id=
    value:
      ValExp:
        val=Hello World!
  DeclareExp: id=number_one const=True type=integer
    value:
      ValExp:
        val=1
  DeclareExp: id=counter const=False type=integer
    value:
      ValExp:
        val=0
  SetExp: id=counter field_id=
    value:
      ValExp:
        id=number_one
  StructExp: id=address
    Fields:
      city: string
      state: string
      street: string
      name: string
      zip: integer
  DeclareExp: id=my_address const=False type=address
    value:
      ValExp:
        val=None
  SetExp: id=my_address field_id=city
    value:
      ValExp:
        val=Hoboken
"""
exec_08_set = """
"""

# Test 9 - calling builtin functions
test_case_09_call_builtin_funcs = """
declare changeable construct named number_one of type integer with value ten semicolon
call functional construct named print and pass in number_one semicolon
"""
lexer_09_call_builtin_funcs = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'number_one')
('type', 'integer')
('val', 10)
('kw', 'semicolon')
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('id', 'number_one')
('kw', 'semicolon')
"""
parser_09_call_builtin_funcs = """
BodyExp:
  DeclareExp: id=number_one const=False type=integer
    value:
      ValExp:
        val=10
  CallExp: func_id=print ret_id=None
    Args:
      Arg: argument-1
        value:
          ValExp:
            id=number_one
"""
exec_09_call_builtin_funcs = """
10
"""

# Test 10 - declaring functions
test_case_10_declare_funcs = """
declare functional construct named print_five which returns nothing and receives nothing open-curly-brace
    call functional construct named print and pass in five semicolon
close-curly-brace
"""
lexer_10_declare_funcs = """
Tokens:
('kw', 'declare')
('kw', 'functional')
('id', 'print_five')
('kw', 'returns')
('type', 'nothing')
('kw', 'receives')
('type', 'nothing')
('kw', 'open-curly-brace')
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('val', 5)
('kw', 'semicolon')
('kw', 'close-curly-brace')
"""
parser_10_declare_funcs = """
BodyExp:
  FuncExp: id=print_five type=nothing
    Args:
      None
    BodyExp:
      CallExp: func_id=print ret_id=None
        Args:
          Arg: argument-1
            value:
              ValExp:
                val=5
"""
exec_10_declare_funcs = """
"""

# Test 11 - calling functions
test_case_11_call_funcs = """
declare functional construct named print_five which returns nothing and receives nothing open-curly-brace
    call functional construct named print and pass in five semicolon
close-curly-brace
call functional construct named print_five semicolon
"""
lexer_11_call_funcs = """
Tokens:
('kw', 'declare')
('kw', 'functional')
('id', 'print_five')
('kw', 'returns')
('type', 'nothing')
('kw', 'receives')
('type', 'nothing')
('kw', 'open-curly-brace')
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('val', 5)
('kw', 'semicolon')
('kw', 'close-curly-brace')
('kw', 'call')
('kw', 'functional')
('id', 'print_five')
('kw', 'semicolon')
"""
parser_11_call_funcs = """
BodyExp:
  FuncExp: id=print_five type=nothing
    Args:
      None
    BodyExp:
      CallExp: func_id=print ret_id=None
        Args:
          Arg: argument-1
            value:
              ValExp:
                val=5
  CallExp: func_id=print_five ret_id=None
    Args:
      None
"""
exec_11_call_funcs = """
"""

# Test 12 - retrieve source
test_case_12_retrieve = """
call functional construct named print and pass in three semicolon
retrieve source from file named test_retrieve semicolon 
call functional construct named print and pass in seven semicolon
"""
lexer_12_retrieve = """
Tokens:
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('val', 3)
('kw', 'semicolon')
('kw', 'retrieve')
('id', 'test_retrieve')
('kw', 'semicolon')
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('val', 7)
('kw', 'semicolon')
"""
parser_12_retrieve = """
BodyExp:
  CallExp: func_id=print ret_id=None
    Args:
      Arg: argument-1
        value:
          ValExp:
            val=3
  RetrieveExp: id=test_retrieve
  CallExp: func_id=print ret_id=None
    Args:
      Arg: argument-1
        value:
          ValExp:
            val=7
"""
exec_12_retrieve = """
"""

# Test 13 - for loop
test_case_13_for_loop = """
declare changeable construct named fruits of type list with value open-square-bracket double-quote mango double-quote double-quote apple double-quote double-quote strawberry double-quote close-square-bracket semicolon
for every item in the construct named fruits do the following open-curly-brace
    call functional construct named print and pass in item semicolon
close-curly-brace
"""
lexer_13_for_loop = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'fruits')
('type', 'list')
('val', ['mango', 'apple', 'strawberry'])
('kw', 'semicolon')
('kw', 'for')
('id', 'fruits')
('kw', 'open-curly-brace')
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('id', 'item')
('kw', 'semicolon')
('kw', 'close-curly-brace')
"""
parser_13_for_loop = """
BodyExp:
  DeclareExp: id=fruits const=False type=list
    value:
      ValExp:
        val=['mango', 'apple', 'strawberry']
  ForExp: id=fruits
    BodyExp:
      CallExp: func_id=print ret_id=None
        Args:
          Arg: argument-1
            value:
              ValExp:
                id=item
"""
exec_13_for_loop = """
"""

# Test 14 - while loop
test_case_14_while_loop = """
declare changeable construct named counter of type integer with value ten semicolon
while counter is greater than zero run the following open-curly-brace
    call functional construct named print and pass in counter semicolon
close-curly-brace
"""
lexer_14_while_loop = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'counter')
('type', 'integer')
('val', 10)
('kw', 'semicolon')
('kw', 'while')
('id', 'counter')
('op', 'is greater than')
('val', 0)
('kw', 'open-curly-brace')
('kw', 'call')
('kw', 'functional')
('id', 'print')
('kw', 'pass')
('id', 'counter')
('kw', 'semicolon')
('kw', 'close-curly-brace')
"""
parser_14_while_loop = """
BodyExp:
  DeclareExp: id=counter const=False type=integer
    value:
      ValExp:
        val=10
  WhileExp:
    GreaterExp:
      ValExp:
        id=counter
      ValExp:
        val=0
    BodyExp:
      CallExp: func_id=print ret_id=None
        Args:
          Arg: argument-1
            value:
              ValExp:
                id=counter
"""
exec_14_while_loop = """
"""

# Test 15 - break statement

# Test 16 - continue statement

# Test 17 - if statement

# Test 18 - try / catch

# Test 19 - exit statement
