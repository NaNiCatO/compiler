import ply.lex as lex
import ply.yacc as yacc
import csv

# List of token names
tokens = (
    'INT', 'REAL', 'VAR', 'POW', 'ASSIGN', 'ADD', 'SUB', 'MUL',
    'DIV', 'INTDIV', 'LPAREN', 'RPAREN', 'GT', 'GTE', 'LT', 'LTE',
    'EQ', 'NEQ', 'LBRACKET', 'RBRACKET', 'LIST', 'SIN', 'COS', 'TAN', 'ERR'
)

# Regular expression rules for tokens
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

# Token rules for functions
def t_SIN(t):
    r'sin'
    return t

def t_COS(t):
    r'cos'
    return t

def t_TAN(t):
    r'tan'
    return t

def t_LIST(t):
    r'list'
    return t

def t_REAL(t):
    r'-?(\d+\.\d*|\.\d+)(e[+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_ERR(t):
    r'[^\s\w\d+\-*/^=<>!()[\]\.]'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, pos {t.lexpos}.")
    t.lexer.skip(len(t.value))

# Build the lexer
lexer = lex.lex()

# Symbol Table
symbol_table = {}

def add_to_symbol_table(lexeme, line_number, start_pos, length, token_type, value=None):
    """Add or update an entry in the symbol table."""
    symbol_table[lexeme] = {
        "lexeme": lexeme,
        "line_number": line_number,
        "start_pos": start_pos,
        "length": length,
        "type": token_type,
        "value": value
    }

# Grammar rules
def p_assignment(p):
    'expression : VAR ASSIGN expression'
    lexeme = p[1]
    line_number = p.lineno(1)
    start_pos = p.lexpos(1)

    if isinstance(p[3], str) and "Undefined variable" in p[3]:
        p[0] = p[3]
    else:
        add_to_symbol_table(lexeme, line_number, start_pos, len(lexeme), "variable", p[3])
        p[0] = f"({lexeme}={p[3]})"

def p_expression_arithmetic(p):
    '''expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression POW expression'''
    p[0] = f"({p[1]}{p[2]}{p[3]})"

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = f"({p[2]})"

def p_expression_number(p):
    '''expression : INT
                  | REAL'''
    p[0] = str(p[1])

def p_expression_var(p):
    'expression : VAR'
    lexeme = p[1]
    if lexeme not in symbol_table:
        line_number = p.lineno(1)
        start_pos = p.lexpos(1)
        p[0] = f"Undefined variable '{lexeme}' at line {line_number}, pos {start_pos}"
    else:
        p[0] = lexeme

def p_expression_list_declaration(p):
    'expression : VAR ASSIGN LIST LBRACKET INT RBRACKET'
    if p[5] <= 0:
        p[0] = "Semantic Error: List size must be positive."
    else:
        add_to_symbol_table(p[1], p.lineno(1), p.lexpos(1), len(p[1]), "list", [0] * p[5])
        p[0] = f"({p[1]}=(list[({p[5]})]))"

def p_expression_list_access(p):
    'expression : VAR LBRACKET INT RBRACKET'
    list_value = symbol_table.get(p[1], {}).get("value", [])
    if not isinstance(list_value, list):
        p[0] = f"Semantic Error: '{p[1]}' is not a list."
    elif p[3] < 0 or p[3] >= len(list_value):
        p[0] = f"Semantic Error: Index out of range for list '{p[1]}' at index {p[3]}."
    else:
        p[0] = f"(({p[1]}[({p[3]})]))"

def p_expression_function(p):
    '''expression : SIN LPAREN expression RPAREN
                  | COS LPAREN expression RPAREN
                  | TAN LPAREN expression RPAREN'''
    p[0] = f"({p[1]}({p[3]}))"

def p_error(p):
    if p:
        raise SyntaxError(f"SyntaxError at line {p.lineno}, pos {p.lexpos}")
    else:
        raise SyntaxError("SyntaxError at EOF")

# Build the parser
parser = yacc.yacc()

def parse_input(input_file, bracket_output, csv_output):
    """Parse input, generate bracketed output and symbol table."""
    with open(input_file, 'r') as infile, open(bracket_output, 'w') as bracket_file:
        for lineno, line in enumerate(infile, start=1):
            try:
                result = parser.parse(line)
                if result and "Undefined variable" not in result:
                    bracket_file.write(f"{result}\n")
                elif "Undefined variable" in result:
                    bracket_file.write(f"{result}\n")
                else:
                    bracket_file.write(f"SyntaxError at line {lineno}\n")
            except SyntaxError as e:
                bracket_file.write(f"{str(e)}\n")
            except Exception as e:
                bracket_file.write(f"UnexpectedError at line {lineno}: {e}\n")

    with open(csv_output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["lexeme", "line_number", "start_pos", "length", "type", "value"])
        for entry in symbol_table.values():
            writer.writerow([entry["lexeme"], entry["line_number"], entry["start_pos"],
                             entry["length"], entry["type"], entry["value"]])

def main():
    input_file = "input.txt"
    bracket_output = "parser/parser_output.bracket"
    csv_output = "parser/symbol_table.csv"
    parse_input(input_file, bracket_output, csv_output)

if __name__ == "__main__":
    main()
