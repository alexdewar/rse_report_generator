"""Provides a class for encapsulating the limited GitHub functionality we need."""

from collections.abc import AsyncIterable
from datetime import datetime

from githubkit import (
    GitHub,
)
from githubkit.versions.latest.models import PullRequestSimple


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
        self, from_date: datetime, to_date: datetime
    ) -> AsyncIterable[PullRequestSimple]:
        """Get all PRs merged within the given date range."""
        async for pr in self._github.paginate(
            self._github.rest.pulls.async_list,
            owner=self._owner,
            repo=self._repo,
            state="closed",
        ):
            if pr.merged_at and from_date <= pr.merged_at < to_date:
                yield pr
