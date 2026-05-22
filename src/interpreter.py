from quadruple_generator import Quadruple, Operand, Variable
from dataclasses import dataclass

"""
Operators list:
<
>
<=
>=
==
+
- (double and unary)
*
/
%
and
or
not (unary)
write
goto
gotof
end
call
return
"""

@dataclass
class Symbol:
  type: str
  value: any

def interpret(quadruples: list[Quadruple]):

  symbols: dict[str, Symbol] = {}
  jump_stack = []

  def set_value(symbol, value):
    if symbol not in symbols:
      symbols[symbol] = Symbol("temp", value)
      return
    
    s = symbols[symbol]
    if s.type == "int": 
      s.value = int(value)
    elif s.type == "float": 
      s.value = float(value)
    elif s.type == "char": 
      s.value = str(value)[0]
    elif s.type == "string": 
      s.value = str(value)
    elif s.type == "bool": 
      s.value = bool(value)
    else: s.value = value

  def get_value(operand: Operand):
    if isinstance(operand, Variable):
      return symbols[operand.name].value
    else:
      return operand
  
  def simple_op(op, op1, op2):
    if op == "+": return op1 + op2
    elif op == "*": return op1 * op2
    elif op == "/": 
      if isinstance(op1, int) and isinstance(op2, int):
        return op1 // op2;
      return op1 / op2
    elif op == "%": return op1 % op2
    elif op == "<": return op1 < op2
    elif op == ">": return op1 > op2
    elif op == "<=": return op1 <= op2
    elif op == ">=": return op1 >= op2
    elif op == "==": return op1 == op2
    elif op == "!=": return op1 != op2
    elif op == "and": return op1 and op2
    elif op == "or": return op1 or op2

  i = 0
  while not quadruples[i].operator == "end":
    op = quadruples[i].operator
    q = quadruples[i]
    if op == "write":
      print(get_value(q.operand1))
    elif op == "goto":
      i = q.result
      continue
    elif op == "gotof":
      if not get_value(q.operand1):
        i = q.result
        continue
    elif op == "call":
      jump_stack.append(i + 1)
      i = q.result
      continue
    elif op == "return":
      i = jump_stack.pop()
      continue
    elif op == ":=":
      if q.operand2 is not None:
        # Variable initialization
        symbols[q.result.name] = Symbol(q.operand2, get_value(q.operand1))
      else:
        set_value(q.result.name, get_value(q.operand1))
    elif op == "-":
      if q.operand2 is not None:
        set_value(q.result.name, get_value(q.operand1) - get_value(q.operand2))
      else:
        # Unary minus
        set_value(q.result.name, get_value(q.operand1) * -1)
    elif op == "not":
      # Unary not
      set_value(q.result.name, not get_value(q.operand1))
    else: set_value(q.result.name, simple_op(op, get_value(q.operand1), get_value(q.operand2)))
    i += 1
