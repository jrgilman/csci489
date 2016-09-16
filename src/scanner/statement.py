from grammar import Grammar

import re

class Statement:

    identifier_list = {}

    def __init__(self, first_line):
        self.statement_text = first_line
        self.expected_grammar = None

        temp = ''
        for char in self.statement_text:
            temp += char
            if temp in Grammar.single_line_grammars:
                
