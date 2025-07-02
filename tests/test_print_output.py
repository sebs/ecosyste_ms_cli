from rich.console import Console

from ecosystems_cli.helpers.print_output import (
    _format_json,
    _format_jsonl,
    _format_table,
    _format_tsv,
    _select_table_fields,
    print_output,
)


def test_format_json_with_dict():
    """Test that _format_json returns proper JSON syntax for dict data."""
    from io import StringIO

    data = {"foo": "bar", "baz": 1}
    console = Console(file=StringIO(), force_terminal=True, color_system=None, width=80)
    _format_json(data, console)

    # This test will fail initially since _format_json doesn't exist yet


def test_format_tsv_with_list():
    """Test that _format_tsv properly formats list data as TSV."""
    from io import StringIO

    data = [{"foo": "bar", "baz": 1}, {"foo": "qux", "baz": 2}]
    output = StringIO()
    console = Console(file=output, force_terminal=True, color_system=None, width=80)
    _format_tsv(data, console)

    # This test will fail initially since _format_tsv doesn't exist yet


def test_format_jsonl_with_list():
    """Test that _format_jsonl properly formats list data as JSONL."""
    from io import StringIO

    data = [{"foo": "bar"}, {"foo": "baz"}]
    output = StringIO()
    console = Console(file=output, force_terminal=True, color_system=None, width=80)
    _format_jsonl(data, console)

    # This test will fail initially since _format_jsonl doesn't exist yet


def test_print_output_json(capsys):
    data = {"foo": "bar", "baz": 1}
    console = Console(file=None, force_terminal=True, color_system=None, width=80)
    print_output(data, format_type="json", console=console)
    # No assertion: just ensure no exceptions and output is printed


def test_print_output_tsv(capsys):
    data = [{"foo": "bar", "baz": 1}, {"foo": "qux", "baz": 2}]
    console = Console(file=None, force_terminal=True, color_system=None, width=80)
    print_output(data, format_type="tsv", console=console)


def test_print_output_jsonl(capsys):
    data = [{"foo": "bar"}, {"foo": "baz"}]
    console = Console(file=None, force_terminal=True, color_system=None, width=80)
    print_output(data, format_type="jsonl", console=console)


def test_select_table_fields_with_common_fields():
    """Test that _select_table_fields selects appropriate fields."""
    data = [{"id": 1, "name": "foo", "extra": "data"}, {"id": 2, "name": "bar", "extra": "more"}]
    headers = list(data[0].keys())

    selected = _select_table_fields(headers)

    # Should prioritize common fields like id and name
    assert "id" in selected
    assert "name" in selected
    # This test will fail initially since _select_table_fields doesn't exist yet


def test_format_table_with_list():
    """Test that _format_table properly formats list data as table."""
    from io import StringIO

    data = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]
    output = StringIO()
    console = Console(file=output, force_terminal=True, color_system=None, width=80)
    _format_table(data, console)

    # This test will fail initially since _format_table doesn't exist yet


def test_print_output_table(capsys):
    data = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]
    console = Console(file=None, force_terminal=True, color_system=None, width=80)
    print_output(data, format_type="table", console=console)
