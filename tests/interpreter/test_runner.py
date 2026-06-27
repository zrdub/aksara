from aksara.interpreter import run_source


def test_run_source_executes_language_example() -> None:
    source = """
buat nama = "Reza"
buat umur = 21

jika umur >= 18
    tulis "Halo, " + nama
jika_tidak
    tulis "Anak"
selesai
"""

    result = run_source(source)

    assert result.output == ("Halo, Reza",)


def test_run_source_supports_lists_dictionaries_and_stdlib() -> None:
    source = """
buat data = ["a", "b", "c"]
tulis panjang(data)
tulis gabung(data, "-")
tulis {"nama": "Reza"}
"""

    result = run_source(source)

    assert result.output == ("3", "a-b-c", "{nama: Reza}")
