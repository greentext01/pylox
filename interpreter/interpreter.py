from interpreter.clock import Clock
from interpreter.environment import Environment
from interpreter.lox_runtime_error import LoxRuntimeError
from parser.expr import Assign, Binary, Call, Expr, Literal, Logical, LoxCallable, Unary, ExprVisitor, Grouping, Variable
from parser.stmt import Block, Expression, Function, If, Print, Stmt, StmtVisitor, Var, While
from scanner.token_type import TokenType as tt
import lox


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

        self.globals.define("clock", Clock())

    def interpret(self, stmts: list[Stmt]):
        try:
            for stmt in stmts:
                self.run(stmt)

        except LoxRuntimeError as error:
            lox.Lox.runtime_error(error)

    def run(self, expr: Expr | Stmt):
        return expr.accept(self)

    def execute_block(self, stmts: list[Stmt], environment: Environment):
        previous = self.environment

        try:
            self.environment = environment

            for stmt in stmts:
                self.run(stmt)
        finally:
            self.environment = previous

    def visit_block_stmt(self, expr: Block):
        self.execute_block(expr.statements, Environment(self.environment))

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.run(expr.expr)

    def visit_if_stmt(self, expr: If):
        if self.is_truthy(self.run(expr.condition)):
            self.run(expr.thenBranch)
        elif expr.elseBranch != None:
            self.run(expr.elseBranch)

    def visit_unary_expr(self, expr: Unary):
        right = self.run(expr.right)

        if expr.op.type == tt.MINUS:
            self.check_number_operand(right)
            return -right

        elif expr.op.type == tt.BANG:
            return not self.is_truthy(right)

    def visit_logical_expr(self, expr: Logical):
        left = self.run(expr.left)

        if expr.op.type == tt.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.run(expr.right)

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

        elif expr.op.type == tt.MODULO:
            self.check_number_operands(expr.op, left,
                                       right)
            return left % right

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

    def visit_var_stmt(self, expr: Var):
        value = None

        if expr.initializer != None:
            value = self.run(expr.initializer)

        self.environment.define(expr.name, value)

    def visit_while_stmt(self, expr: While):
        while(self.is_truthy(self.run(expr.condition))):
            self.run(expr.body)

    def visit_assignment_expr(self, expr: Assign):
        val = self.run(expr.value)
        self.environment.set(expr.name, val)
        return val
    
    def visit_call_expr(self, expr: Call):
        callee = self.run(expr.callee)
        
        arguments = 9
    
    def visit_function_stmt(self, expr: Function):
        raise NotImplemented

    def visit_variable_expr(self, expr: Variable):
        return self.environment.get(expr.name)

    def is_truthy(self, object) -> bool:
        """
        Returns False if the value is either None or False
        Otherwise, return True
        """
        if object == None:
            return False

        elif type(object) == bool:
            return object

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
            raise LoxRuntimeError(operator, "Operand must be a number")

    def check_number_operands(self, operator, left: Expr, right: Expr):
        if type(left) != float \
                or type(right) != float:

            raise LoxRuntimeError("Operands must be numbers", operator)
