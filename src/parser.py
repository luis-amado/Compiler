from lark import Lark

def get_parser():
  with open("grammar.lark", 'r') as grammar_file:
    return Lark(grammar_file.read(), parser="lalr", lexer="basic", propagate_positions=True)

def parse_file(path):
  parser = get_parser()
  with open(path, 'r') as code_file:
    return parser.parse(code_file.read())
