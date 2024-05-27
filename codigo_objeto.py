import ast

class GeneradorCodigoIntermedio:
    def __init__(self):
        self.codigo_intermedio = []
        self.temporales = 0

    def nuevo_temporal(self):
        self.temporales += 1
        return f't{self.temporales}'

    def generar_codigo(self, nodo):
        try:
            if isinstance(nodo, ast.Module):
                for stmt in nodo.body:
                    self.generar_codigo(stmt)
            elif isinstance(nodo, ast.FunctionDef):
                self.codigo_intermedio.append(f'function {nodo.name}()')
                for stmt in nodo.body:
                    self.generar_codigo(stmt)
                self.codigo_intermedio.append(f'end function {nodo.name}')
            elif isinstance(nodo, ast.Assign):
                target = nodo.targets[0]
                value = self.generar_codigo(nodo.value)
                if isinstance(target, ast.Name):
                    self.codigo_intermedio.append(f'{target.id} = {value}')
                else:
                    raise NotImplementedError('Asignaciones complejas no están soportadas')
            elif isinstance(nodo, ast.BinOp):
                left = self.generar_codigo(nodo.left)
                right = self.generar_codigo(nodo.right)
                op = self.obtener_operador(nodo.op)
                temp = self.nuevo_temporal()
                self.codigo_intermedio.append(f'{temp} = {left} {op} {right}')
                return temp
            elif isinstance(nodo, ast.Constant):
                return nodo.value
            elif isinstance(nodo, ast.Name):
                return nodo.id
            elif isinstance(nodo, ast.Expr):
                return self.generar_codigo(nodo.value)
            elif isinstance(nodo, ast.Call):
                args = [str(self.generar_codigo(arg)) for arg in nodo.args]
                func_name = nodo.func.id
                temp = self.nuevo_temporal()
                self.codigo_intermedio.append(f'{temp} = {func_name}({", ".join(args)})')
                return temp
            elif isinstance(nodo, ast.Return):
                value = self.generar_codigo(nodo.value)
                self.codigo_intermedio.append(f'return {value}')
            else:
                raise NotImplementedError(f'Nodo no soportado: {type(nodo).__name__}')
        except NotImplementedError as e:
            print(f'Error en la generación de código intermedio: {e}')

    def obtener_operador(self, op):
        if isinstance(op, ast.Add):
            return '+'
        elif isinstance(op, ast.Sub):
            return '-'
        elif isinstance(op, ast.Mult):
            return '*'
        elif isinstance(op, ast.Div):
            return '/'
        else:
            raise NotImplementedError(f'Operador no soportado: {type(op).__name__}')

    def imprimir_codigo_intermedio(self):
        for instruccion in self.codigo_intermedio:
            print(instruccion)
