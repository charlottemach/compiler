import sys, getopt
from lex import Lexer

def main(argv):
    if len(sys.argv) < 2:
        print("Missing arguments. \nUsage: python lex_test.py <code file>")
        sys.exit()
    
    lexer = Lexer()
    
    with open(sys.argv[1], 'r') as file:
        data = file.read()
    
    print(data)
    lexer.input(data)
     
    for tok in lexer:
        print(tok)


if __name__ == "__main__":
   main(sys.argv[1:])



