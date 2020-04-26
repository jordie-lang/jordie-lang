"""
jordie-lang lexer

Tokens:
("kw", "define")
("kw", "semicolon")
("id", "addnums")
("id", "number_one")
("val", 8)
("val", "hello there")
("op", "with")
("op", "value")
"""
kw_list = ["declare", "nonchangeable", "functional", "changeable", "construct", "named", "of", "type", "with", "value"]
type_list = ["integer", "string"]
id_list = []
val_list = ["double-quote"]
op_list = []
eol = "semicolon"
open_blk = "open-curly-brace"
close_blk = "close-curly-brace"

def lex_error(error_msg):
    print(error_msg)
    exit(0)

def remove_comments(source_string):
    comment_locations = [i for i in range(len(source_string)) if source_string.startswith("comment", i)]
    tmp_locs = iter(comment_locations)
    comment_locations = list(zip(tmp_locs, tmp_locs))
    comment_locations.reverse()
    for comment in comment_locations:
        source_string = source_string[:comment[0]] + source_string[comment[1]+7:]
    return source_string

def remove_excess_whitespace(source_string):
    # Remove string values
    string_locations = [i for i in range(len(source_string)) if source_string.startswith("double-quote", i)]
    tmp_locs = iter(string_locations)
    string_locations = list(zip(tmp_locs, tmp_locs))
    string_locations.reverse()
    string_values = []
    for string in string_locations:
        string_values.append(source_string[string[0]+12:string[1]])
        source_string = source_string[:string[0]+13] + source_string[string[1]:]

    # Remove excess whitespace
    source_string = ' '.join(source_string.split())

    # Replace string values
    string_locations = [i for i in range(len(source_string)) if source_string.startswith("double-quote", i)]
    tmp_locs = iter(string_locations)
    string_locations = list(zip(tmp_locs, tmp_locs))
    string_locations.reverse()
    for loc, value in zip(string_locations, string_values):
        start_index = loc[0] + 12
        source_string = source_string[:start_index] + value + source_string[start_index+1:]
    return source_string

def pop_next_element(source_string):
    tmp_list = source_string.split(' ')
    tmp_elem = tmp_list[0]
    source_string = ' '.join(tmp_list[1:])
    return (tmp_elem, source_string)

def get_string_value(source_string):
    end_index = source_string.find("double-quote")
    string_val = source_string[:end_index-1]
    source_string = source_string[end_index+13:]
    return (string_val, source_string)

def get_list_value(source_string):
    end_index = source_string.find("close-square-bracket")
    list_source = source_string[:end_index]
    list_val = []
    while list_source:
        list_item, list_source = pop_next_value(list_source)
        list_val.append(list_item)
    source_string = source_string[end_index+21:]
    return (list_val, source_string)

def get_dict_value(source_string):
    end_index = source_string.find("close-curly-brace")
    dict_source = source_string[:end_index]
    dict_val = {}
    while dict_source:
        dict_item_key, dict_item_val, dict_source = pop_next_pair(dict_source)
        dict_val[dict_item_key] = dict_item_val
    source_string = source_string[end_index+18:]
    return (dict_val, source_string)

def get_struct_fields(source_string):
    tmp_tokens = []
    
    while(source_string):
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "close-curly-brace"):
            tmp_tokens.append(("kw", tmp_elem))
            return (tmp_tokens, source_string)
        elif(tmp_elem == "field"):
            tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "named"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                tmp_tokens.append(("id", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "of"):
                    #tmp_tokens.append(("kw", "of"))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "type"):
                        #tmp_tokens.append(("kw", "type"))
                        tmp_elem, source_string = pop_next_element(source_string)
                        tmp_tokens.append(("type", tmp_elem))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == eol):
                            tmp_tokens.append(("kw", eol))
                        else:
                            lex_error("Error 5_1: Expected EOL.")
                    else:
                        lex_error("Error 5_2: Expected type.")
                else:
                    lex_error("Error 5_3: Expected of.")
            else:
                lex_error("Error 5_4: Expected named.")
        else:
            lex_error("Error 5_5: Expected field or close-curly-brace.")

def pop_next_value(source_string):
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "double-quote"): # Handle strings
        return get_string_value(source_string)
    elif(tmp_elem == "open-square-bracket"): # Handle lists
        return get_list_value(source_string)
    elif(tmp_elem == "open-curly-brace"): # Handle dicts
        return get_dict_value(source_string)
    else:
        if(tmp_elem == "true"): # Handle boolean True
            return (True, source_string)
        elif(tmp_elem == "false"): # Handle boolean False
            return (False, source_string)
        else: # Handle Numbers or identifiers
            if is_valid_number(tmp_elem):
                #check_valid_number(tmp_elem)
                num_val = convert_text_to_num(tmp_elem)
                return (num_val, source_string)
            else:
                return (("id", tmp_elem), source_string)

def pop_next_val_exp(source_string): #what is a val exp and when would it end? 2 ids?
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "double-quote"): # Handle strings
        return get_string_value(source_string)
    elif(tmp_elem == "open-square-bracket"): # Handle lists
        return get_list_value(source_string)
    elif(tmp_elem == "open-curly-brace"): # Handle dicts
        return get_dict_value(source_string)
    else:
        if(tmp_elem == "true"): # Handle boolean True
            return (True, source_string)
        elif(tmp_elem == "false"): # Handle boolean False
            return (False, source_string)
        else: # Handle Numbers or identifiers
            if is_valid_number(tmp_elem):
                #check_valid_number(tmp_elem)
                num_val = convert_text_to_num(tmp_elem)
                return (num_val, source_string)
            else:
                return (("id", tmp_elem), source_string)

"""
val
counter
counter op val
val op val
val op counter
counter op counter
val op val op val
"""

def pop_next_pair(source_string):
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "key"):
        tmp_key, source_string = pop_next_value(source_string)
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "value"):
            tmp_value, source_string = pop_next_value(source_string)
        else:
            lex_error("Error 22_2: Expected value.")
    else:
        lex_error("Error 22_1: Expected key.")
    return(tmp_key, tmp_value, source_string)

def get_all_elements(source_string):
    tmp_elements = []
    while(source_string):
        tmp_elem, source_string = pop_next_element(source_string)
        tmp_elements.append(tmp_elem)
    return tmp_elements

op_list = [
    "and",
    "or",
    "not",
    "is equal to",
    "is greater than",
    "is less than",
    "plus",
    "minus",
    "times",
    "divides"
]
# end_string = "run"
# source_string = "number_six is greater than six and true run the fo"
def pop_val_exp(source_string, end_string):
    tmp_tokens = []
    end_index = source_string.find(end_string)
    exp_string = source_string[:end_index]
    source_string = source_string[end_index:]

    while(exp_string):
        tmp_elem, exp_string = pop_next_element(exp_string)
        if(tmp_elem == "and" or tmp_elem == "or" or tmp_elem == "not" or tmp_elem == "plus" or tmp_elem == "minus" or tmp_elem == "times" or tmp_elem == "divides"):
            tmp_tokens.append(("op", tmp_elem))
        elif(tmp_elem == "is"):
            tmp_elem, exp_string = pop_next_element(exp_string)
            if(tmp_elem == "equal"):
                tmp_elem, exp_string = pop_next_element(exp_string)
                if(tmp_elem == "to"):
                    tmp_tokens.append(("op", "is equal to"))
                else:
                    lex_error("")
            elif(tmp_elem == "greater"):
                tmp_elem, exp_string = pop_next_element(exp_string)
                if(tmp_elem == "than"):
                    tmp_tokens.append(("op", "is greater than"))
                else:
                    lex_error("")
            elif(tmp_elem == "less"):
                tmp_elem, exp_string = pop_next_element(exp_string)
                if(tmp_elem == "than"):
                    tmp_tokens.append(("op", "is less than"))
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            if(is_valid_number(tmp_elem)):
                num_val = convert_text_to_num(tmp_elem)
                tmp_tokens.append(("val", num_val))
            elif(tmp_elem == "true" or tmp_elem == "false"):
                if tmp_elem == "true":
                    tmp_tokens.append(("val", True))
                else:
                    tmp_tokens.append(("val", False))
            elif(tmp_elem == "double-quote"):
                str_val, exp_string = get_string_value(exp_string)
                tmp_tokens.append(("val", str_val))
            elif(tmp_elem == "open-square-bracket"):
                list_val, exp_string = get_list_value(exp_string)
                tmp_tokens.append(("val", list_val))
            elif(tmp_elem == "open-curly-brace"):
                dict_val, exp_string = get_dict_value(exp_string)
                tmp_tokens.append(("val", dict_val))
            else:
                tmp_tokens.append(("id", tmp_elem))
    return(tmp_tokens, source_string)

valid_num_parts = {
    "dot": None,
    "negative": -1,
    "zero": 0,
    "one": 1, 
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "fourty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
    "thousand": 1000,
    "million": 1000000,
    "billion": 1000000000
}

def check_valid_number(num_str):
    num_parts = num_str.split("-")
    for part in num_parts:
        if part not in valid_num_parts.keys():
            lex_error("Invalid Number: {}".format(num_str))

def is_valid_number(num_str):
    num_parts = num_str.split("-")
    for part in num_parts:
        if part not in valid_num_parts.keys():
            return False
    return True

def convert_text_to_num(num_str):
    num_parts = num_str.split("-")
    final_change = 1
    in_dec = False
    cur_num = 0
    cnt = 0
    cnt2 = 0.1
    num_decimal_parts = 0
    if len(num_parts) < 2:
        return valid_num_parts[num_parts[0]]
    for part in num_parts:
        if part == "negative":
            final_change = -1
            cnt += 1
        elif cnt+1 == len(num_parts):
            cur_num += valid_num_parts[part]
            cnt += 1
        elif part == "hundred" or part == "thousand" or part == "million" or part == "billion":
            continue
        elif num_parts[cnt+1] == "hundred" or num_parts[cnt+1] == "thousand" or num_parts[cnt+1] == "million" or num_parts[cnt+1] == "billion":
            cur_num += valid_num_parts[part] * valid_num_parts[num_parts[cnt+1]]
            cnt += 2
        elif part == "dot":
            in_dec = True
            dot_index = num_parts.index("dot")
            num_decimal_parts = len(num_parts[dot_index+1:])
        elif in_dec:
            cur_num += valid_num_parts[part] * cnt2
            cnt += 1
            cnt2 *= 0.1
        else:
            cur_num += valid_num_parts[part]
            cnt += 1
    cur_num *= final_change
    if in_dec:
        cur_num = round(cur_num, num_decimal_parts)
    return cur_num

def kw_retrieve(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "retrieve"))
    tmp_elem, source_string = pop_next_element(source_string)
    
    if(tmp_elem == "source"):
        #tmp_tokens.append(("kw", "source"))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "from"):
            #tmp_tokens.append(("kw", "from"))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "file"):
                #tmp_tokens.append(("kw", "file"))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "named"):
                    #tmp_tokens.append(("kw", "named"))
                    tmp_elem, source_string = pop_next_element(source_string)
                    tmp_tokens.append(("id", tmp_elem))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == eol):
                        tmp_tokens.append(("kw", eol))
                    else:
                        lex_error("Error 1_1: Expected EOL.")
                else:
                    lex_error("Error 1_2: Expected named.")
            else:
                lex_error("Error 1_3: Expected file.")
        else:
            lex_error("Error 1_4: Expected from.")
    else:
        lex_error("Error 1_5: Expected source.")

    return tmp_tokens, source_string

def kw_declare(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "declare"))
    tmp_elem, source_string = pop_next_element(source_string)

    if(tmp_elem == "nonchangeable" or tmp_elem == "changeable"):
        if(tmp_elem == "nonchangeable"):
            tmp_tokens.append(("kw", "nonchangeable"))
        else:
            tmp_tokens.append(("kw", "changeable"))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "construct"):
            #tmp_tokens.append(("kw", "construct"))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "named"):
                #tmp_tokens.append(("kw", "named"))
                tmp_elem, source_string = pop_next_element(source_string)
                tmp_tokens.append(("id", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "of"):
                    #tmp_tokens.append(("kw", "of"))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "type"):
                        #tmp_tokens.append(("kw", "type"))
                        tmp_elem, source_string = pop_next_element(source_string)
                        tmp_tokens.append(("type", tmp_elem))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == eol):
                            tmp_tokens.append(("kw", eol))
                        elif(tmp_elem == "with"):
                            #tmp_tokens.append(("kw", "with"))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "value"):
                                #tmp_tokens.append(("kw", "value"))
                                tmp_val, source_string = pop_next_value(source_string)
                                tmp_tokens.append(("val", tmp_val))
                                tmp_elem, source_string = pop_next_element(source_string)
                                if(tmp_elem == eol):
                                    tmp_tokens.append(("kw", eol))
                                else:
                                    lex_error("Error 1: Expected EOL.")
                            else:
                                lex_error("Error 2: Expected value.")
                        else:
                            lex_error("Error 3: Expected EOL or with.")
                    else:
                        lex_error("Error 4: Expected type.")
                else:
                    lex_error("Error 5: Expected of.")
            else:
                lex_error("Error 6: Expected named.")
        else:
            lex_error("Error 7: Expected construct.")
    elif(tmp_elem == "functional"):
        tmp_tokens.append(("kw", "functional"))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "construct"):
            #tmp_tokens.append(("kw", "construct"))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "named"):
                #tmp_tokens.append(("kw", "named"))
                tmp_elem, source_string = pop_next_element(source_string)
                tmp_tokens.append(("id", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "which"):
                    #tmp_tokens.append(("kw", "which"))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "returns"):
                        tmp_tokens.append(("kw", "returns"))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == "type"):
                            #tmp_tokens.append(("kw", "type"))
                            tmp_elem, source_string = pop_next_element(source_string)
                            tmp_tokens.append(("type", tmp_elem))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "and"):
                                #tmp_tokens.append(("kw", "and"))
                                tmp_elem, source_string = pop_next_element(source_string)
                                if(tmp_elem == "receives"):
                                    tmp_tokens.append(("kw", "receives"))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    while(tmp_elem != "open-curly-brace"):
                                        if(tmp_elem == "type"):
                                            #tmp_tokens.append(("kw", "type"))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                            tmp_tokens.append(("type", tmp_elem))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        elif(tmp_elem == "and"):
                                            #tmp_tokens.append(("kw", "and"))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        elif(tmp_elem == "nothing"):
                                            tmp_tokens.append(("type", "nothing"))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        else:
                                            lex_error("Error 8: Expected type or nothing.")
                                    if(tmp_elem == "open-curly-brace"):
                                        tmp_tokens.append(("kw", "open-curly-brace"))
                                    else:
                                        lex_error("Error 9: Expected open-curly-brace.")
                                else:
                                    lex_error("Error 10: Expected receives.")
                            else:
                                lex_error("Error 11: Expected and.")
                        elif(tmp_elem == "nothing"):
                            tmp_tokens.append(("type", "nothing"))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "and"):
                                #tmp_tokens.append(("kw", "and"))
                                tmp_elem, source_string = pop_next_element(source_string)
                                if(tmp_elem == "receives"):
                                    tmp_tokens.append(("kw", "receives"))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    while(tmp_elem != "open-curly-brace"):
                                        if(tmp_elem == "type"):
                                            #tmp_tokens.append(("kw", "type"))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                            tmp_tokens.append(("type", tmp_elem))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        elif(tmp_elem == "and"):
                                            #tmp_tokens.append(("kw", "and"))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        elif(tmp_elem == "nothing"):
                                            tmp_tokens.append(("type", "nothing"))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        else:
                                            lex_error("Error 12: Expected type or nothing.")
                                    if(tmp_elem == "open-curly-brace"):
                                        tmp_tokens.append(("kw", "open-curly-brace"))
                                    else:
                                        lex_error("Error 13: Expected open-curly-brace.")
                                else:
                                    lex_error("Error 14: Expected receives.")
                            else:
                                lex_error("Error 15: Expected and.")
                        else:
                            lex_error("Error 16: Expected type or nothing.")
                    else:
                        lex_error("Error 17: Expected returns.")
                else:
                    lex_error("Error 18: Expected which.")
            else:
                lex_error("Error 19: Expected named.")
        else:
            lex_error("Error 20: Expected construct.")
    elif(tmp_elem == "structure"):
        tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "named"):
            #tmp_tokens.append(("kw", "named"))
            tmp_elem, source_string = pop_next_element(source_string)
            tmp_tokens.append(("id", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "open-curly-brace"):
                tmp_tokens.append(("kw", "open-curly-brace"))
                struct_tokens, source_string = get_struct_fields(source_string)
                tmp_tokens += struct_tokens
            else:
                lex_error("Error 99: Expected open-curly-brace.")
        else:
            lex_error("Error 98: Expected named.")
    else:
        lex_error("Error 21: Expected changeable, nonchangeable, or functional.")

    return (tmp_tokens, source_string)

def kw_set(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "set"))
    tmp_elem, source_string = pop_next_element(source_string)
    
    if(tmp_elem == "construct"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "named"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            tmp_tokens.append(("id", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "with"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "value"):
                    exp_tokens, source_string = pop_val_exp(source_string, eol)
                    tmp_tokens += exp_tokens
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == eol):
                        tmp_tokens.append(("kw", eol))
                    else:
                        lex_error("Error 3_1: Expected EOL.")
                else:
                    lex_error("Error 3_2: Expected named.")
            else:
                lex_error("Error 3_3: Expected file.")
        else:
            lex_error("Error 3_4: Expected from.")
    elif(tmp_elem == "field"):
        tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "named"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            tmp_tokens.append(("id", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "of"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "construct"):
                    #tmp_tokens.append(("kw", tmp_elem))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "named"):
                        #tmp_tokens.append(("kw", tmp_elem))
                        tmp_elem, source_string = pop_next_element(source_string)
                        tmp_tokens.append(("id", tmp_elem))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == "with"):
                            #tmp_tokens.append(("kw", tmp_elem))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "value"):
                                #tmp_tokens.append(("kw", tmp_elem))
                                if(source_string[:4] == "from"):
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    #tmp_tokens.append(("kw", "from"))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    if(tmp_elem == "construct"):
                                        #tmp_tokens.append(("kw", tmp_elem))
                                        tmp_elem, source_string = pop_next_element(source_string)
                                        if(tmp_elem == "named"):
                                            #tmp_tokens.append(("kw", tmp_elem))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                            tmp_tokens.append(("id", tmp_elem))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                        else:
                                            lex_error("Error 3_6: Expected named.")
                                    else:
                                        lex_error("Error 3_7: Expected construct.")
                                else:
                                    tmp_val, source_string = pop_next_value(source_string)
                                    tmp_tokens.append(("val", tmp_val))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                if(tmp_elem == eol):
                                    tmp_tokens.append(("kw", eol))
                                else:
                                    lex_error("Error")
                            else:
                                lex_error("Error")
                        else:
                            lex_error("Error")
                    else:
                        lex_error("Error")
                else:
                    lex_error("Error")
            else:
                lex_error("Error")
        else:
            lex_error("Error")
    else:
        lex_error("Error 3_5: Expected source.")
    return (tmp_tokens, source_string)

def kw_close_block(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "close-curly-brace"))

    return (tmp_tokens, source_string)

def kw_call(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "call"))
    tmp_elem, source_string = pop_next_element(source_string)

    if(tmp_elem == "functional"):
        tmp_tokens.append(("kw", "functional"))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "construct"):
            #tmp_tokens.append(("kw", "construct"))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "named"):
                #tmp_tokens.append(("kw", "named"))
                tmp_elem, source_string = pop_next_element(source_string)
                tmp_tokens.append(("id", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "and"):
                    #tmp_tokens.append(("kw", "and"))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "pass"):
                        tmp_tokens.append(("kw", "pass"))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == "in"):
                            #tmp_tokens.append(("kw", "in"))
                            #tmp_elem, source_string = pop_next_element(source_string)
                            while(not (tmp_elem == "return" or tmp_elem == eol)):
                                #print("bibiddy babiddy booo")
                                #print(tmp_elem)
                                #print(source_string[:30])
                                tmp_val, source_string = pop_next_value(source_string)
                                #tmp_val_tokens, source_string = pop_next_val_exp(source_string)
                        
                                #print("yo yo yo")
                                #print(tmp_val)
                                if type(tmp_val) is tuple:
                                    tmp_tokens.append(("id", tmp_val[1]))
                                else:
                                    tmp_tokens.append(("val", tmp_val))
                                
                                #tmp_tokens += tmp_val_tokens
                                tmp_elem, source_string = pop_next_element(source_string)
                                #print("yeet yeet")
                                #print(tmp_elem)
                                if(tmp_elem == "and"):
                                    #print("positive yeeting")
                                    tmp_tokens.append(("kw", tmp_elem))
                                    #tmp_elem, source_string = pop_next_element(source_string)
                                    #print("end of positive yeeting")
                                    #print(tmp_elem)
                                    tmp_source_string = source_string
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    source_string = tmp_source_string
                            #print("WHAT IF HIS FINGER PRINTS CAN TOO?")
                            #print(tmp_elem)
                            #print(source_string[:30])
                            if tmp_tokens[-1] == ("kw", "and"):
                                tmp_tokens.pop()
                            #print("YUMMY")
                            #print(tmp_tokens)
                            #print(source_string[:30])
                            #print("END YUMMY")
                            if(tmp_elem == eol):
                                tmp_tokens.append(("kw", eol))
                            elif(tmp_elem == "return"):
                                tmp_elem, source_string = pop_next_element(source_string)
                                #print("######################")
                                #print(tmp_elem)
                                #print(tmp_tokens)
                                #print(source_string[:30])
                                #print("######################")
                                #print("RETURN IS HERE")
                                tmp_tokens.append(("kw", "return"))
                                tmp_elem, source_string = pop_next_element(source_string)
                                #print("************************")
                                #print(tmp_elem)
                                #print(tmp_tokens)
                                #print(source_string[:30])
                                #print("************************")
                                if(tmp_elem == "value"):
                                    #print("VALUE IS HERE")
                                    #tmp_tokens.append(("kw", tmp_elem))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    if(tmp_elem == "to"):
                                        #tmp_tokens.append(("kw", tmp_elem))
                                        tmp_elem, source_string = pop_next_element(source_string)
                                        if(tmp_elem == "construct"):
                                            #tmp_tokens.append(("kw", tmp_elem))
                                            tmp_elem, source_string = pop_next_element(source_string)
                                            if(tmp_elem == "named"):
                                                #tmp_tokens.append(("kw", "named"))
                                                tmp_elem, source_string = pop_next_element(source_string)
                                                tmp_tokens.append(("id", tmp_elem))
                                                tmp_elem, source_string = pop_next_element(source_string)
                                                if(tmp_elem == eol):
                                                    tmp_tokens.append(("kw", tmp_elem))
                                                else:
                                                    lex_error("Error 22: Expected EOL.")
                                            else:
                                                lex_error("Error 23: Expected named.")
                                        else:
                                            lex_error("Error 24: Expected construct.")
                                    else:
                                        lex_error("Error 25: Expected to.")
                                else:
                                    lex_error("Error 26: Expected value.")
                            else:
                                lex_error("Error 27: Expected EOL or return.")
                        else:
                            lex_error("Error 28: Expected in.")
                    elif(tmp_elem == "return"):
                        tmp_tokens.append(("kw", "return"))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == "value"):
                            #tmp_tokens.append(("kw", tmp_elem))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "to"):
                                #tmp_tokens.append(("kw", tmp_elem))
                                tmp_elem, source_string = pop_next_element(source_string)
                                if(tmp_elem == "construct"):
                                    #tmp_tokens.append(("kw", tmp_elem))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    if(tmp_elem == "named"):
                                        #tmp_tokens.append(("kw", "named"))
                                        tmp_elem, source_string = pop_next_element(source_string)
                                        tmp_tokens.append(("id", tmp_elem))
                                        tmp_elem, source_string = pop_next_element(source_string)
                                        if(tmp_elem == eol):
                                            tmp_tokens.append(("kw", tmp_elem))
                                        else:
                                            lex_error("Error 29: Expected EOL.")
                                    else:
                                        lex_error("Error 30: Expected named.")
                                else:
                                    lex_error("Error 31: Expected construct.")
                            else:
                                lex_error("Error 32: Expected to.")
                        else:
                            lex_error("Error 33: Expected value.")
                    else:
                        lex_error("Error 34: Expected pass or return.")
                elif(tmp_elem == eol):
                    tmp_tokens.append(("kw", tmp_elem))
                else:
                    lex_error("Error 35: Expected EOL or and.")
            else:
                lex_error("Error 36: Expected named.")
        else:
            lex_error("Error 37: Expected construct.")
    else:
        lex_error("Error 38: Expected functional.")
    return (tmp_tokens, source_string)

def kw_while(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "while"))
    exp_tokens, source_string = pop_val_exp(source_string, "run")
    tmp_tokens += exp_tokens
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "run"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "the"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "following"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "open-curly-brace"):
                    tmp_tokens.append(("kw", tmp_elem))
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_break(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "break"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "out"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "of"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "loop"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == eol):
                    tmp_tokens.append(("kw", tmp_elem))
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_jump(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "jump"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "to"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "next"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "iteration"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == eol):
                    tmp_tokens.append(("kw", tmp_elem))
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_for(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "for"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "every"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "item"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "in"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "the"):
                    #tmp_tokens.append(("kw", tmp_elem))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "construct"):
                        #tmp_tokens.append(("kw", tmp_elem))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == "named"):
                            #tmp_tokens.append(("kw", "named"))
                            tmp_elem, source_string = pop_next_element(source_string)
                            tmp_tokens.append(("id", tmp_elem))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "do"):
                                #tmp_tokens.append(("kw", tmp_elem))
                                tmp_elem, source_string = pop_next_element(source_string)
                                if(tmp_elem == "the"):
                                    #tmp_tokens.append(("kw", tmp_elem))
                                    tmp_elem, source_string = pop_next_element(source_string)
                                    if(tmp_elem == "following"):
                                        #tmp_tokens.append(("kw", tmp_elem))
                                        tmp_elem, source_string = pop_next_element(source_string)
                                        if(tmp_elem == "open-curly-brace"):
                                            tmp_tokens.append(("kw", tmp_elem))
                                        else:
                                            lex_error("")
                                    else:
                                        lex_error("")
                                else:
                                    lex_error("")
                            else:
                                lex_error("")
                        else:
                            lex_error("")
                    else:
                        lex_error("")
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_return(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "return"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "value"):
        exp_tokens, source_string = pop_val_exp(source_string, eol)
        tmp_tokens += exp_tokens
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == eol):
            tmp_tokens.append(("kw", eol))
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_if(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "if"))

    exp_tokens, source_string = pop_val_exp(source_string, "run")
    tmp_tokens += exp_tokens

    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "run"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "the"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "following"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "open-curly-brace"):
                    tmp_tokens.append(("kw", tmp_elem))
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_or(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "or"))

    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "if"):
        tmp_tokens.append(("kw", tmp_elem))
        #print("$$$$$$$$$$$$$$$$$$")
        #print(source_string[:50])
        #print("##################")
        exp_tokens, source_string = pop_val_exp(source_string, "run")
        #print(exp_tokens)
        #print("******************")
        tmp_tokens += exp_tokens
        tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "run"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "the"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "following"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "open-curly-brace"):
                    tmp_tokens.append(("kw", tmp_elem))
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_try(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "try"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "to"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "run"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "the"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "following"):
                    #tmp_tokens.append(("kw", tmp_elem))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "open-curly-brace"):
                        tmp_tokens.append(("kw", tmp_elem))
                    else:
                        lex_error("")
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_catch(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "catch"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "error"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == "named"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            tmp_tokens.append(("id", tmp_elem))
            tmp_elem, source_string = pop_next_element(source_string)
            if(tmp_elem == "and"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string = pop_next_element(source_string)
                if(tmp_elem == "run"):
                    #tmp_tokens.append(("kw", tmp_elem))
                    tmp_elem, source_string = pop_next_element(source_string)
                    if(tmp_elem == "the"):
                        #tmp_tokens.append(("kw", tmp_elem))
                        tmp_elem, source_string = pop_next_element(source_string)
                        if(tmp_elem == "following"):
                            #tmp_tokens.append(("kw", tmp_elem))
                            tmp_elem, source_string = pop_next_element(source_string)
                            if(tmp_elem == "open-curly-brace"):
                                tmp_tokens.append(("kw", tmp_elem))
                            else:
                                lex_error("")
                        else:
                            lex_error("")
                    else:
                        lex_error("")
                else:
                    lex_error("")
            else:
                lex_error("")
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_assert(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "assert"))
    tmp_elem, source_string = pop_next_element(source_string)
    if(tmp_elem == "that"):
        #tmp_tokens.append(("kw", tmp_elem))
        exp_tokens, source_string = pop_val_exp(source_string, eol)
        tmp_tokens += exp_tokens
        tmp_elem, source_string = pop_next_element(source_string)
        if(tmp_elem == eol):
            tmp_tokens.append(("kw", eol))
        else:
            lex_error("")
    else:
        lex_error("")
    return (tmp_tokens, source_string)

def kw_exit(source_string):
    tmp_tokens = []
    tmp_tokens.append(("kw", "exit"))
    return (tmp_tokens, source_string)

def create_token_list(source_string):
    token_list = []
    while(source_string):
        tmp_elem, source_string = pop_next_element(source_string)
        switch = {
            "retrieve": kw_retrieve,
            "declare": kw_declare,
            "set": kw_set,
            "close-curly-brace": kw_close_block,
            "call": kw_call,
            "while": kw_while,
            "break": kw_break,
            "jump": kw_jump,
            "for": kw_for,
            "return": kw_return,
            "if": kw_if,
            "or": kw_or,
            "try": kw_try,
            "catch": kw_catch,
            "assert": kw_assert,
            "exit": kw_exit
        }
        tmp_tokens, source_string = switch.get(tmp_elem)(source_string)
        token_list += tmp_tokens
    return token_list

def print_tokens(token_list):
    print("Tokens:")
    for token in token_list:
        print(token)

def format_token_output(token_list):
    output_str = ""
    output_str += "Tokens:\n"
    for token in token_list:
        output_str += str(token) + "\n"
    return output_str

def lex(source_string):
    source_string = remove_comments(source_string)
    source_string = remove_excess_whitespace(source_string)
    token_list = create_token_list(source_string)
    return token_list