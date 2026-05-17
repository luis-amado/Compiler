from lark import Token, Tree, tree
from ast_tree import ASTTransformer
from run_test_cases import test_cases
import parser

def semantic_analysis(tree):
  # INT = "I"
  # FLOAT = "F"
  # BOOL = "B"
  # STRING = "S"
  # CHAR = "C"
  # SEMANTIC_ERROR = "X"
  # NONE

  # If a type combo is not included, all are considered to be errors (eg, string and int)
  semantic_rules = {
  # op1,op2,     +,   *-,  /%,  ><,  ==,  &|
    ('I', 'I'): ('I', 'I', 'F', 'B', 'B', 'X'),
    ('I', 'F'): ('F', 'F', 'F', 'B', 'B', 'X'),
    ('F', 'I'): ('F', 'F', 'F', 'B', 'B', 'X'),
    ('S', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('S', 'C'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('C', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('B', 'B'): ('X', 'X', 'X', 'X', 'B', 'B'),
  }

  unary_semantic_rules = {
    #    -,  !
    'I': ('I', 'X'),
    'F': ('F', 'X'),
    'B': ('X', 'B')
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

  parse_tree = parser.parse_file("code.txt")
  tree.pydot__tree_to_png(parse_tree, "tree.png")
  print(parse_tree.pretty())
  semantic_analysis(parse_tree)

  ast = ASTTransformer().transform(parse_tree)
  print(ast)
    
  
if __name__ == "__main__":
  main()