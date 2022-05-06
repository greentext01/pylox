from scanner.keywords import KEYWORDS as kwds
from scanner.token import Token
import lox
from scanner.token_type import TokenType as tt


class Scanner:
    """
    Splits the source code into tokens
    """

    def __init__(self, source: str):
        # The full source code
        self.source = source

        # The tokens previously scanned
        self.tokens = []

        # Start is the beginning of the token
        self.start = 0

        # Currnet is the character that we're currently scanning
        self.current = 0

        # The current line being scanned
        self.line = 1

    def scan(self):
        """
        Scan the entire source code
        """
        while not self.is_done():
            # After scanning a token, set the beginning of
            # the current token to the current character
            self.start = self.current
            self.scan_token()

        # Add the EOF token
        self.tokens.append(Token(tt.EOF, '', None, self.line))
        return self.tokens

    def scan_token(self):
        """
        Scan a single token
        """
        c = self.advance()

        # To support versions below 3.10
        if c == "(":
            self.add_token(tt.LEFT_PAREN)

        elif c == ")":
            self.add_token(tt.RIGHT_PAREN)

        elif c == "{":
            self.add_token(tt.LEFT_BRACE)

        elif c == "}":
            self.add_token(tt.RIGHT_BRACE)

        elif c == ",":
            self.add_token(tt.COMMA)

        elif c == ".":
            self.add_token(tt.DOT)

        elif c == "-":
            self.add_token(tt.MINUS)

        elif c == "+":
            self.add_token(tt.PLUS)

        elif c == ";":
            self.add_token(tt.SEMICOLON)

        elif c == "*":
            self.add_token(tt.STAR)

        # Match tokens where the first character has a different
        # meaning when it's by itself
        elif c == "!":
            self.add_token(tt.BANG_EQUAL if self.match("=") else tt.BANG)

        elif c == "=":
            self.add_token(tt.EQUAL_EQUAL if self.match("=") else tt.EQUAL)

        elif c == "<":
            self.add_token(tt.LESS_EQUAL if self.match("=") else tt.LESS)

        elif c == ">":
            self.add_token(tt.GREATER_EQUAL if self.match("=") else tt.GREATER)

        # Ignore spaces, carriage returns, and tabs
        elif c == " " or c == "\r" or c == "\t":
            pass

        # Handle slash and comments
        elif c == "/":
            # If the slash has another slash after
            if self.match("/"):
                # Ignore characters until newline or program end
                while self.peek() != "\n" and not self.is_done():
                    self.advance()
            else:
                self.add_token(tt.SLASH)

        elif c == "\n":
            self.line += 1

        # Find string literals
        elif c == '"':
            while self.peek() != '"' and not self.is_done():
                if self.peek() == "\n":
                    self.line += 1

                self.advance()

            if self.is_done():
                lox.Lox.report(self.line, "Unterminated string")

            # Ending "
            self.advance()

            # Cut off off both "
            self.add_token(tt.STRING, self.source[self.start + 1:self.current - 1])

        # Find number literals
        elif c.isdigit():
            while self.peek().isdigit():
                self.advance()

            # Find a fractional part
            if self.peek() == "." and self.peek_next().isdigit():
                # Consume the "."
                self.advance()

                while self.peek().isdigit():
                    self.advance()

            self.add_token(tt.NUMBER, float(
                self.source[self.start:self.current]))

        # Find keywords and identifiers
        elif c.isalnum():
            while self.peek().isalpha():
                self.advance()

            keyword = kwds.get(self.source[self.start:self.current])

            if keyword == None:
                keyword = tt.IDENTIFIER

            self.add_token(keyword)

        else:
            lox.Lox.report(self.line, f"Unexpected character '{c}'")

    def peek(self):
        """
        Return current character without incrementing current
        """
        if self.is_done():
            return "\0"

        return self.source[self.current]

    def peek_next(self):
        """
        Return next character without incrementing current
        """
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def peek_previous(self):
        """
        Return previous character without incrementing current
        """
        if self.current - 1 >= len(self.source) or self.current - 1 < 0:
            return "\0"

        return self.source[self.current - 1]

    def advance(self):
        """
        Return current character, and increment current
        """
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected):
        """
        If current character is equal to `expected`,
        return True and increment current.

        Otherwise, return false without incrementing
        current.
        """
        if self.is_done():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def is_done(self):
        """
        Returns True if current has passed
        the end of the source code
        """
        return self.current >= len(self.source)

    def add_token(self, type: tt, literal=None):
        """
        Generates and adds a new token,
        without incrementing current
        """
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
