import sys 
import pydot
from lex import Lexer
from yacc import Parser

def graph(edges):
    g=pydot.graph_from_edges(edges) 
    print('Writing to output.svg') 
    g.write_svg("output.svg", prog='dot') 
        
def main():
    lexer = Lexer()
    parser = Parser()
    
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
    else:
        print('Usage: python generate_ast.py <tiger file>')
        sys.exit(1)
    print('Parsing ..')
    print(data)
    ast = parser.parse(data,lexer)	
    edges = ast.calculate_edges()
    graph(edges)
        
if __name__:
    main()
