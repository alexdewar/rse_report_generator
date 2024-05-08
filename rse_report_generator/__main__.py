"""The entry point for RSE report generator."""

import asyncio
import sys
from datetime import datetime

from dateparser import parse

from .report import generate_report


def _get_date(date_str: str) -> datetime:
    if parsed_date := parse(date_str):
        return parsed_date.astimezone()

    raise ValueError(f"{date_str} is not a valid date string")


async def main() -> None:
    """Main entry point for program."""
    repo_name = sys.argv[1]
    from_date = _get_date(sys.argv[2])
    to_date = (
        _get_date(sys.argv[3]) if len(sys.argv) >= 4 else datetime.now().astimezone()
    )

    await generate_report(repo_name, from_date, to_date, sys.stdout)


if __name__ == "__main__":
    asyncio.run(main())
