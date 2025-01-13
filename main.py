import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'INT',        # Integer literals (including negatives)
    'REAL',       # Real numbers in decimal/scientific notation (including negatives)
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
    r'-?(\d+\.\d*|\.\d+)(e[+-]?\d+)?'
    t.value = float(t.value)  # Convert to a float for real numbers (including negative values)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)  # Convert to an integer (including negative values)
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in ['list', 'sin', 'cos', 'tan']:
        t.type = t.value.upper()  # Convert to the corresponding function token type
    return t

def t_ERR(t):
    r'[^\s\w\d+\-*/^=<>!()[\]\.]'
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

# Function to read from input.txt and output formatted results to output.tok
def process_lexical(input_file, output_file):
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



# Symbol Table to track semantic information
symbol_table = {}

# Function to add entries to the symbol table
def add_to_symbol_table(lexeme, line_number, start_pos, length, symbol_type, value=None):
    symbol_table[lexeme] = {
        "lexeme": lexeme,
        "line_number": line_number,
        "start_pos": start_pos,
        "length": length,
        "type": symbol_type,
        "value": value
    }

# Syntactic and semantic analysis
# Grammar rules
def p_assignment(p):
    'expression : VAR ASSIGN expression'
    lexeme = p[1]
    line_number = p.lineno(1)
    start_pos = p.lexpos(1)
    length = len(lexeme)

    # Check if variable is already declared, if not, add it
    if lexeme not in symbol_table:
        add_to_symbol_table(lexeme, line_number, start_pos, length, "variable", p[3])
    else:
        symbol_table[lexeme]["value"] = p[3]  # Update the value

    p[0] = f"ASSIGN: {lexeme} := {p[3]}"

def p_expression_arithmetic(p):
    '''expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression POW expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            print("Semantic Error: Division by zero.")
            p[0] = None
        else:
            p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INT
                  | REAL'''
    p[0] = p[1]

def p_expression_var(p):
    'expression : VAR'
    lexeme = p[1]
    if lexeme not in symbol_table:
        print(f"Semantic Error: Variable '{lexeme}' not declared at line {p.lineno(1)}.")
    else:
        print(f"Using variable '{lexeme}' with value {symbol_table[lexeme]['value']} at line {p.lineno(1)}.")
    p[0] = symbol_table.get(lexeme, {}).get("value", None)

def p_expression_list_access(p):
    'expression : LIST LBRACKET INT RBRACKET'
    if p[3] < 0:
        print("Semantic Error: List index cannot be negative.")
    p[0] = f"LIST ACCESS INDEX {p[3]}"

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

def process_syntax(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = infile.read()

    results = []
    for line in data.splitlines():
        result = parser.parse(line)
        if result is not None:
            results.append(f"{line.strip()} -> {result}")
        else:
            results.append(f"{line.strip()} -> Syntax Error")

    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')

# Example usage
def main():
    input_file = "input.txt"  # The file containing input expressions
    output_file_tok = "lex/lexical_output.tok"  # The file where tokenized output is saved
    output_file_bracket = "parser/parser_output.bracket"  # The file where parsed output is saved

    # Lexical analysis
    process_lexical(input_file, output_file_tok)

    # Syntactic analysis
    process_syntax(input_file, output_file_bracket)

    # Print symbol table
    print("Symbol Table:")
    for key, value in symbol_table.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
