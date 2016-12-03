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
    print('Program Scanned.')
    parser = Parser(scanned_program)
    print('Program Parsed.')
    print(parser.postfix_list)

    interpreter_dict = merge_dicts(
        dict((v,k) for k,v in scanned_program.identifier_dict.items()),
        Grammar.flattenToValueKeyed()
    )

    print(interpreter_dict)
