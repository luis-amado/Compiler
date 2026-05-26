from Parser.parser import parse_file, SyntaxError
from Semantic.semantic_analyzer import semantic_analysis, SemanticError
from Quadruples.quadruple_generator import generate_quadruples, print_quadruples
from Quadruples.interpreter import interpret
from AST.ast_tree import ASTTransformer
import sys
import os

def handle_error(error, err_type):
  print(f"\033[31m{err_type}: {error}\033[0m")

def compile_file(file_path: str):
  if not os.path.isfile(file_path):
    print(f"File '{file_path}' not found")
    return 1

  try:
    parse_tree = parse_file(file_path)
    ast = ASTTransformer().transform(parse_tree)
    semantic_analysis(ast)
    quadruples = generate_quadruples(ast)
  except SyntaxError as e:
    handle_error(e, "Syntax Error")
    return 1
  except SemanticError as e:
    handle_error(e, "Semantic Error")
    return 1

  interpret(quadruples)
  return 0

def compile_file_quads(file_path: str, show_error: bool = False):
  if not os.path.isfile(file_path):
    print(f"File '{file_path}' not found")
    return None

  try:
    parse_tree = parse_file(file_path)
    ast = ASTTransformer().transform(parse_tree)
    semantic_analysis(ast)
    quadruples = generate_quadruples(ast)
  except SyntaxError as e:
    if show_error: handle_error(e, "Syntax Error")
    return None
  except SemanticError as e:
    if show_error: handle_error(e, "Semantic Error")
    return None
  
  return quadruples

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
  
  quadruples = compile_file_quads(sys.argv[1], show_error=True)
  if quadruples == None:
    sys.exit(1)

  if "-q" in sys.argv or "--quads" in sys.argv:
    print("\n\nGenerated quadruple table:\n")
    print_quadruples(quadruples)
  
if __name__ == "__main__":
  main()
