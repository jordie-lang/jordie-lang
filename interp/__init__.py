import lexer
import parser
import json

def run(soure_string):
    token_list = lexer.lex(soure_string)
    #lexer.print_tokens(token_list)
    ast = parser.parse(token_list)
    #ast.print_tree()
    ast.execute()
