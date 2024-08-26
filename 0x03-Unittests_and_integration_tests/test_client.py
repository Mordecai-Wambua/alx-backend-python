#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from utils import get_json
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
