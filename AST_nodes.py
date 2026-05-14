from dataclasses import dataclass

@dataclass 
class ProgramNode:
    var_declarations: list
    procedures: list
    begin_end: any

@dataclass
class VarNode:
    identifier: list 
    var_type: str

@dataclass
class ProcedureNode:
    procedure_name: str
    begin_end: any

@dataclass
class BeginEndNode:
    code_block: list

@dataclass
class IfNode:
    exp: any
    code_block: any
    else_block: any = None

@dataclass
class WhileNode:
    exp: any
    code_block: any

@dataclass
class ForNode:
    inicialization: any
    condition: any
    step: any
    code_block: any

@dataclass 
class WriteNode:
    exp: any

@dataclass
class AssignmentNode:
    identifier: str
    value: any

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

@dataclass
class VariableNode:
    name: str




