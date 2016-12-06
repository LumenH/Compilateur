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
    'DIV_OP',
    'EGAL',
    'OPEN_LT'
    'CLOSE_GT',
    'APOSTROPHE',
    'GUILLEMET'

)
