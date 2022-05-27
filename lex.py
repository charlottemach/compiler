# ------------------------------------------------------------
# based on examples from http://www.dabeaz.com/ply/ply.html
#
# tokenizer for tiger
# ------------------------------------------------------------
import ply.lex as lex
 
reserved = {
    'array' : 'ARRAY',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'to' : 'TO',
    'do' : 'DO',
    'let' : 'LET',
    'in' : 'IN',
    'end' : 'END',
    'of' : 'OF',
    'break' : 'BREAK',
    'nil' : 'NIL',
    'function' : 'FUNCTION',
    'var' : 'VAR',
    'type' : 'TYPE',
#    'import' : 'IMPORT',
    'primitive' : 'PRIMITIVE',
}

# List of token names.
tokens = [
    'LPAREN',
    'RPAREN',
    'LSQPAREN',
    'RSQPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COMMA',
    'COLON',
    'DOT',
    'ASSIGN',
    'LT',
    'GT',
    'LEQ',
    'GEQ',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'AND',
    'OR',
    'NOT',
    'EQ',
    'INTEGER',
    'STRING',
    'ID',
#    'COMMENT',
] + list(reserved.values())

def Lexer():
    # Regular expression rules for simple tokens
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_TIMES     = r'\*'
    t_DIVIDE    = r'/'
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LSQPAREN  = r'\['
    t_RSQPAREN  = r'\]'
    t_LBRACE    = r'\{'
    t_RBRACE    = r'\}'
    t_SEMICOLON = r'\;'
    t_COMMA     = r'\,'
    t_COLON     = r'\:'
    t_DOT       = r'\.'
    t_LT        = r'\<'
    t_GT        = r'\>'
    t_LEQ       = r'\<\='
    t_GEQ       = r'\>\='
    t_AND       = r'\&'
    t_OR        = r'\|'
    t_NOT       = r'\<\>'
    t_EQ        = r'\='
    t_ASSIGN    = r'\:\='
     
    def t_INTEGER(t):
        r'\d+'
        #r'0|[1-9][0-9]*'
        t.value = int(t.value)    
        return t

    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')    # Check for reserved words
        return t

    def t_STRING(t):
        r'\"([^\\\"]|(\\.))*\"'
        return t
    
    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
     
    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'
    t_ignore_COMMENT = r'\/\*(\*(?!\/)|[^*])*\*\/'
    
    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    return lex.lex()
