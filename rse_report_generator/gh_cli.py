import asyncio
from typing import Sequence, Any
import json


async def _run_gh_command(*command: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        "gh", *command, stdout=asyncio.subprocess.PIPE
    )

    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("Failed to run gh")

    return stdout.decode()


async def _run_gh_command_json(*command: str) -> dict[str, Any]:
    return json.loads(await _run_gh_command(*command))


_projects: dict[str, Any] = {}


async def get_github_token() -> str:
    return (await _run_gh_command("auth", "token")).strip()


async def get_projects(org: str) -> list[dict[str, Any]]:
    try:
        return _projects[org]
    except KeyError:
        _projects[org] = (
            await _run_gh_command_json(
                "project", "list", "--format", "json", "--owner", org
            )
        )["projects"]
        return _projects[org]


async def get_project_id(org: str, project_name: str) -> str:
    projects = await get_projects(org)
    try:
        return next(
            project["id"] for project in projects if project["title"] == project_name
        )
    except StopIteration:
        raise ValueError(f'Project "{project_name}" not found in {org}')
