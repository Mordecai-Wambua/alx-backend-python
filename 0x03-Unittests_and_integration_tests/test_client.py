#!/usr/bin/env python3
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, MagicMock, PropertyMock
from client import GithubOrgClient
from typing import Dict
from fixtures import TEST_PAYLOAD


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


@parameterized_class(
    [
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Test suite for public_repos."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the fixtures."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def mock_requests_get(url, *args, **kwargs):
            if url.endswith('orgs/test-org'):
                return MagicMock(json=lambda: cls.org_payload)
            elif url.endswith('repos'):
                return MagicMock(json=lambda: cls.repos_payload)
            raise ValueError("Unexpected URL")

        cls.mock_get.side_effect = mock_requests_get

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the fixtures."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Tests the method public_repos."""
        self.assertEqual(
            GithubOrgClient('test-org').public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the method public_repos with arg: license="apache-2.0."""
        self.assertEqual(
            GithubOrgClient('test-org').public_repos(license="apache-2.0"),
            self.apache2_repos
        )
