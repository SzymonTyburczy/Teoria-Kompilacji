# AST Node Classes

class Node(object):
    def __str__(self):
        return self.printTree()


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssignExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class IfElse(Node):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class WhileLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForLoop(Node):
    def __init__(self, variable, range_expr, body):
        self.variable = variable
        self.range = range_expr
        self.body = body


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Break(Node):
    pass


class Continue(Node):
    pass


class Return(Node):
    def __init__(self, value=None):
        self.value = value


class Print(Node):
    def __init__(self, args):
        self.args = args if isinstance(args, list) else [args]


class InstructionList(Node):
    def __init__(self):
        self.instructions = []

    def add(self, instruction):
        self.instructions.append(instruction)


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args if isinstance(args, list) else [args]


class Transpose(Node):
    def __init__(self, expr):
        self.expr = expr


class Negation(Node):
    def __init__(self, expr):
        self.expr = expr


class ArrayRef(Node):
    def __init__(self, array, indices):
        self.array = array
        self.indices = indices if isinstance(indices, list) else [indices]


class MatrixInit(Node):
    def __init__(self, rows):
        self.rows = rows


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class Error(Node):
    def __init__(self):
        pass