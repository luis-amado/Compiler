from lark import Transformer
from ast_nodes import *

class ASTTransformer(Transformer):
    def start (self, items):
        return items
    
    def INT(self, token):
        return IntNode(int(token))
    
    def FLOAT(self, token):
        return FloatNode(float(token))
    
    def CHAR(self, token):
        return CharNode(str(token)[1:-1].encode().decode('unicode_escape'))

    def STRING(self, token):
        return StringNode(str(token)[1:-1].encode().decode('unicode_escape'))
    
    def BOOL(self, token):
        return BoolNode(str(token) == "true")
    
    def assignment(self, tokens):
        return AssignmentNode(str(tokens[0]), tokens[1])
    
    def write(self, tokens):
        return WriteNode(tokens[0])

    def factor(self, tokens):
        if len(tokens) == 1:
            return tokens[0]
        else:
            return UnitaryOpNode(str(tokens[0]), tokens[1])
    
    def variable(self, tokens):
        return VariableNode(str(tokens[0]))
    
    def additive_expression(self, tokens):
        if len(tokens) == 1:
            return tokens[0]
    
        else:
            op = OperationNode(tokens[0], str(tokens[1]), tokens[2])
            for i in range(3, len(tokens), 2):
                op = OperationNode(op, str(tokens[i]), tokens[i+1])
            return op

    def multiplicative_expression(self, tokens):
        if len(tokens) == 1:
            return tokens[0]
        
        else:
            op = OperationNode(tokens[0], str(tokens[1]), tokens[2])
            for i in range(3, len(tokens), 2):
                op = OperationNode(op, str(tokens[i]), tokens[i+1])
            return op
        
    def if_(self, tokens):
        if len(tokens) == 2:
            return IfNode(tokens[0], tokens[1])
        else:
            return IfNode(tokens[0], tokens[1], tokens[2])
        
    def while_(self, tokens):
        return WhileNode(tokens[0], tokens[1])
    
    def for_stmt(self, tokens):
        return ForNode(tokens[0], tokens[1], tokens[2], tokens[3])
    
    def begin(self, tokens):
        return BeginEndNode(tokens)
    
    def block(self, tokens):
        return tokens
    
    def var_declaration(self, tokens):
        return VarNode(tokens[:-1], tokens[-1])
    
    def procedure(self, tokens):
        return ProcedureNode(str(tokens[0]), tokens[1])

