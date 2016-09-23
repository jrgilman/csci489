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
        self.scanned_program = ''

        try:
            self.handle = open(file_to_scan, 'r')
        except OSError as os_e:
            print('ERROR: File \'%s\' could not be accessed.' % file_to_scan)
            sys.exit()

        self.handleToString()
        self.scanString()

    # loads the handle (file) into a string with no spacing or newline characters
    # so that parsing can begin
    def handleToString(self):

        temp_program_string = ''
        for line in self.handle:
            temp_program_string += line.replace('\n', '').replace(' ', '')

        self.program_string = temp_program_string

    # scans the string created via handleToString into a program using the grammar
    # and vocabulary described in grammar.py
    def scanString(self):
        i = 0
        while( i < len(self.program_string) ):
            char = self.program_string[i]

            lower_test = char in string.ascii_lowercase
            upper_test = char in string.ascii_uppercase
            digit_test = char in string.digits
            if( lower_test or upper_test ):
                # this section tests for either a keyword, or a identifier.

                temp = ''
                identifier = True

                while( lower_test or upper_test or digit_test ):
                    temp += char

                    i += 1

                    if temp in Grammar.keyword_tokens:
                        self.scanned_program += str(Grammar.keyword_tokens[temp][1]) + ' '
                        identifier = False
                        break

                    char = self.program_string[i]

                    lower_test = char in string.ascii_lowercase
                    upper_test = char in string.ascii_uppercase
                    digit_test = char in string.digits

                if( identifier is True ):
                    if( temp not in self.identifier_dict ):
                        self.identifier_dict[temp] = self.current_identifier
                        self.current_identifier += 1
                    else:
                        self.scanned_program += str(Grammar.special_tokens['identifier'][1]) + ' '

                    self.scanned_program += str(self.identifier_dict[temp]) + ' '

            elif( char in Grammar.tokens ):
                temp = char
                token = Grammar.tokens[char]

                i += 1

                if type(token) is dict:
                    try:
                        char = self.program_string[i]
                        temp += char
                    except IndexError:
                        print('Unexpected token at end of file %s' % temp[1:])
                        sys.exit()

                    if( temp in token ):
                        token = token[temp]
                        i += 1
                    else:
                        print('Improperly formatted token %s' % temp)
                        sys.exit()

                self.scanned_program += str(token[1])
                if( token[0] != 'NER' ):
                    self.scanned_program += ' '

            elif( digit_test ):

                temp = ''
                while( digit_test ):
                    temp += char

                    i += 1
                    char = self.program_string[i]

                    digit_test = char in string.digits

                self.scanned_program += str(Grammar.special_tokens['constant'][1]) + ' '
                self.scanned_program += str(temp) + ' '

            else:
                raise Exception('Unrecognizable character \'%s\'' % char)

# used for unit testing of the scanner class itself
if __name__ == "__main__":
    try:
        scanner = Scanner(sys.argv[1])
        print(scanner.scanned_program)
        print(sorted(scanner.identifier_dict.items()))
    except IndexError as ie_e:
        raise ie_e
        print('ERROR: You must provide a file to scan as an argument to this python program.')
        sys.exit()
