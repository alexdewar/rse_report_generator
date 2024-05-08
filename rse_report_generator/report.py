"""Module for generating report."""

from datetime import datetime
from typing import TextIO

from githubkit import (
    BaseAuthStrategy,
    GitHub,
    TokenAuthStrategy,
    UnauthAuthStrategy,
)

from .gh_cli import get_github_token


def get_repo_from_name(name: str) -> tuple[str, str]:
    """Get a repository from a string name."""
    owner, sep, repo = name.partition("/")
    if not sep:
        raise ValueError("Repository name must be in the form org/repo")

    return owner, repo


async def _get_auth_strategy() -> BaseAuthStrategy:
    if token := await get_github_token():
        return TokenAuthStrategy(token)

    return UnauthAuthStrategy()


async def generate_report(
    repo_name: str, from_date: datetime, to_date: datetime, fd: TextIO
) -> None:
    """Generate a report and write to specified file."""
    print(
        f"# Report for {repo_name} ({from_date.date()} to {to_date.date()})\n", file=fd
    )

    github = GitHub(await _get_auth_strategy())
    owner, repo = get_repo_from_name(repo_name)

    print("## Merged pull requests\n", file=fd)
    async for pr in github.paginate(
        github.rest.pulls.async_list, owner=owner, repo=repo, state="closed"
    ):
        if pr.merged_at and from_date <= pr.merged_at < to_date:
            print(f"- {pr.number}: {pr.title}", file=fd)
