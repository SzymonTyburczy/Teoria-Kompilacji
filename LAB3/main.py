import sys
from Scanner import Scanner
from Parser import MParser
import TreePrinter  # Import to add printTree methods to AST classes


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    lexer = Scanner()
    parser = MParser()

    try:
        ast = parser.parse(lexer.tokenize(text))
        if ast is not None:
            ast.printTree()
    except Exception as e:
        print(f"Error during parsing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()