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
from .repository import Repository


async def _get_auth_strategy() -> BaseAuthStrategy:
    if token := await get_github_token():
        return TokenAuthStrategy(token)

    return UnauthAuthStrategy()


async def generate_report(
    repo_name: str, from_date: datetime, to_date: datetime, fd: TextIO
) -> None:
    """Generate a report and write to specified file."""
    github = GitHub(await _get_auth_strategy())
    repo = Repository(github, repo_name)

    print(
        f"# Report for {repo_name} ({from_date.date()} to {to_date.date()})\n", file=fd
    )

    print("## Merged pull requests\n", file=fd)
    async for pr in repo.get_merged_pull_requests(from_date, to_date):
        print(f"- {pr.number}: {pr.title}", file=fd)
