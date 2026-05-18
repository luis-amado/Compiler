from dataclasses import dataclass

#para las declaraciones de variables
@dataclass
class VarDeclarationNode:
    identifiers: list[str] 
    var_type: str
@dataclass
class IfNode:
    condition: any
    code_blocks: any
    else_blocks: any = None

@dataclass
class WhileNode:
    condition: any
    code_blocks: any

@dataclass
class ForNode:
    initialization: any
    condition: any
    step: any
    code_blocks: any

@dataclass 
class WriteNode:
    exp: any

@dataclass
class AssignmentNode:
    identifier: str
    value: any
@dataclass
class BeginEndNode:
    code_blocks: list[IfNode | WhileNode | ForNode | WriteNode | AssignmentNode]
@dataclass
class ProcedureNode:
    procedure_name: str
    begin_end: BeginEndNode
@dataclass 
class ProgramNode:
    var_declarations: list[VarDeclarationNode]
    procedures: list[ProcedureNode]
    begin_end: BeginEndNode

@dataclass
class IntNode:
    value: int

@dataclass
class FloatNode:
    value: float

@dataclass
class StringNode:
    value: str

@dataclass
class BoolNode:
    value: bool

@dataclass
class CharNode:
    value: str

@dataclass
class OperationNode:
    valueLeft: any
    operator: str
    valueRight: any

@dataclass
class UnitaryOpNode:
    operator: str
    value: any

#para el uso o acceso de las variables
@dataclass
class VariableNode:
    name: str
    array_index: any = None
    step_operator: str = None

@dataclass
class StepOperatorNode:
    type: str

@dataclass
class ArrayIndexNode:
    index: any

@dataclass
class FunctionCallNode:
    name: str
