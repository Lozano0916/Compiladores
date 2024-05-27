
from analizador_lexico import lexer
from analizador_sintactico import AnalizadorSintactico
from analizador_semantico import AnalizadorSemantico
from codigo_objeto import GeneradorCodigo


def analizar_todo(nombre_archivo):
    # Analizador léxico
    entrada = open(nombre_archivo, mode="r")
    lexer.input(entrada.read())
    print("""=====================================================
          Analizador lexico
=====================================================""")
    while True:
        token = lexer.token()
        if not token:
            break
        print(f"{token.type}: {token.value}")

    # Analizador sintáctico
analizador_sintactico = AnalizadorSintactico()
print("""=====================================================
          Analizador sintactico
=====================================================""")
arbol_abstracto = analizador_sintactico.analizar_codigo("analisis.txt")

        # Analizador semántico

analizador_sintactico = AnalizadorSintactico()
analizador_semantico = AnalizadorSemantico()
arbol_abstracto = analizador_sintactico.analizar_codigo("analisis.txt")
analizador_semantico.analizar(arbol_abstracto)

# Generador de código objeto
print("""=====================================================
          Generador de Código Objeto
=====================================================""")
generador_codigo = GeneradorCodigo()
codigo_objeto = generador_codigo.generar_codigo(arbol_abstracto)
for instruccion in codigo_objeto:
    print(instruccion)

