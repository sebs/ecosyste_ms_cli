from ecosystems_cli.helpers.parse_endpoints import flatten_dict, parse_endpoints


def test_parse_endpoints_basic():
    spec = {
        "paths": {
            "/foo": {
                "get": {
                    "operationId": "getFoo",
                    "parameters": [
                        {"name": "id", "in": "query", "required": True, "schema": {"type": "string"}, "description": "ID param"}
                    ],
                    "description": "Get foo.",
                    "summary": "Get foo summary.",
                }
            }
        }
    }
    endpoints = parse_endpoints(spec)
    assert "getFoo" in endpoints
    endpoint = endpoints["getFoo"]
    assert endpoint["path"] == "/foo"
    assert endpoint["method"] == "get"
    assert "id" in endpoint["params"]
    assert endpoint["params"]["id"]["required"] is True
    assert endpoint["description"] == "Get foo."
    assert endpoint["summary"] == "Get foo summary."
    assert "id" in endpoint["required_params"]


def test_parse_endpoints_no_paths():
    spec = {}
    endpoints = parse_endpoints(spec)
    assert endpoints == {}


# Test for flatten_dict in helpers.parse_endpoints
def test_flatten_dict_simple():
    d = {"a": 1, "b": 2}
    assert flatten_dict(d) == {"a": 1, "b": 2}


def test_flatten_dict_nested():
    d = {"a": {"b": 2, "c": 3}, "d": 4}
    assert flatten_dict(d) == {"a_b": 2, "a_c": 3, "d": 4}


def test_flatten_dict_deep_nested():
    d = {"a": {"b": {"c": 1}}, "d": 2}
    assert flatten_dict(d) == {"a_b_c": 1, "d": 2}


def test_flatten_dict_with_sep():
    d = {"a": {"b": 1}}
    assert flatten_dict(d, sep=".") == {"a.b": 1}
