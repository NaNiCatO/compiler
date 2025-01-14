
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD ASSIGN COS DIV EQ ERR GT GTE INT INTDIV LBRACKET LIST LPAREN LT LTE MUL NEQ POW RBRACKET REAL RPAREN SIN SUB TAN VARexpression : VAR ASSIGN expressionexpression : expression ADD expression\n                  | expression SUB expression\n                  | expression MUL expression\n                  | expression DIV expression\n                  | expression POW expressionexpression : LPAREN expression RPARENexpression : INT\n                  | REALexpression : VARexpression : VAR ASSIGN LIST LBRACKET INT RBRACKETexpression : VAR LBRACKET INT RBRACKETexpression : SIN LPAREN expression RPAREN\n                  | COS LPAREN expression RPAREN\n                  | TAN LPAREN expression RPAREN'
    
_lr_action_items = {'VAR':([0,3,9,10,11,12,13,14,17,18,19,],[2,2,2,2,2,2,2,2,2,2,2,]),'LPAREN':([0,3,6,7,8,9,10,11,12,13,14,17,18,19,],[3,3,17,18,19,3,3,3,3,3,3,3,3,3,]),'INT':([0,3,9,10,11,12,13,14,15,17,18,19,32,],[4,4,4,4,4,4,4,4,27,4,4,4,37,]),'REAL':([0,3,9,10,11,12,13,14,17,18,19,],[5,5,5,5,5,5,5,5,5,5,5,]),'SIN':([0,3,9,10,11,12,13,14,17,18,19,],[6,6,6,6,6,6,6,6,6,6,6,]),'COS':([0,3,9,10,11,12,13,14,17,18,19,],[7,7,7,7,7,7,7,7,7,7,7,]),'TAN':([0,3,9,10,11,12,13,14,17,18,19,],[8,8,8,8,8,8,8,8,8,8,8,]),'$end':([1,2,4,5,20,21,22,23,24,25,28,33,34,35,36,38,],[0,-10,-8,-9,-2,-3,-4,-5,-6,-1,-7,-12,-13,-14,-15,-11,]),'ADD':([1,2,4,5,16,20,21,22,23,24,25,28,29,30,31,33,34,35,36,38,],[9,-10,-8,-9,9,9,9,9,9,9,9,-7,9,9,9,-12,-13,-14,-15,-11,]),'SUB':([1,2,4,5,16,20,21,22,23,24,25,28,29,30,31,33,34,35,36,38,],[10,-10,-8,-9,10,10,10,10,10,10,10,-7,10,10,10,-12,-13,-14,-15,-11,]),'MUL':([1,2,4,5,16,20,21,22,23,24,25,28,29,30,31,33,34,35,36,38,],[11,-10,-8,-9,11,11,11,11,11,11,11,-7,11,11,11,-12,-13,-14,-15,-11,]),'DIV':([1,2,4,5,16,20,21,22,23,24,25,28,29,30,31,33,34,35,36,38,],[12,-10,-8,-9,12,12,12,12,12,12,12,-7,12,12,12,-12,-13,-14,-15,-11,]),'POW':([1,2,4,5,16,20,21,22,23,24,25,28,29,30,31,33,34,35,36,38,],[13,-10,-8,-9,13,13,13,13,13,13,13,-7,13,13,13,-12,-13,-14,-15,-11,]),'ASSIGN':([2,],[14,]),'RPAREN':([2,4,5,16,20,21,22,23,24,25,28,29,30,31,33,34,35,36,38,],[-10,-8,-9,28,-2,-3,-4,-5,-6,-1,-7,34,35,36,-12,-13,-14,-15,-11,]),'LBRACKET':([2,26,],[15,32,]),'LIST':([14,],[26,]),'RBRACKET':([27,37,],[33,38,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,3,9,10,11,12,13,14,17,18,19,],[1,16,20,21,22,23,24,25,29,30,31,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> VAR ASSIGN expression','expression',3,'p_assignment','main.py',95),
  ('expression -> expression ADD expression','expression',3,'p_expression_arithmetic','main.py',107),
  ('expression -> expression SUB expression','expression',3,'p_expression_arithmetic','main.py',108),
  ('expression -> expression MUL expression','expression',3,'p_expression_arithmetic','main.py',109),
  ('expression -> expression DIV expression','expression',3,'p_expression_arithmetic','main.py',110),
  ('expression -> expression POW expression','expression',3,'p_expression_arithmetic','main.py',111),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','main.py',115),
  ('expression -> INT','expression',1,'p_expression_number','main.py',119),
  ('expression -> REAL','expression',1,'p_expression_number','main.py',120),
  ('expression -> VAR','expression',1,'p_expression_var','main.py',124),
  ('expression -> VAR ASSIGN LIST LBRACKET INT RBRACKET','expression',6,'p_expression_list_declaration','main.py',134),
  ('expression -> VAR LBRACKET INT RBRACKET','expression',4,'p_expression_list_access','main.py',142),
  ('expression -> SIN LPAREN expression RPAREN','expression',4,'p_expression_function','main.py',152),
  ('expression -> COS LPAREN expression RPAREN','expression',4,'p_expression_function','main.py',153),
  ('expression -> TAN LPAREN expression RPAREN','expression',4,'p_expression_function','main.py',154),
]
