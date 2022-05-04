from dataclasses import dataclass
from scanner.token_type import TokenType as tt


@dataclass
class Token:
    type: tt
    lexeme: str
    literal: object
    line: int

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal} {self.line}"
