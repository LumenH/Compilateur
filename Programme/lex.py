import ply.lex as lex

'''Définition des lexèmes utilisés'''
reserved_words = (
    'while',
    'for',
    'callFunction',
    'if'
    'function',
    'programme',
    'name',
    'args',
    'return',
    'variable',
    'value',
    'type',
    'void',
    'integer',
    'float',
    'iterator',
    'condition',
    'step',
    'varRet',
    'else',
)
tokens = (
    'NUMBER',
    'IDENTIFIER',
    'ADD_OP',
    'MUL_OP',
    'EGAL',
    'OPEN_LT'#<
    'CLOSE_GT',#>
    'APOSTROPHE',
    'GUILLEMET'
)+tuple(map(lambda s:s.upper(), reserved_words))

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value=float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s !"%(t.lineno,t.value))
        t.value = 0
    return t

def t_ADD_OP(t):
    r'[+-]'
    return t

def t_MUL_OP(t):
    r'[*/]'
    return t

def t_EGAL(t):
    r'[=]'
    return t

def t_APOSTROPHE(t):
    r'\'[A-Za-z"]+\''
    return t

def t_GUILLEMET(t):
    r'\"[A-Za-z]+\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'"%repr(t.value[0]))
    t.lexer.skip(1)

lex.lex()

if __name__=="__main__":
    import sys
    prog = open(sys.argv[1].read())

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)"%(tok.lineno, tok.type, tok.value))
