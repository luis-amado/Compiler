from Parser.parser import parse_file, SyntaxError
from Semantic.semantic_analyzer import semantic_analysis, SemanticError
from Quadruples.quadruple_generator import generate_quadruples, print_quadruples
from Quadruples.interpreter import interpret
from AST.ast_tree import ASTTransformer
import sys
import os

def handle_error(error, err_type):
  print(f"\033[31m{err_type}: {error}\033[0m")
  sys.exit(1)

def main():
  """
    Compile and interpret the provided file

    Usage: compiler.py <file_name>

    -q, --quads: Show the generated quadruples
  """

  if "-h" in sys.argv or "--help" in sys.argv:
    print(main.__doc__)
    sys.exit(1)

  if len(sys.argv) < 2:
    print("Provide a file name to compile")
    sys.exit(1)
  
  file_path = sys.argv[1]
  if not os.path.isfile(file_path):
    print(f"File '{file_path}' not found")
    sys.exit(1)

  try:
    parse_tree = parse_file(file_path)
    ast = ASTTransformer().transform(parse_tree)
    semantic_analysis(ast)
    quadruples = generate_quadruples(ast)
  except SyntaxError as e:
    handle_error(e, "Syntax Error")
  except SemanticError as e:
    handle_error(e, "Semantic Error")

  if "-q" in sys.argv or "--quads" in sys.argv:
    print("\n\nGenerated quadruple table:\n")
    print_quadruples(quadruples)
  else:

    interpret(quadruples)
  
if __name__ == "__main__":
  main()
