from scanner.scanner import Scanner
from scanner.grammar import Grammar

import sys
import string

class Parser:

    def __init__(self, scanned_program):
        # we need an actual reference to the object since we will be potentially
        # creating special loop variables that are hidden from the user. But will
        # be necessary for the interpreting (milestone 4) portion of the code.
        self.scanned_program = scanned_program

        self.code_format = scanned_program.scanned_program
        self.identifier_dict = scanned_program.identifier_dict.items()

        self.postfix_list = []

        self.current_code = (-1, None)
        self.nextCode()

        self.program()

        self.program_tree = {
            'declare_part': {},
            'statement_group': {}
        }

    def nextCode(self):
        next_location = self.current_code[0] + 1
        code = self.code_format[next_location]
        self.current_code = (next_location, code)
        #print(self.current_code)

    def program(self):

        # if the first code in the program is a declare statement, that means
        # there is a declare part to the code.
        if self.current_code[1] == Grammar.keyword_tokens['declare'][1]:
            self.declare_part()

        self.statement_group()

        assert self.current_code[1] == Grammar.tokens['#']['##'][1]
        self.postfix_list.append(Grammar.tokens['#']['##'][1])

    def declare_part(self):

        while( self.current_code[1] == Grammar.keyword_tokens['declare'][1] ):

            assert self.current_code[1] == Grammar.keyword_tokens['declare'][1]
            self.nextCode()

            assert self.current_code[1] == Grammar.keyword_tokens['integer'][1]
            self.nextCode()

            self.identifier_list(dont_queue = True)

            # let's not bother adding declarations to the output queue
            #self.postfix_list.append(Grammar.keyword_tokens['integer'][1])
            #self.postfix_list.append(Grammar.keyword_tokens['declare'][1])

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

        self.postfix_list.append(Grammar.keyword_tokens['read'][1])

    def write_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['write'][1]
        self.nextCode()

        self.output_list()

        self.postfix_list.append(Grammar.keyword_tokens['write'][1])

    def identifier_list(self, dont_queue = False):

        self.identifier()

        if(dont_queue is True):
            self.postfix_list.pop()
            self.postfix_list.pop()

        while( self.current_code[1] == Grammar.tokens[','][1] ):
            self.nextCode()
            self.identifier()

            if(dont_queue is True):
                self.postfix_list.pop()
                self.postfix_list.pop()

    def identifier(self):
        assert self.current_code[1] == Grammar.special_tokens['identifier'][1]
        self.postfix_list.append(self.current_code[1])
        self.nextCode()

        assert self.current_code[1] in [datum[1] for datum in self.identifier_dict]
        self.postfix_list.append(self.current_code[1])
        self.nextCode()

    def constant(self):
        assert self.current_code[1] == Grammar.special_tokens['constant'][1]
        self.postfix_list.append(self.current_code[1])
        self.nextCode()

        assert Parser.check_int(self.current_code[1])
        self.postfix_list.append(self.current_code[1])
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
        if self.current_code[1] == Grammar.special_tokens['quote'][1]:
            self.quote()
        else:
            self.expression()

        while self.current_code[1] == Grammar.tokens[','][1]:
            self.nextCode()
            if self.current_code[1] == Grammar.special_tokens['quote'][1]:
                self.quote()
            else:
                self.expression()

    def quote(self):
        assert self.current_code[1] == Grammar.special_tokens['quote'][1]
        self.postfix_list.append(self.current_code[1])
        self.nextCode()

        word = self.current_code[1]
        for char in word:
            lower_test = char in string.ascii_lowercase
            upper_test = char in string.ascii_uppercase
            digit_test = char in string.digits
            if not (lower_test or upper_test or digit_test):
                print('Your string has an invalid character: %s' % char)
                sys.exit()

        self.postfix_list.append(self.current_code[1])
        self.nextCode()

    def expression(self):
        self.term()

        plus_check = self.current_code[1] == Grammar.tokens['+'][1]
        minus_check = self.current_code[1] == Grammar.tokens['-'][1]

        while( plus_check or minus_check ):

            previous_operator = self.current_code[1]

            self.nextCode()
            self.term()

            self.postfix_list.append(previous_operator)

            plus_check = self.current_code[1] == Grammar.tokens['+'][1]
            minus_check = self.current_code[1] == Grammar.tokens['-'][1]

    def term(self):
        self.factor()

        multiply_check = self.current_code[1] == Grammar.tokens['*'][1]
        divide_check = self.current_code[1] == Grammar.tokens['/'][1]

        while( multiply_check or divide_check ):

            previous_operator = self.current_code[1]

            self.nextCode()
            self.factor()

            self.postfix_list.append(previous_operator)

            multiply_check = self.current_code[1] == Grammar.tokens['*'][1]
            divide_check = self.current_code[1] == Grammar.tokens['/'][1]

    def factor(self):

        previous_operator = None

        if self.current_code[1] == Grammar.tokens['-'][1]:
            assert self.current_code[1] == Grammar.tokens['-'][1]

            # not a fan of forcing this, but for now it will work.
            # not sure yet how to best map between human and machine readable
            previous_operator = Grammar.parser_tokens['UM'][1]

            self.nextCode()

        self.factor2()

        if previous_operator is not None:
            self.postfix_list.append(previous_operator)

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

        self.postfix_list.append(Grammar.tokens[':'][':='][1])

    def loop_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['to'][1]
        self.nextCode()

        # the hidden loop var being created
        hidden_loop_var = "hidden:loop%i" % self.scanned_program.current_identifier
        self.scanned_program.identifier_dict[hidden_loop_var] = self.scanned_program.current_identifier
        self.scanned_program.current_identifier += 1

        # we then set the loop var to zero via a hidden assignment stmt
        self.postfix_list.append(Grammar.special_tokens['identifier'][1])
        self.postfix_list.append(self.scanned_program.identifier_dict[hidden_loop_var])

        self.postfix_list.append(Grammar.special_tokens['constant'][1])
        self.postfix_list.append(0)

        self.postfix_list.append(Grammar.tokens[':'][':='][1])

        # now we can compare that new hidden loop variable to the expression
        # since our loops only count up, that means we just need to make sure that
        # the variable is less than the expression.
        self.postfix_list.append(Grammar.special_tokens['identifier'][1])
        jump_back_loc = len(self.postfix_list) - 1
        self.postfix_list.append(self.scanned_program.identifier_dict[hidden_loop_var])

        self.expression()

        self.postfix_list.append(Grammar.tokens['<']['<'][1])

        # now we insert our branch on false code
        self.postfix_list.append(Grammar.special_tokens['constant'][1])
        self.postfix_list.append('?')
        false_loc_replace = len(self.postfix_list) - 1
        self.postfix_list.append(Grammar.parser_tokens['BF'][1])

        assert self.current_code[1] == Grammar.keyword_tokens['loop'][1]
        self.nextCode()

        self.statement_group()

        # this code manages incrementing the variable by manually creating postfix
        self.postfix_list.append(Grammar.special_tokens['identifier'][1])
        self.postfix_list.append(self.scanned_program.identifier_dict[hidden_loop_var])

        self.postfix_list.append(Grammar.special_tokens['identifier'][1])
        self.postfix_list.append(self.scanned_program.identifier_dict[hidden_loop_var])

        self.postfix_list.append(Grammar.special_tokens['constant'][1])
        self.postfix_list.append(1)

        self.postfix_list.append(Grammar.tokens['+'][1])

        self.postfix_list.append(Grammar.tokens[':'][':='][1])
        # end of manual increment

        # we then jump back to the part of the code where we read in the loop
        # variable and start the process over gain
        self.postfix_list.append(Grammar.special_tokens['constant'][1])
        self.postfix_list.append(jump_back_loc)
        self.postfix_list.append(Grammar.parser_tokens['BR'][1])

        # and now we replace the ? placeholder from earlier with our final branch location
        # so that we skip the looping branch above
        self.postfix_list[false_loc_replace] = len(self.postfix_list)

        assert self.current_code[1] == Grammar.keyword_tokens['endloop'][1]
        self.nextCode()

    def cond_stmt(self):
        assert self.current_code[1] == Grammar.keyword_tokens['if'][1]
        self.nextCode()

        self.expression()

        rel_op = self.current_code[1]
        self.relational_operator()

        self.expression()

        assert self.current_code[1] == Grammar.keyword_tokens['then'][1]
        self.nextCode()

        self.postfix_list.append(rel_op)

        self.postfix_list.append(Grammar.special_tokens['constant'][1])
        self.postfix_list.append('?')

        false_loc_replace = len(self.postfix_list) - 1
        self.postfix_list.append(Grammar.parser_tokens['BF'][1])

        self.statement_group()

        self.postfix_list.append(Grammar.special_tokens['constant'][1])
        self.postfix_list.append('?')
        end_loc_replace = len(self.postfix_list) - 1
        self.postfix_list.append(Grammar.parser_tokens['BR'][1])

        # it will jump to one after the ?
        false_jump_loc = len(self.postfix_list)

        if self.current_code[1] == Grammar.keyword_tokens['else'][1]:
            self.nextCode()

            self.statement_group()
        else:
            false_jump_loc = len(self.postfix_list)

        assert self.current_code[1] == Grammar.keyword_tokens['fi'][1]
        self.nextCode()

        self.postfix_list[false_loc_replace] = false_jump_loc
        self.postfix_list[end_loc_replace] = len(self.postfix_list)

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
