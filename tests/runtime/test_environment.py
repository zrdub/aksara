import pytest

from aksara.errors import RuntimeAksaraError
from aksara.lexer import Token, TokenType
from aksara.runtime import Environment


def test_environment_returns_defined_value() -> None:
    environment = Environment()
    environment.define("nama", "Reza")

    token = Token(TokenType.IDENTIFIER, "nama", None, 1, 1)

    assert environment.get(token) == "Reza"


def test_environment_suggests_close_name() -> None:
    environment = Environment({"nama": "Reza"})
    token = Token(TokenType.IDENTIFIER, "namaa", None, 10, 1)

    with pytest.raises(RuntimeAksaraError) as error:
        environment.get(token)

    assert "Variabel \"namaa\" tidak ditemukan." in str(error.value)
    assert "nama" in str(error.value)
