import Parser.parser as parser
import Semantic.semantic_analyzer as semantic_analyzer
import Quadruples.quadruple_generator as quadruple_generator
import AST.ast_tree as ast_tree
import Quadruples.interpreter as interpreter

template = """
program main {
DECLARATION
begin;
INIT
    write(EXPRESSION);
end;
}
"""

variables = {
    "a": ("int", 10),
    "b": ("int", 5),
    "c": ("int", 2),
    "d": ("int", 8),
    "e": ("int", 3),
    "f": ("int", 7),
    "g": ("int", 12),
    "h": ("int", 1),
    "f1": ("float", 10.5),
    "f2": ("float", 2.5),
    "f3": ("float", 0.5),
    "f4": ("float", 4.0),
    "x": ("int", 20),
    "y": ("int", 4),
    "z": ("int", 2),
    "s1": ("string", "\"Hello\""),
    "s2": ("string", "\"World\""),
    "s3": ("string", "\" \""),
    "s4": ("string", "\"!\""),
    "w": ("bool", "true"),
    "v": ("bool", "false"),
    "status": ("int", 0),
    "val": ("float", 100.0)
}

# VARIABLES
a = 10
b = 5
c = 2
d = 8
e = 3
f = 7
g = 12
h = 1
f1 = 10.5
f2 = 2.5
f3 = 0.5
f4 = 4.0
x = 20
y = 4
z = 2
s1 = "Hello"
s2 = "World"
s3 = " "
s4 = "!"
w = True
v = False
status = 0
val = 100.0

test_cases = {
    # Arithmetic & Unary
    "a + b": a + b,
    "x - y": x - y,
    "10.0 * 2.5": 10.0 * 2.5,
    "val / 4.0": val / 4.0,
    "15.5 % f2": 15.5 % f2,
    "-f1": -f1,
    "-(f1 + f2)": -(f1 + f2),
    "a + f1 + b + f2": a + f1 + b + f2,
    "10.0 * f3 / 5.0": 10.0 * f3 / 5.0,
    "x % y % z": x % y % z,
    "f1 - f2 - f3": f1 - f2 - f3,
    "1.5 + 2 * 3.0": 1.5 + 2 * 3.0,
    "(f1 + b) * f3": (f1 + b) * f3,
    "10.0 / z - 1.0": 10.0 / z - 1.0,
    "val / (f2 - 0.5)": val / (f2 - 0.5),
    "-5.5 + f1": -5.5 + f1,
    "f1 * -f2": f1 * -f2,
    "f1 + (b - f2)": f1 + (b - f2),
    "(f1 * y) / z": (f1 * y) / z,
    "val - (f1 / 2.0)": val - (f1 / 2.0),

    # String Operations (Using Double Quotes)
    "s1 + s2": s1 + s2,
    "s1 + s3 + s2": s1 + s3 + s2,
    's1 + ""': s1 + "",
    '"" + s4': "" + s4,
    "s1 + s2 + s3 + s4": s1 + s2 + s3 + s4,
    "s1 == s2": s1 == s2,
    "s1 != s2": s1 != s2,
    '(s1 + s2) == "HelloWorld"': (s1 + s2) == "HelloWorld",
    's1 == "Hello"': s1 == "Hello",
    's2 != "World"': s2 != "World",

    # Comparison Logic
    "f1 > a": f1 > a,
    "f3 < f2": f3 < f2,
    "val >= 100.0": val >= 100.0,
    "5.0 <= f2": 5.0 <= f2,
    "f4 == 4.0": f4 == 4.0,
    "f1 != 10.5": f1 != 10.5,
    "(f1 + b) > a": (f1 + b) > a,
    "f3 < (f2 * f3)": f3 < (f2 * f3),
    "a + f1 == 20.5": a + f1 == 20.5,
    "f1 != b + f2": f1 != b + f2,
    "f1 >= a - f3": f1 >= a - f3,
    "(x / z) <= f1": (x / z) <= f1,
    "-f1 > -20.0": -f1 > -20.0,
    "status == -status": status == -status,
    "f1 + f2 != a + b": f1 + f2 != a + b,
    "x * f3 >= z / 1.0": x * f3 >= z / 1.0,
    "(a % z) == 0": (a % z) == 0,
    "(x % z) != 1": (x % z) != 1,
    "val > f1": val > f1,
    "(f1 - b) <= (f2 + f3)": (f1 - b) <= (f2 + f3),

    # Boolean & Logical Precedence
    "not w": not w,
    "not (w or v)": not (w or v),
    "w and v": w and v,
    "w or v": w or v,
    "w and v and w": w and v and w,
    "w or v or w": w or v or w,
    "w and (v or w)": w and (v or w),
    "(w and v) or w": (w and v) or w,
    "not w and v": not w and v,
    "not (w and v)": not (w and v),
    "w or not v": w or not v,
    "(not w) or (not v)": (not w) or (not v),
    "w and not (v or w)": w and not (v or w),
    "not not w": not not w,
    "w and false": w and False,
    "w or (v and w) or v": w or (v and w) or v,
    "(w or v) and (w or v)": (w or v) and (w or v),
    "not (not w or not v)": not (not w or not v),
    "w and v or w and v": w and v or w and v,
    "not w or not v and not w": not w or not v and not w,

    # High Complexity & Mixed
    "f1 + f2 > a - b": f1 + f2 > a - b,
    "(x * f3) == (a + b)": (x * f3) == (a + b),
    "f1 / f2 < a * b": f1 / f2 < a * b,
    "a % y == status": a % y == status,
    "x + 10.0 >= f2 * 8.0": x + 10.0 >= f2 * 8.0,
    "-(f1 + f2) != a": -(f1 + f2) != a,
    "10.5 + 20.0 * f3 > val": 10.5 + 20.0 * f3 > val,
    "(10.5 + 20.0) * f3 > 10.0": (10.5 + 20.0) * f3 > 10.0,
    "a + b + f1 == 25.5": a + b + f1 == 25.5,
    "f1 - f2 - f3 < status": f1 - f2 - f3 < status,
    "a * f2 / b >= f3": a * f2 / b >= f3,
    "val / z != f1 + 80.0": val / z != f1 + 80.0,
    "(a + b) % z == 1": (a + b) % z == 1,
    "x > y + z * f2": x > y + z * f2,
    "(f1 > a) == (z < x)": (f1 > a) == (z < x),
    "-f1 + f2 < -f3 + f4": -f1 + f2 < -f3 + f4,
    "val / 10.0 / 2.0 == 5.0": val / 10.0 / 2.0 == 5.0,
    "f1 * (b + c) <= x / (f2 - f3)": f1 * (b + c) <= x / (f2 - f3),
    "f1 - b > f2 or a + b < x": f1 - b > f2 or a + b < x,
    '(f1 == 10.5) and (w != v)': (f1 == 10.5) and (w != v),
    "not (f1 > a) and (f2 < f4 or w == v)": not (f1 > a) and (f2 < f4 or w == v),
    "f1 + f2 > a and not (b <= c)": f1 + f2 > a and not (b <= c),
    "(f1 * b + a / f2) % f4 == 0.0": (f1 * b + a / f2) % f4 == 0.0,
    "not (w and v) or (f1 > a and f2 < f4)": not (w and v) or (f1 > a and f2 < f4),
    "f1 + f2 + f3 + f4 != a - b - c": f1 + f2 + f3 + f4 != a - b - c,
    "((w or v) and (w or v)) or not w": ((w or v) and (w or v)) or not w,
    "f1 > f2 and f2 > f3 and f3 > f4": f1 > f2 and f2 > f3 and f3 > f4,
    "not (-f1 > f2 + f3)": not (-f1 > f2 + f3),
    "(f1 + f2) * (f2 - f3) / (a % b + 1) == status": (f1 + f2) * (f2 - f3) / (a % b + 1) == status,
    '(s1 + s2 == "HelloWorld") and (f1 + f2 == 13.0)': (s1 + s2 == "HelloWorld") and (f1 + f2 == 13.0)
}

def run_operation_tests():
    global template
    declaration = ""
    intialization = ""
    for var in variables:
        declaration += f"var {var} : {variables[var][0]};\n"
        intialization += f"{var} := {variables[var][1]};\n"
    template = template.replace("DECLARATION", declaration)
    template = template.replace("INIT", intialization)

    fail_count = 0
    for test_case in test_cases:
        try:
            code = template.replace("EXPRESSION", test_case)
            tree = parser.parse_code(code)
            ast = ast_tree.ASTTransformer().transform(tree)
            # semantic_analyzer.semantic_analysis(ast)
            quads = quadruple_generator.generate_quadruples(ast)
            results = interpreter.interpret_silent(quads)
            if results[0] == test_cases[test_case]:
                print(f"TEST PASSED: {test_case}")
            else:
                raise Exception("Incorrect result")
        except Exception as e:
            fail_count += 1
            print(f"\033[31mTEST FAILED: {test_case} ({e})\033[0m")

    if fail_count == 0:
        print("\033[32mALL TESTS PASSED\033[0m")
    else:
        print(f"\033[31m{fail_count} TEST{"S" if fail_count > 1 else ""} FAILED\033[0m")

if __name__ == "__main__":
    run_operation_tests()