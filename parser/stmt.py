from dataclasses import dataclass
from parser.expr import Expr


class Stmt:
    def accept(self, visitor):
        pass


@dataclass
class Expression(Stmt):
    expr: Expr

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expr: Expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)


class StmtVisitor:
    def visit_expression_stmt(self, expr: Expression):
        pass

    def visit_print_stmt(self, expr: Print):
        pass
