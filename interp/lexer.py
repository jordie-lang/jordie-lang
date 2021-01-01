"""
jordie-lang lexer

"""

from pprint import pprint

kw_list = ["declare", "nonchangeable", "functional", "changeable", "construct", "named", "of", "type", "with", "value"]
type_list = ["integer", "string"]
id_list = []
val_list = ["double-quote"]
op_list = []
eol = "semicolon"
open_blk = "open-curly-brace"
close_blk = "close-curly-brace"

def lex_error(ln, ecc, error_msg):
    print(f"syntax error ({ln},{ecc}): {error_msg}.")
    exit(0)

def pop_next_element(s, ln, cc):
    tmp_elem = ""
    ecc = cc
    
    while(s):
        if (s[0] == "\n" or s[0] == "\r" or s[0] == "\n\r" or s[0] == "\r\n") and tmp_elem == "":
            # add to newline count, reset character count
            ln += 1
            cc = 1
            ecc = 1
        elif (s[0] == "\n" or s[0] == "\r" or s[0] == "\n\r" or s[0] == "\r\n") and tmp_elem != "":
            break
        elif s[0] == " " and tmp_elem == "":
            cc += 1
            ecc += 1
        elif s[0] == " ":
            # end of element, return new element
            cc += 1
            s = s[1:]
            break
        else:
            tmp_elem += s[0]
            cc += 1
        s = s[1:]
    
    return (tmp_elem, s, ln, cc, ecc)

def get_string_value(source_string, ln, cc):
    ecc = cc
    end_index = source_string.find("double-quote")
    if end_index == 0:
        string_val = ""
    else:
        string_val = source_string[:end_index-1]
    source_string = source_string[end_index+13:]
    cc += end_index + 13
    return (string_val, source_string, ln, cc, ecc)

def get_list_value(source_string, ln, cc):
    end_index = source_string.find("close-square-bracket")
    list_source = source_string[:end_index]
    list_val = []
    while list_source:
        list_item, list_source, ln, cc, ecc = pop_next_value(list_source, ln, cc)
        list_val.append(list_item)
    source_string = source_string[end_index+21:]
    cc += end_index + 21
    return (list_val, source_string, ln, cc, ecc)

def get_dict_value(source_string, ln, cc):
    ecc = cc
    end_index = source_string.find("close-curly-brace")
    dict_source = source_string[:end_index]
    dict_val = {}
    while dict_source:
        dict_item_key, dict_item_val, dict_source, ln, cc = pop_next_pair(dict_source, ln, cc)
        dict_val[dict_item_key] = dict_item_val
    source_string = source_string[end_index+18:]
    cc += end_index + 18
    return (dict_val, source_string, ln, cc, ecc)

def get_struct_fields(source_string, ln, cc):
    tmp_tokens = []
    
    while(source_string):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "close-curly-brace"):
            tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
            return (tmp_tokens, source_string, ln, cc, ecc)
        elif(tmp_elem == "field"):
            tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "named"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "of"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "type"):
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        tmp_tokens.append(("type", tmp_elem, f"{ln},{ecc}"))
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == eol):
                            tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'type'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'of'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'field' or 'close-curly-brace'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def pop_next_value(source_string, ln, cc):
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "double-quote"): # Handle strings
        return get_string_value(source_string, ln, cc)
    elif(tmp_elem == "open-square-bracket"): # Handle lists
        return get_list_value(source_string, ln, cc)
    elif(tmp_elem == "open-curly-brace"): # Handle dicts
        return get_dict_value(source_string, ln, cc)
    else:
        if(tmp_elem == "true"): # Handle boolean True
            return (True, source_string, ln, cc, ecc)
        elif(tmp_elem == "false"): # Handle boolean False
            return (False, source_string, ln, cc, ecc)
        else: # Handle Numbers or identifiers
            if is_valid_number(tmp_elem):
                num_val = convert_text_to_num(tmp_elem)
                return (num_val, source_string, ln, cc, ecc)
            else:
                return (("id", tmp_elem), source_string, ln, cc, ecc)

"""
val
counter
counter op val
val op val
val op counter
counter op counter
val op val op val
"""

def pop_next_pair(source_string, ln, cc):
    _cc = cc
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "key"):
        tmp_key, source_string, ln, cc, ecc = pop_next_value(source_string, ln, cc)
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "value"):
            tmp_value, source_string, ln, cc, _cc = pop_next_value(source_string, ln, cc)
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'value'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'key'")
    return(tmp_key, tmp_value, source_string, ln, ecc)

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
# source_string = "number_six is greater than six and true then run the fo"
def pop_val_exp(source_string, end_string, ln, cc):
    tmp_tokens = []
    end_index = source_string.find(end_string)
    exp_string = source_string[:end_index]
    source_string = source_string[end_index:]

    while(exp_string):
        tmp_elem, exp_string, ln, cc, ecc = pop_next_element(exp_string, ln, cc)
        if(tmp_elem == "and" or tmp_elem == "or" or tmp_elem == "not" or tmp_elem == "plus" or tmp_elem == "minus" or tmp_elem == "times" or tmp_elem == "divides"):
            tmp_tokens.append(("op", tmp_elem, f"{ln},{ecc}"))
        elif(tmp_elem == "is"):
            tmp_elem, exp_string, ln, cc, ecc = pop_next_element(exp_string, ln, cc)
            if(tmp_elem == "equal"):
                tmp_elem, exp_string, ln, cc, ecc = pop_next_element(exp_string, ln, cc)
                if(tmp_elem == "to"):
                    tmp_tokens.append(("op", "is equal to", f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'to'")
            elif(tmp_elem == "greater"):
                tmp_elem, exp_string, ln, cc, ecc = pop_next_element(exp_string, ln, cc)
                if(tmp_elem == "than"):
                    tmp_tokens.append(("op", "is greater than", f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'than'")
            elif(tmp_elem == "less"):
                tmp_elem, exp_string, ln, cc, ecc = pop_next_element(exp_string, ln, cc)
                if(tmp_elem == "than"):
                    tmp_tokens.append(("op", "is less than", f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'than'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'equal', 'greater', or 'less'")
        else:
            if(is_valid_number(tmp_elem)):
                num_val = convert_text_to_num(tmp_elem)
                tmp_tokens.append(("val", num_val, f"{ln},{ecc}"))
            elif(tmp_elem == "true" or tmp_elem == "false"):
                if tmp_elem == "true":
                    tmp_tokens.append(("val", True, f"{ln},{ecc}"))
                else:
                    tmp_tokens.append(("val", False, f"{ln},{ecc}"))
            elif(tmp_elem == "double-quote"):
                str_val, exp_string, ln, cc, ecc = get_string_value(exp_string, ln, cc)
                tmp_tokens.append(("val", str_val, f"{ln},{ecc}"))
            elif(tmp_elem == "open-square-bracket"):
                list_val, exp_string, ln, cc, ecc = get_list_value(exp_string, ln, cc)
                tmp_tokens.append(("val", list_val, f"{ln},{ecc}"))
            elif(tmp_elem == "open-curly-brace"):
                dict_val, exp_string, ln, cc, ecc = get_dict_value(exp_string, ln, cc)
                tmp_tokens.append(("val", dict_val, f"{ln},{ecc}"))
            else:
                tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
    return(tmp_tokens, source_string, ln, cc, ecc)

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

def kw_retrieve(source_string, ln, cc, ecc):
    #print("kw_retrieve")
    tmp_tokens = []
    tmp_tokens.append(("kw", "retrieve", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    
    if(tmp_elem == "source"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "from"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "file"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "named"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == eol):
                        tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'file'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'from'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'source'")

    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_declare(source_string, ln, cc, ecc):
    #print("kw_declare")
    tmp_tokens = []
    tmp_tokens.append(("kw", "declare", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)

    if(tmp_elem == "nonchangeable" or tmp_elem == "changeable"):
        if(tmp_elem == "nonchangeable"):
            tmp_tokens.append(("kw", "nonchangeable", f"{ln},{ecc}"))
        else:
            tmp_tokens.append(("kw", "changeable", f"{ln},{ecc}"))
        
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "construct"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "named"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "of"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "type"):
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        tmp_tokens.append(("type", tmp_elem, f"{ln},{ecc}"))
                        
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == eol):
                            tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                        elif(tmp_elem == "with"):
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "value"):
                                tmp_val, source_string, ln, cc, ecc = pop_next_value(source_string, ln, cc)
                                tmp_tokens.append(("val", tmp_val, f"{ln},{ecc}"))
                                
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                
                                if(tmp_elem == eol):
                                    tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'value'")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon' or 'with'")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'type'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'of'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
    elif(tmp_elem == "functional"):
        tmp_tokens.append(("kw", "functional", f"{ln},{ecc}"))
        
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "construct"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "named"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "which"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "returns"):
                        tmp_tokens.append(("kw", "returns", f"{ln},{ecc}"))
                        
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == "type"):
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            tmp_tokens.append(("type", tmp_elem, f"{ln},{ecc}"))
                            
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "and"):
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                if(tmp_elem == "receives"):
                                    tmp_tokens.append(("kw", "receives", f"{ln},{ecc}"))
                                    
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    while(tmp_elem != "open-curly-brace"):
                                        if(tmp_elem == "type"):
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                            tmp_tokens.append(("type", tmp_elem, f"{ln},{ecc}"))
                                            
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        elif(tmp_elem == "and"):
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        elif(tmp_elem == "nothing"):
                                            tmp_tokens.append(("type", "nothing", f"{ln},{ecc}"))
                                            
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        else:
                                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'type' or 'nothing'")
                                    if(tmp_elem == "open-curly-brace"):
                                        tmp_tokens.append(("kw", "open-curly-brace", f"{ln},{ecc}"))
                                    else:
                                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'receives'")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'and'")
                        elif(tmp_elem == "nothing"):
                            tmp_tokens.append(("type", "nothing", f"{ln},{ecc}"))
                            
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "and"):
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                if(tmp_elem == "receives"):
                                    tmp_tokens.append(("kw", "receives", f"{ln},{ecc}"))
                                    
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    while(tmp_elem != "open-curly-brace"):
                                        if(tmp_elem == "type"):
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                            tmp_tokens.append(("type", tmp_elem, f"{ln},{ecc}"))
                                            
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        elif(tmp_elem == "and"):
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        elif(tmp_elem == "nothing"):
                                            tmp_tokens.append(("type", "nothing", f"{ln},{ecc}"))
                                            
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        else:
                                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'type' or 'nothing'")
                                    if(tmp_elem == "open-curly-brace"):
                                        tmp_tokens.append(("kw", "open-curly-brace", f"{ln},{ecc}"))
                                    else:
                                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'receives'")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'and'")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'type' or 'nothing'")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'returns'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'which'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
    elif(tmp_elem == "structure"):
        tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
        
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "named"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
            
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "open-curly-brace"):
                tmp_tokens.append(("kw", "open-curly-brace", f"{ln},{ecc}"))
                
                struct_tokens, source_string, ln, cc, ecc = get_struct_fields(source_string, ln, cc)
                tmp_tokens += struct_tokens
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'changeable', 'nonchangeable', 'functional', or 'structure'")

    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_set(source_string, ln, cc, ecc):
    #print("kw_set")
    tmp_tokens = []
    tmp_tokens.append(("kw", "set", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    
    if(tmp_elem == "construct"):
        #tmp_tokens.append(("kw", tmp_elem))
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "named"):
            #tmp_tokens.append(("kw", tmp_elem))
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "with"):
                #tmp_tokens.append(("kw", tmp_elem))
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "value"):
                    exp_tokens, source_string, ln, cc, ecc = pop_val_exp(source_string, eol, ln, cc)
                    tmp_tokens += exp_tokens
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == eol):
                        tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'file'") #unsure what file means here
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'from'")
    elif(tmp_elem == "field"):
        tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "named"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "of"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "construct"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "named"):
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == "with"):
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "value"):
                                if(source_string[:4] == "from"):
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    if(tmp_elem == "construct"):
                                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        if(tmp_elem == "named"):
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                            tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        else:
                                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
                                    else:
                                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
                                else:
                                    tmp_val, source_string, ln, cc, ecc = pop_next_value(source_string, ln, cc)
                                    tmp_tokens.append(("val", tmp_val, f"{ln},{ecc}"))
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                if(tmp_elem == eol):
                                    tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected value")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'with'")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'of'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'source'") # not sure what source is here
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_close_block(source_string, ln, cc, ecc):
    #print("kw_close_block")
    tmp_tokens = []
    tmp_tokens.append(("kw", "close-curly-brace", f"{ln},{ecc}"))

    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_call(source_string, ln, cc, ecc):
    #print("kw_call")
    tmp_tokens = []
    tmp_tokens.append(("kw", "call", f"{ln},{ecc}"))
    
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)

    if(tmp_elem == "functional"):
        tmp_tokens.append(("kw", "functional", f"{ln},{ecc}"))
        
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "construct"):
            
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "named"):
                
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "and"):
                    
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "pass"):
                        tmp_tokens.append(("kw", "pass", f"{ln},{ecc}"))
                        
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == "in"):
                            while(not (tmp_elem == "return" or tmp_elem == eol)):
                                tmp_val, source_string, ln, cc, ecc = pop_next_value(source_string, ln, cc)
                        
                                
                                if type(tmp_val) is tuple:
                                    tmp_tokens.append(("id", tmp_val[1], f"{ln},{ecc}"))
                                else:
                                    tmp_tokens.append(("val", tmp_val, f"{ln},{ecc}"))
                                
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                
                                if(tmp_elem == "and"):
                                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                                    
                                    tmp_source_string = source_string
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    source_string = tmp_source_string
                            
                            if tmp_tokens[-1][1] == "and":
                                tmp_tokens.pop()
                            
                            if(tmp_elem == eol):
                                tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
                            elif(tmp_elem == "return"):
                                
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                
                                tmp_tokens.append(("kw", "return", f"{ln},{ecc}"))
                                
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                
                                if(tmp_elem == "value"):
                                    
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    if(tmp_elem == "to"):
                                        
                                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        if(tmp_elem == "construct"):
                                            
                                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                            if(tmp_elem == "named"):
                                                
                                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                                tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                                                
                                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                                if(tmp_elem == eol):
                                                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                                                else:
                                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                                            else:
                                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
                                        else:
                                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
                                    else:
                                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'to'")
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected value")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon' or 'return'")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'in'")
                    elif(tmp_elem == "return"):
                        tmp_tokens.append(("kw", "return", f"{ln},{ecc}"))
                        
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == "value"):
                            
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "to"):
                                
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                if(tmp_elem == "construct"):
                                    
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    if(tmp_elem == "named"):
                                        
                                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                                        
                                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        if(tmp_elem == eol):
                                            tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                                        else:
                                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
                                    else:
                                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'to'")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected value")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'pass' or 'return'")
                elif(tmp_elem == eol):
                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon' or 'and'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'functional'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_while(source_string, ln, cc, ecc):
    #print("kw_while")
    tmp_tokens = []
    tmp_tokens.append(("kw", "while", f"{ln},{ecc}"))
    exp_tokens, source_string, ln, cc, ecc = pop_val_exp(source_string, "run", ln, cc)
    tmp_tokens += exp_tokens
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "run"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "the"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "following"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "open-curly-brace"):
                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'following'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'run'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_break(source_string, ln, cc, ecc):
    #print("kw_break")
    tmp_tokens = []
    tmp_tokens.append(("kw", "break", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "out"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "of"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "loop"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == eol):
                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'loop'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'of'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'out'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_jump(source_string, ln, cc, ecc):
    #print("kw_jump")
    tmp_tokens = []
    tmp_tokens.append(("kw", "jump", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "to"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "next"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "iteration"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == eol):
                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'iteration'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'next'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'to'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_for(source_string, ln, cc, ecc):
    #print("kw_for")
    tmp_tokens = []
    tmp_tokens.append(("kw", "for", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "every"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "item"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "in"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "the"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "construct"):
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == "named"):
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "do"):
                                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                if(tmp_elem == "the"):
                                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                    if(tmp_elem == "following"):
                                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                                        if(tmp_elem == "open-curly-brace"):
                                            tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                                        else:
                                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
                                    else:
                                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'following'")
                                else:
                                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'do'")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'construct'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'in'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'item'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'every'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_return(source_string, ln, cc, ecc):
    #print("kw_return")
    tmp_tokens = []
    tmp_tokens.append(("kw", "return", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "value"):
        exp_tokens, source_string, ln, cc, ecc = pop_val_exp(source_string, eol, ln, cc)
        
        tmp_tokens += exp_tokens
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == eol):
            tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'value'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_if(source_string, ln, cc, ecc):
    #print("kw_if")
    tmp_tokens = []
    tmp_tokens.append(("kw", "if", f"{ln},{ecc}"))

    exp_tokens, source_string, ln, cc, ecc = pop_val_exp(source_string, "run", ln, cc)
    tmp_tokens += exp_tokens

    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    
    if(tmp_elem == "run"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "the"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "following"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "open-curly-brace"):
                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'following'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'run'")
    
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_or(source_string, ln, cc, ecc):
    #print("kw_or")
    tmp_tokens = []
    tmp_tokens.append(("kw", "or", f"{ln},{ecc}"))

    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "if"):
        tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
        exp_tokens, source_string, ln, cc, ecc = pop_val_exp(source_string, "run", ln, cc)
        
        tmp_tokens += exp_tokens
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "run"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "the"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "following"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "open-curly-brace"):
                    tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'following'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'run'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_try(source_string, ln, cc, ecc):
    #print("kw_try")
    tmp_tokens = []
    tmp_tokens.append(("kw", "try", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "to"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "run"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "the"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "following"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "open-curly-brace"):
                        tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'following'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'run'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'to'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_catch(source_string, ln, cc, ecc):
    #print("kw_catch")
    tmp_tokens = []
    tmp_tokens.append(("kw", "catch", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "error"):
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == "named"):
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            tmp_tokens.append(("id", tmp_elem, f"{ln},{ecc}"))
            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
            if(tmp_elem == "and"):
                tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                if(tmp_elem == "run"):
                    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                    if(tmp_elem == "the"):
                        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                        if(tmp_elem == "following"):
                            tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
                            if(tmp_elem == "open-curly-brace"):
                                tmp_tokens.append(("kw", tmp_elem, f"{ln},{ecc}"))
                            else:
                                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'open-curly-brace'")
                        else:
                            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'following'")
                    else:
                        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'the'")
                else:
                    lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'run'")
            else:
                lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'and'")
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'named'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'error'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_assert(source_string, ln, cc, ecc):
    #print("kw_assert")
    tmp_tokens = []
    tmp_tokens.append(("kw", "assert", f"{ln},{ecc}"))
    tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
    if(tmp_elem == "that"):
        exp_tokens, source_string, ln, cc, ecc = pop_val_exp(source_string, eol, ln, cc)
        tmp_tokens += exp_tokens
        tmp_elem, source_string, ln, cc, ecc = pop_next_element(source_string, ln, cc)
        if(tmp_elem == eol):
            tmp_tokens.append(("kw", eol, f"{ln},{ecc}"))
        else:
            lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'semicolon'")
    else:
        lex_error(ln, ecc, f"unknown element '{tmp_elem}' - expected 'that'")
    return (tmp_tokens, source_string, ln, cc, ecc)

def kw_exit(source_string, ln, cc, ecc):
    #print("kw_exit")
    tmp_tokens = []
    tmp_tokens.append(("kw", "exit", f"{ln},{ecc}"))
    return (tmp_tokens, source_string, ln, cc, ecc)

def skip_comment(s, ln, cc):
    while(s):
        if s.startswith("comment"):
            s = s[7:]
            cc += 7
            break
        elif s[0] == "\n" or s[0] == "\r" or s[0] == "\n\r" or s[0] == "\r\n":
            ln += 1
            cc = 1
        else:
            cc += 1
        s = s[1:]
    return (s, ln, cc)

def create_token_list(source_string):
    token_list = []
    line_number = 1
    character_count = 1
    while(source_string):
        tmp_elem, source_string, line_number, character_count, ecc = pop_next_element(source_string, line_number, character_count)
        
        if tmp_elem == "comment":
            source_string, line_number, character_count = skip_comment(source_string, line_number, character_count)
        elif tmp_elem == "" or tmp_elem == " " or tmp_elem == "\n":
            pass
        else:
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
            
            tmp_tokens, source_string, line_number, character_count, ecc = switch.get(tmp_elem)(source_string, line_number, character_count, ecc)
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
    return create_token_list(source_string)
