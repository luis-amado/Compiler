from lark import Lark
from pathlib import Path

# def test_cases(tree):
#   folder_path = Path("tests")
#   for file in folder_path.iterdir():
#       with open(file, 'r') as test_file_code:
#         tree.parse(test_file_code.read())

def main():

  with open("grammar.lark", 'r') as grammar_file:
    l = Lark(grammar_file.read())
  
  # test_cases(l)

  with open("code.txt", 'r') as code_file:
    print(l.parse(code_file.read()))

if __name__ == "__main__":
  main()