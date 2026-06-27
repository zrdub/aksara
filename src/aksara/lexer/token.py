"""Token definitions for the AKSARA lexer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """All lexical token kinds supported by AKSARA."""

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    MINUS = auto()
    PLUS = auto()
    SLASH = auto()
    STAR = auto()
    PERCENT = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    IDENTIFIER = auto()
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    NEWLINE = auto()
    EOF = auto()
    BUAT = auto()
    TULIS = auto()
    JIKA = auto()
    JIKA_TIDAK = auto()
    SELESAI = auto()
    FUNGSI = auto()
    KEMBALI = auto()
    ULANG = auto()
    DARI = auto()
    SAMPAI = auto()
    UNTUK = auto()
    SETIAP = auto()
    DI = auto()
    BENAR = auto()
    SALAH = auto()
    KOSONG = auto()
    IMPOR = auto()
    KELAS = auto()
    OBJEK = auto()
    COBA = auto()
    TANGKAP = auto()
    AKHIRNYA = auto()
    LEMPAR = auto()
    LANJUT = auto()
    BERHENTI = auto()


KEYWORDS: dict[str, TokenType] = {
    "buat": TokenType.BUAT,
    "tulis": TokenType.TULIS,
    "jika": TokenType.JIKA,
    "jika_tidak": TokenType.JIKA_TIDAK,
    "selesai": TokenType.SELESAI,
    "fungsi": TokenType.FUNGSI,
    "kembali": TokenType.KEMBALI,
    "ulang": TokenType.ULANG,
    "dari": TokenType.DARI,
    "sampai": TokenType.SAMPAI,
    "untuk": TokenType.UNTUK,
    "setiap": TokenType.SETIAP,
    "di": TokenType.DI,
    "benar": TokenType.BENAR,
    "salah": TokenType.SALAH,
    "kosong": TokenType.KOSONG,
    "impor": TokenType.IMPOR,
    "kelas": TokenType.KELAS,
    "objek": TokenType.OBJEK,
    "coba": TokenType.COBA,
    "tangkap": TokenType.TANGKAP,
    "akhirnya": TokenType.AKHIRNYA,
    "lempar": TokenType.LEMPAR,
    "lanjut": TokenType.LANJUT,
    "berhenti": TokenType.BERHENTI,
}


@dataclass(frozen=True, slots=True)
class Token:
    """A source token with its literal value and source location."""

    type: TokenType
    lexeme: str
    literal: object | None
    line: int
    column: int
