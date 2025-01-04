import ply.lex as lex

# List of token names
tokens = (
    'INT',        # Integer literals
    'REAL',       # Real numbers in decimal/scientific notation
    'VAR',        # Variable names
    'POW',        # Power operator
    'ASSIGN',     # Assignment operator
    'ADD',        # Addition operator
    'SUB',        # Subtraction operator
    'MUL',        # Multiplication operator
    'DIV',        # Floating-point division operator
    'INTDIV',     # Integer division operator
    'LPAREN',     # Left parenthesis
    'RPAREN',     # Right parenthesis
    'GT',         # Greater than
    'GTE',        # Greater than or equal to
    'LT',         # Less than
    'LTE',        # Less than or equal to
    'EQ',         # Equal to
    'NEQ',        # Not equal to
    'LBRACKET',   # Left bracket for list indexing
    'RBRACKET',   # Right bracket for list indexing
    'LIST',       # Keyword for lists
    'SIN',        # Sine function
    'COS',        # Cosine function
    'TAN',        # Tangent function
)

# Regular expression rules for simple tokens
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_INTDIV = r'//'
t_POW = r'\^'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
t_EQ = r'=='
t_NEQ = r'!='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_LIST(t):
    r'list'
    return t

def t_SIN(t):
    r'sin'
    return t

def t_COS(t):
    r'cos'
    return t

def t_TAN(t):
    r'tan'
    return t

# Regular expressions with actions
def t_REAL(t):
    r'\d+\.\d+(e[+-]?\d+)?'
    t.value = float(t.value)  # Convert to a float for real numbers
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)  # Convert to an integer
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Define a rule to handle whitespace (ignored tokens)
t_ignore = ' \t'

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define a rule for handling errors
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
try:
    lexer = lex.lex()
except Exception as e:
    print(f"Error building lexer: {e}")

# Write the output to .tok file and lexical grammar to .lex file
def write_to_files(group_name):
    input_data = """
    23+8
    2.5 * 0
    5NUM^ 3.0
    x=5
    10*x
    x =y
    x!=5
    X#+8
    (2+5)
    x = list[2]
    (2.5 ^ 3) - sin(90)
    tan(45) <= 1
    cos(0)
    """

    lexer.input(input_data)

    # Tokenized output .tok
    with open(f"{group_name}.tok", "w") as tok_file:
        for tok in lexer:
            tok_file.write(f"{tok.value}/{tok.type} at line {tok.lineno}\n")

    # Lexical grammar .lex
    with open(f"{group_name}.lex", "w") as lex_file:
        lex_file.write("# Lexical Grammar Definitions\n")
        lex_file.write("INT: [0-9]+\n")
        lex_file.write("REAL: [0-9]+\\.[0-9]+(e[+-]?[0-9]+)?\n")
        lex_file.write("VAR: [a-zA-Z_][a-zA-Z_0-9]*\n")
        lex_file.write("LIST: list\n")
        lex_file.write("SIN: sin\n")
        lex_file.write("COS: cos\n")
        lex_file.write("TAN: tan\n")
        lex_file.write("Operators: +, -, *, /, //, ^, ==, !=, >, >=, <, <=\n")

# Create README
with open("README.txt", "w") as readme_file:
    readme_file.write("# Instructions for Lexical Analyzer\n")
    readme_file.write("\n## How to Compile and Run\n")
    readme_file.write("1. Run the Python script to build the lexer and generate .tok and .lex files.\n")
    readme_file.write("2. Example command: python lexical_analyzer.py\n")
    readme_file.write("3. Check `Codezilla.tok` for tokenized output and `Codezilla.lex` for lexical grammar.\n")

def main():
    write_to_files("Codezilla")

if __name__ == "__main__":
    main()
