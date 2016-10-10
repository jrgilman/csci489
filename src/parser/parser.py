from scanner.scanner import Scanner
from scanner.grammar import Grammar

class Parser:

    def __init__(self, scanned_program):
        self.scanned_program = scanned_program.scanned_program
        self.identifier_dict = scanned_program.identifier_dict.items()
        self.current_code = (-1, None)

        self.nextCode()
        self.program()

    def nextCode(self):
        next_location = self.current_code[0] + 1
        code = self.scanned_program[next_location]
        self.current_code = (next_location, code)
        print(self.current_code)

    def program(self):
        if self.current_code[1] == Grammar.keyword_tokens['declare'][1]:
            self.declare_part()
        self.statement_group()
        assert self.current_code[1] == Grammar.tokens['#']['##'][1]

    def declare_part(self):

        assert self.current_code[1] == Grammar.keyword_tokens['declare'][1]
        self.nextCode()

        assert self.current_code[1] == Grammar.keyword_tokens['integer'][1]
        self.nextCode()

        assert self.current_code[1] == Grammar.special_tokens['identifier'][1]
        self.nextCode()

        assert self.current_code[1] in [datum[1] for datum in self.identifier_dict]
        self.nextCode()

        while( self.current_code[1] == Grammar.tokens[','][1] ):
            self.nextCode()
            if self.current_code[1] == Grammar.tokens[';'][1]:
                break
            else:
                assert self.current_code[1] == Grammar.special_tokens['identifier'][1]
                self.nextCode()
                assert self.current_code[1] in [datum[1] for datum in self.identifier_dict]
                self.nextCode()

        assert self.current_code[1] == Grammar.tokens[';'][1]
        self.nextCode()

        if self.current_code[1] == Grammar.keyword_tokens['declare'][1]:
            self.declare_part()

    def statement_group(self):
        while(self.statement()):
            pass

    def statement(self):
        if self.current_code[1] == Grammar.tokens[':'][':='][1]:
            # do assign statement stuff
        elif self.current_code[1] == Grammar.keyword_tokens['read'][1]:
            # do read statement stuff
        elif self.current_code[1] == Grammar.keyword_tokens['write'][1]:
            # do write statement stuff
        elif self.current_code[1] == Grammar.keyword_tokens['if'][1]:
            # do if statement stuff
        elif self.current_code[1] == Grammar.keyword_tokens['to'][1]:
            # do loop stuff
        else:
            # not a statement. Thus end statement group.
            return False
