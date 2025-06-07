import unittest

from ecosystems_cli.helpers.build_url import build_url


class TestBuildUrl(unittest.TestCase):
    def test_build_url_with_params(self):
        base_url = "https://api.example.com"
        path = "/foo/{bar}/baz/{qux}"
        path_params = {"bar": "123", "qux": "abc"}
        expected = "https://api.example.com/foo/123/baz/abc"
        self.assertEqual(build_url(base_url, path, path_params), expected)

    def test_build_url_with_missing_params(self):
        base_url = "https://api.example.com"
        path = "/foo/{bar}/baz/{qux}"
        path_params = {"bar": "123"}
        expected = "https://api.example.com/foo/123/baz/{qux}"
        self.assertEqual(build_url(base_url, path, path_params), expected)

    def test_build_url_with_no_params(self):
        base_url = "https://api.example.com"
        path = "/foo/bar"
        path_params = None
        expected = "https://api.example.com/foo/bar"
        self.assertEqual(build_url(base_url, path, path_params), expected)


if __name__ == "__main__":
    unittest.main()
