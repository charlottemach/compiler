# ------------------------------------------------------------
# based on examples from http://www.dabeaz.com/ply/ply.html
#
# parser for tiger
# ------------------------------------------------------------
import logging
import ply.yacc as yacc
from lex import tokens, Lexer
from Node import Node

logging.basicConfig(level=logging.DEBUG,format ="[%(lineno)d - %(funcName)s: %(message)s")

precedence = (
    ('nonassoc','DO','IF','OF'),
    ('nonassoc','ELSE'),
    ('nonassoc','ASSIGN'),
    ('nonassoc','AND','OR'),
    ('nonassoc','EQ','NOT','LT','LEQ','GT','GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES','DIVIDE'),
    )

def Parser():
    def p_program(p):
        '''program : exp
                   | decs'''
        p[0] = p[1]
        logging.debug(p[:])

    def p_exp_literal(p):
        '''exp : NIL
               | INTEGER
               | STRING'''
        p[0] = Node('literal', [p[1]])
        logging.debug(p[:])

    def p_exp_typeid(p):
        '''exp : ID LSQPAREN exp RSQPAREN OF exp
               | ID LBRACE idequals RBRACE'''
        if len(p) == 4:
            p[0] = Node('typeid',p[1],p[3])
        else:
            p[0] = Node('typeid',[p[1],p[3],p[6]])
        logging.debug(p[:])

    def p_idequals(p):
        '''idequals : ID EQ exp
                    | ID EQ exp COMMA idequals'''
        if len(p) == 3:
            p[0] = Node('id',[p[1],p[3]])
        else:
            p[0] = Node('id',[p[1],p[3],p[5]])
        logging.debug(p[:])

    def p_exp_lvalue(p):
        '''exp : lvalue
               | lvalue DOT ID LPAREN RPAREN
               | lvalue DOT ID LPAREN exps RPAREN'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 6:
            p[0] = Node('dot',[p[1],p[3]])
        else:
            p[0] = Node('dot',[p[1],p[3],p[5]])
        logging.debug(p[:])
    
    def p_lvalue(p):
        '''lvalue : ID
                  | lvalue DOT ID
                  | lvalue LSQPAREN exp RSQPAREN'''
        if len(p) == 2:
            p[0] = Node('id', [p[1]])
        else:
            p[0] = Node('id',[p[1],p[3]])
        logging.debug(p[:])

    def p_exps(p):
        '''exps : exp SEMICOLON exps
                | exp'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('exps', [p[1], p[3]])
        logging.debug(p[:])

    def p_exp_call(p):
        '''exp : ID LPAREN RPAREN
               | ID LPAREN explist RPAREN'''
        if len(p) == 4:
            p[0] = Node('call', p[1])
        else:
            p[0] = Node('call', [p[1],p[3]])
        logging.debug(p[:])

    def p_explist(p):
        '''explist : exp COMMA explist
                   | exp'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('explist', [p[1], p[3]])
        logging.debug(p[:])

    def p_exp_binop(p):
        '''exp : MINUS exp
               | LPAREN exps RPAREN
               | exp PLUS exp
               | exp MINUS exp
               | exp TIMES exp
               | exp DIVIDE exp
               | exp LT exp
               | exp GT exp
               | exp LEQ exp
               | exp GEQ exp
               | exp AND exp
               | exp OR exp
               | exp NOT exp
               | exp EQ exp '''
        if len(p) == 2:
            p[0] = Node(p[2], [p[1]])
        elif p[1] == '(':
            p[0] = Node('()', [p[2]])
        else:
            p[0] = Node(p[2], [p[1],p[3]])
        logging.debug(p[:])

    def p_exp_assign(p):
        '''exp : lvalue ASSIGN exp'''
        p[0] = Node('assign',[p[1],p[3]])
        logging.debug(p[:])

    def p_exp_control(p):
        '''exp : IF exp THEN exp
               | IF exp THEN exp ELSE exp
               | WHILE exp DO exp
               | BREAK
               | FOR ID ASSIGN exp TO exp DO exp
               | LET decs IN exps END'''
        if p[1] == 'if':
            if len(p) == 6:
                p[0] = Node('if_else', [p[2], p[4], p[6]])
            else:
                p[0] = Node('if', [p[2], p[4]])
        elif p[1] == 'for':
            p[0] = Node('for', [p[2], p[4], p[6], p[8]])
        elif p[1] == 'break':
            p[0] = Node('break', [])
        # let and while
        else:
            p[0] = Node('while', [p[2], p[4]])
        logging.debug(p[:])

    def p_decs(p):
        '''decs : dec decs
                | dec'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('decs',[p[1],p[2]])
        logging.debug(p[:])

    def p_dec(p):
        '''dec : TYPE ID EQ ty
               | vardec'''
        if p[1] == 'type':
            p[0] = Node('type', [p[2]])
        else:
            p[0] = p[1]
        logging.debug(p[:])

    def p_ty(p):
        '''ty : ID
              | ARRAY OF ID
              | LBRACE tyfields RBRACE'''
        if p[1] == '{':
            p[0] = Node('record', [p[2]])
        elif p[1] == 'array':
            p[0] = Node('array', [p[3]])
        else:
            p[0] = Node('ID', [p[1]])
        logging.debug(p[:])

    def p_tyfields(p):
        '''tyfields : tyfield COMMA tyfields
                    | tyfield'''
        if len(p) == 4:
            p[0] = Node('tyfields',[p[1],p[3]])
        else:
            p[0] = p[1]
        logging.debug(p[:])
    
    def p_tyfield(p):
        'tyfield : ID COLON ID'
        p[0] = Node('tyfield',[p[1],p[3]])
        logging.debug(p[:])
    
    def p_dec_fun(p):
        '''dec : FUNCTION ID LPAREN RPAREN EQ exp
               | FUNCTION ID LPAREN RPAREN COLON ID EQ exp
               | FUNCTION ID LPAREN tyfields RPAREN EQ exp
               | FUNCTION ID LPAREN tyfields RPAREN COLON ID EQ exp
               | PRIMITIVE ID LPAREN tyfields RPAREN
               | PRIMITIVE ID LPAREN tyfields RPAREN COLON ID'''
        if len(p) == 6:
            p[0] = Node(p[1], [p[4]])
        elif len(p) == 8:
            p[0] = Node(p[1], [p[2],p[4],p[7]])
        elif len(p) == 9:
            p[0] = Node(p[1], [p[2],p[6],p[8]])
        elif len(p) == 10:
            p[0] = Node(p[1], [p[2],p[4],p[7],p[9]])
        else:
            p[0] = Node(p[1], [p[4]])
        logging.debug(p[:])

    def p_vardec(p):
        '''vardec : VAR ID ASSIGN exp
                  | VAR ID COLON ID ASSIGN exp'''
        if len(p)==5:
            p[0] = Node('assign',[p[2],p[4]]);
        else:
            p[0] = Node('assign_type',[p[2],p[4],p[6]])
        logging.debug(p[:])

    # Error rule for syntax errors
    def p_error(p):
        print(f"Syntax error in line {p.lineno}. Token: {p}.")

    return yacc.yacc()
