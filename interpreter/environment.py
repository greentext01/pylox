from scanner.token import Token
from interpreter.lox_runtime_error import LoxRuntimeError


class Environment:
    def __init__(self, enclosing=None):
        self.variables = {}
        self.enclosing: Environment = enclosing

    def get(self, name: Token):
        if name.lexeme in self.variables:
            return self.variables[name.lexeme]
        elif self.enclosing != None:
            return self.enclosing.get(name)
        else:
            raise LoxRuntimeError(f"Undefined variable "
                                  f"'{name.lexeme}'", name)

    def define(self, name: Token, value):
        if name.lexeme in self.variables:
            raise LoxRuntimeError(f"Variable already defined "
                                  f"'{name.lexeme}'", name)
        else:
            self.variables[name.lexeme] = value
            
    def set(self, name: Token, value):
        if name.lexeme in self.variables:
            self.variables[name.lexeme] = value
        elif self.enclosing != None:
            self.enclosing.set(name, value)
        else:
            raise LoxRuntimeError(f"Undefined variable "
                                  f"'{name.lexeme}'", name)
        
