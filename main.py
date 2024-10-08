import sys
from os.path import isfile

from parser import Parser
READ_MODE = "r"

def main(argv):
    code, rc = read_file(argv[1])
    file_name = argv[1].split("/").pop()

    if not rc:
        parser = Parser(code)
        print(parser.parse())
    elif rc == 1:
        print(f'File: "{file_name}" not found')
    elif rc == 2:
        print(f'File extension "{file_name.split(".").pop()}" not correct')


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
