from aksara.stdlib import create_standard_environment


def test_standard_environment_contains_core_functions() -> None:
    environment = create_standard_environment()

    panjang = environment.values["panjang"]
    huruf_besar = environment.values["huruf_besar"]

    assert panjang("aksara") == 6
    assert huruf_besar("aksara") == "AKSARA"
