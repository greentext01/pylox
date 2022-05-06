from dataclasses import dataclass
from parser.expr import Expr
from scanner.token import Token


class Stmt:
    def accept(self, visitor):
        pass


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


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


@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


@dataclass
class If(Stmt):
    condition: Expr
    thenBranch: Stmt
    elseBranch: Stmt | None

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


class StmtVisitor:
    def visit_expression_stmt(self, expr: Expression):
        pass

    def visit_print_stmt(self, expr: Print):
        pass

    def visit_var_stmt(self, expr: Var):
        pass

    def visit_block_stmt(self, expr: Var):
        pass

    def visit_if_stmt(self, expr: Var):
        pass
