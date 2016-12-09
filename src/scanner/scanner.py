import sys
import string
from scanner.grammar import Grammar

class Scanner:

    def __init__(self, file_to_scan):
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

        self.line_counter = 0
        self.scanProgram()

    # scans the string created via handleToString into a program using the grammar
    # and vocabulary described in grammar.py
    def scanProgram(self):

        for full_line in self.handle:

            i = 0
            line = full_line[:-1] # strips off new line.
            self.line_counter += 1 # only used to help the user diagnose errors.

            while( i < len(line) ):

                char = line[i]
                # these tests are used later to determine what type of word we
                # are currently scanning.
                lower_test = char in string.ascii_lowercase
                upper_test = char in string.ascii_uppercase
                digit_test = char in string.digits
                white_space_test = (char is ' ')
                token_test = char in Grammar.tokens
                quote_test = (char is '\'')

                if( lower_test or upper_test ):
                    i = self.scanIdentifierOrKeyword(line, i)
                elif( token_test ):
                    i = self.scanToken(line, i)
                elif( digit_test ):
                    i = self.scanConstant(line, i)
                elif( quote_test ):
                    i = self.scanQuote(line, i)
                elif( white_space_test ):
                    # white space is just a delimeter essentially, so we can skip it.
                    i += 1
                else:
                    print('Unrecognizable character \'%s\' on line %i' % (char, self.line_counter))
                    sys.exit()

    def scanIdentifierOrKeyword(self, line, i):
        # this section tests for either a keyword, or a identifier.

        char = line[i]

        lower_test = char in string.ascii_lowercase
        upper_test = char in string.ascii_uppercase
        digit_test = char in string.digits

        temp = ''

        while( lower_test or upper_test or digit_test ):
            temp += char

            i += 1

            try:
                char = line[i]
            except IndexError as ie:
                # occurs if somehow we've attempted to read a chracter that
                # is past the line's total length
                break

            lower_test = char in string.ascii_lowercase
            upper_test = char in string.ascii_uppercase
            digit_test = char in string.digits

        if temp in Grammar.keyword_tokens:
            self.scanned_program.append(Grammar.keyword_tokens[temp][1])
        else:

            # we need to check that the variable is in a declare
            # statement if it is not currently in the identifier dict

            find_declare = (line.find('declare') != -1)
            find_integer = (line.find('integer') != -1)
            declare_test = find_declare and find_integer

            if( temp not in self.identifier_dict and declare_test ):
                self.identifier_dict[temp] = self.current_identifier
                self.current_identifier += 1
            elif( temp not in self.identifier_dict and not declare_test ):
                print('Undeclared variable %s used on line %i' % (temp, self.line_counter))
                sys.exit()

            self.scanned_program.append(Grammar.special_tokens['identifier'][1])
            self.scanned_program.append(self.identifier_dict[temp])

        return i

    def scanToken(self, line, i):
        char = line[i]
        temp = char
        token = Grammar.tokens[char]

        i += 1

        if type(token) is dict:
            try:
                char = line[i]
                temp += char
            except IndexError:
                print('Unexpected token %s at end of line %i' % (temp[1:], self.line_counter))
                sys.exit()

            if( temp in token ):
                token = token[temp]
                i += 1
            else:
                if(temp[:1] in token):
                    token = token[temp[:1]]
                else:
                    print('Improperly formatted token %s on line %i' % (temp, self.line_counter))
                    sys.exit()

        self.scanned_program.append(token[1])

        return i

    def scanConstant(self, line, i):
        char = line[i]
        temp = ''

        digit_test = char in string.digits

        while( digit_test ):
            temp += char

            i += 1
            try:
                char = line[i]
            except IndexError as ie:
                break

            digit_test = char in string.digits

        self.scanned_program.append(Grammar.special_tokens['constant'][1])
        self.scanned_program.append(int(temp))

        return i

    def scanQuote(self, line, i):

        #skip the first quote
        i += 1
        char = line[i]
        quote_test = (char is '\'')

        temp = ''

        while( not quote_test ):
            try:
                char = line[i]
                quote_test = (char is '\'')
                if not quote_test:
                    temp += char
                i += 1
            except IndexError as ie:
                print('No end quote found.')
                sys.exit()

        self.scanned_program.append(Grammar.special_tokens['quote'][1])
        self.scanned_program.append(temp)

        return i

# used for unit testing of the scanner class itself
if __name__ == "__main__":
    try:
        scanner = Scanner(sys.argv[1])
        print(' '.join(str(code) for code in scanner.scanned_program))
        print(sorted(scanner.identifier_dict.items()))
    except IndexError as ie_e:
        raise ie_e
        print('ERROR: You must provide a file to scan as an argument to this python program.')
        sys.exit()
