from dataclasses import dataclass
from parser.expr import Expr
from scanner.token import Token


class LoxCallable:
    def call(self, interpreter, args):
        pass

    def arity(self) -> int:
        pass


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


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


@dataclass
class Function(Stmt):
    name: Token
    body: list[Stmt]
    arguments: list[Expr]

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class StmtVisitor:
    def visit_expression_stmt(self, expr: Expression):
        pass

    def visit_print_stmt(self, expr: Print):
        pass

    def visit_var_stmt(self, expr: Var):
        pass

    def visit_block_stmt(self, expr: Block):
        pass

    def visit_if_stmt(self, expr: If):
        pass

    def visit_while_stmt(self, expr: While):
        pass

    def visit_function_stmt(self, expr: Function):
        pass
