import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "forge-webhook-parser.py"


def run_script(args):
    """Helper function to run the script as a subprocess"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)] + args, capture_output=True, text=True
    )
    return result


def test_read_github_payload_file(temp_github_payload):
    """Test reading GitHub payload from JSON file."""
    result = run_script(["-f", temp_github_payload])

    assert result.returncode == 0
    assert "Added: ADDED.md" in result.stdout
    assert "Removed: REMOVED.md" in result.stdout
    assert "Modified: MODIFIED.md" in result.stdout


def test_read_gitlab_payload_file(temp_gitlab_payload):
    """Test reading GitLab payload from JSON file."""
    result = run_script(["-f", temp_gitlab_payload])

    assert result.returncode == 0
    assert "Added: ADDED_FILE.md" in result.stdout
    assert "Removed: REMOVED_FILE.md" in result.stdout
    assert "Modified: MODIFIED_FILE.md" in result.stdout


def test_empty_json(empty_json_file):
    """Test handling of empty JSON."""
    result = run_script(["-f", empty_json_file])
    assert result.returncode == 1
    assert "An error occurred" in result.stderr
