"""The entry point for RSE report generator."""

import asyncio
import sys

from .report import generate_report


async def main() -> None:
    """Main entry point for program."""
    if len(sys.argv) != 3:
        raise RuntimeError("Repo name and project name must be provided")

    await generate_report(sys.argv[1], sys.argv[2], sys.stdout)


if __name__ == "__main__":
    asyncio.run(main())
