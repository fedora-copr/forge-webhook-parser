"""Pytest conftest.py"""

import json
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

TESTS_DIR = Path(__file__).parent
JSON_DIR = TESTS_DIR / "json"
EMPTY_PAYLOAD: Dict[str, Any] = {}


def load_json_payload(filename: str) -> Dict[str, Any]:
    with open(JSON_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def github_payload() -> Dict[str, Any]:
    """Return GitHub payload as a Python dict."""
    file_path = JSON_DIR / "github-payload.json"
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def empty_payload() -> Dict[str, Any]:
    """Return empty payload dict."""
    return {}


@pytest.fixture
def mock_args_file():
    """Mock command line args for file input."""
    args = MagicMock()
    args.file = "payload.json"
    args.url = None
    return args


@pytest.fixture
def mock_args_url():
    """Mock command line args for URL input."""
    args = MagicMock()
    args.file = None
    args.url = "http://example.com/payload.json"
    return args
