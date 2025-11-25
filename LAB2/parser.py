import sys
from sly import Parser
from scanner import Scanner

class MatrixParser(Parser):
    tokens = Scanner.tokens

    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('right', '=', ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN),
        ('left', EQ, NEQ),
        ('left', '<', '>', LEQ, GEQ),
        ('left', '+', '-', DOTADD, DOTSUB),
        ('left', '*', '/', DOTMUL, DOTDIV),
        ('right', UMINUS),
        ('left', "'"),
        ('left', '['),
    )

    def __init__(self):
        self.errors = []

    @_('statements')
    def program(self, p):
        return ('program', p.statements)

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('')
    def statements(self, p):
        return []

    @_('"{" statements "}"')
    def statement(self, p):
        return ('compound', p.statements)

    @_('simple_statement ";"')
    def statement(self, p):
        return p.simple_statement

    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('while_statement')
    def statement(self, p):
        return p.while_statement

    @_('for_statement')
    def statement(self, p):
        return p.for_statement

    @_('assignment')
    def simple_statement(self, p):
        return p.assignment

    @_('expression')
    def simple_statement(self, p):
        return ('expression_stmt', p.expression)

    @_('BREAK')
    def simple_statement(self, p):
        return ('break',)

    @_('CONTINUE')
    def simple_statement(self, p):
        return ('continue',)

    @_('RETURN expression')
    def simple_statement(self, p):
        return ('return', p.expression)

    @_('RETURN')
    def simple_statement(self, p):
        return ('return', None)

    @_('PRINT print_list')
    def simple_statement(self, p):
        return ('print', p.print_list)

    @_('print_list "," expression')
    def print_list(self, p):
        return p.print_list + [p.expression]

    @_('expression')
    def print_list(self, p):
        return [p.expression]

    @_('IF "(" expression ")" statement ELSE statement')
    def if_statement(self, p):
        return ('if_else', p.expression, p.statement0, p.statement1)

    @_('IF "(" expression ")" statement %prec IFX')
    def if_statement(self, p):
        return ('if', p.expression, p.statement)

    @_('WHILE "(" expression ")" statement')
    def while_statement(self, p):
        return ('while', p.expression, p.statement)

    @_('FOR ID "=" range statement')
    def for_statement(self, p):
        return ('for', p.ID, p.range, p.statement)

    @_('expression ":" expression')
    def range(self, p):
        return ('range', p.expression0, p.expression1)

    @_('lvalue "=" expression')
    def assignment(self, p):
        return ('assign', p.lvalue, p.expression)

    @_('lvalue ADDASSIGN expression')
    def assignment(self, p):
        return ('add_assign', p.lvalue, p.expression)

    @_('lvalue SUBASSIGN expression')
    def assignment(self, p):
        return ('sub_assign', p.lvalue, p.expression)

    @_('lvalue MULASSIGN expression')
    def assignment(self, p):
        return ('mul_assign', p.lvalue, p.expression)

    @_('lvalue DIVASSIGN expression')
    def assignment(self, p):
        return ('div_assign', p.lvalue, p.expression)

    @_('ID')
    def lvalue(self, p):
        return ('id', p.ID)

    @_('ID "[" expression "," expression "]"')
    def lvalue(self, p):
        return ('array_ref', p.ID, p.expression0, p.expression1)

    @_('ID "[" expression "]"')
    def lvalue(self, p):
        return ('vector_ref', p.ID, p.expression)

    @_('expression "+" expression')
    def expression(self, p):
        return ('add', p.expression0, p.expression1)

    @_('expression "-" expression')
    def expression(self, p):
        return ('sub', p.expression0, p.expression1)

    @_('expression "*" expression')
    def expression(self, p):
        return ('mul', p.expression0, p.expression1)

    @_('expression "/" expression')
    def expression(self, p):
        return ('div', p.expression0, p.expression1)

    @_('expression DOTADD expression')
    def expression(self, p):
        return ('dotadd', p.expression0, p.expression1)

    @_('expression DOTSUB expression')
    def expression(self, p):
        return ('dotsub', p.expression0, p.expression1)

    @_('expression DOTMUL expression')
    def expression(self, p):
        return ('dotmul', p.expression0, p.expression1)

    @_('expression DOTDIV expression')
    def expression(self, p):
        return ('dotdiv', p.expression0, p.expression1)

    @_('expression EQ expression')
    def expression(self, p):
        return ('eq', p.expression0, p.expression1)

    @_('expression NEQ expression')
    def expression(self, p):
        return ('neq', p.expression0, p.expression1)

    @_('expression "<" expression')
    def expression(self, p):
        return ('lt', p.expression0, p.expression1)

    @_('expression ">" expression')
    def expression(self, p):
        return ('gt', p.expression0, p.expression1)

    @_('expression LEQ expression')
    def expression(self, p):
        return ('leq', p.expression0, p.expression1)

    @_('expression GEQ expression')
    def expression(self, p):
        return ('geq', p.expression0, p.expression1)

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        return ('uminus', p.expression)

    @_('expression "\'"')
    def expression(self, p):
        return ('transpose', p.expression)

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('ID "[" expression "," expression "]"')
    def expression(self, p):
        return ('array_ref', p.ID, p.expression0, p.expression1)

    @_('ID "[" expression "]"')
    def expression(self, p):
        return ('vector_ref', p.ID, p.expression)

    @_('EYE "(" expression ")"')
    def expression(self, p):
        return ('eye', p.expression)

    @_('ZEROS "(" expression ")"')
    def expression(self, p):
        return ('zeros', p.expression)

    @_('ONES "(" expression ")"')
    def expression(self, p):
        return ('ones', p.expression)

    @_('"[" matrix_rows "]"')
    def expression(self, p):
        return ('matrix', p.matrix_rows)

    @_('matrix_rows ";" matrix_row')
    def matrix_rows(self, p):
        return p.matrix_rows + [p.matrix_row]

    @_('matrix_row')
    def matrix_rows(self, p):
        return [p.matrix_row]

    @_('matrix_row "," expression')
    def matrix_row(self, p):
        return p.matrix_row + [p.expression]

    @_('expression')
    def matrix_row(self, p):
        return [p.expression]

    @_('ID')
    def expression(self, p):
        return ('id', p.ID)

    @_('INTNUM')
    def expression(self, p):
        return ('int', p.INTNUM)

    @_('FLOATNUM')
    def expression(self, p):
        return ('float', p.FLOATNUM)

    @_('STRING')
    def expression(self, p):
        return ('string', p.STRING)

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: Unexpected token '{p.value}'")
            self.errors.append(p.lineno)
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    scanner = Scanner()
    parser = MatrixParser()

    filename = "example1.m"

    with open(filename, "r") as file:
        text = file.read()

    result = parser.parse(scanner.tokenize(text))
    print(result)