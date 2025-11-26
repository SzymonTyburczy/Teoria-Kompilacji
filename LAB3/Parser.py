from sly import Parser
from Scanner import Scanner
import AST


class MParser(Parser):
    tokens = Scanner.tokens

    precedence = (
        ('nonassoc', IF),
        ('nonassoc', ELSE),
        ('right', '=', ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN),
        ('left', '<', '>', LE, GE, EQ, NE),
        ('left', '+', '-', DOTADD, DOTSUB),
        ('left', '*', '/', DOTMUL, DOTDIV),
        ('right', UMINUS),
        ('left', "'"),
    )

    @_('instructions')
    def program(self, p):
        return p.instructions

    @_('instructions instruction')
    def instructions(self, p):
        p.instructions.add(p.instruction)
        return p.instructions

    @_('instruction')
    def instructions(self, p):
        instrs = AST.InstructionList()
        instrs.add(p.instruction)
        return instrs

    @_('')
    def instructions(self, p):
        return AST.InstructionList()

    @_('assignment ";"',
       'if_statement',
       'while_loop',
       'for_loop',
       'BREAK ";"',
       'CONTINUE ";"',
       'RETURN expr ";"',
       'RETURN ";"',
       'PRINT print_args ";"',
       'compound_instr')
    def instruction(self, p):
        if hasattr(p, 'assignment'):
            return p.assignment
        elif hasattr(p, 'if_statement'):
            return p.if_statement
        elif hasattr(p, 'while_loop'):
            return p.while_loop
        elif hasattr(p, 'for_loop'):
            return p.for_loop
        elif hasattr(p, 'BREAK'):
            return AST.Break()
        elif hasattr(p, 'CONTINUE'):
            return AST.Continue()
        elif hasattr(p, 'RETURN'):
            if hasattr(p, 'expr'):
                return AST.Return(p.expr)
            else:
                return AST.Return()
        elif hasattr(p, 'PRINT'):
            return AST.Print(p.print_args)
        elif hasattr(p, 'compound_instr'):
            return p.compound_instr

    @_('print_args "," expr')
    def print_args(self, p):
        return p.print_args + [p.expr]

    @_('expr')
    def print_args(self, p):
        return [p.expr]

    @_('"{" instructions "}"')
    def compound_instr(self, p):
        return p.instructions

    @_('IF "(" expr ")" instruction %prec IF')
    def if_statement(self, p):
        return AST.IfElse(p.expr, p.instruction)

    @_('IF "(" expr ")" instruction ELSE instruction')
    def if_statement(self, p):
        return AST.IfElse(p.expr, p.instruction0, p.instruction1)

    @_('WHILE "(" expr ")" instruction')
    def while_loop(self, p):
        return AST.WhileLoop(p.expr, p.instruction)

    @_('FOR ID "=" range instruction')
    def for_loop(self, p):
        return AST.ForLoop(AST.Variable(p.ID), p.range, p.instruction)

    @_('expr ":" expr')
    def range(self, p):
        return AST.Range(p.expr0, p.expr1)

    @_('lvalue "=" expr',
       'lvalue ADDASSIGN expr',
       'lvalue SUBASSIGN expr',
       'lvalue MULASSIGN expr',
       'lvalue DIVASSIGN expr')
    def assignment(self, p):
        op = p[1]
        return AST.AssignExpr(op, p.lvalue, p.expr)

    @_('ID',
       'ID "[" indices "]"')
    def lvalue(self, p):
        if hasattr(p, 'indices'):
            return AST.ArrayRef(AST.Variable(p.ID), p.indices)
        else:
            return AST.Variable(p.ID)

    @_('indices "," expr')
    def indices(self, p):
        return p.indices + [p.expr]

    @_('expr')
    def indices(self, p):
        return [p.expr]

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(p[1], p.expr0, p.expr1)

    @_('expr "<" expr',
       'expr ">" expr',
       'expr LE expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NE expr')
    def expr(self, p):
        return AST.RelExpr(p[1], p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return AST.Negation(p.expr)

    @_('expr "\'"')
    def expr(self, p):
        return AST.Transpose(p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('ID')
    def expr(self, p):
        return AST.Variable(p.ID)

    @_('INTNUM')
    def expr(self, p):
        return AST.IntNum(p.INTNUM)

    @_('FLOATNUM')
    def expr(self, p):
        return AST.FloatNum(p.FLOATNUM)

    @_('STRING')
    def expr(self, p):
        return AST.String(p.STRING)

    @_('ID "[" indices "]"')
    def expr(self, p):
        return AST.ArrayRef(AST.Variable(p.ID), p.indices)

    @_('ZEROS "(" expr ")"',
       'ONES "(" expr ")"',
       'EYE "(" expr ")"')
    def expr(self, p):
        return AST.FunctionCall(p[0], [p.expr])

    @_('"[" rows "]"')
    def expr(self, p):
        return AST.MatrixInit(p.rows)

    @_('rows ";" row')
    def rows(self, p):
        return p.rows + [p.row]

    @_('row')
    def rows(self, p):
        return [p.row]

    @_('row "," expr')
    def row(self, p):
        return p.row + [p.expr]

    @_('expr')
    def row(self, p):
        return [p.expr]

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: unexpected token '{p.value}'")
        else:
            print("Syntax error: unexpected end of file")