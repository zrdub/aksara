"""Variable environment for AKSARA execution."""

from __future__ import annotations

from dataclasses import dataclass, field

from aksara.errors import RuntimeAksaraError
from aksara.errors.suggestions import suggest_name
from aksara.lexer import Token


@dataclass(slots=True)
class Environment:
    """A lexical scope for AKSARA variable bindings."""

    values: dict[str, object] = field(default_factory=dict)
    parent: "Environment | None" = None

    def define(self, name: str, value: object) -> None:
        """Define or replace a value in the current scope."""
        self.values[name] = value

    def get(self, name: Token) -> object:
        """Read a value by token, raising a friendly error when absent."""
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.parent:
            return self.parent.get(name)

        known_names = self.names()
        suggestion = suggest_name(name.lexeme, known_names)
        raise RuntimeAksaraError(
            f'Variabel "{name.lexeme}" tidak ditemukan.',
            name.line,
            name.column,
            suggestion,
        )

    def names(self) -> list[str]:
        """Return visible names for diagnostics and tooling."""
        names = list(self.values)
        if self.parent:
            names.extend(self.parent.names())
        return names
