import parser
import tokenizer
from symbol_table import symbol_table
import file


def main():
    sentence = file.read()
    _tokenizer = tokenizer.Tokenizer(sentence)
    table = symbol_table()
    parser.init(_tokenizer, table)
    print("Successfully Compiled\n")
    
    return 

if __name__ == "__main__":
    main()
