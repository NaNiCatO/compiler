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
    'TAN',        # Tangent function,
    'ERR'         # Error token for invalid characters
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
    r'(\d+\.\d*|\.\d+)(e[+-]?\d+)?'
    t.value = float(t.value)  # Convert to a float for real numbers
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)  # Convert to an integer
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in ['list', 'sin', 'cos', 'tan']:
        t.type = t.value.upper()  # Convert to the corresponding function token type
    return t

def t_ERR(t):
    r'[^\s\w\d+\-*/^=<>!()[\]\\.]'
    return t

# Define a rule to handle whitespace (ignored tokens)
t_ignore = ' \t'

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define a rule for handling errors
def t_error(t):
    t.type = 'ERR'
    return t

# Build the lexer
try:
    lexer = lex.lex()
except Exception as e:
    print(f"Error building lexer: {e}")

# Function to read from input.txt and output formatted results to output.tok
def process_input_output(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = infile.read()

    lexer.input(data)

    with open(output_file, 'w') as outfile:
        for line in data.splitlines():
            lexer.input(line)
            tokens = []
            for tok in lexer:
                tokens.append(f"{tok.value}/{tok.type}")
            outfile.write(' '.join(tokens) + '\n')

# Example usage
def main():
    input_file = "input.txt"  # The file containing input expressions
    output_file = "Codezilla.tok"  # The file where tokenized output is saved
    process_input_output(input_file, output_file)

if __name__ == "__main__":
    main()
