# Copilot instructions

## Commands

- Show CLI help with `python -m onefactorauth --help` or `python -m onefactorauth code --help`.
- Build a source distribution and wheel with `python setup.py sdist bdist_wheel`.
- The release workflow passes the tag ref to `setup.py` before building, for example `python setup.py refs/tags/v0.1.0 sdist bdist_wheel`.
- This repository has no configured test runner, tests, or lint command. `config.py` imports `yaml`; ensure PyYAML is available when running the CLI (it is not currently listed in `requirements.txt`).

## Architecture

- `onefactorauth/__main__.py` defines the `config` and `code` subcommands and dispatches to `config.py` and `code.py`. `setup.py` exposes the same entry point as `onefactorauth` and `1fa`.
- `config.py` stores the configured phone number in `~/.secrets.yml`. It keeps a list of app entries and updates the entry whose `app` is `onefa`.
- `code.py` fetches the SMS page through a `requests.Session`, extracts the code using the configured regex, reads the nearby `<date>` timestamp, and rejects codes older than the configured maximum age. Clipboard copying is optional.

## Conventions

- Keep the CLI arguments used to construct `ParseConf` in `__main__.py` aligned with its fields in `code.py`; dispatch currently selects arguments by matching field names.
- Preserve the existing secrets YAML structure: app entries have `app` and `env` keys, and `env` is a list of `{name, value}` mappings. When updating OneFactorAuth configuration, retain other app entries.
- Passcode patterns are expected to contain one capture group for the code. Timestamp parsing relies on the message date appearing in a `<date>...</date>` element before that code in the fetched HTML.
