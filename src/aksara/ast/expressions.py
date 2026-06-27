"""Expression nodes for the AKSARA AST."""

from __future__ import annotations

from dataclasses import dataclass

from aksara.lexer import Token


class Expression:
    """Base class for all AKSARA expressions."""


@dataclass(frozen=True, slots=True)
class LiteralExpression(Expression):
    """A literal value such as a number, string, boolean, or kosong."""

    value: object | None


@dataclass(frozen=True, slots=True)
class VariableExpression(Expression):
    """A reference to a named value."""

    name: Token


@dataclass(frozen=True, slots=True)
class UnaryExpression(Expression):
    """A unary operation such as numeric negation."""

    operator: Token
    right: Expression


@dataclass(frozen=True, slots=True)
class BinaryExpression(Expression):
    """A binary operation such as addition or comparison."""

    left: Expression
    operator: Token
    right: Expression


@dataclass(frozen=True, slots=True)
class GroupingExpression(Expression):
    """A parenthesized expression."""

    expression: Expression


@dataclass(frozen=True, slots=True)
class CallExpression(Expression):
    """A function call expression."""

    callee: Expression
    paren: Token
    arguments: tuple[Expression, ...]


@dataclass(frozen=True, slots=True)
class ListExpression(Expression):
    """A list literal expression."""

    items: tuple[Expression, ...]


@dataclass(frozen=True, slots=True)
class DictionaryExpression(Expression):
    """A dictionary literal expression."""

    entries: tuple[tuple[Expression, Expression], ...]
