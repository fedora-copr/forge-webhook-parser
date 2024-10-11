"""Pytest conftest.py"""

import json
import os
import tempfile
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent
JSON_DIR = TESTS_DIR / "json"


def load_json_payload(filename):
    with open(JSON_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


TEST_PAYLOADS = {
    file.stem.upper().replace("-", "_"): load_json_payload(file.name)
    for file in JSON_DIR.glob("*.json")
}


@pytest.fixture
def temp_github_payload():
    """Create a temporary JSON file with GitHub payload."""
    test_data = TEST_PAYLOADS["GITHUB_PAYLOAD"]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_gitlab_payload():
    """Create a temporary JSON file with GitLab payload."""
    test_data = TEST_PAYLOADS["GITLAB_PAYLOAD"]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def empty_json_file():
    """Create an empty JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{}")
    yield f.name
    os.unlink(f.name)
