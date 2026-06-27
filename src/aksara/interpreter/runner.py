"""Convenience helpers for running AKSARA source text."""

from __future__ import annotations

from dataclasses import dataclass

from aksara.interpreter.interpreter import Interpreter
from aksara.lexer import Lexer
from aksara.parser import Parser


@dataclass(frozen=True, slots=True)
class RunResult:
    """Result of running an AKSARA program from source."""

    output: tuple[str, ...]


def run_source(source: str) -> RunResult:
    """Lex, parse, and execute source code, collecting printed output."""
    lines: list[str] = []
    tokens = Lexer(source).scan_tokens()
    program = Parser(tokens).parse()
    Interpreter(output=lines.append).interpret(program)
    return RunResult(tuple(lines))
