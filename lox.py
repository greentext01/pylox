from parser.ast_printer import AstPrinter
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
            print("Usage: pylox [script]")
            exit(1)
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
        
        parser = Parser(tokens)
        tree = parser.parse()
        
        printer = AstPrinter()
        printer.print(tree)
