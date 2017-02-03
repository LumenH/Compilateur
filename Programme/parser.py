import ply.yacc as yacc
from lex import tokens
import AST


vars = {}


# def p_executable(p):
#     ''' executable : fonction newline '''
#     p[0] = AST.ExecutableNode(p[1])
#
#
# def p_executable_recursif(p):
#     ''' executable : function newline executable '''
#     p[0] = AST.ExecutableNode([p[1]] + p[3].children)


def p_program_statement(p):
    '''   programme : statement '''
    p[0] = AST.ProgramNode(p[1])


def p_program_recursive(p):
    ''' programme : statement programme'''
    p[0] = AST.ProgramNode([p[1]] + p[2].children)


def p_program_state(p):
    ''' prog : OPEN_PROG NAME EGAL APOSTROPHE STRING APOSTROPHE CLOSE_ONELINE programme CLOSE_PROG'''
    p[0] = AST.ProgNode(p[5], p[8])



def p_expression_string(p):
    ''' expression : STRING '''
    p[0] = AST.TokenNode(p[1])



def p_expression_var_or_num(p):
    ''' expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])


def p_expression_op(p):
    ''' expression : expression ADD_OP expression
            | expression MUL_OP expression
            | expression CMP_OP expression
            | expression EQ_OP expression
            | expression NEQ_OP expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_statement(p):
    ''' statement : assignation
            | structure
            | prog '''
    p[0] = p[1]



def p_statement_newline(p):
    ''' statement : NEWLINE '''
    p[0] = AST.Node()


def p_assign(p):
    '''assignation : CHEVRON_OP_VAR NAME EGAL APOSTROPHE expression APOSTROPHE VALUE EGAL APOSTROPHE expression APOSTROPHE TYPE EGAL APOSTROPHE type APOSTROPHE CLOSE_ONELINE '''
    p[0] = AST.AssignNode([p[5], p[10]])


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS '''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_structure_for(p):
    ''' structure : OPEN_FOR ITERATOR EGAL APOSTROPHE expression APOSTROPHE CONDITION EGAL APOSTROPHE expression APOSTROPHE STEP EGAL APOSTROPHE expression APOSTROPHE CLOSE_ONELINE programme CLOSE_FOR'''
    p[0] = AST.ForNode([p[5], p[10], p[15], p[18]])


def p_structure_while(p):
    ''' structure : OPEN_WHILE CONDITION EGAL APOSTROPHE expression APOSTROPHE CLOSE_ONELINE programme CLOSE_WHILE '''
    p[0] = AST.WhileNode([p[5], p[8]])


def p_type_stat(p):
    ''' type : VOID
        | STRING
        | INTEGER
        | FLOAT '''


def p_condition(p):
    ''' statement : OPEN_IF CONDITION EGAL APOSTROPHE expression APOSTROPHE CLOSE_ONELINE programme CLOSE_IF'''
    p[0] = AST.CondNode([p[5], p[8]])


def p_condition_else(p):
    '''statement : OPEN_IF CONDITION EGAL APOSTROPHE expression APOSTROPHE CLOSE_ONELINE programme CLOSE_IF OPEN_ELSE programme CLOSE_ELSE'''
    p[0] = AST.CondNode([p[5], p[8], p[11]])


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Syntax error : unexpected end of file !")

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated', debug=0)

if __name__ == "__main__":
    import sys
    print("Parsing ....")
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    if result:
        print(result)
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("Wrote ast to " + name)
    else:
        print("Parsing return no result!")