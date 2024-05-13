"""Module for generating report."""

from datetime import datetime
from typing import TextIO

from githubkit import (
    BaseAuthStrategy,
    GitHub,
    TokenAuthStrategy,
    UnauthAuthStrategy,
)
from jinja2 import Environment, PackageLoader, select_autoescape

from .config import PACKAGE_NAME
from .repository import Repository
from .token import get_github_token


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
    env = Environment(
        loader=PackageLoader(PACKAGE_NAME),
        autoescape=select_autoescape(),
        enable_async=True,
        keep_trailing_newline=True,
        line_statement_prefix="%%",
    )
    template = env.get_template("report.md.jinja")
    async for chunk in template.generate_async(
        repo_name=repo_name, from_date=from_date, to_date=to_date, repo=repo
    ):
        fd.write(chunk)
