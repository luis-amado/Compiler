from pathlib import Path
import compiler
import Quadruples.interpreter as interpreter

def case_passed(file):
  print("Test case passed: ", file)
  return True

def case_failed(file, suffix = ""):
  if suffix != "": suffix = " " + suffix
  print(f"\033[31mTest case failed{suffix}: \033[0m", file)
  return False

def run_test_pass(file):
  if compiler.compile_file(file) is not None:
    return case_passed(file)
  else:
    return case_failed(file)

def run_test_fail(file):
  if compiler.compile_file(file) is None:
    return case_passed(file)
  else:
    return case_failed(file, "(was accepted)")

def run_test_with_results(file):
  with open(file, "r") as file_content:
    program, results = file_content.read().split("###")
    quads = compiler.compile_code(program, show_error=True)
    if quads == None:
      return case_failed(file, "(did not compile)")
    actual_results = interpreter.interpret_silent(quads) # Interpret without printning results
    expected_results = results.split("\n")[1:]
    for i in range(len(expected_results)):
      act = str(actual_results[i]) if i < len(actual_results) else None
      if expected_results[i] != act:
        return case_failed(file, f"(expected '{expected_results[i]}' got {f"'{act}'" if act is not None else None})")
    return case_passed(file)

def run_test_suite(directory, test_func):
  print(f"Running test suite: {directory}")
  fail_count = 0
  for file in Path(directory).iterdir():
    if not test_func(file): fail_count += 1
  print("")
  return fail_count

def test_cases():
  professor_folder = "tests/professor"
  success_folder = "tests/success"
  fail_folder = "tests/fail"
  results_folder = "tests/results"

  total_fails = 0

  total_fails += run_test_suite(professor_folder, run_test_pass)
  total_fails += run_test_suite(success_folder, run_test_pass)
  total_fails += run_test_suite(fail_folder, run_test_fail)
  total_fails += run_test_suite(results_folder, run_test_with_results)

  if total_fails > 0:
    print("\033[31m", total_fails, f" TEST{"S" if total_fails > 1 else ""} FAILED.\033[0m", sep="")
  else:
    print("\033[32mALL TESTS PASSED\033[0m")

def main():
  test_cases()

if __name__ == "__main__":
  main()