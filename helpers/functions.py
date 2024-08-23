import ast
import inspect


def contains_explicit_return(f):
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))
