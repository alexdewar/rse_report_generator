"""Module for generating report."""

from typing import TextIO

from .gh_cli import get_project_id


def get_repo_from_name(name: str) -> tuple[str, str]:
    """Get a repository from a string name."""
    owner, sep, repo = name.partition("/")
    if not sep:
        raise ValueError("Repository name must be in the form org/repo")

    return owner, repo


async def generate_report(repo_name: str, project_name: str, fd: TextIO) -> None:
    """Generate a report and write to specified file."""
    owner, repo = get_repo_from_name(repo_name)
    project_id = await get_project_id(owner, project_name)
    print(project_id)
