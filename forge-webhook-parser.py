#!/usr/bin/python3
"""
Parse a webhook payload file to clone the git repository to
the current directory.
"""

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class PayloadFields:
    """
    Dataclass of details extracted from the payload.
    """

    added: List[str]
    removed: List[str]
    modified: List[str]
    default_repo_url: Optional[str] = None
    default_clone_path: Optional[Path] = None


PAYLOAD_FILE = "./github-payload.json"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", "--file", help="webhook payload file to parse", default=PAYLOAD_FILE
)
args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as file:
    data = json.load(file)

if "repository" in data and "clone_url" in data["repository"]:
    default_repo_url = data["repository"]["clone_url"]
elif "project" in data and "git_http_url" in data["project"]:
    default_repo_url = data["project"]["git_http_url"]
else:
    default_repo_url = ""


def extract_project_name() -> str:
    """Extract the name of the project from the clone url."""
    if default_repo_url:
        remove_git = default_repo_url.rstrip(".git")
        project_name = remove_git.split("/")[-1]
        return project_name
    return ""


default_clone_path = Path.cwd() / extract_project_name()


def clean_clone_path(clone_path: Path = default_clone_path):
    """Remove already cloned repositories if they exist."""
    if clone_path.exists():
        shutil.rmtree(clone_path, ignore_errors=True)


def clone_repo(repo_url: str = default_repo_url, clone_path: Path = default_clone_path):
    """Clone the repository to the current working directory."""
    cmd: list[str] = ["git", "clone", repo_url, "--depth=1"]
    cmd.append(str(clone_path))
    subprocess.run(cmd, check=True)


def parse_commits(commit_data: List[dict]) -> List[PayloadFields]:
    """Parse the commit fields in the JSON payload.

    Args:
        commit_data (dict): List of commit data from the payload.

    Returns:
        List[PayloadFields]: List of changes for each commit.
    """
    commit_changes = []
    for commit in commit_data:
        changes = PayloadFields(
            added=commit.get("added", []),
            removed=commit.get("removed", []),
            modified=commit.get("modified", []),
        )
        commit_changes.append(changes)
    return commit_changes


def main():
    """
    Main execution function.
    """
    clean_clone_path()
    clone_repo()

    commits = data.get("commits", [])
    commit_changes = parse_commits(commits)

    for i, changes in enumerate(commit_changes, 1):
        print(f"Commit {i}:")
        print(f"Added: {', '.join(changes.added)}")
        print(f"Removed: {', '.join(changes.removed)}")
        print(f"Modified: {', '.join(changes.modified)}")


if __name__ == "__main__":
    main()
