from ast_tree import ASTTransformer, ProgramNode

class SemanticError(Exception):
  pass

def semantic_analysis(ast: ProgramNode, print_fn = print):
  semantic_rules = {
  # op1,op2,     +,   *-,  /%,  ><,  ==,  &|
    ('I', 'I'): ('I', 'I', 'I', 'B', 'B', 'X'),
    ('I', 'F'): ('F', 'F', 'F', 'B', 'B', 'X'),
    ('F', 'I'): ('F', 'F', 'F', 'B', 'B', 'X'),
    ('S', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('C', 'C'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('S', 'C'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('C', 'S'): ('S', 'X', 'X', 'X', 'B', 'X'),
    ('B', 'B'): ('X', 'X', 'X', 'X', 'B', 'B'),
  }

  unary_semantic_rules = {
    #    -,  !,     --++,   
    'I': ('I', 'X', 'I'),
    'F': ('F', 'X', 'F'),
    'B': ('X', 'B', 'X'),
  }

  # Name, location in memory, type (no arrays any more)

  symbol_table = {}
  last_address = 0

  # Variable declarations
  for var_declaration in ast.var_declarations:
    for identifier in var_declaration.identifiers:
      if identifier.value in symbol_table:
        raise SemanticError(f"Redefinition of identifier: {identifier.value} on line {identifier.line}")
      symbol_table[identifier.value] = (last_address, var_declaration.var_type)
      last_address += 1
  
  # Procedure declarations
  for procedure in ast.procedures:
    if procedure.procedure_name.value in symbol_table:
      raise SemanticError(f"Redefinition of identifier: {procedure.procedure_name.value} on line {procedure.procedure_name.line}")
    symbol_table[procedure.procedure_name.value] = (-1, "procedure")

      
  print_fn(symbol_table)