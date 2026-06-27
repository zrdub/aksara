"""Value helpers for AKSARA runtime objects."""

from __future__ import annotations


def stringify(value: object) -> str:
    """Convert a Python runtime value into AKSARA display text."""
    if value is None:
        return "kosong"
    if value is True:
        return "benar"
    if value is False:
        return "salah"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, list):
        return "[" + ", ".join(stringify(item) for item in value) + "]"
    if isinstance(value, dict):
        pairs = (f"{stringify(key)}: {stringify(item)}" for key, item in value.items())
        return "{" + ", ".join(pairs) + "}"
    return str(value)


def aksara_type_name(value: object) -> str:
    """Return the AKSARA type name for a runtime value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dictionary"
    if callable(value):
        return "function"
    return "object"
