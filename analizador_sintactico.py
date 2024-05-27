import ast

print("""=====================================================
          Analizador sintactico
=====================================================""")
class AnalizadorSintactico:

    def analizar_archivo(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            codigo = archivo.read()
            return codigo

    def analizar_codigo(self, nombre_archivo):
        codigo = self.analizar_archivo(nombre_archivo)
        expresion_analizada = ast.parse(codigo)
        print(ast.dump(expresion_analizada))
        return expresion_analizada

analizador = AnalizadorSintactico()
analizador.analizar_codigo("analisis.txt")