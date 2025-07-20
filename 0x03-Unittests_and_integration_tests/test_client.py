#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        # Set up the mock return value
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Create client and call .org()
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json called with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        with patch.object(GithubOrgClient, "org", return_value=test_payload):
            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    # mock get_json using patch as a decorator
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        # Define a fake payload that get_json will return
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        # Mock the _public_repos_url property using patch as a context manager
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=patch.PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"

            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            # Assert the result is a list of repo names
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Check each mock was called exactly once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Patch requests.get and set side_effects for org and repos URLs"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Mock the response objects with a .json() method
        mock_get.side_effect = [
            Mock(**{"json.return_value": cls.org_payload}),
            Mock(**{"json.return_value": cls.repos_payload})
        ]

    @classmethod
    def tearDownClass(cls):
        # Stop patcher
        cls.get_patcher.stop()

    def test_public_repos(self):
        # Integration test for all public repos
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
