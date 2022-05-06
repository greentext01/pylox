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


@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)


@dataclass
class Logical(Expr):
    left: Expr
    op: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor):
        return visitor.visit_assignment_expr(self)


class ExprVisitor:
    def visit_binary_expr(self, expr: Binary):
        pass
    
    def visit_logical_expr(self, expr: Binary):
        pass

    def visit_unary_expr(self, expr: Unary):
        pass

    def visit_literal_expr(self, expr: Literal):
        pass

    def visit_grouping_expr(self, expr: Grouping):
        pass

    def visit_variable_expr(self, expr: Variable):
        pass

    def visit_assignment_expr(self, expr: Assign):
        pass
