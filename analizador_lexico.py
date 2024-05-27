from ply import lex, yacc
import keyword
import ply.yacc
import ply.lex


ply.yacc.yaccdebug = False
ply.lex.lexdebug = False

tokens = (
    'NUMERO',
    'IDENTIFICADOR',
    'PALABRA_RESERVADA',
    'CADENA',
    'OPERADOR',  
    'SIMBOLO_ESPECIAL',  
    'COMENTARIO'
)


contadores_tokens = {
    'PALABRA_RESERVADA': 0,
    'IDENTIFICADOR': 0,
    'CADENA': 0,
    'NUMERO': 0,
    'OPERADOR': 0,  
    'SIMBOLO_ESPECIAL': 0, 
    'COMENTARIO':0,
}

#palabras reservadas traidas con keyword
palabras_reservadas = {kw: kw.upper() for kw in keyword.kwlist}

# identificador
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFICADOR' if t.value not in palabras_reservadas else 'PALABRA_RESERVADA'
    contadores_tokens[t.type] += 1
    return t

# palabras reservadas
def t_PALABRA_RESERVADA(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabras_reservadas.get(t.value, 'IDENTIFICADOR')
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

#Comentario
def t_COMENTARIO(t):
    r'\#.*'
    contadores_tokens['COMENTARIO'] += 1
    return t

# ignorar salto de lineas y espacios en blanco
t_ignore = ' \t\n'

# manejo de errores
def t_ANY_error(t):
    print(f"Carácteres no reconocidos: {t.value}")
    t.lexer.skip(1)


# lexer
lexer = lex.lex()

# entrada a analizar 
entrada = open("analisis.txt", mode="r")
lexer.input(entrada.read())

######################################### Analizador Lexico ###########################################

print("""=====================================================
          Analizador lexico
=====================================================""")
while True:
    token = lexer.token()
    if not token:
        break
    
    print(f"{token.type}: {token.value}")

