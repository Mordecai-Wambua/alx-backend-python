import unittest
from parameterized import parameterized

from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function"""
    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_value):
        """Test successful retrieval from nested map."""
        self.assertEqual(access_nested_map(nested_map, path), expected_value)



if __name__ == "__main__":
    unittest.main(verbosity=2)