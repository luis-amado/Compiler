from lark import exceptions
from pathlib import Path
import sys
from parser import get_parser

def run_test_pass(file, parser):
  with open(file, 'r') as code:
    try:
      parser.parse(code.read())
      print("Test case passed: ", file)
      return True
    except exceptions.LarkError as e:
      print("\033[31mTest case failed: \033[0m", file)
      print(e)
      return False

def run_test_fail(file, parser):
  with open(file, 'r') as code:
    try:
      parser.parse(code.read())
      print("\033[31mTest case failed (was accepted): \033[0m")
      return False
    except exceptions.LarkError:
      print("Test case passed: ", file)
      return True

def run_test_suite(directory, test_func, parser):
  fail_count = 0
  for file in Path(directory).iterdir():
    if not test_func(file, parser): fail_count += 1
  return fail_count

def test_cases(parser):
  professor_folder = "tests/professor"
  success_folder = "tests/success"
  fail_folder = "tests/fail"

  total_fails = 0

  total_fails += run_test_suite(professor_folder, run_test_pass, parser)
  total_fails += run_test_suite(success_folder, run_test_pass, parser)
  total_fails += run_test_suite(fail_folder, run_test_fail, parser)

  if total_fails > 0:
    print("\033[31m", total_fails, f" TEST{"S" if total_fails > 1 else ""} FAILED.\033[0m", sep="")
  else:
    print("\033[32mALL TESTS PASSED\033[0m")

def main():
  parser = get_parser()
  test_cases(parser)

if __name__ == "__main__":
  main()