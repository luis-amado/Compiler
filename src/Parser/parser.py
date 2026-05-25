from lark import Lark, exceptions
from pathlib import Path

class SyntaxError(Exception):
  pass

GRAMMAR_PATH = Path(__file__).resolve().parent.parent.parent / "grammar.lark"
PROJECT_ROOT = GRAMMAR_PATH.parent

parser = None

error_token_terminals = {
  "lbrace": "{",
  "rbrace": "}",
  "lpar": "(",
  "rpar": ")",
  "lessthan": "<",
  "morethan": ">",
  "slash": "/",
  "minus": "-",
  "star": "*",
  "percent": "%",
  "plus": "+",
  "semicolon": ";",
}

def syntax_error(error: exceptions.LarkError):
  if isinstance(error, exceptions.UnexpectedToken):
    expected_str = ""
    i = 0

    # Forgot to close parenthesis to expression
    if "RPAR" in error.accepts:
      raise SyntaxError(f"Unexpected token '{error.token}' in line {error.line}, expected ')' to close expression.")

    raise SyntaxError(f"Unexpected token '{error.token}' in line {error.line}.")
  
  elif isinstance(error, exceptions.UnexpectedCharacters):
    raise SyntaxError(f"Unexpected character in line {error.line}:\n\n{error._context}")
  else:
    raise SyntaxError(error)

def get_parser():
  global parser
  if parser is None:
    with open(GRAMMAR_PATH, 'r') as grammar_file:
      parser = Lark(grammar_file.read(), parser="lalr", lexer="basic", propagate_positions=True)
  return parser

def parse_file(path):
  parser = get_parser()
  file_path = Path(path)
  if not file_path.is_absolute():
    file_path = PROJECT_ROOT / file_path
  with open(file_path, 'r') as code_file:
    try:
      return parser.parse(code_file.read())
    except exceptions.LarkError as e:
      syntax_error(e)

def parse_code(code):
  parser = get_parser()
  try:
    return parser.parse(code)
  except exceptions.LarkError as e:
    syntax_error(e)
