from ply import lex, yacc
import keyword
import ply.yacc
import ply.lex
import struct


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

print("""======================================================
      Analizador sintáctico
======================================================""")

def p_definicion_funcion(p):
    '''
    definicion_funcion : COMENTARIO definicion_funcion_no_comentario
                       | definicion_funcion_no_comentario
    '''

def p_definicion_funcion_no_comentario(p):
    '''
    definicion_funcion_no_comentario : PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL parametros SIMBOLO_ESPECIAL
                                     | PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL
    '''

def p_parametros(p):
    '''
    parametros : IDENTIFICADOR
               | parametros SIMBOLO_ESPECIAL IDENTIFICADOR
               | parametros SIMBOLO_ESPECIAL CADENA
               | parametros SIMBOLO_ESPECIAL NUMERO
               | parametros SIMBOLO_ESPECIAL OPERADOR
    '''



def p_error(p):
    print("Error de sintaxis:", p)

parser = yacc.yacc()

if __name__ == '__main__':
    with open("analisis.txt", mode="r") as entrada:
        resultado = parser.parse(entrada.read(), lexer=lexer)

        

##################################### Analizador semantico #############################################
#
#print("""======================================================
#      Analizador Semantico
#======================================================""")
## Lista para almacenar variables definidas
#variables_definidas = []
#
#def p_definicion_variable(p):
#    '''
#    definicion_variable : PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL OPERADOR NUMERO
#                        | PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL OPERADOR CADENA
#    '''
#    variables_definidas.append(p[2])  # Agregar el identificador de la variable a la lista de variables definidas
#
#def p_uso_variable(p):
#    '''
#    uso_variable : IDENTIFICADOR
#    '''
#    if variables_definidas and p[1] not in variables_definidas:
#        print(f"Error semántico: La variable '{p[1]}' no está definida.")
#
#def p_definicion_funcion_semantica(p):
#    '''
#    definicion_funcion_semantica : PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL identificador_coma SIMBOLO_ESPECIAL COMENTARIO
#    '''
## Integración del análisis semántico
#def p_definicion_funcion(p):
#    '''
#    definicion_funcion : COMENTARIO
#                       | definicion_funcion_def
#                       | definicion_variable
#                       | uso_variable
#                       | definicion_funcion_semantica
#    '''
#
#
## Llamada al parser yacc
#parser = yacc.yacc()
#
#if __name__ == '__main__':
#    with open("analisis.txt", mode="r") as entrada:
#        resultado = parser.parse(entrada.read(), lexer=lexer)
#        print('Resultado:', resultado)
#
############################# Optimizacion codigo ###########################################  
#class IntermediateCode:
#    def __init__(self):
#        self.code = []
#
#    def add_instruction(self, opcode, operands):
#        self.code.append((opcode, operands))
#
#    def __str__(self):
#        return '\n'.join(f'{opcode} {", ".join(operands)}' for opcode, operands in self.code)
#
#intermediate_code = IntermediateCode()
#
#def p_statement(p):
#    '''statement : IDENTIFIER '=' expression'''
#    p[0] = p[3]  # In a real compiler, you would generate intermediate code here
#    intermediate_code.add_instruction('MOV', [p[3], p[1]])
#
#def optimize_code(code):
#    optimized_code = []
#    last_assigned = None
#    for opcode, operands in code:
#        if opcode == 'MOV':
#            dest, src = operands
#            if src != last_assigned:
#                optimized_code.append((opcode, operands))
#                last_assigned = dest
#        else:
#            optimized_code.append((opcode, operands))
#            last_assigned = None
#    return optimized_code
#
## Optimizing the intermediate code
#optimized_code = optimize_code(intermediate_code.code)
#
#def generate_machine_code(optimized_code):
#    machine_code = []
#    for opcode, operands in optimized_code:
#        # Translate intermediate code to machine code
#        # Example: MOV eax, ebx
#        machine_code.append(f'{opcode} {", ".join(operands)}')
#    return machine_code
#
## Generating machine code
#machine_code = generate_machine_code(optimized_code)
#
#
######################################### Codigo objeto ####################################################
#class ELFObjectFile:
#    def __init__(self, filename):
#        self.filename = filename
#        self.sections = []
#
#    def add_section(self, name, data):
#        self.sections.append((name, data))
#
#    def write(self):
#        with open(self.filename, 'wb') as f:
#            # Write ELF header
#            f.write(b'\x7fELF')  # ELF magic number
#            f.write(b'\x01')     # 32-bit format (change to b'\x02' for 64-bit)
#            f.write(b'\x01')     # Little-endian encoding
#            f.write(b'\x01')     # ELF version
#            f.write(b'\x00' * 9) # Padding
#
#            # Write program header (for simplicity, set to all zeros)
#            f.write(b'\x00' * 32)
#
#            # Write section header table
#            section_offset = 52 + len(self.sections) * 40  # ELF header size + program header size
#            f.write(struct.pack('<I', section_offset))     # Offset of section header table
#            f.write(struct.pack('<H', len(self.sections)))# Number of sections
#            f.write(struct.pack('<H', 0))                 # Size of each section header entry
#            f.write(struct.pack('<I', 0))                 # Index of section header entry for string table (unused)
#
#            # Write section headers
#            for i, (name, data) in enumerate(self.sections, start=1):
#                f.write(struct.pack('<I', i))               # Index of section name in string table
#                f.write(struct.pack('<I', 1))               # Type (SHT_PROGBITS)
#                f.write(struct.pack('<I', 6))               # Flags (SHF_EXECINSTR)
#                f.write(struct.pack('<I', 0))               # Address (unused)
#                f.write(struct.pack('<I', len(data)))       # Offset
#                f.write(struct.pack('<I', len(data)))       # Size
#                f.write(struct.pack('<I', 0))               # Link (unused)
#                f.write(struct.pack('<I', 0))               # Info (unused)
#                f.write(struct.pack('<I', 1))               # Alignment
#                f.write(struct.pack('<I', 0))               # Entry size (unused)
#
#            # Write section data
#            for name, data in self.sections:
#                f.write(data)
#
## Uso de la clase ELFObjectFile
#elf_file = ELFObjectFile('output.o')
#elf_file.add_section('.text', b'\x90\x90\x90\x90')  # Por ejemplo, aquí añadimos la sección de código de máquina
#elf_file.write()
#
################################# Tabla de simbolos ################################
#
#print("""======================================================
#      Tabla de simbolos 
#======================================================""")
#
#class SymbolTable:
#    def __init__(self):
#        self.symbols = {}
#
#    def add_symbol(self, name, value):
#        self.symbols[name] = value
#
#    def get_symbol_value(self, name):
#        return self.symbols.get(name)
#
#    def __str__(self):
#        return '\n'.join(f'{name}: {value}' for name, value in self.symbols.items())
#
############################## tabla de símbolos #####################################
#
## Clase para la tabla de símbolos
#class SymbolTable:
#    def __init__(self):
#        self.symbols = {}
#
#    def add_symbol(self, name, value):
#        self.symbols[name] = value
#
#    def get_symbol_value(self, name):
#        return self.symbols.get(name)
#
#    def __str__(self):
#        return '\n'.join(f'{name}: {value}' for name, value in self.symbols.items())
#
############################# tabla de símbolos ########################
#
## Crear una instancia de la tabla de símbolos
#symbol_table = SymbolTable()
#
## Actualizar el análisis semántico para construir la tabla de símbolos
#def p_definicion_variable(p):
#    '''
#    definicion_variable : PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL OPERADOR NUMERO
#                        | PALABRA_RESERVADA IDENTIFICADOR SIMBOLO_ESPECIAL OPERADOR CADENA
#    '''
#    variable_name = p[2]
#    variable_value = p[4] if isinstance(p[4], int) else p[4][1:-1]  # Obtener el valor de la variable
#    symbol_table.add_symbol(variable_name, variable_value)
#
#def p_uso_variable(p):
#    '''
#    uso_variable : IDENTIFICADOR
#    '''
#    variable_name = p[1]
#    if symbol_table.get_symbol_value(variable_name) is None:
#        print(f"Error semántico: La variable '{variable_name}' no está definida.")
#
## Visualización de la tabla de símbolos
#print("Tabla de símbolos:")
#print(symbol_table)
#