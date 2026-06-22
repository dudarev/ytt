# Repository Safety Policy

Apply this policy to `main` after the CI workflow from this branch has passed on
the default branch.

## Required `main` Settings

- Require a pull request before merging.
- Require status checks to pass before merging.
- Require the `tox (3.12)` and `tox (3.13)` checks.
- Disable force pushes.
- Disable branch deletion.

## Verification

The required CI workflow runs on pull requests and pushes to `main`. It executes
the tox environments for Python 3.12 and 3.13. Each tox environment runs the unit
tests plus installed-package smoke checks for:

- `ytt --help`
- `ytt --version`
- Import `ytt` and `ytt.domain` from a temporary directory, assert the import
  path is in `site-packages`, and assert installed package metadata matches
  `ytt.__version__`.
