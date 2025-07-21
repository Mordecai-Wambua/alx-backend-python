#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class"""

    @parameterized.expand(
        [
            ('google',),
            ('abc',),
        ]
    )
    @patch('client.get_json')
    def test_org(self, org_name, mock_response):
        """Test that the org property returns the expected value"""
        expected_payload = {'login': org_name}
        mock_response.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_response.assert_called_once_with(GithubOrgClient.ORG_URL.format(org=org_name))


if __name__ == "__main__":
    unittest.main()

