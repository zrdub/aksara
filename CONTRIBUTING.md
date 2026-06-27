# Contributing to AKSARA

Thank you for helping improve AKSARA. This project welcomes bug reports,
documentation improvements, tests, examples, and carefully scoped language
implementation changes.

## Code of Conduct

All participation in this project is governed by
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Be respectful, constructive, and
patient with contributors at every experience level.

## Before You Start

- Search existing issues and pull requests before opening a new one.
- Open an issue first for significant language, runtime, parser, CLI, packaging,
  or compatibility changes.
- Keep pull requests focused on one concern.
- Include tests for behavior changes and documentation for user-facing changes.

## Development Setup

Use Python 3.12 or newer.

```bash
git clone https://github.com/zrdub/aksara.git
cd aksara
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip install build ruff
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Quality Checks

Run the checks before opening a pull request:

```bash
python -m ruff format --check src tests
python -m pytest
python -m build
```

The GitHub Actions workflow runs these checks on Python 3.12 and Python 3.13.

## Project Structure

- `src/aksara/` contains the AKSARA package.
- `tests/` contains automated tests.
- `examples/` contains runnable `.aks` programs.
- `docs/` contains language documentation.
- `.github/` contains repository automation and contribution templates.

## Commit and Pull Request Guidelines

- Use clear, imperative commit messages, for example `Add parser test for nested blocks`.
- Explain why the change is needed in the pull request body.
- Link related issues with `Closes #123` when applicable.
- Update `CHANGELOG.md` for user-visible changes.
- Keep generated build artifacts such as `build/` and `dist/` out of commits.

## Testing Expectations

- Bug fixes should include a regression test that fails without the fix.
- New language features should include parser/runtime tests and a documentation update.
- CLI changes should include tests that cover exit codes and user-facing output.
- Documentation-only changes do not need new runtime tests, but should remain accurate.

## Release Process

Maintainers prepare releases using [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).
Release pull requests should update version references, changelog entries, and
documentation before a tag is created.
