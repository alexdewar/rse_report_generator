"""Module for interacting with the gh command-line tool."""

import asyncio
import logging
import os

_NO_TOKEN_MSG = (
    "Could not retrieve a GitHub token from your environment. This is only an issue if "
    "you want to access private repositories.\n\n"
    "To use a GitHub token, either manually generate one and set the GITHUB_TOKEN "
    "environment variable or install the GitHub command-line tools "
    '(https://cli.github.com/) and log in with "gh auth login".\n\n'
)


async def _run_gh_command(*command: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        "gh", *command, stdout=asyncio.subprocess.PIPE
    )

    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("Failed to run gh")

    return stdout.decode()


async def get_github_token() -> str | None:
    """Get the auth token being used by gh."""
    try:
        return (await _run_gh_command("auth", "token")).strip()
    except Exception:
        pass

    if token := os.environ.get("GITHUB_TOKEN"):
        return token

    logging.warn(_NO_TOKEN_MSG)
    return None
