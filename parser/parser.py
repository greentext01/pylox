from parser.expr import Binary, Grouping, Literal, Unary
from parser.parsing_error import ParseError

import lox
from parser.stmt import Expression, Print
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
                statements.append(self.statement())

            return statements
        except ParseError:
            return None

    def statement(self):
        if self.match(tt.PRINT):
            return self.print_statement()
        else:
            return self.expression_statement()

    def print_statement(self):
        expr = self.expression()
        self.expect(tt.SEMICOLON, "Expected ';' after value")
        return Print(expr)

    def expression_statement(self):
        expr = self.expression()
        self.expect(tt.SEMICOLON, "Expected ';' after expression")
        return Expression(expr)

    def expression(self):
        return self.equality()

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
            self.error(self.peek().line, error)

    def error(self, line: int, message: str):
        lox.Lox.error(line, message)
        return ParseError()

    def advance(self):
        if not self.is_done():
            self.current += 1

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
