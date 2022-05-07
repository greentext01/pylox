import time
from interpreter.interpreter import Interpreter
from parser.expr import LoxCallable


class Clock(LoxCallable):
    def arity(self):
        return 0

    def call(interpreter: Interpreter, arguments: list):
        return time.time()

    def __str__(self) -> str:
        return "<native fn>"
