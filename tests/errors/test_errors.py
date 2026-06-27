from aksara.errors import RuntimeAksaraError
from aksara.errors.suggestions import suggest_name


def test_error_string_is_human_friendly() -> None:
    error = RuntimeAksaraError('Variabel "namaa" tidak ditemukan.', 10, suggestion="nama")

    text = str(error)

    assert "Kesalahan pada baris 10" in text
    assert "Apakah yang dimaksud:" in text
    assert "nama" in text


def test_suggest_name_returns_close_match() -> None:
    assert suggest_name("namaa", ["nama", "umur"]) == "nama"
