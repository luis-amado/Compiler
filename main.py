from lark import Lark, tree, exceptions
from pathlib import Path
import pydot

def test_cases(parser):
  folder_path = Path("tests")
  for file in folder_path.iterdir():
      with open(file, 'r') as test_file_code:
        try:
          parser.parse(test_file_code.read())
        except exceptions.LarkError as e:
          print("Failed on file: ", file)
          print(e)


def main():

  with open("grammar.lark", 'r') as grammar_file:
    l = Lark(grammar_file.read(), parser="lalr", lexer="basic")
  
  test_cases(l)

  with open("code.txt", 'r') as code_file:
    parse_tree = l.parse(code_file.read())
    tree.pydot__tree_to_png(parse_tree, "tree.png")
    print(parse_tree)
  

if __name__ == "__main__":
  main()