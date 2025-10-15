import sys
from sly import Lexer


class Scanner(Lexer):
    tokens = {
        'ID',
    'INT',
    'FLOAT',
    'STRING',

    # Operatory binarne
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',

    # Operatory macierzowe element-po-elemencie
    'DOTPLUS',
    'DOTMINUS',
    'DOTTIMES',
    'DOTDIVIDE',

    # Operatory przypisania
    'ASSIGN',
    'PLUSASSIGN',
    'MINUSASSIGN',
    'TIMESASSIGN',
    'DIVIDEASSIGN',

    # Operatory relacyjne
    'LT',
    'GT',
    'LE',
    'GE',
    'NE',
    'EQ',

    # Nawiasy
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',

    # Inne operatory
    'COLON',
    'TRANSPOSE',
    'COMMA',
    'SEMICOLON'}


if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")


  