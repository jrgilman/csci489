class Grammar:

# global token/minilang grammar file

    keyword_tokens = {
        'read': ('KWRD', 3, 'INF'),
        'write': ('KWWR', 4, 'INF'),
        'if': ('KWIF', 5, None),
        'then': ('KWTH', 6, None),
        'else': ('KWEL', 7, None),
        'fi': ('KWFI', 8, None),
        'to': ('KWTO', 9, None),
        'do': ('KWDO', 10, None),
        'loop': ('KWSTRL', 29, None),
        'endloop': ('KWENDL', 11, None),
        'declare': ('KWDEC', 27, None),
        'integer': ('KWINT', 28, None)
    }

    tokens = {
        ';': ('SEMI', 12, None),
        ',': ('COMMA', 13, None),
        ':': {
            ':=': ('ASGN', 14, 2)
        },
        '+': ('PLUS', 15, 2),
        '-': ('MINUS', 16, 2),
        '*': ('MUL', 17, 2),
        '/': ('DIV', 18, 2),
        '=': ('EQR', 19, 2),
        '>': {
            '>': ('GTR', 20, 2),
            '>=': ('GER', 23, 2),
        },
        '<': {
            '<': ('LTR', 21, 2),
            '<=': ('LER', 22, 2)
        },
        '#': {
            '#': ('NOTEQUAL', 30, 2),
            '##': ('HALT', 24, 0)
        },
        '(': ('LPAR', 25, None),
        ')': ('RPAR', 26, None)
    }

    special_tokens = {
        'identifier': ('IDR', 1, -1),
        'constant': ('CONST', 2, -1),
        'quote': ('QUOTE', 31, -1)
    }

    parser_tokens = {
        'UM': ('UNARYMINUS', 32, 1),
        'BR': ('BRANCH', 33, 2),
        'BF': ('BRFALSE', 34, 2)
    }

    def flattenToValueKeyed():
        return_dict = {};

        for key, token in Grammar.keyword_tokens.items():
            if(token[2] != None):
                return_dict[token[1]] = (key, token[2])

        for key, token in Grammar.tokens.items():
            if type(token) is tuple:
                if(token[2] != None):
                    return_dict[token[1]] = (key, token[2])
            else:
                for sub_key, sub_token in token.items():
                    if(sub_token[2] != None):
                        return_dict[sub_token[1]] = (sub_key, sub_token[2])

        for key, token in Grammar.special_tokens.items():
            if(token[2] != None):
                return_dict[token[1]] = (key, token[2])

        for key, token in Grammar.parser_tokens.items():
            if(token[2] != None):
                return_dict[token[1]] = (key, token[2])

        return return_dict
