"""Error hierarchy for AKSARA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AksaraError(Exception):
    """Base exception rendered in Indonesian for AKSARA users."""

    message: str
    line: int | None = None
    column: int | None = None
    suggestion: str | None = None

    def __str__(self) -> str:
        """Return a human-friendly Indonesian error message."""
        parts: list[str] = []
        if self.line is not None:
            parts.append(f"Kesalahan pada baris {self.line}")
        parts.append(self.message)
        if self.suggestion:
            parts.append(f"Apakah yang dimaksud:\n{self.suggestion}")
        return "\n\n".join(parts)


class SyntaxAksaraError(AksaraError):
    """Raised when AKSARA source code cannot be parsed."""


class RuntimeAksaraError(AksaraError):
    """Raised when AKSARA code fails during execution."""
