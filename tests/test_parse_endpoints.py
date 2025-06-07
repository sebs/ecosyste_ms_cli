from ecosystems_cli.helpers.parse_endpoints import parse_endpoints


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
