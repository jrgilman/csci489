#!/usr/bin/env python3

from scanner.scanner import Scanner
from scanner.grammar import Grammar
from parser.parser import Parser

import sys

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

if __name__ == "__main__":

    source_code_path = None
    try:
        source_code_path = sys.argv[1]
    except IndexError as ie_e:
        raise ie_e
        print('ERROR: You must provide a file to scan as an argument to the interpreter')
        sys.exit()

    scanned_program = Scanner(source_code_path)
    parser = Parser(scanned_program)

    interpreter_dict = merge_dicts(
        dict((v,k) for k,v in scanned_program.identifier_dict.items()),
        Grammar.flattenToValueKeyed()
    )

    program_stack = []
    program_temp_values = {}
    postfix_list_count = 0

    while(postfix_list_count < len(parser.postfix_list)):
        if parser.postfix_list[postfix_list_count] == Grammar.special_tokens['identifier'][1] or parser.postfix_list[postfix_list_count] == Grammar.special_tokens['constant'][1] or parser.postfix_list[postfix_list_count] == Grammar.special_tokens['quote'][1]:
            program_stack.append(parser.postfix_list[postfix_list_count])
            postfix_list_count+=1
            program_stack.append(parser.postfix_list[postfix_list_count])

        elif parser.postfix_list[postfix_list_count]  == Grammar.keyword_tokens['read'][1]:
            tok = program_stack[-2]
            while (len(program_stack) > 0 and  (tok != Grammar.special_tokens['constant'][1] or tok != Grammar.special_tokens['identifier'][1])):
                var = program_stack[-1]
                var = (interpreter_dict.get([var][0]))
                varValue = int(input("Please Enter a Value for %s: " % (var)))
                var = program_stack.pop()
                tok = program_stack.pop()
                program_temp_values[var] = varValue

        elif parser.postfix_list[postfix_list_count] == Grammar.keyword_tokens['write'][1]:
                tok = program_stack[-2]
                printList = []
                while (len(program_stack) > 0 and (tok != Grammar.special_tokens['constant'][1] or tok != Grammar.special_tokens['identifier'][1] or tok!= Grammar.special_tokens['quote'][1])):
                    val = program_stack.pop()
                    tok = program_stack.pop()
                    if(tok == Grammar.special_tokens['identifier'][1]):
                        val = program_temp_values.get(val)
                    printList.append(val)

                printList.reverse()
                for val in printList:
                    encoded = str(val).encode('UTF-8')
                    if "\\n" in u"%s" % encoded:
                        print("")
                    else:
                        print(val, end="")


        elif parser.postfix_list[postfix_list_count]  == Grammar.tokens[':'][':='][1]:
            asgnVal = program_stack.pop()
            assert(program_stack.pop() == Grammar.special_tokens['identifier'][1] or Grammar.special_tokens['constant'][1])
            asgnVar = program_stack.pop()
            program_temp_values[asgnVar] = asgnVal
            assert(program_stack.pop() == Grammar.special_tokens['identifier'][1] or Grammar.special_tokens['constant'][1])

        elif parser.postfix_list[postfix_list_count]  == Grammar.tokens['+'][1]:
            val1 = program_stack.pop()
            val1Check = program_stack.pop()

            if val1Check == Grammar.special_tokens['identifier'][1]:
                val1 = program_temp_values.get(val1)

            val2 = program_stack.pop()
            val2Check = program_stack.pop()

            if val2Check == Grammar.special_tokens['identifier'][1]:
                val2 = program_temp_values.get(val2)

            program_stack.append(Grammar.special_tokens['constant'][1])
            program_stack.append(val2 + val1)

        elif parser.postfix_list[postfix_list_count]  == Grammar.tokens['-'][1]:
            val1 = program_stack.pop()
            val1Check = program_stack.pop()

            if val1Check == Grammar.special_tokens['identifier'][1]:
                val1 = program_temp_values.get(val1)

            val2 = program_stack.pop()
            val2Check = program_stack.pop()

            if val2Check == Grammar.special_tokens['identifier'][1]:
                val2 = program_temp_values.get(val2)

            program_stack.append(Grammar.special_tokens['constant'][1])
            program_stack.append(val2 - val1)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['*'][1]:
            val1 = program_stack.pop()
            val1Check = program_stack.pop()

            if val1Check == Grammar.special_tokens['identifier'][1]:
                val1 = program_temp_values.get(val1)

            val2 = program_stack.pop()
            val2Check = program_stack.pop()

            if val2Check == Grammar.special_tokens['identifier'][1]:
                val2 = program_temp_values.get(val2)

            program_stack.append(Grammar.special_tokens['constant'][1])
            program_stack.append(val1 * val2)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['/'][1]:
            val1 = program_stack.pop()
            val1Check = program_stack.pop()

            if val1Check == Grammar.special_tokens['identifier'][1]:
                val1 = program_temp_values.get(val1)

            val2 = program_stack.pop()
            val2Check = program_stack.pop()

            if val2Check == Grammar.special_tokens['identifier'][1]:
                val2 = program_temp_values.get(val2)

            program_stack.append(Grammar.special_tokens['constant'][1])
            program_stack.append(val2 / val1)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['='][1]:
            var1 = program_stack.pop()
            varType1 = program_stack.pop()
            if(varType1 == Grammar.special_tokens['identifier'][1]):
                var1 = program_temp_values.get(var1)

            var2 = program_stack.pop()
            varType2 = program_stack.pop()
            if (varType2 == Grammar.special_tokens['identifier'][1]):
                var2 = program_temp_values.get(var2)

            if(var2 == var1):
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(1)   #1 for true else 0 for false
            else:
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(0)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['<']['<'][1]:
            var1 = program_stack.pop()
            varType1 = program_stack.pop()
            if (varType1 == Grammar.special_tokens['identifier'][1]):
                var1 = program_temp_values.get(var1)

            var2 = program_stack.pop()
            varType2 = program_stack.pop()
            if (varType2 == Grammar.special_tokens['identifier'][1]):
                var2 = program_temp_values.get(var2)

            if (var2 < var1):
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(1)  # 1 for true else 0 for false
            else:
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(0)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['<']['<='][1]:
            var1 = program_stack.pop()
            varType1 = program_stack.pop()
            if (varType1 == Grammar.special_tokens['identifier'][1]):
                var1 = program_temp_values.get(var1)

            var2 = program_stack.pop()
            varType2 = program_stack.pop()
            if (varType2 == Grammar.special_tokens['identifier'][1]):
                var2 = program_temp_values.get(var2)

            if (var2 <= var1):
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(1)  # 1 for true else 0 for false
            else:
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(0)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['>']['>'][1]:
            var1 = program_stack.pop()
            varType1 = program_stack.pop()
            if (varType1 == Grammar.special_tokens['identifier'][1]):
                var1 = program_temp_values.get(var1)

            var2 = program_stack.pop()
            varType2 = program_stack.pop()
            if (varType2 == Grammar.special_tokens['identifier'][1]):
                var2 = program_temp_values.get(var2)

            if (var2 > var1):
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(1)  # 1 for true else 0 for false
            else:
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(0)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['>']['>='][1]:
            var1 = program_stack.pop()
            varType1 = program_stack.pop()
            if (varType1 == Grammar.special_tokens['identifier'][1]):
                var1 = program_temp_values.get(var1)

            var2 = program_stack.pop()
            varType2 = program_stack.pop()
            if (varType2 == Grammar.special_tokens['identifier'][1]):
                var2 = program_temp_values.get(var2)

            if (var2 >= var1):
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(1)  # 1 for true else 0 for false
            else:
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(0)

        elif parser.postfix_list[postfix_list_count] == Grammar.tokens['#']['#'][1]:
            var1 = program_stack.pop()
            varType1 = program_stack.pop()
            if (varType1 == Grammar.special_tokens['identifier'][1]):
                var1 = program_temp_values.get(var1)

            var2 = program_stack.pop()
            varType2 = program_stack.pop()
            if (varType2 == Grammar.special_tokens['identifier'][1]):
                var2 = program_temp_values.get(var2)

            if (var2 != var1):
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(1)  # 1 for true else 0 for false
            else:
                program_stack.append(Grammar.special_tokens['constant'][1])
                program_stack.append(0)

        elif parser.postfix_list[postfix_list_count] == Grammar.parser_tokens['UM'][1]:
            var = program_stack.pop()
            varType = program_stack.pop()
            if(varType == Grammar.special_tokens['identifier'][1]):
                var = program_temp_values[var]

            var = -var
            program_stack.append(Grammar.special_tokens['constant'][1])
            program_stack.append(var)

        elif parser.postfix_list[postfix_list_count] == Grammar.parser_tokens['BR'][1]:
            Branch_loc = program_stack.pop()
            assert(program_stack.pop() == Grammar.special_tokens['constant'][1])
            postfix_list_count = (Branch_loc - 1)   #Since plus 1 added to list_count at end

        elif parser.postfix_list[postfix_list_count] == Grammar.parser_tokens['BF'][1]:
            Branch_loc = program_stack.pop()
            assert(program_stack.pop() == Grammar.special_tokens['constant'][1])
            checkFalse = program_stack.pop()
            assert(program_stack.pop() == Grammar.special_tokens['constant'][1])
            if(checkFalse == 0):
                postfix_list_count = Branch_loc - 1

        postfix_list_count +=1
