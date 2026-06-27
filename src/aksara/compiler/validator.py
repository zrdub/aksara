"""Validation entry point for future compiler backends."""

from __future__ import annotations

from aksara.ast import Program
from aksara.lexer import Lexer
from aksara.parser import Parser


def validate_source(source: str) -> Program:
    """Parse source and return its AST for compiler pipeline consumers."""
    tokens = Lexer(source).scan_tokens()
    return Parser(tokens).parse()
