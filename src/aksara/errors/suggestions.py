"""Name suggestion helpers for AKSARA diagnostics."""

from __future__ import annotations

from difflib import get_close_matches


def suggest_name(name: str, candidates: list[str]) -> str | None:
    """Return the closest known name for a misspelled identifier."""
    matches = get_close_matches(name, candidates, n=1, cutoff=0.6)
    return matches[0] if matches else None
