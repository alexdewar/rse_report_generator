"""Provides a class for encapsulating the limited GitHub functionality we need."""

from collections.abc import AsyncIterable
from datetime import datetime

from githubkit import (
    GitHub,
)
from githubkit.versions.latest.models import Issue, PullRequestSimple


def _get_repo_from_name(name: str) -> tuple[str, str]:
    """Get a repository from a string name."""
    owner, sep, repo = name.partition("/")
    if not sep:
        raise ValueError("Repository name must be in the form org/repo")

    return owner, repo


class Repository:
    """A class for interacting with the GitHub API for a given repo."""

    def __init__(self, github: GitHub, repo_name: str) -> None:
        """Create a new Repository.

        Args:
            github: GitHub API instance
            repo_name: Name of repository in form owner/repo
        """
        self._github = github
        self._owner, self._repo = _get_repo_from_name(repo_name)

    async def get_merged_pull_requests(
        self, from_date: datetime, to_date: datetime, ignore_bots: bool = False
    ) -> AsyncIterable[PullRequestSimple]:
        """Get all PRs merged within the given date range."""
        async for pr in self._github.paginate(
            self._github.rest.pulls.async_list,
            owner=self._owner,
            repo=self._repo,
            state="closed",
        ):
            if ignore_bots and pr.user.type == "Bot":
                continue
            if pr.merged_at and from_date <= pr.merged_at < to_date:
                yield pr

    async def get_closed_issues(
        self, from_date: datetime, to_date: datetime
    ) -> AsyncIterable[Issue]:
        """Get all issues closed within the given date range."""
        async for issue in self._github.paginate(
            self._github.rest.issues.async_list_for_repo,
            owner=self._owner,
            repo=self._repo,
            state="closed",
            since=from_date,
        ):
            if (
                not issue.pull_request
                and issue.closed_at
                and from_date <= issue.closed_at < to_date
            ):
                yield issue
