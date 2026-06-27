from aksara.ast import IfStatement, VarStatement
from aksara.lexer import Lexer
from aksara.parser import Parser


def test_parser_builds_program_with_if_statement() -> None:
    source = 'buat umur = 21\njika umur >= 18\n    tulis "Halo"\nselesai\n'
    program = Parser(Lexer(source).scan_tokens()).parse()

    assert isinstance(program.statements[0], VarStatement)
    assert isinstance(program.statements[1], IfStatement)
    assert len(program.statements[1].then_branch) == 1
