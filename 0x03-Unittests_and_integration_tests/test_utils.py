#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


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
    def test_access_nested_map_exception(self, nested_map, path, exception_message):
        """Test that KeyError is raised with correct missing key message"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{exception_message}'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
