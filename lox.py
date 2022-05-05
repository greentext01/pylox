from interpreter.interpreter import Interpreter
from interpreter.lox_runtime_error import LoxRuntimeError
from parser.parser import Parser
import sys
from scanner.scanner import Scanner


class Lox:
    has_error = False

    @classmethod
    def error(self, line: int, message: str):
        print(f"Error at line {line}: {message}")
        self.has_error = True

    def main(self):
        if len(sys.argv) < 2:
            self.runShell()
        else:
            self.runFile(sys.argv[1])

    def runFile(self, path: str):
        with open(path) as file:
            self.run(file.read(), False)

        if self.has_error:
            exit(1)

    def runShell(self):
        while True:
            try:
                self.run(input(">>> "), True)
            except KeyboardInterrupt:
                exit(0)
            except BaseException as error:
                print(error)

    def run(self, source, repl):
        scanner = Scanner(source)
        tokens = scanner.scan()

        if self.has_error:
            return

        parser = Parser(tokens)
        tree = parser.parse()

        if self.has_error:
            return

        interpreter = Interpreter(repl)
        interpreter.interpret(tree)

        if self.has_error:
            return

    @classmethod
    def runtime_error(self, error: LoxRuntimeError):
        print(f"Error at line {error.token.line}:\n"
              f"{error.message}")

        self.has_error = True
