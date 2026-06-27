"""Statement nodes for the AKSARA AST."""

from __future__ import annotations

from dataclasses import dataclass

from aksara.ast.expressions import Expression
from aksara.lexer import Token


class Statement:
    """Base class for executable AKSARA statements."""


@dataclass(frozen=True, slots=True)
class Program:
    """A complete AKSARA program."""

    statements: tuple[Statement, ...]


@dataclass(frozen=True, slots=True)
class VarStatement(Statement):
    """A variable declaration introduced by `buat`."""

    name: Token
    initializer: Expression


@dataclass(frozen=True, slots=True)
class PrintStatement(Statement):
    """A `tulis` statement."""

    expression: Expression


@dataclass(frozen=True, slots=True)
class ExpressionStatement(Statement):
    """A standalone expression statement."""

    expression: Expression


@dataclass(frozen=True, slots=True)
class IfStatement(Statement):
    """A conditional statement with optional else branch."""

    condition: Expression
    then_branch: tuple[Statement, ...]
    else_branch: tuple[Statement, ...]
