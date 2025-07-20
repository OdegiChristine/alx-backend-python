#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import Mock, patch

class TestAccessNestedMap(unittest.TestCase):
    # Lets me run the same test method with different inputs, without the need to repeat code for many input variations.
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a","b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[len(cm.exception.args[0] - 1)]))

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, name, test_url, test_payload):
        # Patch replaces requests.get in the utils module with a mock
        with patch("utils.requests.get") as mock_get:
            # create a mock response with .json method returning test_payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            # Assert requests.get was called once with test_url
            mock_get.assert_called_with(test_url)

            # Assert the result matches the expected payload
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # mocks TestClass.a_method
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property() # First call, should call a_method
            result2 = obj.a_property() # Second call, should not call a_method again

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once
            mock_method.assert_called_once()
