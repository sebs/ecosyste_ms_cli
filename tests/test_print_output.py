from rich.console import Console

from ecosystems_cli.helpers.print_output import print_output


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


def test_print_output_table(capsys):
    data = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]
    console = Console(file=None, force_terminal=True, color_system=None, width=80)
    print_output(data, format_type="table", console=console)
