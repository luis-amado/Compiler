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
class VariableNode(ASTNode):
    name: IdentifierNode
    step_operator: Optional[StepOperatorNode] = None

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    args: list[ExpressionNode] = field(default_factory=list)

# --- Control Flow & Statement Nodes ---

@dataclass
class IfNode(ASTNode):
    condition: ExpressionNode
    code_blocks: list[CodeBlockNode]
    else_blocks: Optional[list[CodeBlockNode]] = None

@dataclass
class WhileNode(ASTNode):
    condition: ExpressionNode
    code_blocks: list[CodeBlockNode]

@dataclass
class ForNode(ASTNode):
    initialization: StatementNode
    condition: ExpressionNode
    step: StatementNode
    code_blocks: list[CodeBlockNode]

@dataclass 
class WriteNode(ASTNode):
    exp: ExpressionNode

@dataclass
class AssignmentNode(ASTNode):
    identifier: IdentifierNode
    value: ExpressionNode

# --- Structure Nodes ---

@dataclass
class VarDeclarationNode(ASTNode):
    identifiers: list[IdentifierNode]
    var_type: str

@dataclass
class BeginEndNode(ASTNode):
    code_blocks: list[CodeBlockNode]

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

LiteralNode = Union[
    IntNode, FloatNode, StringNode, BoolNode, CharNode
]

ExpressionNode = Union[
    LiteralNode, VariableNode, OperationNode, UnitaryOpNode
]

StatementNode = Union[
    WriteNode, AssignmentNode, FunctionCallNode, ExpressionNode
]

CodeBlockNode = Union[
    IfNode, WhileNode, ForNode, StatementNode
]