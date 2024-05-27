# generador_codigo.py
import ast

class GeneradorCodigo:
    def __init__(self):
        self.codigo_intermedio = []

    def generar_codigo(self, arbol):
        self.visit(arbol)
        return self.codigo_intermedio

    def visit(self, nodo):
        print(f"Visitando nodo de tipo: {type(nodo)}")
        if isinstance(nodo, ast.Module):
            for stmt in nodo.body:
                self.visit(stmt)
        elif isinstance(nodo, ast.FunctionDef):
            self.visit_functiondef(nodo)
        elif isinstance(nodo, ast.Assign):
            self.visit_assign(nodo)
        elif isinstance(nodo, ast.Expr):
            self.visit_expr(nodo)
        elif isinstance(nodo, ast.Return):
            self.visit_return(nodo)
        elif isinstance(nodo, ast.Call):
            self.visit_call(nodo)
        elif isinstance(nodo, ast.Name):
            self.visit_name(nodo)
        elif isinstance(nodo, ast.BinOp):
            self.visit_binop(nodo)
        elif isinstance(nodo, ast.Num):
            self.visit_num(nodo)
        elif isinstance(nodo, ast.Constant):
            self.visit_constant(nodo)
        else:
            raise NotImplementedError(f"Node type {type(nodo)} is not implemented in the generator")

    def visit_functiondef(self, nodo):
        print(f"Visitando nodo de tipo FunctionDef: {nodo.name}")
        self.codigo_intermedio.append(f"FUNC_BEGIN {nodo.name}")
        for stmt in nodo.body:
            self.visit(stmt)
        self.codigo_intermedio.append("FUNC_END")

    def visit_assign(self, nodo):
        print("Visitando nodo de tipo Assign")
        for target in nodo.targets:
            if isinstance(target, ast.Name):
                self.visit(nodo.value)
                self.codigo_intermedio.append(f"STORE {target.id}")

    def visit_expr(self, nodo):
        print("Visitando nodo de tipo Expr")
        self.visit(nodo.value)

    def visit_return(self, nodo):
        print("Visitando nodo de tipo Return")
        if nodo.value:
            self.visit(nodo.value)
        self.codigo_intermedio.append("RETURN")

    def visit_call(self, nodo):
        print("Visitando nodo de tipo Call")
        for arg in nodo.args:
            self.visit(arg)
        if isinstance(nodo.func, ast.Name):
            self.codigo_intermedio.append(f"CALL {nodo.func.id}")
        else:
            raise NotImplementedError(f"Function call type {type(nodo.func)} is not implemented in the generator")

    def visit_name(self, nodo):
        print("Visitando nodo de tipo Name")
        self.codigo_intermedio.append(f"LOAD {nodo.id}")

    def visit_binop(self, nodo):
        print("Visitando nodo de tipo BinOp")
        self.visit(nodo.left)
        self.visit(nodo.right)
        op_map = {
            ast.Add: "ADD",
            ast.Sub: "SUB",
            ast.Mult: "MUL",
            ast.Div: "DIV"
        }
        if isinstance(nodo.op, ast.Add):
            self.codigo_intermedio.append(op_map[ast.Add])
        elif isinstance(nodo.op, ast.Sub):
            self.codigo_intermedio.append(op_map[ast.Sub])
        elif isinstance(nodo.op, ast.Mult):
            self.codigo_intermedio.append(op_map[ast.Mult])
        elif isinstance(nodo.op, ast.Div):
            self.codigo_intermedio.append(op_map[ast.Div])

    def visit_num(self, nodo):
        print("Visitando nodo de tipo Num")
        self.codigo_intermedio.append(f"PUSH {nodo.n}")

    def visit_constant(self, nodo):
        print("Visitando nodo de tipo Constant")
        if isinstance(nodo.value, str):
            self.codigo_intermedio.append(f"PUSH \"{nodo.value}\"")
        elif isinstance(nodo.value, bool):
            self.codigo_intermedio.append(f"PUSH {int(nodo.value)}")
        elif nodo.value is None:
            self.codigo_intermedio.append("PUSH None")
        else:
            raise NotImplementedError(f"Constant value {nodo.value} of type {type(nodo.value)} is not implemented in the generator")

if __name__ == "__main__":
    from analizador_sintactico import AnalizadorSintactico

    analizador_sintactico = AnalizadorSintactico()
    arbol = analizador_sintactico.analizar_codigo("analisis.txt")

    generador_codigo = GeneradorCodigo()
    codigo_objeto = generador_codigo.generar_codigo(arbol)

    print("""=====================================================
              Código Objeto
    =====================================================""")
    for instruccion in codigo_objeto:
        print(instruccion)
