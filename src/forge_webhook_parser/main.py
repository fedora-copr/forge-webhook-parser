#!/usr/bin/python3
"""
Parse a webhook payload file to clone the git repository to
the current directory.
"""

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import requests


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


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="webhook payload file to parse")
    group.add_argument("-u", "--url", help="url of the webhook payload file")
    return parser.parse_args()


def load_json_data(args):
    if args.url is not None:
        response = requests.get(args.url)
        return response.json()
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as payload:
            return json.load(payload)


def extract_repository_url(data):
    if "repository" in data and "clone_url" in data["repository"]:
        return data["repository"]["clone_url"]
    elif "project" in data and "git_http_url" in data["project"]:
        return data["project"]["git_http_url"]
    else:
        print("Payload does not include a repository url.")
        sys.exit(1)


def extract_project_name(repo_url: str) -> str:
    """Extract the name of the project from the clone url."""
    if repo_url:
        remove_git = repo_url.rstrip(".git")
        project_name = remove_git.split("/")[-1]
        return project_name
    return ""


def clean_clone_path(clone_path: Path):
    """Remove already cloned repositories if they exist."""
    if clone_path.exists():
        shutil.rmtree(clone_path, ignore_errors=True)


def clone_repo(repo_url: str, clone_path: Path):
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
    args = parse_arguments()
    data = load_json_data(args)
    repo_url = extract_repository_url(data)
    project_name = extract_project_name(repo_url)
    clone_path = Path.cwd() / "dst" / "tmp" / "output" / project_name

    clean_clone_path(clone_path)
    clone_repo(repo_url, clone_path)

    commits = data.get("commits", [])
    commit_changes = parse_commits(commits)

    for i, changes in enumerate(commit_changes, 1):
        print(f"Commit {i}:")
        print(f"Added: {', '.join(changes.added)}")
        print(f"Removed: {', '.join(changes.removed)}")
        print(f"Modified: {', '.join(changes.modified)}")


if __name__ == "__main__":
    main()
