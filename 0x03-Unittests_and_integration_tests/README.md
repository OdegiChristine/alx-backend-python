# GithubOrgClient Testing

This project demonstrates a comprehensive test suite for a client that interacts with the GitHub API. The tests cover both **unit** and **integration** cases using `unittest`, `parameterized`, and `unittest.mock`.

---

## 📁 Project Structure
├── client.py # Contains GithubOrgClient class

├── utils.py # Helper functions (get_json, memoize, access_nested_map)

├── test_client.py # Unit and integration tests for GithubOrgClient

├── test_utils.py # Unit tests for utility functions in utils.py

├── fixtures.py # JSON fixtures used in integration tests

└── README.md # This file


---

## ✅ Features Tested

### `utils.py`

- **`access_nested_map`**
  - Unit tested with valid paths using `@parameterized.expand`
  - Raises `KeyError` when path is invalid
- **`get_json`**
  - Mocked `requests.get` to avoid external HTTP calls
- **`memoize`**
  - Confirmed that method is only called once and subsequent calls return cached result

### `client.py`

- **`GithubOrgClient.org`**
  - Returns expected org data using mocked `get_json`
- **`GithubOrgClient._public_repos_url`**
  - Returns correct `repos_url` from the org payload
- **`GithubOrgClient.public_repos`**
  - Returns a list of repo names
  - Supports filtering by license
- **`GithubOrgClient.has_license`**
  - Correctly detects presence of a specific license in a repo

---

## 🧪 Test Files Overview

### `test_utils.py`

Tests:
- `access_nested_map`
- `get_json` (mocked)
- `memoize` (caches method call)

### `test_client.py`

#### Unit Tests
- `.org()` with mocked `get_json`
- `._public_repos_url` with mocked `.org`
- `.public_repos()` with mocked `get_json` and `_public_repos_url`
- `.has_license()` using `@parameterized.expand`

#### Integration Tests
- `TestIntegrationGithubOrgClient` class:
  - Uses `@parameterized_class` with fixtures
  - Mocks only `requests.get`
  - Tests `.public_repos()` and license filtering with real method logic

---

## 🧰 How to Run Tests

```bash
# Run all tests
python3 -m unittest discover
```
```bash
# Or run specific files
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

## 🧪 Dependencies
- Python 3.8+
- `parameterized`