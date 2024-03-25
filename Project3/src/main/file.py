import os
import parser
import tokenizer
filename =""
def get_file_name_without_extension():
    global filename
    return filename

def get_test_folder_name():
    return "community"

def run_single_test(filename_="6.redundant_load"):
    global filename 
    filename = filename_
    print(f"File:: {filename} =====> starting ... \n")
    sentence = read()
    _tokenizer = tokenizer.Tokenizer(sentence)
    parser.init(_tokenizer)
    print(f"File:: {filename} =====> Done\n")


def run_tests():
    global filename
    for file in os.listdir(get_test_folder_path()):
        filename,ext = os.path.splitext(file)
        run_single_test(filename)

def get_test_folder_path():
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)
    test_dir = os.path.dirname(current_directory)
    test_dir = os.path.join(test_dir, os.path.join("test", get_test_folder_name()))
    return test_dir

def get_test_dot_folder_path():
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)
    test_dir = os.path.dirname(current_directory)
    test_dir = os.path.join(test_dir, os.path.join("resource", "dot", get_test_folder_name()))
    os.makedirs(test_dir, exist_ok=True)
    
    return test_dir

def get_dot_file_path():
    path = os.path.join(get_test_dot_folder_path(), get_file_name_without_extension())
    return path

def get_file_path_without_extension():
    path =  os.path.join(get_test_folder_path(), get_file_name_without_extension())
    return path

def read():
    with open(os.path.join(get_test_folder_path(),get_file_name_without_extension())+".smpl", 'r') as f:
        return f.read()

# def write_graph(graph_str):

