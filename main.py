from lark import Lark, tree, exceptions, Token, Tree
from pathlib import Path
import sys

def run_test_pass(file, parser):
  with open(file, 'r') as code:
    try:
      parser.parse(code.read())
      print("Test case passed: ", file)
    except exceptions.LarkError as e:
      print("Test case failed: ", file)
      print(e, file=sys.stderr)

def test_cases(parser):
  professor_folder = "tests/professor"
  success_folder = "tests/success"

  for file in Path(professor_folder).iterdir(): run_test_pass(file, parser)
  for file in Path(success_folder).iterdir(): run_test_pass(file, parser)

def semantic_analysis(tree):
  # INT = "I"
  # FLOAT = "F"
  # BOOL = "B"
  # STRING = "S"
  # CHAR = "C"
  # SEMANTIC_ERROR = "X"

  # If a type combo is not included, all are considered to be errors (eg, string and int)
  semantic_rules = {
  # op1,op2,     +,   *-,  /%,  ><,  ==,  &|!
    ('I', 'I'): ('I', 'I', 'F', 'B', 'B', 'X'),
    ('I', 'F'): ('F', 'F', 'F', 'B', 'B', 'X'),
    ('F', 'I'): ('F', 'F', 'F', 'B', 'B', 'X'),
    ('S', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('S', 'C'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('C', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('B', 'B'): ('X', 'X', 'X', 'X', 'B', 'B'),
  }

  # Name, location in memory, type (ignoring arrays for now)

  symbol_table = {}
  last_address = 0

  # SUPER BAD CODE
  for outer_scope_child in tree.children:
    if outer_scope_child.data == "var_declaration":
      new_symbols = set()
      for child in outer_scope_child.children:
        if isinstance(child, Token) and child.type == "IDENTIFIER":
          if child.value in new_symbols or child.value in symbol_table:
            print(f"SEMANTIC ERROR: Redefined symbol: {child.value}")
            return
          new_symbols.add(child.value)
        elif isinstance(child, Tree) and child.data == "type":
          for symbol in new_symbols:
            symbol_table[symbol] = (last_address, child.children[0].value)
            last_address += 1
  
  for symbol in symbol_table:
    print(symbol, symbol_table[symbol])

def main():

  with open("grammar.lark", 'r') as grammar_file:
    l = Lark(grammar_file.read(), parser="lalr", lexer="basic", propagate_positions=True)
  
  test_cases(l)

  # with open("code.txt", 'r') as code_file:
  #   parse_tree = l.parse(code_file.read())
  #   tree.pydot__tree_to_png(parse_tree, "tree.png")
  #   # print(parse_tree.pretty())
  #   semantic_analysis(parse_tree)
  

if __name__ == "__main__":
  main()