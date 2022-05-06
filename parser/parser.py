from parser.expr import Assign, Binary, Grouping, Literal, Unary, Variable
from parser.parsing_error import ParseError

import lox
from parser.stmt import Block, Expression, If, Print, Var
from scanner.token import Token
from scanner.token_type import TokenType as tt


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            statements = []

            while not self.is_done():
                statements.append(self.declaration())

            return statements
        except ParseError:
            return None

    def declaration(self):
        if self.match(tt.VAR):
            return self.var_declaration()
        else:
            return self.statement()

    def var_declaration(self):
        name = self.expect(tt.IDENTIFIER, "Expected variable name")
        initializer = None

        if self.match(tt.EQUAL):
            initializer = self.expression()

        self.expect(
            tt.SEMICOLON, "Expected ';' after variable declaration")

        return Var(name, initializer)

    def statement(self):
        if self.match(tt.PRINT):
            return self.print_statement()
        elif self.match(tt.LEFT_BRACE):
            return Block(self.block())
        elif self.match(tt.IF):
            return self.if_statement()
        else:
            return self.expression_statement()
        
    def if_statement(self):
        self.expect(tt.LEFT_PAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.expect(tt.RIGHT_PAREN, "Expected ')' after if condition")
        
        thenBranch = self.statement()
        elseBranch = None
        
        if self.match(tt.ELSE):
            elseBranch = self.statement()
        
        return If(condition, thenBranch, elseBranch)

    def print_statement(self):
        expr = self.expression()
        self.expect(tt.SEMICOLON, "Expected ';' after value")
        return Print(expr)

    def expression_statement(self):
        expr = self.expression()
        self.expect(tt.SEMICOLON, "Expected ';' after expression")
        return Expression(expr)

    def block(self):
        statements = []

        while not self.check(tt.RIGHT_BRACE) and not self.is_done():
            statements.append(self.declaration())

        self.expect(tt.RIGHT_BRACE, "Expect '}' after block")

        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        # Too hard to explain
        # Just look at the book
        # https://craftinginterpreters.com/statements-and-state.html
        expr = self.equality()

        if self.match(tt.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if type(expr) == Variable:
                return Assign(expr.name, value)

            self.error(equals, "Invalid assignment target")

        return expr

    def equality(self):
        comparison = self.comparison()

        while self.match(tt.EQUAL_EQUAL, tt.BANG_EQUAL):
            op = self.previous()
            comparison = Binary(comparison, op, self.comparison())

        return comparison

    def comparison(self):
        term = self.term()

        while self.match(tt.GREATER, tt.GREATER_EQUAL,
                         tt.LESS, tt.LESS_EQUAL):

            op = self.previous()
            term = Binary(term, op, self.term())

        return term

    def term(self):
        expr = self.factor()

        while self.match(tt.PLUS, tt.MINUS):
            op = self.previous()
            expr = Binary(expr, op, self.factor())

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(tt.STAR, tt.SLASH):
            op = self.previous()
            expr = Binary(expr, op, self.unary())

        return expr

    def unary(self):
        if self.match(tt.BANG, tt.MINUS):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)
        else:
            return self.primary()

    def primary(self):
        if self.match(tt.NUMBER, tt.STRING):
            return Literal(self.previous().literal)

        elif self.match(tt.TRUE):
            return Literal(True)

        elif self.match(tt.FALSE):
            return Literal(False)

        elif self.match(tt.NIL):
            return Literal(None)

        elif self.match(tt.LEFT_PAREN):
            expr = self.expression()
            self.expect(tt.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expr)

        elif self.match(tt.IDENTIFIER):
            return Variable(self.previous())

    def match(self, *expected: tt):
        if self.peek().type in expected:
            self.advance()
            return True

        return False

    def check(self, expected: tt):
        return self.peek().type == expected

    def expect(self, expected: tt, error: str):
        if self.check(expected):
            return self.advance()
        else:
            self.error(self.peek(), error)

    def error(self, token: Token, message: str):
        lox.Lox.error(token, message)
        return ParseError()

    def advance(self):
        if not self.is_done():
            self.current += 1
            return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()

        while not self.is_done():
            if self.previous().type == tt.SEMICOLON:
                return

            if self.peek().type in [
                tt.CLASS,
                tt.FUN,
                tt.VAR,
                tt.FOR,
                tt.IF,
                tt.WHILE,
                tt.PRINT,
                tt.RETURN
            ]:
                return

        self.advance()

    def is_done(self):
        return self.peek().type == tt.EOF
