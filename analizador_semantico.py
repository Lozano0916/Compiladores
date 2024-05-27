import ast
from analizador_sintactico import AnalizadorSintactico
from prettytable import PrettyTable

class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = []

    def analizar(self, arbol):
        self.visit(arbol, "global") 
        self.imprimir_tabla_simbolos()

    def visit(self, nodo, ambito):
        if isinstance(nodo, ast.FunctionDef):
            for arg in nodo.args.args:
                self.agregar_variable(arg.arg, "parámetro", nodo.name, nodo.name)  
            ambito = nodo.name 
        elif isinstance(nodo, ast.Assign):
            for target in nodo.targets:
                if isinstance(target, ast.Name):
                    valor = nodo.value
                    tipo_dato = self.obtener_tipo_dato(valor)
                    self.agregar_variable(target.id, tipo_dato, ambito, ambito)  

        for child_node in ast.iter_child_nodes(nodo):
            self.visit(child_node, ambito)

    def agregar_variable(self, nombre, tipo, ambito, ambito_actual):
        self.tabla_simbolos.append({"variable": nombre, "tipo": tipo, "ambito": ambito_actual})

    def obtener_tipo_dato(self, valor):
        if isinstance(valor, ast.Str):
            return "str"
        elif isinstance(valor, ast.Num):
            return type(valor.n).__name__
        elif isinstance(valor, ast.List):
            return "list"
        elif isinstance(valor, ast.Dict):
            return "dict"
        elif isinstance(valor, ast.Tuple):
            return "tuple"
        elif isinstance(valor, ast.NameConstant):
            return str(type(valor.value).__name__)
        elif isinstance(valor, ast.UnaryOp):  
            return self.deducir_tipo_de_valor(valor.operand)
        elif isinstance(valor, ast.BinOp):
            return self.deducir_tipo_de_valor(valor.left)
        elif isinstance(valor, ast.Call):  
            return "funcion"
        else:
            return "desconocido"


    def imprimir_tabla_simbolos(self):

        tabla = PrettyTable()
        tabla.field_names = ["Variable", "Tipo", "Ámbito"] 
        
        for simbolo in self.tabla_simbolos:
            tabla.add_row([simbolo["variable"], simbolo["tipo"], simbolo["ambito"]]) 
        
        print("""=====================================================
          Analizador Semantico
=====================================================""")
        print(tabla)

