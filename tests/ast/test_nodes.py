from aksara.ast import LiteralExpression, PrintStatement, Program


def test_ast_nodes_are_immutable_data_objects() -> None:
    expression = LiteralExpression("Halo")
    statement = PrintStatement(expression)
    program = Program((statement,))

    assert program.statements[0].expression.value == "Halo"
