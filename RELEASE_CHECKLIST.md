# Release Checklist

Use this checklist for every AKSARA release.

## Preparation

- Confirm the release scope and target version.
- Confirm all intended changes are merged into the default branch.
- Confirm `CHANGELOG.md` has a dated entry for the release.
- Confirm version references are consistent in `pyproject.toml`, `src/aksara/__init__.py`,
  README badges or text, and documentation.
- Confirm supported Python versions are accurate in `pyproject.toml`, README, and CI.

## Verification

- Run formatting checks:

  ```bash
  python -m ruff format --check src tests
  ```

- Run tests:

  ```bash
  python -m pytest
  ```

- Build release artifacts:

  ```bash
  python -m build
  ```

- Inspect the generated wheel and source distribution in `dist/`.
- Install the built wheel in a clean virtual environment and run `aksara versi`.
- Run the example program:

  ```bash
  aksara jalankan examples/halo.aks
  ```

## GitHub Release

- Create an annotated tag named `vX.Y.Z`.
- Push the tag to GitHub.
- Create a GitHub Release from the tag.
- Attach the built wheel and source distribution if publishing artifacts through GitHub.
- Include release notes copied from the matching `CHANGELOG.md` section.

## After Release

- Verify the GitHub Actions workflow completed successfully for the release tag.
- Confirm documentation links and badges render correctly on GitHub.
- Open a follow-up issue for any release debt discovered during verification.
