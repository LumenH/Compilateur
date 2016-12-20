import ply.yacc as yacc
import AST
from lex import tokens


def p_programme_statement(p):
    '''programme : statement'''
    p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    '''statement : assignation
        | structure'''
    p[0] = p[1]

def p_statement_print(p):
    '''statement : PRINT expression'''
    p[0] = AST.PrintNode(p[2])


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP')
)

def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_expression_ltgt(p):
    '''expression : '<' expression '>' '''
    p[0] = p[2]


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])


def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Parsing returned no result!")
