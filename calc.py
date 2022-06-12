from ast import Expression, parse
from glob import glob

import ply.lex as lex #analizador léxico
import ply.yacc as yacc #analizaodor sintáctico
import sys

# lista de tokens que identifica la gramática
tokens = [
    'INT',
    'FLOAT',
    'ID',
    'SUMA',
    'RESTA',
    'MUL',
    'DIV',
    'IGUAL',
    'POTEN',
    'MOD',
    'GATO',
    'PARABRE',
    'PARCIERRA'
]

# ply usa t_<nombre token> para interpretar el token
#gato
t_GATO = r'\#'
# suma
t_SUMA = r'\+'
# resta
t_RESTA = r'\-'
# multiplicación
t_MUL = r'\*'
# división
t_DIV = r'\/'
# igual
t_IGUAL = r'\='
# POTEN
t_POTEN = r'\^'
#MOD
t_MOD = r'\%'
# paréntesis que abre
t_PARABRE = r'\('
# paréntesis que cierra
t_PARCIERRA = r'\)'
#ignoramos los espacios en blanco
t_ignore = r' '

# definimos enteros y flotantes

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value) # convertirmos el string a entero
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_]*' #expresion regular
    t.type = 'ID'
    return t

def t_error(t): # manejo de errores
    print("Caracter invalido.")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MUL', 'DIV'),
    ('left','POTEN','MOD')
)
 
def p_calc(p):
    '''
    calc :  GATO expression 
         |  GATO var_assing 
         |  GATO empty 
    '''
    print(run(p[2]))

def p_var_assing(p):
    '''
    var_assing : ID IGUAL expression
    '''
    p[0] = ('=', p[1], p[3])


def p_expression(p):
    '''
    expression : expression SUMA expression
               | expression RESTA expression
               | expression MUL expression
               | expression DIV expression
               | expression POTEN expression
               | expression MOD expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_par(p):
    '''
    expression : PARABRE expression PARCIERRA
                
    '''
    p[0] = (p[2])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : ID
    '''
    p[0] = ('var', p[1])


def p_error(p):
    print("error de sintaxis")

def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None

parser = yacc.yacc()

env = {}
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == 'var':
            if p[1] not in env:
                raise ValueError('variable no declarada',p[1])
            else:
                return env[p[1]]    
        elif p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '^':
            return run(p[1]**p[2])
        elif p[0] == '%':
            return run(p[1]%p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])      
    else:
        return p

while True:
    print("\nIngresa la operacion a realizar")
    try:
        s = input('//')
        parser.parse(s)
    except ValueError as e:
        print(e)
    
    