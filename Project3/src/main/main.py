import os

import parser
import tokenizer
from symbol_table import symbol_table

def get_file_name_without_extension():
    return "live_var_nested_while"

def get_test_folder_path():
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)
    test_dir = os.path.dirname(current_directory)
    test_dir = os.path.join(test_dir, os.path.join("test", "live var"))
    return test_dir

def read():
    with open(os.path.join(get_test_folder_path(),get_file_name_without_extension())+".smpl", 'r') as f:
        return f.read()

def main():
    sentence = read()
    _tokenizer = tokenizer.Tokenizer(sentence)
    table = symbol_table()
    parser.init(_tokenizer, table)
    print("Successfully Compiled\n")
    
    return 

if __name__ == "__main__":
    main()
