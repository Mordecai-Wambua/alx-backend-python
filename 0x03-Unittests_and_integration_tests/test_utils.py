#!/usr/bin/env python3
"""Unittests for utils.py functions."""
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Test suite for the access_nested_map method."""
    @parameterized.expand([
        ({"a": 1}, "a", 1),
        ({"a": {"b": 2}}, "a", {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """unittest for access_nested_map method. """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, 'a', KeyError),
        ({'a': 1}, ('a', 'b'), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """unittest for exception handling."""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test suite for the get_json method."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that utils.get_json returns the expected result."""
        with patch('utils.requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = test_payload
            self.assertEqual(get_json(test_url), test_payload)
            mocked_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test suite for the memoize method."""
    def test_memoize(self) -> None:
        """
        Test that when calling a_property twice,

        The correct result is returned but a_method is only called once.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(
                TestClass,
                'a_method',
                return_value=42,
                ) as mock_function:
            tests = TestClass()
            self.assertEqual(tests.a_property, 42)
            self.assertEqual(tests.a_property, 42)
            mock_function.assert_called_once()
