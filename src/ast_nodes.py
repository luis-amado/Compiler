from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Union

@dataclass
class ASTNode:
    line: Optional[int] = field(default=None, kw_only=True, repr=False)
    column: Optional[int] = field(default=None, kw_only=True, repr=False)

@dataclass
class IdentifierNode(ASTNode):
    value: str

# --- Value Nodes ---

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
    valueLeft: ExpressionNode
    operator: str
    valueRight: ExpressionNode

@dataclass
class UnitaryOpNode(ASTNode):
    operator: str
    value: ExpressionNode

@dataclass
class StepOperatorNode(ASTNode):
    type: str

@dataclass
class ArrayIndexNode(ASTNode):
    index: ExpressionNode

@dataclass
class VariableNode(ASTNode):
    name: str
    array_index: Optional[ArrayIndexNode] = None
    step_operator: Optional[StepOperatorNode] = None

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    args: list[ExpressionNode] = field(default_factory=list)

# --- Control Flow & Statement Nodes ---

@dataclass
class IfNode(ASTNode):
    condition: ExpressionNode
    code_blocks: list[StatementNode]
    else_blocks: Optional[list[StatementNode]] = None

@dataclass
class WhileNode(ASTNode):
    condition: ExpressionNode
    code_blocks: list[StatementNode]

@dataclass
class ForNode(ASTNode):
    initialization: AssignmentNode
    condition: ExpressionNode
    step: Union[AssignmentNode, VariableNode]
    code_blocks: list[StatementNode]

@dataclass 
class WriteNode(ASTNode):
    exp: ExpressionNode

@dataclass
class AssignmentNode(ASTNode):
    identifier: IdentifierNode
    value: ExpressionNode

# --- Structure Nodes ---

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
class BeginEndNode(ASTNode):
    code_blocks: list[StatementNode]

@dataclass
class ProcedureNode(ASTNode):
    procedure_name: IdentifierNode
    begin_end: BeginEndNode

@dataclass
class ProgramNode(ASTNode):
    var_declarations: list[VarDeclarationNode]
    procedures: list[ProcedureNode]
    begin_end: BeginEndNode

# --- The Union Type Definitions ---

ExpressionNode = Union[
    IntNode, FloatNode, StringNode, BoolNode, CharNode, 
    VariableNode, FunctionCallNode, OperationNode, UnitaryOpNode
]

StatementNode = Union[
    IfNode, WhileNode, ForNode, WriteNode, AssignmentNode, 
    ExpressionNode, BeginEndNode
]