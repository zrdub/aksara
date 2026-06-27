"""Recursive-descent parser for AKSARA."""

from __future__ import annotations

from aksara.ast import (
    BinaryExpression,
    CallExpression,
    DictionaryExpression,
    Expression,
    ExpressionStatement,
    GroupingExpression,
    IfStatement,
    ListExpression,
    LiteralExpression,
    PrintStatement,
    Program,
    Statement,
    UnaryExpression,
    VarStatement,
    VariableExpression,
)
from aksara.errors import SyntaxAksaraError
from aksara.lexer import Token, TokenType


class Parser:
    """Parse AKSARA tokens into a typed abstract syntax tree."""

    def __init__(self, tokens: list[Token]) -> None:
        """Create a parser for the token sequence produced by the lexer."""
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Program:
        """Parse a complete program."""
        statements: list[Statement] = []
        self._skip_newlines()
        while not self._is_at_end():
            statements.append(self._declaration())
            self._skip_newlines()
        return Program(tuple(statements))

    def _declaration(self) -> Statement:
        if self._match(TokenType.BUAT):
            return self._var_declaration()
        return self._statement()

    def _var_declaration(self) -> VarStatement:
        name = self._consume(
            TokenType.IDENTIFIER, "Nama variabel diperlukan setelah 'buat'."
        )
        self._consume(TokenType.EQUAL, "Gunakan '=' setelah nama variabel.")
        initializer = self._expression()
        self._consume_line_end(
            "Akhiri deklarasi variabel dengan baris baru atau akhir berkas."
        )
        return VarStatement(name, initializer)

    def _statement(self) -> Statement:
        if self._match(TokenType.TULIS):
            return self._print_statement()
        if self._match(TokenType.JIKA):
            return self._if_statement()
        return self._expression_statement()

    def _print_statement(self) -> PrintStatement:
        expression = self._expression()
        self._consume_line_end(
            "Akhiri perintah 'tulis' dengan baris baru atau akhir berkas."
        )
        return PrintStatement(expression)

    def _expression_statement(self) -> ExpressionStatement:
        expression = self._expression()
        self._consume_line_end("Akhiri ekspresi dengan baris baru atau akhir berkas.")
        return ExpressionStatement(expression)

    def _if_statement(self) -> IfStatement:
        condition = self._expression()
        self._consume_line_end("Akhiri kondisi 'jika' dengan baris baru.")
        then_branch = self._block_until(TokenType.JIKA_TIDAK, TokenType.SELESAI)
        else_branch: tuple[Statement, ...] = ()
        if self._match(TokenType.JIKA_TIDAK):
            self._consume_line_end("Akhiri 'jika_tidak' dengan baris baru.")
            else_branch = self._block_until(TokenType.SELESAI)
        self._consume(TokenType.SELESAI, "Blok 'jika' harus ditutup dengan 'selesai'.")
        self._consume_line_end("Akhiri 'selesai' dengan baris baru atau akhir berkas.")
        return IfStatement(condition, then_branch, else_branch)

    def _block_until(self, *terminators: TokenType) -> tuple[Statement, ...]:
        statements: list[Statement] = []
        self._skip_newlines()
        while not self._is_at_end() and not self._check_any(*terminators):
            statements.append(self._declaration())
            self._skip_newlines()
        return tuple(statements)

    def _expression(self) -> Expression:
        return self._equality()

    def _equality(self) -> Expression:
        expression = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expression = BinaryExpression(expression, operator, right)
        return expression

    def _comparison(self) -> Expression:
        expression = self._term()
        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expression = BinaryExpression(expression, operator, right)
        return expression

    def _term(self) -> Expression:
        expression = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expression = BinaryExpression(expression, operator, right)
        return expression

    def _factor(self) -> Expression:
        expression = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator = self._previous()
            right = self._unary()
            expression = BinaryExpression(expression, operator, right)
        return expression

    def _unary(self) -> Expression:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            return UnaryExpression(operator, self._unary())
        return self._call()

    def _call(self) -> Expression:
        expression = self._primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                expression = self._finish_call(expression)
            else:
                return expression

    def _finish_call(self, callee: Expression) -> CallExpression:
        arguments: list[Expression] = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(self._expression())
                if not self._match(TokenType.COMMA):
                    break
        paren = self._consume(
            TokenType.RIGHT_PAREN, "Gunakan ')' setelah argumen fungsi."
        )
        return CallExpression(callee, paren, tuple(arguments))

    def _primary(self) -> Expression:
        if self._match(TokenType.SALAH):
            return LiteralExpression(False)
        if self._match(TokenType.BENAR):
            return LiteralExpression(True)
        if self._match(TokenType.KOSONG):
            return LiteralExpression(None)
        if self._match(TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING):
            return LiteralExpression(self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return VariableExpression(self._previous())
        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Gunakan ')' setelah ekspresi.")
            return GroupingExpression(expression)
        if self._match(TokenType.LEFT_BRACKET):
            return self._list_literal()
        if self._match(TokenType.LEFT_BRACE):
            return self._dictionary_literal()
        token = self._peek()
        raise SyntaxAksaraError("Ekspresi diperlukan.", token.line, token.column)

    def _list_literal(self) -> ListExpression:
        items: list[Expression] = []
        if not self._check(TokenType.RIGHT_BRACKET):
            while True:
                items.append(self._expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_BRACKET, "Gunakan ']' setelah isi list.")
        return ListExpression(tuple(items))

    def _dictionary_literal(self) -> DictionaryExpression:
        entries: list[tuple[Expression, Expression]] = []
        if not self._check(TokenType.RIGHT_BRACE):
            while True:
                key = self._expression()
                self._consume(
                    TokenType.COLON, "Gunakan ':' antara kunci dan nilai dictionary."
                )
                value = self._expression()
                entries.append((key, value))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_BRACE, "Gunakan '}' setelah isi dictionary.")
        return DictionaryExpression(tuple(entries))

    def _consume_line_end(self, message: str) -> None:
        if self._match(TokenType.NEWLINE):
            self._skip_newlines()
            return
        if (
            self._check(TokenType.EOF)
            or self._check(TokenType.JIKA_TIDAK)
            or self._check(TokenType.SELESAI)
        ):
            return
        token = self._peek()
        raise SyntaxAksaraError(message, token.line, token.column)

    def _skip_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            pass

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        raise SyntaxAksaraError(message, token.line, token.column)

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type == TokenType.EOF
        return self._peek().type == token_type

    def _check_any(self, *types: TokenType) -> bool:
        return any(self._check(token_type) for token_type in types)

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]
