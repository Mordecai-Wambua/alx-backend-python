#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock, PropertyMock
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOggClient class."""
    @parameterized.expand([
        ('google', {"login": "google"}),
        ('abc', {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org: str, output: Dict, mocked_json: MagicMock) -> None:
        """Tests the output of the org method."""
        mocked_json.return_value = output
        obj = GithubOrgClient(org)
        self.assertEqual(obj.org, output)
        mocked_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self) -> None:
        """Tests the method _public_repos_url."""
        with patch(
                'client.GithubOrgClient.org',
                new_callable=PropertyMock
                ) as mocked_prop:
            output = {"repos_url": "https://api.github.com/orgs/google/repos"}
            mocked_prop.return_value = output
            obj = GithubOrgClient('google')
            result = obj._public_repos_url
            self.assertEqual(result, output["repos_url"])
