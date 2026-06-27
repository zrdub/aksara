from aksara.lexer import Lexer, TokenType


def test_lexer_scans_keywords_literals_and_operators() -> None:
    tokens = Lexer('buat nama = "Reza"\njika umur >= 18\n').scan_tokens()

    types = [token.type for token in tokens]

    assert types[:8] == [
        TokenType.BUAT,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.STRING,
        TokenType.NEWLINE,
        TokenType.JIKA,
        TokenType.IDENTIFIER,
        TokenType.GREATER_EQUAL,
    ]
    assert tokens[3].literal == "Reza"
    assert tokens[8].literal == 18
