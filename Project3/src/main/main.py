import os

import parser
import tokenizer
from symbol_table import symbol_table

def read():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, './test1.smpl'), 'r') as f:
        return f.read()

def main(): 
    sentence = read()#"main \n var var1, var2;\n  var var3, var4;   \n function ident(var1, var2);"
    #sentence = input("Enter your expression: ")
    _tokenizer = tokenizer.Tokenizer(sentence)
    table = symbol_table()

    parser.init(_tokenizer, table)
    print("Successfully Compiled\n")
    
    pass

if __name__ == "__main__":
    main()
