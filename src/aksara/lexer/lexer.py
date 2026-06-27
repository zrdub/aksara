"""Lexer implementation for AKSARA."""

from __future__ import annotations

from aksara.errors import SyntaxAksaraError
from aksara.lexer.token import KEYWORDS, Token, TokenType


class Lexer:
    """Convert AKSARA source text into a stream of tokens."""

    def __init__(self, source: str) -> None:
        """Create a lexer for the provided source text."""
        self._source = source
        self._tokens: list[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._column = 1
        self._token_column = 1

    def scan_tokens(self) -> list[Token]:
        """Scan and return all tokens, including the EOF token."""
        while not self._is_at_end():
            self._start = self._current
            self._token_column = self._column
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line, self._column))
        return self._tokens

    def _scan_token(self) -> None:
        char = self._advance()
        if char == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif char == "[":
            self._add_token(TokenType.LEFT_BRACKET)
        elif char == "]":
            self._add_token(TokenType.RIGHT_BRACKET)
        elif char == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self._add_token(TokenType.COMMA)
        elif char == ".":
            self._add_token(TokenType.DOT)
        elif char == ":":
            self._add_token(TokenType.COLON)
        elif char == "-":
            self._add_token(TokenType.MINUS)
        elif char == "+":
            self._add_token(TokenType.PLUS)
        elif char == "*":
            self._add_token(TokenType.STAR)
        elif char == "%":
            self._add_token(TokenType.PERCENT)
        elif char == "!":
            self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            )
        elif char == "=":
            self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            )
        elif char == "<":
            self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            )
        elif char == ">":
            self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )
        elif char == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif char in {" ", "\r", "\t"}:
            return
        elif char == "\n":
            self._add_token(TokenType.NEWLINE)
            self._line += 1
            self._column = 1
        elif char == '"':
            self._string()
        else:
            if char.isdigit():
                self._number()
            elif char.isalpha() or char == "_":
                self._identifier()
            else:
                raise SyntaxAksaraError(
                    f"Karakter tidak dikenal: {char!r}.",
                    self._line,
                    self._token_column,
                )

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        text = self._source[self._start : self._current]
        self._add_token(KEYWORDS.get(text, TokenType.IDENTIFIER))

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        is_float = False
        if self._peek() == "." and self._peek_next().isdigit():
            is_float = True
            self._advance()
            while self._peek().isdigit():
                self._advance()

        text = self._source[self._start : self._current]
        literal: int | float = float(text) if is_float else int(text)
        self._add_token(TokenType.FLOAT if is_float else TokenType.INTEGER, literal)

    def _string(self) -> None:
        value_chars: list[str] = []
        while self._peek() != '"' and not self._is_at_end():
            char = self._advance()
            if char == "\n":
                self._line += 1
                self._column = 1
            elif char == "\\":
                value_chars.append(self._escape_sequence())
            else:
                value_chars.append(char)

        if self._is_at_end():
            raise SyntaxAksaraError(
                "String belum ditutup.", self._line, self._token_column
            )

        self._advance()
        self._add_token(TokenType.STRING, "".join(value_chars))

    def _escape_sequence(self) -> str:
        char = self._advance()
        escapes = {'"': '"', "\\": "\\", "n": "\n", "t": "\t"}
        if char not in escapes:
            raise SyntaxAksaraError(
                f"Escape sequence tidak dikenal: \\{char}.",
                self._line,
                self._column,
            )
        return escapes[char]

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self._source[self._current] != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return "\0"
        return self._source[self._current + 1]

    def _advance(self) -> str:
        char = self._source[self._current]
        self._current += 1
        self._column += 1
        return char

    def _add_token(self, token_type: TokenType, literal: object | None = None) -> None:
        text = self._source[self._start : self._current]
        self._tokens.append(
            Token(token_type, text, literal, self._line, self._token_column)
        )

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)
