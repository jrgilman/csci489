from scanner.scanner import Scanner
from scanner.grammar import Grammar

import sys

class Parser:

    def __init__(self, scanned_program):
        self.scanned_program = scanned_program.scanned_program
        self.identifier_dict = scanned_program.identifier_dict.items()
        self.current_code = (-1, None)

        self.nextCode()
        self.program()

        self.program_tree = {
            'declare_part': {},
            'statement_group': {}
        }

    def nextCode(self):
        next_location = self.current_code[0] + 1
        code = self.scanned_program[next_location]
        self.current_code = (next_location, code)
        #print(self.current_code)

    def program(self):

        # if the first code in the program is a declare statement, that means
        # there is a declare part to the code.
        if self.current_code[1] == Grammar.keyword_tokens['declare'][1]:
            self.declare_part()

        self.statement_group()

        assert self.current_code[1] == Grammar.tokens['#']['##'][1]

    def declare_part(self):

        while( self.current_code[1] == Grammar.keyword_tokens['declare'][1] ):

            assert self.current_code[1] == Grammar.keyword_tokens['declare'][1]
            self.nextCode()

            assert self.current_code[1] == Grammar.keyword_tokens['integer'][1]
            self.nextCode()

            self.identifier_list()

            assert self.current_code[1] == Grammar.tokens[';'][1]
            self.nextCode()

    def statement_group(self):
        # this needs to be improved so that the last statement doesn't require a ;
        last_run = False
        while( not last_run ):
            self.statement()
            if self.current_code[1] != Grammar.tokens[';'][1]:
                last_run = True
            else:
                self.nextCode()

    def statement(self):
        if self.current_code[1] == Grammar.keyword_tokens['read'][1]:
            #print('read stmt')
            self.read_stmt()
        elif self.current_code[1] == Grammar.keyword_tokens['write'][1]:
            #print('write stmt')
            self.write_stmt()
        elif self.current_code[1] == Grammar.keyword_tokens['if'][1]:
            #print('cond stmt')
            self.cond_stmt()
        elif self.current_code[1] == Grammar.keyword_tokens['to'][1]:
            #print('loop stmt')
            self.loop_stmt()
        elif self.current_code[1] == Grammar.special_tokens['identifier'][1]:
            #print('asgn stmt')
            self.assignment_stmt()
        else:
            # not a statement. Thus end statement group.
            return False

    def read_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['read'][1]
        self.nextCode()

        self.identifier_list()

    def write_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['write'][1]
        self.nextCode()

        self.output_list()

    def identifier_list(self):

        self.identifier()

        while( self.current_code[1] == Grammar.tokens[','][1] ):
            self.nextCode()
            self.identifier()

    def identifier(self):
        assert self.current_code[1] == Grammar.special_tokens['identifier'][1]
        self.nextCode()
        assert self.current_code[1] in [datum[1] for datum in self.identifier_dict]
        self.nextCode()

    def constant(self):
        assert self.current_code[1] == Grammar.special_tokens['constant'][1]
        self.nextCode()
        assert Parser.check_int(self.current_code[1])
        self.nextCode()

    def check_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def output_list(self):
        # the documentation says to support quotes, but I won't be doing that yet
        # as it requires a thoughtful addition to the scanner and grammar.
        self.expression()

        while self.current_code[1] == Grammar.tokens[','][1]:
            self.nextCode()
            self.expression()

    def expression(self):
        self.term()

        plus_check = self.current_code[1] == Grammar.tokens['+'][1]
        minus_check = self.current_code[1] == Grammar.tokens['-'][1]

        while( plus_check or minus_check ):
            self.nextCode()
            self.term()
            plus_check = self.current_code[1] == Grammar.tokens['+'][1]
            minus_check = self.current_code[1] == Grammar.tokens['-'][1]

    def term(self):
        self.factor()

        multiply_check = self.current_code[1] == Grammar.tokens['*'][1]
        divide_check = self.current_code[1] == Grammar.tokens['/'][1]

        while( multiply_check or divide_check ):
            self.nextCode()
            self.factor()
            multiply_check = self.current_code[1] == Grammar.tokens['*'][1]
            divide_check = self.current_code[1] == Grammar.tokens['/'][1]

    def factor(self):
        if self.current_code[1] == Grammar.tokens['-'][1]:
            assert self.current_code[1] == Grammar.tokens['-'][1]
            self.nextCode()

        self.factor2()

    def factor2(self):
        if self.current_code[1] == Grammar.special_tokens['identifier'][1]:
            self.identifier()
        elif self.current_code[1] == Grammar.special_tokens['constant'][1]:
            self.constant()
        else:
            assert self.current_code[1] == Grammar.tokens['('][1]
            self.nextCode()

            self.expression()

            assert self.current_code[1] == Grammar.tokens[')'][1]
            self.nextCode()

    def assignment_stmt(self):
        self.identifier()

        assert self.current_code[1] == Grammar.tokens[':'][':='][1]
        self.nextCode()

        self.expression()

    def loop_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['to'][1]
        self.nextCode()

        self.expression()

        assert self.current_code[1] == Grammar.keyword_tokens['loop'][1]
        self.nextCode()

        self.statement_group()

        assert self.current_code[1] == Grammar.keyword_tokens['endloop'][1]
        self.nextCode()

    def cond_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['if'][1]
        self.nextCode()

        self.expression()
        self.relational_operator()
        self.expression()

        assert self.current_code[1] == Grammar.keyword_tokens['then'][1]
        self.nextCode()

        self.statement_group()

        if self.current_code[1] == Grammar.keyword_tokens['else'][1]:
            self.nextCode()

            self.statement_group()

        assert self.current_code[1] == Grammar.keyword_tokens['fi'][1]
        self.nextCode()

    def relational_operator(self):
        try:
            placeholder = {
                Grammar.tokens['>']['>'][1]: 1,
                Grammar.tokens['>']['>='][1]: 1,
                Grammar.tokens['<']['<'][1]: 1,
                Grammar.tokens['<']['<='][1]: 1,
                Grammar.tokens['#']['#'][1]: 1,
                Grammar.tokens['='][1]: 1,
            }[self.current_code[1]]
            self.nextCode()
        except KeyError as ke:
            print('improper relational operator in loop')
            sys.exit()
