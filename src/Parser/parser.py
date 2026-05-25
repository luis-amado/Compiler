from lark import Lark
from pathlib import Path

GRAMMAR_PATH = Path(__file__).resolve().parent.parent.parent / "grammar.lark"
PROJECT_ROOT = GRAMMAR_PATH.parent

def get_parser():
  with open(GRAMMAR_PATH, 'r') as grammar_file:
    return Lark(grammar_file.read(), parser="lalr", lexer="basic", propagate_positions=True)

def parse_file(path):
  parser = get_parser()
  file_path = Path(path)
  if not file_path.is_absolute():
    file_path = PROJECT_ROOT / file_path
  with open(file_path, 'r') as code_file:
    return parser.parse(code_file.read())

def parse_code(code):
  parser = get_parser()
  return parser.parse(code)
