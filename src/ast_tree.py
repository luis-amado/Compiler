from curses import meta

from lark import Transformer, Token, Tree, v_args
from ast_nodes import *

# Helper methods

# Get the value of a single token
def _get_token_value(token):
    if isinstance(token, Token):
        return token.value
    if isinstance(token, Tree) and token.children:
        return _get_token_value(token.children[0])
    return None

def _extract_nested(token):
    if isinstance(token, Tree):
        return _extract_nested(token.children[0])
    return token

def _filter_items_by_type(items, type):
    return [i for i in items if isinstance(i, type)]

def _handle_expression(tokens, meta):
    if len(tokens) == 1:
        return _extract_nested(tokens[0])

    else:
        op = OperationNode(_extract_nested(tokens[0]), _get_token_value(tokens[1]), _extract_nested(tokens[2]), line=meta.line, column=meta.column)
        for i in range(3, len(tokens), 2):
            op = OperationNode(op, _get_token_value(tokens[i]), _extract_nested(tokens[i+1]), line=meta.line, column=meta.column)
        return op

class ASTTransformer(Transformer):

    @v_args(meta=True)
    def start(self, meta, items):
        var_declarations = _filter_items_by_type(items, VarDeclarationNode)
        procedures = _filter_items_by_type(items, ProcedureNode)
        begin_end = _filter_items_by_type(items, BeginEndNode)[0]
        return ProgramNode(var_declarations, procedures, begin_end, line=meta.line, column=meta.column)
    
    def INT(self, token):
        return IntNode(int(token), line=token.line, column=token.column)
    
    def FLOAT(self, token):
        return FloatNode(float(token), line=token.line, column=token.column)
    
    def CHAR(self, token):
        return CharNode(str(token)[1:-1].encode().decode('unicode_escape'), line=token.line, column=token.column)

    def STRING(self, token):
        return StringNode(str(token)[1:-1].encode().decode('unicode_escape'), line=token.line, column=token.column)
    
    def IDENTIFIER(self, token):
        return IdentifierNode(_get_token_value(token), line=token.line, column=token.column)
    
    @v_args(meta=True)
    def bool(self, meta, token):
        return BoolNode(_get_token_value(token[0]) == "true", line=meta.line, column=meta.column)
    
    @v_args(meta=True)
    def assignment(self, meta, tokens):
        return AssignmentNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), line=meta.line, column=meta.column)
    
    @v_args(meta=True)
    def write(self, meta, tokens):
        return WriteNode(_extract_nested(tokens[0]), line=meta.line, column=meta.column)

    @v_args(meta=True)
    def factor(self, meta, tokens):
        if len(tokens) == 1:
            return _extract_nested(tokens[0])
        else:
            return UnitaryOpNode(_get_token_value(tokens[0]), _extract_nested(tokens[1]), line=meta.line, column=meta.column)
    
    @v_args(meta=True)
    def variable(self, meta, tokens):
        if len(tokens) == 1:
            return VariableNode(_extract_nested(tokens[0]), line=meta.line, column=meta.column)
        elif isinstance(tokens[1], StepOperatorNode):
            return VariableNode(_extract_nested(tokens[0]), tokens[1], line=meta.line, column=meta.column)
    """
    @v_args(meta=True)
    def variable(self, meta, tokens):
        if len(tokens) == 1:
            return VariableNode(_extract_nested(tokens[0]), line=meta.line, column=meta.column)
        elif isinstance(tokens[1], StepOperatorNode):
            return VariableNode(_extract_nested(tokens[0]), None, tokens[1], line=meta.line, column=meta.column)
    """
    @v_args(meta=True)
    def step_operator(self, meta, tokens):
        return StepOperatorNode(_get_token_value(tokens[0]), line=meta.line, column=meta.column)

    @v_args(meta=True)
    def function_call(self, meta, tokens):
        return FunctionCallNode(_extract_nested(tokens[0]), line=meta.line, column=meta.column)
    
    @v_args(meta=True)
    def relative_expression(self, meta, tokens):
        return _handle_expression(tokens, meta)
    
    @v_args(meta=True)
    def additive_expression(self, meta, tokens):
        return _handle_expression(tokens, meta)

    @v_args(meta=True)
    def multiplicative_expression(self, meta, tokens):
        return _handle_expression(tokens, meta)
        
    @v_args(meta=True)
    def if_(self, meta, tokens):
        if len(tokens) == 2:
            return IfNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), line=meta.line, column=meta.column)
        else:
            return IfNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), _extract_nested(tokens[2]), line=meta.line, column=meta.column)
        
    @v_args(meta=True)
    def while_(self, meta, tokens):
        return WhileNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), line=meta.line, column=meta.column)
    
    @v_args(meta=True)
    def for_stmt(self, meta, tokens):
        return ForNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), _extract_nested(tokens[2]), _extract_nested(tokens[3]), line=meta.line, column=meta.column)
    
    @v_args(meta=True)
    def begin(self, meta, tokens):
        return BeginEndNode(tokens, line=meta.line, column=meta.column)
    
    def block(self, tokens):
        return tokens
    
    @v_args(meta=True)
    def var_declaration(self, meta, tokens):
        identifiers = [_extract_nested(identifier_token) for identifier_token in tokens[:-1]]
        type_ = _get_token_value(tokens[-1])
        return VarDeclarationNode(identifiers, type_, line=meta.line, column=meta.column)

    """
    @v_args(meta=True)
    def var_declaration(self, meta, tokens):
        identifiers = []
        for identifier_token in tokens[:-1]:
            if isinstance(identifier_token):
                identifiers.append(_extract_nested(identifier_token.identifier))
            else:
                identifiers.append(_extract_nested(identifier_token))
        type = _get_token_value(tokens[-1])

        return VarDeclarationNode(identifiers, type, line=meta.line, column=meta.column)
        """
    
    @v_args(meta=True)
    def procedure(self, meta, tokens):
        return ProcedureNode(_extract_nested(tokens[0]), tokens[1], line=meta.line, column=meta.column)
