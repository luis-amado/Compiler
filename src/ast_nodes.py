from dataclasses import dataclass, field

@dataclass
class ASTNode:
    line: int = field(default=None, kw_only=True, repr=False)
    column: int = field(default=None, kw_only=True, repr=False)

@dataclass
class IdentifierNode(ASTNode):
    value :str
@dataclass
class ArrayDeclarationNode(ASTNode):
    identifier: IdentifierNode
    size: int

@dataclass
class VarDeclarationNode(ASTNode):
    identifiers: list[IdentifierNode]
    arrays: list[ArrayDeclarationNode]
    var_type: str
@dataclass
class IfNode(ASTNode):
    condition: any
    code_blocks: any
    else_blocks: any = None

@dataclass
class WhileNode(ASTNode):
    condition: any
    code_blocks: any

@dataclass
class ForNode(ASTNode):
    initialization: any
    condition: any
    step: any
    code_blocks: any

@dataclass 
class WriteNode(ASTNode):
    exp: any

@dataclass
class AssignmentNode(ASTNode):
    identifier: IdentifierNode
    value: any
@dataclass
class BeginEndNode(ASTNode):
    code_blocks: list[IfNode | WhileNode | ForNode | WriteNode | AssignmentNode]
@dataclass
class ProcedureNode(ASTNode):
    procedure_name: IdentifierNode
    begin_end: BeginEndNode
@dataclass
class ProgramNode(ASTNode):
    var_declarations: list[VarDeclarationNode]
    procedures: list[ProcedureNode]
    begin_end: BeginEndNode

@dataclass
class IntNode(ASTNode):
    value: int

@dataclass
class FloatNode(ASTNode):
    value: float

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class BoolNode(ASTNode):
    value: bool

@dataclass
class CharNode(ASTNode):
    value: str

@dataclass
class OperationNode(ASTNode):
    valueLeft: any
    operator: str
    valueRight: any

@dataclass
class UnitaryOpNode(ASTNode):
    operator: str
    value: any

#para el uso o acceso de las variables
@dataclass
class VariableNode(ASTNode):
    name: str
    array_index: any = None
    step_operator: str = None

@dataclass
class StepOperatorNode(ASTNode):
    type: str

@dataclass
class ArrayIndexNode(ASTNode):
    index: any

@dataclass
class FunctionCallNode(ASTNode):
    name: str
