from interpreter.interpreter import Interpreter
from interpreter.lox_runtime_error import LoxRuntimeError
from parser.parser import Parser
import sys
from scanner.scanner import Scanner
from scanner.token import Token
from scanner.token_type import TokenType as tt


class Lox:
    has_error = False

    @classmethod
    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        self.has_error = True

    @classmethod
    def error(self, token: Token, message: str):
        if (token.type == tt.EOF):
            self.report(token.line, f" at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

        self.has_error = True

    def main(self):
        if len(sys.argv) < 2:
            print("Usage: python main.py [program]")
        else:
            self.runFile(sys.argv[1])

    def runFile(self, path: str):
        with open(path) as file:
            self.run(file.read())

        if self.has_error:
            exit(1)

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan()

        if self.has_error:
            return

        parser = Parser(tokens)
        tree = parser.parse()

        if self.has_error:
            return

        interpreter = Interpreter()
        interpreter.interpret(tree)

        if self.has_error:
            return

    @classmethod
    def runtime_error(self, error: LoxRuntimeError):
        print(f"Error at line {error.token.line}:\n"
              f"{error.message}")
        
        exit(1)
