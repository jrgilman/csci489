import sys
import string
from grammar import Grammar

class Scanner:

    def __init__(self, file_to_scan):
        self.program_string = ''
        self.identifier_list = {}
        self.current_identifier = 100
        self.scanned_program = ''

        try:
            self.handle = open(file_to_scan, 'r')
        except OSError as os_e:
            print('ERROR: File \'%s\' could not be accessed.' % file_to_scan)
            sys.exit()

        self.handleToString()
        self.scanString()
        print(self.scanned_program)

    def handleToString(self):

        temp_program_string = ''
        for line in self.handle:
            temp_program_string += line.replace('\n', '').replace(' ', '')

        self.program_string = temp_program_string

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
                    if( temp not in self.identifier_list ):
                        self.identifier_list[temp] = self.current_identifier
                        self.current_identifier += 1
                    else:
                        self.scanned_program += str(Grammar.special_tokens['identifier'][1]) + ' '

                    self.scanned_program += str(self.identifier_list[temp]) + ' '

            elif( char in Grammar.tokens ):
                temp = char
                token = Grammar.tokens[char]

                while( type(token) is dict ):
                    try:
                        i += 1
                        char = self.program_string[i]
                        temp += char
                    except IndexError:
                        pass

                    if( temp in token ):
                        token = token[temp]
                    else:
                        temp = temp[:1]

                i += 1

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

if __name__ == "__main__":
    try:
        Scanner(sys.argv[1])
    except IndexError as ie_e:
        raise ie_e
        print('ERROR: You must provide a file to scan as an argument to this python program.')
        sys.exit()
