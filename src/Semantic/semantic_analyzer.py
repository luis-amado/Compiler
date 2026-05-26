from AST.ast_nodes import *

class SemanticError(Exception):
  pass

# Type codes:
# I = int, F = float, S = string, C = char, B = bool, X = invalid
SEMANTIC_RULES = {
  # op1, op2     +,  *-,  /%,  ><,  ==,  &|
  ('I', 'I'): ('I', 'I', 'I', 'B', 'B', 'X'),
  ('I', 'F'): ('F', 'F', 'F', 'B', 'B', 'X'),
  ('F', 'I'): ('F', 'F', 'F', 'B', 'B', 'X'),
  ('F', 'F'): ('F', 'F', 'F', 'B', 'B', 'X'),
  ('S', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
  ('C', 'C'): ('S', 'X', 'X', 'X', 'B', 'X'),
  ('S', 'C'): ('S', 'X', 'X', 'X', 'X', 'X'),
  ('C', 'S'): ('S', 'X', 'X', 'X', 'X', 'X'),
  ('B', 'B'): ('X', 'X', 'X', 'X', 'B', 'B'),
}

UNARY_SEMANTIC_RULES = {
  #       -,  not, --++
  'I': ('I', 'X', 'I'),
  'F': ('F', 'X', 'F'),
  'B': ('X', 'B', 'X'),
}

OPERATOR_INDEX = {
  '+': 0,
  '-': 1,
  '*': 1,
  '/': 2,
  '%': 2,
  '>': 3,
  '<': 3,
  '>=': 3,
  '<=': 3,
  '==': 4,
  '!=': 4,
  'and': 5,
  'or': 5,
}

UNARY_OPERATOR_INDEX = {
  '-': 0,
  'not': 1,
}

TYPE_TO_CODE = {
  "int": "I",
  "float": "F",
  "string": "S",
  "char": "C",
  "bool": "B",
}

CODE_TO_TYPE = {
  "I": "int",
  "F": "float",
  "S": "string",
  "C": "char",
  "B": "bool",
}

def semantic_analysis(ast: ProgramNode):
  symbol_table = {}

  register_variables(ast.var_declarations, symbol_table)
  register_procedures(ast.procedures, symbol_table)

  analyze_block(ast.begin_end, symbol_table)

  for procedure in ast.procedures:
    analyze_block(procedure.begin_end, symbol_table)
    
  return symbol_table

def register_variables(var_declarations, symbol_table):
  for var_declaration in var_declarations:
    for identifier in var_declaration.identifiers:
      name = identifier.value

      if name in symbol_table:
        raise SemanticError(f"Redefinition of identifier: {name} on line {identifier.line}")

      symbol_table[name] = var_declaration.var_type

def register_procedures(procedures, symbol_table):
  for procedure in procedures:
    name = procedure.procedure_name.value

    if name in symbol_table:
      raise SemanticError(
        f"Redefinition of identifier: {name} on line {procedure.procedure_name.line}"
      )

    symbol_table[name] = "procedure"

def analyze_block(block, symbol_table):
  for statement in block.code_blocks:
    analyze_statement(statement, symbol_table)

def analyze_statement(statement, symbol_table):
  if isinstance(statement, AssignmentNode):
    analyze_assignment(statement, symbol_table)
  elif isinstance(statement, WriteNode):
    analyze_expression(statement.exp, symbol_table)
  elif isinstance(statement, IfNode):
    analyze_if(statement, symbol_table)
  elif isinstance(statement, WhileNode):
    analyze_while(statement, symbol_table)
  elif isinstance(statement, ForNode):
    analyze_for(statement, symbol_table)
  elif isinstance(statement, FunctionCallNode):
    analyze_function_call(statement, symbol_table)
  elif isinstance(statement, VariableNode):
    analyze_step(statement, symbol_table)
  else:
    raise SemanticError(f"Unsupported statement on line {statement.line}")

def analyze_assignment(assignment, symbol_table):
  variable_name = assignment.identifier.value

  if variable_name not in symbol_table:
    raise SemanticError(
      f"Use of undeclared variable: {variable_name} on line {assignment.identifier.line}"
    )

  variable_type = symbol_table[variable_name]

  if variable_type == "procedure":
    raise SemanticError(
      f"Cannot assign to procedure: {variable_name} on line {assignment.identifier.line}"
    )

  expression_type = analyze_expression(assignment.value, symbol_table)

  if not types_are_assignment_compatible(variable_type, expression_type):
    raise SemanticError(
      f"Type mismatch in assignment to variable '{variable_name}' on line "
      f"{assignment.identifier.line}: cannot assign {expression_type} to {variable_type}"
    )
  
def analyze_if(if_node, symbol_table):
  condition_type = analyze_expression(if_node.condition, symbol_table)

  if condition_type != "bool":
    raise SemanticError(
      f"If condition must be of type bool, got {condition_type} on line {if_node.line}"
    )

  for statement in if_node.code_blocks:
    analyze_statement(statement, symbol_table)

  if if_node.else_blocks is not None:
    for statement in if_node.else_blocks:
      analyze_statement(statement, symbol_table)

def analyze_while(while_node, symbol_table):
  condition_type = analyze_expression(while_node.condition, symbol_table)

  if condition_type != "bool":
    raise SemanticError(
      f"While condition must be of type bool, got {condition_type} on line {while_node.line}"
    )

  for statement in while_node.code_blocks:
    analyze_statement(statement, symbol_table)

def analyze_for(for_node, symbol_table):
  analyze_statement(for_node.initialization, symbol_table)

  condition_type = analyze_expression(for_node.condition, symbol_table)
  if condition_type != "bool":
    raise SemanticError(
      f"For loop condition must be of type bool, got {condition_type} on line {for_node.line}"
    )

  analyze_statement(for_node.step, symbol_table)

  for statement in for_node.code_blocks:
    analyze_statement(statement, symbol_table)


def analyze_step(variable_node, symbol_table):
  if variable_node.step_operator is None:
    analyze_expression(variable_node, symbol_table)
    return

  variable_name = variable_node.name.value

  if variable_name not in symbol_table:
    raise SemanticError(
      f"Use of undeclared variable: {variable_name} on line {variable_node.line}"
    )

  variable_type = symbol_table[variable_name]

  if variable_type not in ("int", "float"):
    raise SemanticError(
      f"Cannot use {variable_node.step_operator.type} on {variable_type} "
      f"on line {variable_node.line}"
    )

def analyze_function_call(function_call, symbol_table):
  function_name = function_call.name.value

  if function_name not in symbol_table:
    raise SemanticError(
      f"Call to undeclared function: {function_name} on line {function_call.line}"
    )

  symbol_type = symbol_table[function_name]

  if symbol_type != "procedure":
    raise SemanticError(f"{function_name} is not a function on line {function_call.line}")

def analyze_expression(expression, symbol_table):
  if isinstance(expression, IntNode):
    return "int"
  elif isinstance(expression, FloatNode):
    return "float"
  elif isinstance(expression, StringNode):
    return "string"
  elif isinstance(expression, CharNode):
    return "char"
  elif isinstance(expression, BoolNode):
    return "bool"
  elif isinstance(expression, VariableNode):
    return analyze_variable(expression, symbol_table)
  elif isinstance(expression, OperationNode):
    return analyze_operation(expression, symbol_table)
  elif isinstance(expression, UnitaryOpNode):
    return analyze_unary_operation(expression, symbol_table)
  elif isinstance(expression, FunctionCallNode):
    raise SemanticError(
      f"Function calls cannot be used as expressions on line {expression.line}"
    )

  raise SemanticError(f"Unsupported expression on line {expression.line}")

def analyze_variable(variable_node, symbol_table):
  variable_name = variable_node.name.value

  if variable_name not in symbol_table:
    raise SemanticError(
      f"Use of undeclared variable: {variable_name} on line {variable_node.name.line}"
    )

  variable_type = symbol_table[variable_name]

  if variable_type == "procedure":
    raise SemanticError(
      f"Procedure {variable_name} cannot be used as a variable on line {variable_node.line}"
    )

  if variable_node.step_operator is not None:
    analyze_step(variable_node, symbol_table)

  return variable_type

def analyze_operation(operation, symbol_table):
  left_type = analyze_expression(operation.valueLeft, symbol_table)
  right_type = analyze_expression(operation.valueRight, symbol_table)
  operator = operation.operator

  left_code = type_to_code(left_type)
  right_code = type_to_code(right_type)

  if (left_code, right_code) not in SEMANTIC_RULES:
    raise_invalid_operation(operation, left_type, right_type)

  result_code = SEMANTIC_RULES[(left_code, right_code)][OPERATOR_INDEX[operator]]

  if result_code == "X":
    raise_invalid_operation(operation, left_type, right_type)

  return code_to_type(result_code)

def analyze_unary_operation(operation, symbol_table):
  operand_type = analyze_expression(operation.value, symbol_table)
  operand_code = type_to_code(operand_type)

  if operand_code not in UNARY_SEMANTIC_RULES:
    raise SemanticError(
      f"Invalid operation: {operation.operator} {operand_type} on line {operation.line}"
    )

  result_code = UNARY_SEMANTIC_RULES[operand_code][UNARY_OPERATOR_INDEX[operation.operator]]

  if result_code == "X":
    raise SemanticError(
      f"Invalid operation: {operation.operator} {operand_type} on line {operation.line}"
    )

  return code_to_type(result_code)

def raise_invalid_operation(operation, left_type, right_type):
  raise SemanticError(
    f"Invalid operation: {left_type} {operation.operator} {right_type} "
    f"on line {operation.line}"
  )

def type_to_code(type_name):
  return TYPE_TO_CODE[type_name]

def code_to_type(type_code):
  return CODE_TO_TYPE[type_code]

def types_are_assignment_compatible(variable_type, expression_type):
  if variable_type == expression_type:
    return True

  return {variable_type, expression_type} == {"int", "float"}
