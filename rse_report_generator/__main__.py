"""The entry point for RSE report generator."""

import asyncio
import sys
from argparse import ArgumentParser
from datetime import datetime
from typing import TextIO

from dateparser import parse

from .report import generate_report


def _get_date(date_str: str) -> datetime:
    if parsed_date := parse(date_str):
        return parsed_date.astimezone()

    raise ValueError(f"{date_str} is not a valid date string")


def _open_file(path: str) -> TextIO:
    if path == "-":
        return sys.stdout

    return open(path, "w")


async def async_main() -> None:
    """Main entry point for program (asynchronous)."""
    parser = ArgumentParser(
        "RSE report generator", "A tool to automatically generate reports for projects"
    )
    parser.add_argument("repo")
    parser.add_argument("-f", "--from-date", default="one month ago", type=_get_date)
    parser.add_argument("-t", "--to-date", default="now", type=_get_date)
    parser.add_argument("-o", "--output", default="-")

    args = parser.parse_args()
    with _open_file(args.output) as file:
        await generate_report(args.repo, args.from_date, args.to_date, file)


def main() -> None:
    """Main entry point for program."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
