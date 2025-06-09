from ecosystems_cli.helpers.format_value import format_value


def test_format_value_simple():
    assert format_value(42) == "42"
    assert format_value("foo") == "foo"
    assert format_value(None) == "None"


def test_format_value_empty_dict():
    assert format_value({}) == "{}"


def test_format_value_small_dict():
    assert format_value({"a": 1, "b": 2}) == "a: 1, b: 2"


def test_format_value_large_dict():
    d = {"a": 1, "b": 2, "c": 3, "d": 4}
    assert format_value(d) == "{...} (4 items)"


def test_format_value_empty_list():
    assert format_value([]) == "[]"


def test_format_value_small_list():
    assert format_value([1, 2]) == "1, 2"


def test_format_value_large_list():
    assert format_value([1, 2, 3, 4]) == "[...] (4 items)"


def test_format_value_nested():
    val = {"a": [1, 2, 3], "b": {"x": 1}}
    # Should use short representation for both dict and list
    result = format_value(val)
    assert "a: 1, 2, 3" in result or "b: x: 1" in result or "{...}" in result
