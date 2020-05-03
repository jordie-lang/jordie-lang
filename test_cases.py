# Test 0 - declaring variables
test_case_0_variables = """
declare changeable construct named sum of type integer semicolon
declare changeable construct named counter of type integer with value zero semicolon
comment
call functional construct named print and pass in sum semicolon
call functional construct named print and pass in counter semicolon
comment
"""
lexer_0_variables = """
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
parser_0_variables = """
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
exec_0_variables = """
"""

# Test 1 - declaring constant
test_case_1_constants = """
declare nonchangeable construct named number_one of type integer with value thirteen semicolon
declare nonchangeable construct named number_two of type integer with value four-thousand-eight-hundred-sixty-seven semicolon
"""
lexer_1_constants = """
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
parser_1_constants = """
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
exec_1_constants = """
"""

# Test 2 - declaring integer
test_case_2_integers = """
declare changeable construct named int_one of type integer with value thirteen semicolon
declare changeable construct named int_two of type integer with value eight semicolon
"""
lexer_2_integers = """
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
parser_2_integers = """
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
exec_2_integers = """
"""

# Test 3 - declaring float
test_case_3_floats = """
declare changeable construct named float_one of type float with value thirteen-dot-five semicolon
declare changeable construct named float_two of type float with value eighty-seven-dot-two-five semicolon
"""
lexer_3_floats = """
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
parser_3_floats = """
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
exec_3_floats = """
"""

# Test 4 - declaring string
test_case_4_strings = """
declare changeable construct named message of type string with value double-quote Hello There! double-quote semicolon
declare changeable construct named empty of type string with value double-quote  double-quote semicolon
"""
lexer_4_strings = """
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
parser_4_strings = """
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
exec_4_strings = """
"""

# Test 5 - declaring list
test_case_5_lists = """
declare changeable construct named fruit of type list with value open-square-bracket double-quote mango double-quote double-quote banana double-quote close-square-bracket semicolon
declare changeable construct named lst of type list with value open-square-bracket double-quote word double-quote seven six-dot-five close-square-bracket semicolon
"""
lexer_5_lists = """
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
parser_5_lists = """
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
exec_5_lists = """
"""

# Test 6 - declaring dictionary
test_case_6_dictionaries = """
declare changeable construct named address of type dictionary with value open-curly-brace key double-quote city double-quote value double-quote Hoboken double-quote key double-quote street double-quote value double-quote Washington double-quote close-curly-brace semicolon
"""
lexer_6_dictionaries = """
Tokens:
('kw', 'declare')
('kw', 'changeable')
('id', 'address')
('type', 'dictionary')
('val', {'city': 'Hoboken', 'street': 'Washington'})
('kw', 'semicolon')
"""
parser_6_dictionaries = """
BodyExp:
  DeclareExp: id=address const=False type=dictionary
    value:
      ValExp:
        val={'city': 'Hoboken', 'street': 'Washington'}
"""
exec_6_dictionaries = """
"""

# Test 7 - declaring structs
test_case_7_structs = """
declare structure named address open-curly-brace
    field named name of type string semicolon
    field named street of type string semicolon
    field named city of type string semicolon
    field named state of type string semicolon
    field named zip of type integer semicolon
close-curly-brace
declare changeable construct named my_address of type address semicolon
"""
lexer_7_structs = """
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
parser_7_structs = """
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
exec_7_structs = """
"""

# Test 8 - setting variables
test_case_8_set = """
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
lexer_8_set = """
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
parser_8_set = """
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
exec_8_set = """
"""

# Test 9 - declaring functions

# Test 10 - calling functions

# Test 11 - including resources

# Test 12 - for loop

# Test 13 - while loop

# Test 14 - break statement

# Test 15 - continue statement

# Test 16 - if statement

# Test 17 - assert statement

# Test 18 - try / catch

# Test 19 - exit statement
