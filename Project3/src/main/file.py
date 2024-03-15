import os

def get_file_name_without_extension():
    return "3.if_statement"

def get_test_folder_path():
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)
    test_dir = os.path.dirname(current_directory)
    test_dir = os.path.join(test_dir, os.path.join("test", "live var"))
    return test_dir

def get_file_path_without_extension():
    path =  os.path.join(get_test_folder_path(), get_file_name_without_extension())
    return path

def read():
    with open(os.path.join(get_test_folder_path(),get_file_name_without_extension())+".smpl", 'r') as f:
        return f.read()