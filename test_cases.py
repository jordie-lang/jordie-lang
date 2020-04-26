# Test 0 - declaring variables
test_case_0_variables = """
declare changeable construct named sum of type integer semicolon
declare changeable construct named counter of type integer with value zero semicolon
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
    Value:
      ValExp:
        val=None
  DeclareExp: id=counter const=False type=integer
    Value:
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
    Value:
      ValExp:
        val=13
  DeclareExp: id=number_two const=True type=integer
    Value:
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
    Value:
      ValExp:
        val=13
  DeclareExp: id=int_two const=False type=integer
    Value:
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
    Value:
      ValExp:
        val=13.5
  DeclareExp: id=float_two const=False type=float
    Value:
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
    Value:
      ValExp:
        val=Hello There!
  DeclareExp: id=empty const=False type=string
    Value:
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
    Value:
      ValExp:
        val=['mango', 'banana']
  DeclareExp: id=lst const=False type=list
    Value:
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
    Value:
      ValExp:
        val={'city': 'Hoboken', 'street': 'Washington'}
"""
exec_6_dictionaries = """
"""

# Test 7 - declaring structs

# Test 8 - setting variables

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
