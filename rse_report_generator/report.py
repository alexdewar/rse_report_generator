"""Module for generating report."""

from typing import TextIO

from githubkit import GitHub, UnauthAuthStrategy

github = GitHub(UnauthAuthStrategy())


def get_repo_from_name(name: str) -> tuple[str, str]:
    """Get a repository from a string name."""
    owner, sep, repo = name.partition("/")
    if not sep:
        raise ValueError("Repository name must be in the form org/repo")

    return owner, repo


async def generate_report(repo_name: str, fd: TextIO) -> None:
    """Generate a report and write to specified file."""
    owner, repo = get_repo_from_name(repo_name)
    async for pr in github.paginate(
        github.rest.pulls.async_list, owner=owner, repo=repo, state="closed"
    ):
        print(f"{pr.number}: {pr.title}", file=fd)
