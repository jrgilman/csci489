import sys
import string
from grammar import Grammar

class Scanner:

    def __init__(self, file_to_scan):
        self.program_string = ''
        self.identifier_dict = {}

        # we start at 100 at the moment, because no keyword/vocab starts even close
        # to this number. In the future though I'd like to completely change the tokens
        # for identifiers so that they cannot be mixed up no matter what.
        self.current_identifier = 100
        self.scanned_program = []

        try:
            self.handle = open(file_to_scan, 'r')
        except OSError as os_e:
            print('ERROR: File \'%s\' could not be accessed.' % file_to_scan)
            sys.exit()

        self.scanProgram()

    # loads the handle (file) into a string with no spacing or newline characters
    # so that parsing can begin
    # def handleToString(self):
    #
    #    temp_program_string = ''
    #    for line in self.handle:
    #        temp_program_string += line.replace('\n', '').replace(' ', '')
    #
    #    self.program_string = temp_program_string

    # scans the string created via handleToString into a program using the grammar
    # and vocabulary described in grammar.py
    def scanProgram(self):

        for full_line in self.handle:

            i = 0
            line = full_line[:-1] # strips off new line.

            while( i < len(line) ):
                char = line[i]

                lower_test = char in string.ascii_lowercase
                upper_test = char in string.ascii_uppercase
                digit_test = char in string.digits
                white_space_test = (char is ' ')

                if( lower_test or upper_test ):
                    # this section tests for either a keyword, or a identifier.

                    temp = ''

                    while( lower_test or upper_test or digit_test ):
                        temp += char

                        i += 1

                        try:
                            char = line[i]
                        except IndexError as ie:
                            break

                        lower_test = char in string.ascii_lowercase
                        upper_test = char in string.ascii_uppercase
                        digit_test = char in string.digits

                    if temp in Grammar.keyword_tokens:
                        self.scanned_program.append(str(Grammar.keyword_tokens[temp][1]))
                    else:

                        # we need to check that the variable is in a declare
                        # statement if it is not currently in the identifier dict

                        declare_test = (self.scanned_program[-2] is Grammar.keyword_tokens['declare'][1])
                        declare_test = declare_test and (self.scanned_program[-1] is Grammar.keyword_tokens['integer'][1])

                        if( temp not in self.identifier_dict and declare_test ):
                            self.identifier_dict[temp] = self.current_identifier
                            self.current_identifier += 1
                        elif( not declare_test ):
                            raise Exception('Undeclared variable used on line')

                        self.scanned_program.append(str(Grammar.special_tokens['identifier'][1]))
                        self.scanned_program.append(str(self.identifier_dict[temp]))

                elif( char in Grammar.tokens ):
                    temp = char
                    token = Grammar.tokens[char]

                    i += 1

                    if type(token) is dict:
                        try:
                            char = line[i]
                            temp += char
                        except IndexError:
                            print('Unexpected token at end of line %s' % temp[1:])
                            sys.exit()

                        if( temp in token ):
                            token = token[temp]
                            i += 1
                        else:
                            if(temp[:1] in token):
                                token = token[temp[:1]]
                            else:
                                print('Improperly formatted token %s' % temp)
                                sys.exit()

                    self.scanned_program.append(str(token[1]))

                elif( digit_test ):

                    temp = ''
                    while( digit_test ):
                        temp += char

                        i += 1
                        try:
                            char = line[i]
                        except IndexError as ie:
                            break

                        digit_test = char in string.digits

                    self.scanned_program.append(str(Grammar.special_tokens['constant'][1]))
                    self.scanned_program.append(str(temp))
                elif( white_space_test ):
                    i += 1
                else:
                    raise Exception('Unrecognizable character \'%s\'' % char)

# used for unit testing of the scanner class itself
if __name__ == "__main__":
    try:
        scanner = Scanner(sys.argv[1])
        print(' '.join(scanner.scanned_program))
        print(sorted(scanner.identifier_dict.items()))
    except IndexError as ie_e:
        raise ie_e
        print('ERROR: You must provide a file to scan as an argument to this python program.')
        sys.exit()
