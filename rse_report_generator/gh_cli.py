"""Module for interacting with the gh command-line tool."""

import asyncio
import logging


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
    except RuntimeError as e:
        logging.warn(str(e))
        return None
