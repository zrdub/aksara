from aksara.runtime import aksara_type_name, stringify


def test_stringify_uses_indonesian_runtime_literals() -> None:
    assert stringify(True) == "benar"
    assert stringify(False) == "salah"
    assert stringify(None) == "kosong"
    assert stringify([1, "dua"]) == "[1, dua]"


def test_aksara_type_name_maps_python_values() -> None:
    assert aksara_type_name(1) == "integer"
    assert aksara_type_name(1.5) == "float"
    assert aksara_type_name({"x": 1}) == "dictionary"
