import sys
from os.path import isfile

from parser import Parser

from GUI import CompWindow

READ_MODE = "r"

def main(argv):
    code, rc = '', 1
    file_name = ''
    message = ''
    if len(argv) == 2:
        file_name = argv[1].split("/").pop()
        code, rc = read_file(argv[1])

    if 1 == rc:
        message = f'File: "{file_name}" not found'
    elif 2 == rc:
        message = 'Invalid extension'

    window = CompWindow(message, code)
    window.start_window()



def read_file(file_path) -> tuple:
    code_str = ""
    r_c = 0
    if isfile(file_path):
        if file_path.endswith(".c"):
            with open(file_path, READ_MODE, encoding='utf-8') as file:
                code_str = file.read()
        else:
            r_c = 2
    else:
        r_c = 1

    return (code_str, r_c)

if __name__ == "__main__":
    main(sys.argv)
