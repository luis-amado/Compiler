import code

from lark import tree, exceptions as lark_exceptions
from run_test_cases import test_cases
import Parser.parser as parser
from Semantic.semantic_analyzer import semantic_analysis
from AST.ast_tree import ASTTransformer

def main():
  parse_tree = parser.parse_file("code.txt")
  # tree.pydot__tree_to_png(parse_tree, "tree.png")
  ast = ASTTransformer().transform(parse_tree)
  semantic_analysis(ast)
  
if __name__ == "__main__":
  main()
