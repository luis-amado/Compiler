from __future__ import annotations
from dataclasses import dataclass
import AST.ast_nodes as nodes

@dataclass
class Variable:
    name: str

Constant = int | float | str | bool
Operand = Variable | Constant | None

@dataclass
class Quadruple:
    operator: str
    operand1: Operand
    operand2: Operand
    result: int | Variable | None

def generate_quadruples(program: nodes.ProgramNode) -> list[Quadruple]:
    quadruples: list[Quadruple] = []
    available_temps = []
    new_temp = 0

    function_addresses = {}
    
    def temp():
        nonlocal new_temp
        if len(available_temps) > 0:
            return Variable(available_temps.pop())
        else:
            new_temp += 1
            return Variable(f"#{new_temp}")
    
    def is_temp(v: Operand):
        if not isinstance(v, Variable): return False

        return v.name.startswith("#") 

    def gen_q(operator, operand1, operand2, result):
        nonlocal quadruples
        quadruples.append(Quadruple(operator, operand1, operand2, result))
        if is_temp(operand1):
            available_temps.append(operand1.name)
        if is_temp(operand2):
            available_temps.append(operand2.name)
        return len(quadruples) - 1
    
    def fill_jump(index, address):
        nonlocal quadruples
        quadruples[index].result = address
    
    def curr_address():
        return len(quadruples) - 1
    
    def generate_expression(exp: nodes.ExpressionNode, value_used: bool = True) -> Operand:
        if isinstance(exp, nodes.LiteralNode):
            return exp.value
        elif isinstance(exp, nodes.VariableNode):
            var = Variable(exp.name.value)
            if exp.step_operator is not None:
                op = exp.step_operator.type[0]
                if value_used:
                    temp_value = temp()
                    gen_q(":=", var, None, temp_value)
                    gen_q(op, var, 1, var)
                    return temp_value
                else:
                    gen_q(op, var, 1, var)
            return var
        elif isinstance(exp, nodes.OperationNode):
            operand1 = generate_expression(exp.valueLeft)
            operand2 = generate_expression(exp.valueRight)
            temp_result = temp()
            gen_q(exp.operator, operand1, operand2, temp_result)
            return temp_result
        elif isinstance(exp, nodes.UnitaryOpNode):
            operand = generate_expression(exp.value)
            temp_result = temp()
            gen_q(exp.operator, operand, None, temp_result)
            return temp_result
    
    def generate_code_blocks(code_blocks: list[nodes.CodeBlockNode]):
        for node in code_blocks:
            if isinstance(node, nodes.WriteNode):
                gen_q("write", generate_expression(node.exp), None, None)
            elif isinstance(node, nodes.AssignmentNode):
                gen_q(":=", generate_expression(node.value), None, Variable(node.identifier.value))
            elif isinstance(node, nodes.ExpressionNode):
                generate_expression(node, value_used=False)
            elif isinstance(node, nodes.IfNode):
                first_jump = gen_q("gotof", generate_expression(node.condition), None, None)
                generate_code_blocks(node.code_blocks)
                if node.else_blocks is not None:
                    final_jump = gen_q("goto", None, None, None)
                    fill_jump(first_jump, curr_address() + 1)
                    generate_code_blocks(node.else_blocks)
                    fill_jump(final_jump, curr_address() + 1)
                else:
                    fill_jump(first_jump, curr_address() + 1)
            elif isinstance(node, nodes.WhileNode):
                condition_jump = curr_address() + 1; # Jump to the start of the calculation for the condition
                jump_to_end = gen_q("gotof", generate_expression(node.condition), None, None)
                generate_code_blocks(node.code_blocks)
                gen_q("goto", None, None, condition_jump)
                fill_jump(jump_to_end, curr_address() + 1)
            elif isinstance(node, nodes.ForNode):
                generate_code_blocks([node.initialization])
                condition_jump = curr_address() + 1  # Jump to the start of the calculation for the condition
                jump_to_end = gen_q("gotof", generate_expression(node.condition), None, None)
                generate_code_blocks(node.code_blocks)
                generate_code_blocks([node.step])
                gen_q("goto", None, None, condition_jump)
                fill_jump(jump_to_end, curr_address() + 1)
            elif isinstance(node, nodes.FunctionCallNode):
                gen_q("call", None, None, function_addresses[node.name.value])
            
    default_values = {
        "int": 0,
        "float": 0.0,
        "string": "",
        "char": "\0",
        "bool": False,
    }

    # Initialize variables
    for var_declaration in program.var_declarations:
        for identifier in var_declaration.identifiers:
            gen_q(":=", default_values[var_declaration.var_type], var_declaration.var_type, Variable(identifier.value))

    # Functions
    jump_to_start = -1
    if len(program.procedures) > 0:
        jump_to_start = gen_q("goto", None, None, None)
    
    for procedure in program.procedures:
        function_addresses[procedure.procedure_name.value] = curr_address() + 1
        generate_code_blocks(procedure.begin_end.code_blocks)
        gen_q("return", None, None, None)

    # Main code block
    if jump_to_start > -1:
        fill_jump(jump_to_start, curr_address() + 1)
    generate_code_blocks(program.begin_end.code_blocks)

    gen_q("end", None, None, None)
    
    return quadruples

def print_quadruples(quadruples: list[Quadruple]):
    def parse(op: Operand):
        if op is None:
            return ""
        elif isinstance(op, Variable):
            return op.name
        elif isinstance(op, bool):
            return "true" if op else "false"
        else:
            return op

    print(f"{" ":>3} {'Op':>7} {'Op1':>7} {'Op2':>7} {'Res':>7}")

    for i, q in enumerate(quadruples):
        print(f"{i:>3} {q.operator.upper():>7} {parse(q.operand1):>7} {parse(q.operand2):>7} {parse(q.result):>7}")