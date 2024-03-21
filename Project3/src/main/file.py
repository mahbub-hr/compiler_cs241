import os

def get_file_name_without_extension():
    return "6.nested_while"

def get_test_folder_path():
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)
    test_dir = os.path.dirname(current_directory)
    test_dir = os.path.join(test_dir, os.path.join("test", "standard"))
    return test_dir

def get_test_dot_folder_path():
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)
    test_dir = os.path.dirname(current_directory)
    test_dir = os.path.join(test_dir, os.path.join("resource", "dot", "array"))
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

