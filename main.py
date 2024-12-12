import ply.lex as lex
import os

# Function to read grammar rules from a file
def read_grammar(filename):
    rules = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            rules[key.strip()] = value.strip()
    return rules

# Define a lexer class
class Lexer:
    def __init__(self, grammar_file):
        # Load grammar rules
        rules = read_grammar(grammar_file)

        # Extract tokens
        self.tokens = tuple(rules.keys())

        # Dynamically assign regex patterns to token handlers
        for token, pattern in rules.items():
            setattr(self, f't_{token}', pattern)

        # Ignore spaces and tabs
        self.t_ignore = ' \t'

    # Define a rule to track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Define a rule for handling errors
    def t_error(self, t):
        t.type = "ERR"
        t.value = t.value[0]
        t.lexer.skip(1)
        return t

    # Build the lexer
    def build(self):
        self.lexer = lex.lex(module=self)

    # Tokenize input data
    def tokenize(self, data):
        self.lexer.input(data)
        tokens = []
        current_line = []
        current_lineno = 1

        for tok in self.lexer:
            if tok.lineno > current_lineno:
                tokens.append(" ".join(current_line))
                current_line = []
                current_lineno = tok.lineno

            current_line.append(f"{tok.value}/{tok.type}")

        if current_line:
            tokens.append(" ".join(current_line))

        return tokens

# Main function
def main():
    grammar_file = "Codezilla.lex"
    input_file = "Input.txt"
    output_file = "Codezilla.tok"

    # Initialize lexer
    lexer = Lexer(grammar_file)
    lexer.build()

    # Read input data
    with open(input_file, 'r') as file:
        data = file.read()

    # Tokenize the input data
    tokens = lexer.tokenize(data)

    # Check if output file exists, create or replace it
    with open(output_file, 'w') as file:
        file.write("\n".join(tokens))

if __name__ == "__main__":
    main()
