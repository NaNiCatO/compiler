import ply.lex as lex

# List of token names
tokens = (
    'INT',        # Integer literals
    'REAL',       # Real numbers in decimal/scientific notation
    'LIST',       # Keyword for lists    
    'LBRACKET',   # Left bracket for list indexing
    'RBRACKET',   # Right bracket for list indexing    
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
)

# Regular expression rules for simple tokens
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
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
    if t.value == "list":  # Check if the value is the reserved keyword 'list'
        t.type = "LIST"    # If so, reassign its token type
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

# Test the lexer
def main():
    # Example input
    data = """
    23 + 8
    2.5 * 0
    x = 5
    10 * x
    x != 5
    list x[2]
    """

    try:
        # Give the lexer input
        lexer.input(data)

        # Tokenize
        for tok in lexer:
            print(tok)
    except Exception as e:
        print(f"Error during tokenization: {e}")

if __name__ == "__main__":
    main()
