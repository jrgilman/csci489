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
        ':=': 25,
        '##': 999
    }

    special_tokens = {
        'constant': 33,
        'identifier': 35
    }

    current_identifier = 100

    identifier_list = {}

    scanned_program = []

    def __init__(self, file_name):
        self.scanFile(file_name)
        print(self.scanned_program)
        print(self.identifier_list)

    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub)

    def is_integer(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def scanFile(self, file_name):
        file_to_interpret = open(file_name, 'r')
        for line in file_to_interpret:

            scanned_line = {}

            clean_line = line.replace('\n','').replace(' ','')
            parse_helper = len(clean_line)*'-'

            for reserved_word in self.reserved_words:
                locations = Scanner.find_all(clean_line, reserved_word)
                for location in locations:
                    if location != -1:
                        for i in range(location, location + len(reserved_word)):
                            parse_helper = parse_helper[:i] + '@' + parse_helper[i + 1:]

                        inside = False
                        for key, value in scanned_line.items():
                            start = key
                            end = key + len(value) - 1
                            if( location in range(start, end) ):
                                inside = True

                        if(not inside):
                            scanned_line[location] = reserved_word

            for single_char_operator in self.single_char_operators:
                locations = Scanner.find_all(clean_line, single_char_operator)
                for location in locations:
                    if location != -1:
                        for i in range(location, location + len(single_char_operator)):
                            parse_helper = parse_helper[:i] + '@' + parse_helper[i + 1:]

                        inside = False
                        for key, value in scanned_line.items():
                            start = key
                            end = key + len(value) - 1
                            if( location in range(start, end) ):
                                inside = True

                        if(not inside):
                            scanned_line[location] = single_char_operator

            for multi_char_operator in self.multi_char_operators:
                locations = Scanner.find_all(clean_line, multi_char_operator)
                for location in locations:
                    if location != -1:
                        for i in range(location, location + len(multi_char_operator)):
                            parse_helper = parse_helper[:i] + '@' + parse_helper[i + 1:]
                        scanned_line[location] = multi_char_operator

                        inside = False
                        for key, value in scanned_line.items():
                            start = key
                            end = key + len(value) - 1
                            if( location in range(start, end) ):
                                inside = True

                        if(not inside):
                            scanned_line[location] = multi_char_operator

            temp = ''
            for i in range(0, len(parse_helper)):
                if( parse_helper[i] == '-' ):
                    stepper = i
                    non_terminal = ''
                    while( (stepper < len(parse_helper)) and (parse_helper[stepper] != '@') ):
                        non_terminal += clean_line[stepper]
                        parse_helper = parse_helper[:stepper] + '@' + parse_helper[stepper + 1:]
                        stepper += 1
                    scanned_line[i] = non_terminal

            scanned_line = [value for (key, value) in sorted(scanned_line.items())]
            new_scanned_line = []

            for part in scanned_line:
                if( part in self.reserved_words ):
                    new_scanned_line.append(self.reserved_words[part])
                elif( part in self.single_char_operators ):
                    new_scanned_line.append(self.single_char_operators[part])
                elif( part in self.multi_char_operators ):
                    new_scanned_line.append(self.multi_char_operators[part])
                elif( Scanner.is_integer(part) ):
                    new_scanned_line.append(self.special_tokens['constant'])
                    new_scanned_line.append(int(part))
                else:
                    if( part not in self.identifier_list ):
                        self.identifier_list[part] = self.current_identifier
                        self.current_identifier += 1

                    new_scanned_line.append(self.special_tokens['identifier'])
                    new_scanned_line.append(self.identifier_list[part])

            self.scanned_program.append(new_scanned_line)

    def __str__(self):
        object_string = '';
        for line in self.scanned_program:
            if( line != [] ):
                object_string += ' '.join(map(str, line)) + '\n'
        return object_string[:-1]

if __name__ == "__main__":
    print(Scanner(sys.argv[1]))
