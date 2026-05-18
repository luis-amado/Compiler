from lark import Transformer, Token, Tree
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

def _handle_expression(tokens):
    if len(tokens) == 1:
        return _extract_nested(tokens[0])

    else:
        op = OperationNode(_extract_nested(tokens[0]), _get_token_value(tokens[1]), _extract_nested(tokens[2]))
        for i in range(3, len(tokens), 2):
            op = OperationNode(op, _get_token_value(tokens[i]), _extract_nested(tokens[i+1]))
        return op

class ASTTransformer(Transformer):
    def start (self, items):
        var_declarations = _filter_items_by_type(items, VarDeclarationNode)
        procedures = _filter_items_by_type(items, ProcedureNode)
        begin_end = _filter_items_by_type(items, BeginEndNode)
        return ProgramNode(var_declarations, procedures, begin_end)
    
    def INT(self, token):
        return IntNode(int(token))
    
    def FLOAT(self, token):
        return FloatNode(float(token))
    
    def CHAR(self, token):
        return CharNode(str(token)[1:-1].encode().decode('unicode_escape'))

    def STRING(self, token):
        return StringNode(str(token)[1:-1].encode().decode('unicode_escape'))
    
    def bool(self, token):
        return BoolNode(_get_token_value(token[0]) == "true")
    
    def assignment(self, tokens):
        return AssignmentNode(_get_token_value(tokens[0]), _extract_nested(tokens[1]))
    
    def write(self, tokens):
        return WriteNode(_extract_nested(tokens[0]))

    def factor(self, tokens):
        if len(tokens) == 1:
            return _extract_nested(tokens[0])
        else:
            return UnitaryOpNode(_get_token_value(tokens[0]), _extract_nested(tokens[1]))
    
    def variable(self, tokens):
        if len(tokens) == 1:
            return VariableNode(_get_token_value(tokens[0]))
        elif isinstance(tokens[1], StepOperatorNode):
            return VariableNode(_get_token_value(tokens[0]), None, tokens[1])
        elif isinstance(tokens[1], ArrayIndexNode):
            return VariableNode(_get_token_value(tokens[0]), tokens[1], tokens[2] if len(tokens) > 2 else None)

    def array_index(self, tokens):
        return ArrayIndexNode(_extract_nested(tokens[0]))

    def step_operator(self, tokens):
        return StepOperatorNode(_get_token_value(tokens[0]))

    def function_call(self, tokens):
        return FunctionCallNode(_get_token_value(tokens[0]))
    
    def relative_expression(self, tokens):
        return _handle_expression(tokens)
    
    def additive_expression(self, tokens):
        return _handle_expression(tokens)

    def multiplicative_expression(self, tokens):
        return _handle_expression(tokens)
        
    def if_(self, tokens):
        if len(tokens) == 2:
            return IfNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]))
        else:
            return IfNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), _extract_nested(tokens[2]))
        
    def while_(self, tokens):
        return WhileNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]))
    
    def for_stmt(self, tokens):
        return ForNode(_extract_nested(tokens[0]), _extract_nested(tokens[1]), _extract_nested(tokens[2]), _extract_nested(tokens[3]))
    
    def begin(self, tokens):
        return BeginEndNode(tokens)
    
    def block(self, tokens):
        return tokens
    
    def var_declaration(self, tokens):
        identifiers = [
            _get_token_value(identifier_token)
            for identifier_token in tokens[:-1]
            if isinstance(identifier_token, Token)
        ]
        type = _get_token_value(tokens[-1])

        return VarDeclarationNode(identifiers, type)
    
    def procedure(self, tokens):
        return ProcedureNode(_get_token_value(tokens[0]), tokens[1])

