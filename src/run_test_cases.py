from pathlib import Path
import compiler

def run_test_pass(file):
  if compiler.compile_file_quads(file) is not None:
    print("Test case passed: ", file)
    return True
  else:
    print("\033[31mTest case failed: \033[0m", file)
    return False

def run_test_fail(file):
  if compiler.compile_file_quads(file) is None:
    print("Test case passed: ", file)
    return True
  else:
    print("\033[31mTest case failed (was accepted): \033[0m", file)
    return False

def run_test_suite(directory, test_func):
  fail_count = 0
  for file in Path(directory).iterdir():
    if not test_func(file): fail_count += 1
  return fail_count

def test_cases():
  professor_folder = "tests/professor"
  success_folder = "tests/success"
  fail_folder = "tests/fail"

  total_fails = 0

  total_fails += run_test_suite(professor_folder, run_test_pass)
  total_fails += run_test_suite(success_folder, run_test_pass)
  total_fails += run_test_suite(fail_folder, run_test_fail)

  if total_fails > 0:
    print("\033[31m", total_fails, f" TEST{"S" if total_fails > 1 else ""} FAILED.\033[0m", sep="")
  else:
    print("\033[32mALL TESTS PASSED\033[0m")

def main():
  test_cases()

if __name__ == "__main__":
  main()