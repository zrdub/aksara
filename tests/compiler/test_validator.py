from aksara.ast import Program
from aksara.compiler import validate_source


def test_validate_source_returns_program_ast() -> None:
    program = validate_source('tulis "Halo"\n')

    assert isinstance(program, Program)
    assert len(program.statements) == 1
