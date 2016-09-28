import scanner
import parser

import sys

if __name__ == "__main__":

    source_code_path = None
    try:
        source_code_path = sys.argv[1]
    except IndexError as ie_e:
        raise ie_e
        print('ERROR: You must provide a file to scan as an argument to the interpreter')
        sys.exit()

    scanned_program = scanner.Scanner(source_code_path)
    parser = parser.Parser(scanned_program)
