# ------------------------------------------------------------
# based on examples from http://www.dabeaz.com/ply/ply.html
#
# parser for tiger
# ------------------------------------------------------------
import logging
import ply.yacc as yacc
from lex import tokens, Lexer
from Node import Node

logging.basicConfig(level=logging.DEBUG)

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
        '''program : exps
                   | decs'''
        p[0] = p[1]
        logging.debug(p[:])
    
    def p_exps(p):
        '''exps : exp SEMICOLON exps
                | exp'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('exps', p[1], p[2])
        logging.debug(p[:])
    
    def p_exp_control(p):
        '''exp : IF LPAREN exp RPAREN THEN exp 
               | IF LPAREN exp RPAREN THEN exp ELSE exp
               | WHILE exp DO exp
               | BREAK
               | FOR exp TO exp DO exp
               | LET decs IN exps END''' 
        if p[1] == 'if' and len(p) != 7:
            p[0] = Node('if_else', [p[6], p[8]], p[3])
        elif p[1] == 'for':
            p[0] = Node('for', [p[2], p[4], p[6]], p[8])
        # if without else & while
        else:
            p[0] = Node(p[1], p[6], p[3])
        logging.debug(p[:])
    
    
    def p_exp_literal(p):
        '''exp : INTEGER
               | STRING
               | NIL
               | ID var'''
        p[0] = p[1]
    
    def p_var(p):
        '''var : DOT ID
               | LSQPAREN exp RSQPAREN
               | DOT ID var
               | LSQPAREN exp RSQPAREN var'''
        if p[1] == '.':
            if len(p) == 3:
                p[0] = Node('field',p[2])
            elif len(p) == 4:
                p[0] = Node('fields',p[2],p[3])
        elif p[1] == '[' and len(p) == 4:
            p[0] = Node('array_idx',p[2])
        else:
            p[0] = Node('array_idxs',p[2],p[4])
        logging.debug(p[:])
    
    def p_exp_binop(p):
        '''exp : exp PLUS exp
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
        if p[2] == '+'  : p[0] = p[1] + p[3]
        elif p[2] == '-': p[0] = p[1] - p[3]
        elif p[2] == '*': p[0] = p[1] * p[3]
        elif p[2] == '/': p[0] = p[1] / p[3]
        else:
            p[0] = Node("binop", [p[1],p[3]], p[2])
        logging.debug(p[:])
    
    
    def p_decs(p):
        '''decs : decs dec
                | dec'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('decs',p[1],p[2])
        logging.debug(p[:])
    
    def p_dec(p):
        '''dec : TYPE ID EQ type
               | vardec
               | FUNCTION ID LPAREN tyfields RPAREN EQ exp
               | FUNCTION ID LPAREN tyfields RPAREN
               | PRIMITIVE ID LPAREN tyfields RPAREN'''
        p[0] = p[2]
        logging.debug(p[:])
    
    def p_type(p):
        '''type : ID
                | array
                | record'''
        if p[1] == 'record':
            p[0] = Node('record', p[1]) 
        elif p[1] == 'array':
            p[0] = Node('array', p[1])
        else:
            p[0] = Node('ID', p[1])
        logging.debug(p[:])
    
    def p_record(p):
        'record : LBRACE tyfields RBRACE'
        p[0] = Node('record', p[2]) 
        logging.debug(p[:])
    
    def p_array(p):
        '''array : ARRAY OF ID
                 | ID LSQPAREN exp RSQPAREN OF exp'''
        if len(p) <= 4:
            p[0] = Node('array', p[2]) 
        else:
            p[0] = Node('array_dec',p[3],p[6])
        logging.debug(p[:])
    
    def p_vardec(p):
        '''vardec : VAR ID ASSIGN exp
                  | VAR ID COLON ID ASSIGN exp'''
        if len(p)==5:
            p[0] = Node('assign',p[2],p[4]);
        else:
            p[0] = Node('assign_type',p[2],p[4],p[6])
        logging.debug(p[:])
    
    def p_tyfields(p):
        '''tyfields : tyfields COMMA tyfield
                   | tyfield'''
        if len(p) == 4:
            p[0] = Node('tyfields',p[1],p[3])
        else:
            p[0] = p[1]
        logging.debug(p[:])
    
    def p_tyfield(p):
        'tyfield : ID COLON ID'
        p[0] = Node('tyfield',p[1],p[3])
        logging.debug(p[:])
    
    
    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")
        logging.debug('--------%s',p)
    
    
    return yacc.yacc()
