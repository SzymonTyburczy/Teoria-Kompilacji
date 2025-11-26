from __future__ import print_function
import AST

def addToClass(cls):
    """Decorator to add methods to existing classes"""
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


# Add printTree methods to AST Node classes

@addToClass(AST.Node)
def printTree(self, indent=0):
    raise Exception("printTree not defined in class " + self.__class__.__name__)


@addToClass(AST.IntNum)
def printTree(self, indent=0):
    print("| " * indent + str(self.value))


@addToClass(AST.FloatNum)
def printTree(self, indent=0):
    print("| " * indent + str(self.value))


@addToClass(AST.String)
def printTree(self, indent=0):
    print("| " * indent + '"' + self.value + '"')


@addToClass(AST.Variable)
def printTree(self, indent=0):
    print("| " * indent + self.name)


@addToClass(AST.BinExpr)
def printTree(self, indent=0):
    print("| " * indent + self.op)
    self.left.printTree(indent + 1)
    self.right.printTree(indent + 1)


@addToClass(AST.RelExpr)
def printTree(self, indent=0):
    print("| " * indent + self.op)
    self.left.printTree(indent + 1)
    self.right.printTree(indent + 1)


@addToClass(AST.AssignExpr)
def printTree(self, indent=0):
    print("| " * indent + self.op)
    self.left.printTree(indent + 1)
    self.right.printTree(indent + 1)


@addToClass(AST.IfElse)
def printTree(self, indent=0):
    print("| " * indent + "IF")
    self.condition.printTree(indent + 1)
    print("| " * indent + "THEN")
    self.if_body.printTree(indent + 1)
    if self.else_body:
        print("| " * indent + "ELSE")
        self.else_body.printTree(indent + 1)


@addToClass(AST.WhileLoop)
def printTree(self, indent=0):
    print("| " * indent + "WHILE")
    self.condition.printTree(indent + 1)
    self.body.printTree(indent + 1)


@addToClass(AST.ForLoop)
def printTree(self, indent=0):
    print("| " * indent + "FOR")
    self.variable.printTree(indent + 1)
    self.range.printTree(indent + 1)
    self.body.printTree(indent + 1)


@addToClass(AST.Range)
def printTree(self, indent=0):
    print("| " * indent + "RANGE")
    self.start.printTree(indent + 1)
    self.end.printTree(indent + 1)


@addToClass(AST.Break)
def printTree(self, indent=0):
    print("| " * indent + "BREAK")


@addToClass(AST.Continue)
def printTree(self, indent=0):
    print("| " * indent + "CONTINUE")


@addToClass(AST.Return)
def printTree(self, indent=0):
    print("| " * indent + "RETURN")
    if self.value:
        self.value.printTree(indent + 1)


@addToClass(AST.Print)
def printTree(self, indent=0):
    print("| " * indent + "PRINT")
    for arg in self.args:
        arg.printTree(indent + 1)


@addToClass(AST.InstructionList)
def printTree(self, indent=0):
    for instr in self.instructions:
        instr.printTree(indent)


@addToClass(AST.FunctionCall)
def printTree(self, indent=0):
    print("| " * indent + self.name.upper())
    for arg in self.args:
        arg.printTree(indent + 1)


@addToClass(AST.Transpose)
def printTree(self, indent=0):
    print("| " * indent + "TRANSPOSE")
    self.expr.printTree(indent + 1)


@addToClass(AST.Negation)
def printTree(self, indent=0):
    print("| " * indent + "-")
    self.expr.printTree(indent + 1)


@addToClass(AST.ArrayRef)
def printTree(self, indent=0):
    print("| " * indent + "REF")
    self.array.printTree(indent + 1)
    for idx in self.indices:
        idx.printTree(indent + 1)


@addToClass(AST.MatrixInit)
def printTree(self, indent=0):
    print("| " * indent + "VECTOR")
    for row in self.rows:
        if len(row) == 1:
            row[0].printTree(indent + 1)
        else:
            print("| " * (indent + 1) + "VECTOR")
            for elem in row:
                elem.printTree(indent + 2)


@addToClass(AST.Vector)
def printTree(self, indent=0):
    print("| " * indent + "VECTOR")
    for elem in self.elements:
        elem.printTree(indent + 1)


@addToClass(AST.Error)
def printTree(self, indent=0):
    pass