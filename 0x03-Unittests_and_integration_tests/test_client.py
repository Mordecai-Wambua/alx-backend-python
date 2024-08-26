#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock, PropertyMock
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient class."""
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

    @patch('client.get_json')
    def test_public_repos(self, mocked_json: MagicMock) -> None:
        """Tests the method public_repos."""
        payload = [{"name": "first", "license": {"key": "mit"}},
                   {"name": "second", "license": {"key": "mit"}},
                   {"name": "third", "license": {"key": "apache-2.0"}},
                   {"name": "fourth", "license": {"key": "apache-2.0"}},
                   ]
        mocked_json.return_value = payload
        mock_repos_url = "https://api.github.com/orgs/google/repos"
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mocked_repos:
            mocked_repos.return_value = mock_repos_url

            obj = GithubOrgClient('google')
            repo = obj.public_repos(license="mit")
            self.assertEqual(repo, ['first', 'second'])
            mocked_json.assert_called_once()
            mocked_repos.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ])
    def test_license(self, repo: Dict, license_key: str, expected: bool):
        """Tests the method has_license."""
        output = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(output, expected)
