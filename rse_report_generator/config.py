"""Constants for use throughout the program."""

from importlib.metadata import version

from . import __name__ as PACKAGE_NAME

APP_NAME = "RSE report generator"
APP_DESCRIPTION = f"{APP_NAME}: A tool to automatically generate reports for projects"
APP_DESCRIPTION_EPILOG = (
    'Dates can be given in a human-readable format (e.g. "one month ago").'
)
APP_VERSION = version(PACKAGE_NAME)
PROG_NAME = "rse-report-generator"
