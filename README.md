[![pre-commit.ci
status](https://results.pre-commit.ci/badge/github/alexdewar/rse_report_generator/main.svg)](https://results.pre-commit.ci/latest/github/alexdewar/rse_report_generator/main)

# RSE report generator

The RSE report generator is a tool for automatically generating markdown-formatted
reports for RSE projects. At present, it just uses information about closed issues and
PRs for GitHub repos, but integration with Clockify is planned.

## Installation

Note that you need Python v3.11 or newer.

You can install directly from GitHub with [`pipx`]:

```sh
pipx install git+https://github.com/alexdewar/rse_report_generator.git
```

The `rse-report-generator` command should now be available on your `PATH`.

[`pipx`]: https://github.com/pypa/pipx

## Get started

To generate a report for this repository, you can run:

```sh
rse-report-generator alexdewar/rse_report_generator
```

By default, this will output to `stdout` a report covering the preceding month's
activity. To view a full list of options, run:

```sh
rse-report-generator --help
```
