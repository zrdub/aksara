"""Tree-walking interpreter for AKSARA programs."""

from __future__ import annotations

from collections.abc import Callable

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
from aksara.errors import RuntimeAksaraError
from aksara.lexer import TokenType
from aksara.runtime import Environment, stringify
from aksara.stdlib import create_standard_environment

OutputWriter = Callable[[str], None]


class Interpreter:
    """Execute AKSARA AST programs."""

    def __init__(self, output: OutputWriter | None = None, environment: Environment | None = None) -> None:
        """Create an interpreter with an optional output sink and environment."""
        self.environment = environment or create_standard_environment()
        self._output = output or print

    def interpret(self, program: Program) -> None:
        """Execute a parsed AKSARA program."""
        for statement in program.statements:
            self._execute(statement)

    def _execute(self, statement: Statement) -> None:
        if isinstance(statement, VarStatement):
            self.environment.define(statement.name.lexeme, self._evaluate(statement.initializer))
            return
        if isinstance(statement, PrintStatement):
            self._output(stringify(self._evaluate(statement.expression)))
            return
        if isinstance(statement, ExpressionStatement):
            self._evaluate(statement.expression)
            return
        if isinstance(statement, IfStatement):
            branch = statement.then_branch if self._is_truthy(self._evaluate(statement.condition)) else statement.else_branch
            for child in branch:
                self._execute(child)
            return
        raise RuntimeAksaraError(f"Statement belum didukung: {type(statement).__name__}.")

    def _evaluate(self, expression: Expression) -> object:
        if isinstance(expression, LiteralExpression):
            return expression.value
        if isinstance(expression, VariableExpression):
            return self.environment.get(expression.name)
        if isinstance(expression, GroupingExpression):
            return self._evaluate(expression.expression)
        if isinstance(expression, UnaryExpression):
            return self._evaluate_unary(expression)
        if isinstance(expression, BinaryExpression):
            return self._evaluate_binary(expression)
        if isinstance(expression, CallExpression):
            return self._evaluate_call(expression)
        if isinstance(expression, ListExpression):
            return [self._evaluate(item) for item in expression.items]
        if isinstance(expression, DictionaryExpression):
            return {self._evaluate(key): self._evaluate(value) for key, value in expression.entries}
        raise RuntimeAksaraError(f"Ekspresi belum didukung: {type(expression).__name__}.")

    def _evaluate_unary(self, expression: UnaryExpression) -> object:
        right = self._evaluate(expression.right)
        if expression.operator.type == TokenType.MINUS:
            self._require_number(right, expression.operator.line)
            return -right
        if expression.operator.type == TokenType.BANG:
            return not self._is_truthy(right)
        raise RuntimeAksaraError("Operator unary tidak dikenal.", expression.operator.line)

    def _evaluate_binary(self, expression: BinaryExpression) -> object:
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)
        token_type = expression.operator.type

        if token_type == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) or isinstance(right, str):
                return stringify(left) + stringify(right)
            raise RuntimeAksaraError("Operator '+' membutuhkan angka atau string.", expression.operator.line)
        if token_type == TokenType.MINUS:
            self._require_numbers(left, right, expression.operator.line)
            return left - right
        if token_type == TokenType.STAR:
            self._require_numbers(left, right, expression.operator.line)
            return left * right
        if token_type == TokenType.SLASH:
            self._require_numbers(left, right, expression.operator.line)
            if right == 0:
                raise RuntimeAksaraError("Pembagian dengan nol tidak diperbolehkan.", expression.operator.line)
            return left / right
        if token_type == TokenType.PERCENT:
            self._require_numbers(left, right, expression.operator.line)
            return left % right
        if token_type == TokenType.GREATER:
            self._require_numbers(left, right, expression.operator.line)
            return left > right
        if token_type == TokenType.GREATER_EQUAL:
            self._require_numbers(left, right, expression.operator.line)
            return left >= right
        if token_type == TokenType.LESS:
            self._require_numbers(left, right, expression.operator.line)
            return left < right
        if token_type == TokenType.LESS_EQUAL:
            self._require_numbers(left, right, expression.operator.line)
            return left <= right
        if token_type == TokenType.EQUAL_EQUAL:
            return left == right
        if token_type == TokenType.BANG_EQUAL:
            return left != right
        raise RuntimeAksaraError("Operator binary tidak dikenal.", expression.operator.line)

    def _evaluate_call(self, expression: CallExpression) -> object:
        callee = self._evaluate(expression.callee)
        arguments = tuple(self._evaluate(argument) for argument in expression.arguments)
        if not callable(callee):
            raise RuntimeAksaraError("Nilai ini tidak dapat dipanggil sebagai fungsi.", expression.paren.line)
        try:
            return callee(*arguments)
        except RuntimeAksaraError:
            raise
        except OSError as error:
            raise RuntimeAksaraError(f"Operasi berkas gagal: {error}", expression.paren.line) from error
        except TypeError as error:
            raise RuntimeAksaraError(f"Pemanggilan fungsi tidak valid: {error}", expression.paren.line) from error

    @staticmethod
    def _is_truthy(value: object) -> bool:
        return bool(value)

    @staticmethod
    def _require_number(value: object, line: int) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise RuntimeAksaraError("Operator membutuhkan angka.", line)

    @classmethod
    def _require_numbers(cls, left: object, right: object, line: int) -> None:
        cls._require_number(left, line)
        cls._require_number(right, line)
