import sys
from sly import Lexer

class Scanner(Lexer):
    # Zbiór wszystkich nazw tokenów
    tokens = {
        # Słowa kluczowe
        IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES, PRINT,

        # Identyfikatory i Literały
        ID, INTNUM, FLOATNUM, STRING,

        # Operatory macierzowe
        DOTADD, DOTSUB, DOTMUL, DOTDIV,

        # Operatory przypisania
        ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,

        # Operatory relacyjne
        LEQ, GEQ, NEQ, EQ
    }

    # Znaki ignorowane
    ignore = ' \t'

    # Ignorowanie komentarzy
    ignore_comment = r'#.*'

    # Literały - tokeny jednorazowe, mapowane bezpośrednio na swój typ
    literals = {
        '+', '-', '*', '/', '=', '<', '>',
        '(', ')', '[', ']', '{', '}',
        ':', ',', ';', "'"
    }

    # --- Definicje tokenów (wyrażenia regularne) ---
    # Kolejność ma znaczenie - bardziej szczegółowe wzorce jako pierwsze

    # Operatory relacyjne
    LEQ = r'<='
    GEQ = r'>='
    NEQ = r'!='
    EQ = r'=='

    # Operatory macierzowe
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    # Operatory przypisania
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='

    # Identyfikatory i słowa kluczowe
    # Słowa kluczowe są rezerwowane i mapowane na odpowiedni typ tokenu
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    # Stringi (w cudzysłowach)
    STRING = r'"([^"\\]|\\.)*"'

    # Liczby zmiennoprzecinkowe (muszą być zdefiniowane przed INTNUM)
    # Obsługuje: 1.23, 1.23e-10, .123, 123.
    @_(r'((\d+\.\d*|\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+)')
    def FLOATNUM(self, t):
        t.value = float(t.value)  # Konwersja na float
        return t

    # Liczby całkowite
    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)  # Konwersja na int
        return t

    # --- Obsługa ignorowanych znaków ---

    # Śledzenie numerów linii
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Obsługa błędów
    def error(self, t):
        print(f"({self.lineno}): Błędny znak '{t.value[0]}'")
        self.index += 1



if __name__ == '__main__':

    lexer = Scanner()
    data = 'x = 3 + 42 * (s - t)'
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")


  