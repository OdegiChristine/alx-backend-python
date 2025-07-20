from typing import List, Dict

org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

repos_payload = [
    {"name": "episodes.dart", "license": {"key": "bsd-3-clause"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
]

expected_repos = ["episodes.dart", "repo2"]
apache2_repos = ["repo2"]
