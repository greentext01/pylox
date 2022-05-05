from interpreter.lox_runtime_error import LoxRuntimeError
from parser.expr import Binary, Expr, Literal, Unary, ExprVisitor, Grouping
from parser.stmt import Expression, Print, Stmt, StmtVisitor
from scanner.token_type import TokenType as tt
import lox


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, repl: bool):
        self.repl = repl

    def interpret(self, stmts: list[Stmt]):
        try:
            for stmt in stmts:
                result = self.run(stmt)
                if self.repl:
                    print(self.stringify(result))

        except LoxRuntimeError as error:
            lox.Lox.runtime_error(error)

    def run(self, expr: Expr | Stmt):
        return expr.accept(self)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.run(expr.expr)

    def visit_unary_expr(self, expr: Unary):
        right = self.run(expr.right)

        if expr.op.type == tt.MINUS:
            self.check_number_operand(right)
            return -right

        elif expr.op.type == tt.BANG:
            return not self.is_truthy(right)

    def visit_binary_expr(self, expr: Binary):
        right = self.run(expr.right)
        left = self.run(expr.left)

        if expr.op.type == tt.PLUS:
            if (type(left) == float and
                    type(right) == float) \
                or (type(left) == str and
                    type(right) == str):

                return left + right

        elif expr.op.type == tt.MINUS:
            self.check_number_operands(expr.op, left,
                                       right)
            return left - right

        elif expr.op.type == tt.STAR:
            self.check_number_operands(expr.op, left,
                                       right)
            return left * right

        elif expr.op.type == tt.SLASH:
            self.check_number_operands(expr.op, left,
                                       right)

            if left == 0:
                raise LoxRuntimeError(
                    f"Division by 0 between {self.stringify(right)} "
                    f"and {self.stringify(left)}",
                    expr.op)

            return left / right

        elif expr.op.type == tt.EQUAL_EQUAL:
            return left == right

        elif expr.op.type == tt.BANG_EQUAL:
            return left != right

        elif expr.op.type == tt.LESS:
            self.check_number_operands(expr.op, left,
                                       right)
            return left < right

        elif expr.op.type == tt.LESS_EQUAL:
            self.check_number_operands(expr.op, left,
                                       right)
            return left <= right

        elif expr.op.type == tt.GREATER:
            self.check_number_operands(expr.op, left,
                                       right)
            return left > right

        elif expr.op.type == tt.GREATER_EQUAL:
            self.check_number_operands(expr.op, left,
                                       right)
            return left >= right

    def visit_expression_stmt(self, expr: Expression):
        self.run(expr.expr)

    def visit_print_stmt(self, expr: Print):
        print(self.stringify(self.run(expr.expr)))

    def is_truthy(self, expr: Literal):
        """
        Returns False if the value is either None or False
        Otherwise, return True
        """
        if expr.value == None:
            return False

        elif type(expr.value) == bool:
            return expr.value

        else:
            return True

    def stringify(self, obj):
        if type(obj) == float:
            if obj.is_integer():
                return str(int(obj))

            return str(obj)
        elif obj == None:
            return "nil"
        else:
            return obj

    def check_number_operand(self, operator, operand):
        if type(operand.value) != float:
            raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left: Expr, right: Expr):
        if type(left) != float \
                or type(right) != float:

            raise LoxRuntimeError(operator, "Operands must be numbers.")
