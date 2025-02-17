import ply.lex as lex
import ply.yacc as yacc
import csv
import math

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
    if t.value in ['list', 'sin', 'cos', 'tan']:
        t.type = t.value.upper()  # Convert to the corresponding function token type
    return t

def t_ERR(t):
    r'[^\s\w\d+\-*/^=<>!()[\]\.]'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, pos {t.lexpos + 1}")
    t.lexer.skip(1)  # Skip the invalid character



# Build the lexer
lexer = lex.lex()

# Symbol Table
symbol_table = {}

def add_to_symbol_table(lexeme, line_number, start_pos, length, token_type, value=None):
    """Add or update an entry in the symbol table."""
    start_pos = start_pos + 1  # Convert to 1-based index
    if lexeme not in symbol_table:
        symbol_table[lexeme] = {
            "lexeme": lexeme,
            "line_number": line_number,
            "start_pos": start_pos,
            "length": length,
            "type": token_type,
            "value": value
        }
    else:
        symbol_table[lexeme].update({
            "line_number": line_number,
            "start_pos": start_pos,
            "length": length,
            "type": token_type,
            "value": value
        })

# Assembly code generation
assembly_code = []
temp_assembly_code = []
register_counter = 0
register_saved = {}

def get_register():
    global register_counter
    register_counter += 1
    return f"R{register_counter - 1}"

def get_expression_register(expression):
    global register_saved
    for (register, expr) in register_saved.items():
        if expr == expression: return register
    return None

def save_register(register, expression):
    global register_saved
    register_saved[register] = expression

def reset_registers():
    global register_counter
    global register_saved
    register_counter = 0
    register_saved = {}

def reset_temp_assembly():
    global temp_assembly_code
    temp_assembly_code = []

def generate_assembly(operation, operand1, operand2=None, result_register=None, isAddress=False, isFunction=False):
    if result_register is None:
        result_register = get_register()
    if isAddress:
        temp_assembly_code.append(f"LD {result_register} {operand1}")
        return result_register
    elif isFunction:
        # arg_expression_register = get_expression_register(operand1)
        # temp_assembly_code.append(f"LD {result_register} {operation}({arg_expression_register or operand1})")
        temp_assembly_code.append(f"LD {result_register} #{operand2}")
        return result_register
    
    if operand2 is None:
        temp_assembly_code.append(f"LD {result_register} #{operand1}")
    else:
        if operation == '+':
            temp_assembly_code.append(f"ADD.i {result_register} {operand1} {operand2}")
        elif operation == '-':
            temp_assembly_code.append(f"SUB.i {result_register} {operand1} {operand2}")
        elif operation == '*':
            temp_assembly_code.append(f"MUL.i {result_register} {operand1} {operand2}")
        elif operation == '/':
            temp_assembly_code.append(f"DIV.f {result_register} {operand1} {operand2}")
        elif operation == '//':
            temp_assembly_code.append(f"DIV.i {result_register} {operand1} {operand2}")
        elif operation == '^':
            temp_assembly_code.append(f"POW.i {result_register} {operand1} {operand2}")
        elif operation == '==':
            temp_assembly_code.append(f"EQ.f {result_register} {operand1} {operand2}")
        elif operation == '!=':
            temp_assembly_code.append(f"NE.f {result_register} {operand1} {operand2}")
        elif operation == '>':
            temp_assembly_code.append(f"GT.f {result_register} {operand1} {operand2}")
        elif operation == '>=':
            temp_assembly_code.append(f"GE.f {result_register} {operand1} {operand2}")
        elif operation == '<':
            temp_assembly_code.append(f"LT.f {result_register} {operand1} {operand2}")
        elif operation == '<=':
            temp_assembly_code.append(f"LE.f {result_register} {operand1} {operand2}")
    
    
    return result_register

# Grammar rules
def p_expression_var_from_list(p):
    'expression : VAR ASSIGN VAR LBRACKET INT RBRACKET'
    list_value = symbol_table.get(p[3], {}).get("value", [])
    if not isinstance(list_value, list):
        p[0] = f"Semantic Error: '{p[3]}' is not a list."
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    elif p[5] < 0 or p[5] >= len(list_value):
        p[0] = f"Semantic Error: Index out of range for list '{p[3]}' at index {p[5]}."
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    else:
        value = list_value[p[5]]
        add_to_symbol_table(p[1], p.lineno(1), p.lexpos(1), len(p[1]), "variable", value)
        temp_assembly_code.append(f"LD R0 {p[5]}")
        temp_assembly_code.append(f"LD R1 @{p[3]}")
        temp_assembly_code.append(f"LD R2 #4")
        temp_assembly_code.append(f"MUL.i R3 R0 R2")
        temp_assembly_code.append(f"ADD.i R4 R1 R3")
        temp_assembly_code.append(f"ST @{p[1]} R4")
        p[0] = f"({p[1]}={value})"


def p_assignment(p):
    'expression : VAR ASSIGN expression'
    lexeme = p[1]
    line_number = p.lineno(1)
    start_pos = p.lexpos(1)

    if isinstance(p[3], str) and "Undefined variable" in p[3]:
        p[0] = p[3]
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    else:
        add_to_symbol_table(lexeme, line_number, start_pos, len(lexeme), "variable", p[3])
        expression_register = get_expression_register(p[3])
        temp_assembly_code.append(f"ST @{lexeme} {expression_register or p[3]}")
        p[0] = f"({lexeme}={p[3]})"


def p_expression_comparison(p):
    '''expression : expression GT expression
                  | expression GTE expression
                  | expression LT expression
                  | expression LTE expression
                  | expression EQ expression
                  | expression NEQ expression'''
    expression = f"({p[1]}{p[2]}{p[3]})"
    operand1 = get_expression_register(p[1])
    operand2 = get_expression_register(p[3])
    result_register = generate_assembly(p[2], operand1 or p[1], operand2 or p[3])
    save_register(result_register, expression)
    temp_assembly_code.append(f"ST @print {result_register}")
    p[0] = expression


def p_expression_arithmetic(p):
    '''expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression POW expression'''
    expression = f"({p[1]}{p[2]}{p[3]})"
    operand1 = get_expression_register(p[1])
    operand2 = get_expression_register(p[3])
    result_register = generate_assembly(p[2], operand1 or p[1], operand2 or p[3])
    save_register(result_register, expression)
    temp_assembly_code.append(f"ST @print {result_register}")
    # print ?? if EOL
    p[0] = expression


def p_expression_intdiv(p):
    'expression : expression INTDIV expression'
    expression = f"({p[1]}//{p[3]})"
    operand1 = get_expression_register(p[1])
    operand2 = get_expression_register(p[3])
    result_register = generate_assembly(p[2], operand1 or p[1], operand2 or p[3])
    save_register(result_register, expression)
    temp_assembly_code.append(f"ST @print {result_register}")
    p[0] = expression


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    # Avoid adding extra parentheses if already enclosed
    if isinstance(p[2], str) and p[2].startswith('(') and p[2].endswith(')'):
        p[0] = p[2]
    else:
        p[0] = f"({p[2]})"

def p_expression_number(p):
    '''expression : INT
                  | REAL'''
    expression = str(p[1])
    result_register = generate_assembly(None, p[1])
    save_register(result_register, expression)
    p[0] = expression

def p_expression_var(p):
    'expression : VAR'
    lexeme = p[1]
    if lexeme not in symbol_table:
        line_number = p.lineno(1)
        start_pos = p.lexpos(1) + 1  # Adjust position to start from 1
        p[0] = f"Undefined variable '{lexeme}' at line {line_number}, pos {start_pos}"
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    else:
        result_register = generate_assembly(None, f"@{lexeme}", isAddress=True)
        save_register(result_register, lexeme)
        p[0] = lexeme


def p_expression_list_declaration(p):
    'expression : VAR ASSIGN LIST LBRACKET INT RBRACKET'
    if p[5] <= 0:
        p[0] = "Semantic Error: List size must be positive."
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    else:
        add_to_symbol_table(p[1], p.lineno(1), p.lexpos(1), len(p[1]), "list", [0] * p[5])
        temp_assembly_code.append(f"LD R0 #0 // load 0, list {p[1]}[{p[5]}]")
        temp_assembly_code.append(f"LD R1 @{p[1]} // load base address of {p[1]}")
        temp_assembly_code.append(f"LD R2 #4 // size = 4 bytes")
        for i in range(p[5]):
            temp_assembly_code.append(f"LD R3 #{i} // load offset {i}")
            temp_assembly_code.append(f"MUL.i R4 R2 R3 // size * offset")
            temp_assembly_code.append(f"ADD.i R5 R1 R4 // {p[1]}[{i}] address")
            temp_assembly_code.append(f"ST R5 R0 // {p[1]}[{i}] = 0")
        p[0] = f"({p[1]}=(list[({p[5]})]))"

def p_expression_list_access(p):
    'expression : VAR LBRACKET INT RBRACKET'
    list_value = symbol_table.get(p[1], {}).get("value", [])
    if not isinstance(list_value, list):
        p[0] = f"Semantic Error: '{p[1]}' is not a list."
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    elif p[3] < 0 or p[3] >= len(list_value):
        p[0] = f"Semantic Error: Index out of range for list '{p[1]}' at index {p[3]}."
        reset_temp_assembly()
        temp_assembly_code.append("ERROR")
    else:
        expression = f"(({p[1]}[({p[3]})]))"
        expression_register = get_register()
        reg1 = get_register()
        reg2 = get_register()
        reg3 = get_register()
        reg4 = get_register()
        reg5 = get_register()
        temp_assembly_code.append(f"LD {reg1} @{p[1]}")
        temp_assembly_code.append(f"LD {reg2} #{p[3]}")
        temp_assembly_code.append(f"LD {reg3} #4")
        temp_assembly_code.append(f"MUL.i {reg4} {reg2} {reg3}")
        temp_assembly_code.append(f"ADD.i {reg5} {reg1} {reg4}")
        temp_assembly_code.append(f"LD {expression_register} {reg5}")
        temp_assembly_code.append(f"ST @print {expression_register} // print {p[1]}[{p[3]}]")
        save_register(expression_register, expression)
        global register_counter
        register_counter -= 5
        p[0] = expression


def p_expression_list_assignment(p):
    'expression : VAR LBRACKET INT RBRACKET ASSIGN expression'
    list_value = symbol_table.get(p[1], {}).get("value", [])
    if not isinstance(list_value, list):
        p[0] = f"Semantic Error: '{p[1]}' is not a list."
    elif p[3] < 0 or p[3] >= len(list_value):
        p[0] = f"Semantic Error: Index out of range for list '{p[1]}' at index {p[3]}."
    else:
        try:
            list_value[p[3]] = float(p[6])
        except:
            list_value[p[3]] = p[6]
        p[0] = f"({p[1]}[({p[3]})]={p[6]})"
        add_to_symbol_table(p[1], p.lineno(1), p.lexpos(1), len(p[1]), "list", list_value)
        expression_register = get_expression_register(p[6])
        reg1 = get_register()
        reg2 = get_register()
        reg3 = get_register()
        reg4 = get_register()
        reg5 = get_register()
        temp_assembly_code.append(f"LD {reg1} #{p[3]}")
        temp_assembly_code.append(f"LD {reg2} @{p[1]}")
        temp_assembly_code.append(f"LD {reg3} #4")
        temp_assembly_code.append(f"MUL.i {reg4} {reg1} {reg3}")
        temp_assembly_code.append(f"ADD.i {reg5} {reg2} {reg4}")
        temp_assembly_code.append(f"ST {reg5} {expression_register}")


def p_function_call(p):
    '''expression : SIN LPAREN expression RPAREN
                  | COS LPAREN expression RPAREN
                  | TAN LPAREN expression RPAREN'''
    p[0] = f"({p[1]}({p[3]}))"
    if p[1] == 'sin':
        p[0] = math.sin(math.radians(eval(p[3])))  # Convert to radians
    elif p[1] == 'cos':
        p[0] = math.cos(math.radians(eval(p[3])))
    elif p[1] == 'tan':
        p[0] = math.tan(math.radians(eval(p[3])))

    result_register = generate_assembly(p[1], p[3], p[0], isFunction=True)
    temp_assembly_code.append(f"ST @print {result_register}")
    
    save_register(result_register, p[0])


def p_error(p):
    reset_temp_assembly()
    temp_assembly_code.append("ERROR")
    if p:
        raise SyntaxError(f"SyntaxError at line {p.lineno}, pos {p.lexpos + 1}")
    else:
        raise SyntaxError("SyntaxError at EOF")


# Build the parser
parser = yacc.yacc()

# Function to process lexical analysis
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


# Function to process syntactic analysis
def process_syntax(input_file, bracket_output):
    with open(input_file, 'r') as infile, open(bracket_output, 'w') as bracket_file:
        for lineno, line in enumerate(infile, start=1):
            try:
                lexer.lineno = lineno  # Explicitly set the lexer's line number
                result = parser.parse(line, lexer=lexer)
                if result:
                    bracket_file.write(f"{result}\n")
                else:
                    bracket_file.write(f"SyntaxError at line {lineno}\n")
            except SyntaxError as e:
                bracket_file.write(f"{str(e)}\n")
            except Exception as e:
                bracket_file.write(f"UnexpectedError at line {lineno}: {e}\n")
            finally:
                assembly_code.extend(temp_assembly_code)
                assembly_code.append("")
                reset_temp_assembly()
                reset_registers()


# Function to output the symbol table
def write_symbol_table(output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["lexeme", "line_number", "start_pos", "length", "type", "value"])
        for entry in symbol_table.values():
            writer.writerow([entry["lexeme"], entry["line_number"], entry["start_pos"],
                             entry["length"], entry["type"], entry["value"]])

def main():
    input_file = "input.txt"  # Input expressions
    output_file_tok = "lex/lexical_output.tok"  # Tokenized output
    output_file_bracket = "parser/parser_output.bracket"  # Parsed output
    symbol_table_file = "parser/symbol_table.csv"  # Symbol table output
    assembly_output_file = "assembly_output.asm"  # Assembly code output

    # Lexical analysis
    process_lexical(input_file, output_file_tok)

    # Syntactic analysis
    process_syntax(input_file, output_file_bracket)

    # Write the symbol table to CSV
    write_symbol_table(symbol_table_file)

    # Write the assembly code to file
    with open(assembly_output_file, 'w') as asm_file:
        for line in assembly_code:
            asm_file.write(line + '\n')


    # Print symbol table to console
    print("Symbol Table:")
    for key, value in symbol_table.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()