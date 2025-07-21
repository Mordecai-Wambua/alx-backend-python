#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function"""

    @parameterized.expand(
        [
            ({"a": 1}, ["a"], 1),
            ({"a": {"b": 2}}, ["a"], {"b": 2}),
            ({"a": {"b": 2}}, ["a", "b"], 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected_value):
        """Test successful retrieval from nested map."""
        self.assertEqual(access_nested_map(nested_map, path), expected_value)

    @parameterized.expand(
        [
            ({}, ["a"], "a"),
            ({"a": 1}, ["a", "b"], "b"),
        ]
    )
    def test_access_nested_map_exception(
            self,
            nested_map,
            path,
            exception_message
    ):
        """Test that KeyError is raised with correct missing key message"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{exception_message}'")


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(
            self,
            url,
            expected_json_payload
    ):
        """Test successful retrieval of JSON payload from URL"""
        mock_response = Mock()
        mock_response.json.return_value = expected_json_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            response = get_json(url)
            mock_get.assert_called_once_with(url)
            self.assertEqual(response, expected_json_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator"""

    def test_memoize(self):
        """Test that the decorator correctly caches the result"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
                TestClass,
                "a_method",
                return_value=42
        ) as mock_method:
            test_object = TestClass()
            result = test_object.a_property
            result2 = test_object.a_property

            self.assertEqual(result, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
