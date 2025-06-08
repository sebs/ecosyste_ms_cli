def test_print_operations_basic(capsys):
    from ecosystems_cli.helpers.print_operations import print_operations

    operations = [
        {"id": "getUser", "method": "GET", "path": "/user", "summary": "Get a user."},
        {"id": "createUser", "method": "POST", "path": "/user", "summary": "Create a new user."},
    ]
    print_operations(operations)
    captured = capsys.readouterr()
    assert "OPERATION" in captured.out
    assert "getUser" in captured.out
    assert "createUser" in captured.out
    assert "Get a user." in captured.out
    assert "Create a new user." in captured.out


def test_print_operations_empty(capsys):
    from ecosystems_cli.helpers.print_operations import print_operations

    print_operations([])
    captured = capsys.readouterr()
    assert "No operations available." in captured.out
