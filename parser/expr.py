from dataclasses import dataclass
from scanner.token import Token


class Expr:
    def accept(self, visitor):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    op: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


@dataclass
class Unary(Expr):
    op: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


@dataclass
class Literal(Expr):
    value: any

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class Grouping(Expr):
    expr: Expr

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Visitor:
    def visit_binary_expr(self, expr: Binary):
        pass

    def visit_unary_expr(self, expr: Unary):
        pass

    def visit_literal_expr(self, expr: Literal):
        pass

    def visit_grouping_expr(self, expr: Grouping):
        pass
