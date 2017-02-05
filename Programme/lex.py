import ply.lex as lex

reserved_words = (
    'name',
    'entry',
    #'function',
    'args',
    #'return',
    'value',
    'type',
    'iterator',
    'condition',
    'step',
    #'varRet',
    'print',
    'void',
    'integer',
    'float'
)

tokens = (
    'NUMBER',
    'IDENTIFIER',
    'ADD_OP',
    'MUL_OP',
    'EQ_OP',
    'NEQ_OP',
    'CMP_OP',
    'NEWLINE',
    'STRING',
    'APOSTROPHE',
    'CHEVRON_OP_VAR',
    'OPEN_IF',
    'CLOSE_ONELINE',
    'CLOSE_IF',
    'CLOSE_ELSE',
    'OPEN_ELSE',
    'EGAL',
    'OPEN_WHILE',
    'CLOSE_WHILE',
    'OPEN_FOR',
    'CLOSE_FOR',
    'OPEN_PROG',
    'CLOSE_PROG',
    'OPEN_CALL'
) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '(),'


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_CLOSE_ONELINE(t):
    r'\/>'
    return t


def t_ADD_OP(t):
    r'[+-]'
    return t


def t_MUL_OP(t):
    r'[*/]'
    return t


def t_CHEVRON_OP_VAR(t):
    r'\<variable'
    return t


def t_OPEN_CALL(t):
    r'\<callFunction'
    return t


def t_OPEN_PROG(t):
    r'\<program'
    return t


def t_CLOSE_PROG(t):
    r'\<\/program>'
    return t


def t_OPEN_WHILE(t):
    r'\<while'
    return t


def t_CLOSE_WHILE(t):
    r'\<\/while>'
    return t


def t_OPEN_FOR(t):
    r'\<for'
    return t


def t_CLOSE_FOR(t):
    r'\<\/for>'
    return t


def t_OPEN_IF(t):
    r'\<if'
    return t

def t_CLOSE_IF(t):
    r'\<\/if>'
    return t

def t_OPEN_ELSE(t):
    r'\<else\/>'
    return t

def t_CLOSE_ELSE(t):
    r'\<\/else>'
    return t


def t_CMP_OP(t):
    r'[<>]'
    return t


def t_EQ_OP(t):
    r'=='
    return t


def t_EGAL(t):
    r'='
    return t


def t_NEQ_OP(t):
    r'!='
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
        t.value = 0
    return t


def t_STRING(t):
    r'".+"'
    return t


def t_APOSTROPHE(t):
    r'\''
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore  = ' \t'


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)

lex.lex()


if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print("Line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))