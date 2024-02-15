from ply import lex

tokens = (
    'NUMERO',
    'IDENTIFICADOR',
    'PALABRA_RESERVADA',
    'CADENA',
    'OPERADOR',  
    'SIMBOLO_ESPECIAL',  
)


contadores_tokens = {
    'PALABRA_RESERVADA': 0,
    'IDENTIFICADOR': 0,
    'CADENA': 0,
    'NUMERO': 0,
    'OPERADOR': 0,  
    'SIMBOLO_ESPECIAL': 0, 
}

# identificador
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFICADOR' if t.value not in palabras_reservadas else 'PALABRA_RESERVADA'
    contadores_tokens[t.type] += 1
    return t

# palabras reservadas
def t_PALABRA_RESERVADA(t):
    r'int|float|string|if|else|while'
    contadores_tokens['PALABRA_RESERVADA'] += 1
    return t

# cadenas
def t_CADENA(t):
    r'\"[^\"]*\"'
    contadores_tokens['CADENA'] += 1
    return t

# numeros
def t_NUMERO(t):
    r'\d+'
    contadores_tokens['NUMERO'] += 1
    t.value = int(t.value)
    return t

# simbolo especial 
def t_SIMBOLO_ESPECIAL(t):
    r'[()\{\}\[\]:,;]'
    contadores_tokens['SIMBOLO_ESPECIAL'] += 1
    return t

# operadores
def t_OPERADOR(t):
    r'[\+\-\*\=/]'
    contadores_tokens['OPERADOR'] += 1
    return t

# ignorar salto de lineas y espacios en blanco
t_ignore = ' \t\n'

# manejo de errores
def t_ANY_error(t):
    print(f"Carácteres no reconocidos: {t.value}")
    t.lexer.skip(1)

# palabras reservadas
palabras_reservadas = {
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
}

# lexer
lexer = lex.lex()

# entrada a analizar 
entrada = 'a = 4 suma = a + 3'
lexer.input(entrada)

while True:
    token = lexer.token()
    if not token:
        break


print("OPERADORES:", contadores_tokens['OPERADOR'])
print("SIMBOLOS ESPECIALES:", contadores_tokens['SIMBOLO_ESPECIAL'])
for tipo_token, cantidad in contadores_tokens.items():
    if tipo_token not in ['OPERADOR', 'SIMBOLO_ESPECIAL']:
        print(f"{tipo_token}: {cantidad}")
