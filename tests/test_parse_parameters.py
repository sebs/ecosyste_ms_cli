import unittest

from ecosystems_cli.helpers.parse_parameters import parse_parameters


class TestParseParameters(unittest.TestCase):
    def test_parse_parameters_basic(self):
        details = {
            "parameters": [
                {
                    "name": "foo",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "A foo parameter.",
                },
                {
                    "name": "bar",
                    "in": "path",
                    "required": False,
                    "schema": {"type": "integer"},
                    "description": "A bar parameter.",
                },
            ]
        }
        expected = {
            "foo": {"in": "query", "required": True, "schema": {"type": "string"}, "description": "A foo parameter."},
            "bar": {"in": "path", "required": False, "schema": {"type": "integer"}, "description": "A bar parameter."},
        }
        self.assertEqual(parse_parameters(details), expected)

    def test_parse_parameters_empty(self):
        details = {}
        self.assertEqual(parse_parameters(details), {})

    def test_parse_parameters_missing_fields(self):
        details = {"parameters": [{"name": "foo"}, {"name": "bar", "in": "header"}]}
        expected = {
            "foo": {"in": None, "required": False, "schema": {}, "description": ""},
            "bar": {"in": "header", "required": False, "schema": {}, "description": ""},
        }
        self.assertEqual(parse_parameters(details), expected)


if __name__ == "__main__":
    unittest.main()
