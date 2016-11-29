class Grammar:

# global token/minilang grammar file

    keyword_tokens = {
        'read': ('KWRD', 3),
        'write': ('KWWR', 4),
        'if': ('KWIF', 5),
        'then': ('KWTH', 6),
        'else': ('KWEL', 7),
        'fi': ('KWFI', 8),
        'to': ('KWTO', 9),
        'do': ('KWDO', 10),
        'loop': ('KWSTRL', 29),
        'endloop': ('KWENDL', 11),
        'declare': ('KWDEC', 27),
        'integer': ('KWINT', 28)
    }

    tokens = {
        ';': ('SEMI', 12),
        ',': ('COMMA', 13),
        ':': {
            ':=': ('ASGN', 14)
        },
        '+': ('PLUS', 15),
        '-': ('MINUS', 16),
        '*': ('MUL', 17),
        '/': ('DIV', 18),
        '=': ('EQR', 19),
        '>': {
            '>': ('GTR', 20),
            '>=': ('GER', 23),
        },
        '<': {
            '<': ('LTR', 21),
            '<=': ('LER', 22)
        },
        '#': {
            '#': ('NOTEQUAL', 30),
            '##': ('NER', 24)
        },
        '(': ('LPAR', 25),
        ')': ('RPAR', 26)
    }

    special_tokens = {
        'identifier': ('IDR', 1),
        'constant': ('CONST', 2),
        'quote': ('QUOTE', 31)
    }

    parser_tokens = {
        'UM': ('UNARYMINUS', 32),
        'BR': ('BRANCH', 33),
        'BF': ('BRFALSE', 34)
    }
