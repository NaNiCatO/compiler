# Lexical Grammar Definitions
INT: \d+  # Matches integers like 1, 25, 1000
REAL: (\d+\.\d*|\.\d+)(e[+-]?\d+)?  # Matches 3.0, .03, 3., and scientific notation like 2.5e-3
VAR: [a-zA-Z_][a-zA-Z_0-9]*  # Matches variable names such as x, y_var, or num1
LIST: list  # Matches the keyword 'list'
SIN: sin  # Matches the trigonometric function 'sin'
COS: cos  # Matches the trigonometric function 'cos'
TAN: tan  # Matches the trigonometric function 'tan'
ADD: \+  # Matches the addition operator '+'
SUB: -  # Matches the subtraction operator '-'
MUL: \*  # Matches the multiplication operator '*'
DIV: /  # Matches the division operator '/'
INTDIV: //  # Matches the integer division operator '//'
POW: \^  # Matches the exponentiation operator '^'
ASSIGN: =  # Matches the assignment operator '='
LPAREN: \(  # Matches the left parenthesis '('
RPAREN: \)  # Matches the right parenthesis ')'
GT: >  # Matches the greater-than operator '>'
GTE: >=  # Matches the greater-than-or-equal-to operator '>='
LT: <  # Matches the less-than operator '<'
LTE: <=  # Matches the less-than-or-equal-to operator '<='
EQ: ==  # Matches the equality operator '=='
NEQ: !=  # Matches the inequality operator '!='
LBRACKET: \[  # Matches the left square bracket '['
RBRACKET: \]  # Matches the right square bracket ']'
ERR: [^\\s\\w\\d+\-*/^=<>!()[\\]\\.]  # Matches any invalid character
