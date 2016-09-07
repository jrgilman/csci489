import sys

class Scanner:

    reserved_words = {
        'read': 1,
        'write': 2,
        'declare': 3,
        'integer': 4,
        'fi': 5,
        'else': 6,
        'if': 7,
        'then': 8,
        'loop': 9,
        'endloop': 10,
        'to': 11,
        'for': 12
    }

    single_char_operators = {
        ',': 32,
        ';': 31,
        '-': 22,
        '+': 21,
        '*': 33
    }

    multi_char_operators = {
        ':=': 25
    }

    current_identifier = 100

    identifier_list = {}

    scanned_program = []

    def __init__(self, file_name):
        self.scanFile(file_name)
        print(self.scanned_program)
        print(self.identifier_list)

    def scanFile(self, file_name):
        file_to_interpret = open(file_name, 'r')
        for line in file_to_interpret:

            scanned_line = []

            clean_line = line.replace('\n','').replace(' ','')
            print(clean_line)
            temp = ''
            for char in clean_line:

                temp += char

                if( char in self.single_char_operators ):

                    if( scanned_line[0] == 3 and scanned_line[1] == 4 ):
                        # current only supports single character variables...
                        self.identifier_list[temp[:-1]] = self.current_identifier
                        self.current_identifier += 1

                        scanned_line.append(self.identifier_list[temp[:-1]])
                    else:
                        if( temp[:-1] != '' ):
                            scanned_line.append(temp[:-1])

                    scanned_line.append(self.single_char_operators[char])
                    temp = ''
                    continue;

                if( temp in self.reserved_words ):
                    scanned_line.append(self.reserved_words[temp])
                    temp = ''
                    continue;

                if( temp in self.identifier_list ):
                    scanned_line.append(self.identifier_list[temp])
                    temp = ''
                    continue;

                if( temp in self.multi_char_operators ):
                    scanned_line.append(self.multi_char_operators[temp])
                    temp = ''
                    continue;

            self.scanned_program.append(scanned_line)

if __name__ == "__main__":
    Scanner(sys.argv[1])
