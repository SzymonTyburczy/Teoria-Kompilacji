from sly import Lexer


class Scanner(Lexer):
    tokens = {
        ID, INTNUM, FLOATNUM, STRING,
        IF, ELSE, FOR, WHILE,
        BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES,
        PRINT,
        DOTADD, DOTSUB, DOTMUL, DOTDIV,
        ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
        LE, GE, NE, EQ,
        # Basic operators are defined as literals below
    }

    literals = {'+', '-', '*', '/', '=', '<', '>',
                '(', ')', '[', ']', '{', '}',
                ':', ';', ',', "'"}

    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Keywords
    IF = r'if'
    ELSE = r'else'
    FOR = r'for'
    WHILE = r'while'
    BREAK = r'break'
    CONTINUE = r'continue'
    RETURN = r'return'
    EYE = r'eye'
    ZEROS = r'zeros'
    ONES = r'ones'
    PRINT = r'print'

    # Operators
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='

    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='

    # Identifiers and numbers
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+\.\d+')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'"([^"\\]|\\.)*"')
    def STRING(self, t):
        t.value = t.value[1:-1]  # Remove quotes
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1