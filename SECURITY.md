# Security Policy

## Supported Versions

Security fixes are applied to the latest released version of AKSARA and the
default branch while the project is in the `0.x` development series.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

## Reporting a Vulnerability

Do not open a public issue for a suspected security vulnerability.

Use GitHub's private vulnerability reporting for this repository when available.
If private vulnerability reporting is unavailable, contact the repository
maintainers through GitHub and request a private disclosure channel before
sharing exploit details.

Include the following information in the report:

- Affected AKSARA version or commit.
- Operating system and Python version.
- Steps to reproduce the issue.
- Expected and actual behavior.
- Impact assessment, including whether code execution, data disclosure,
  denial of service, or dependency compromise is possible.
- Any proof-of-concept code needed to validate the report.

## Response Process

Maintainers aim to acknowledge valid reports within 7 days. After triage, the
maintainers will confirm the impact, prepare a fix, add regression coverage when
appropriate, and coordinate disclosure through GitHub Security Advisories.

Security releases should include a patched version, changelog entry, and advisory
with mitigation guidance.

## Scope

In scope:

- Vulnerabilities in the AKSARA interpreter, parser, runtime, CLI, packaging, or
  documented standard library behavior.
- Dependency or build-chain issues that affect distributed AKSARA packages.
- Denial-of-service behavior caused by crafted AKSARA source input.

Out of scope:

- Reports that require already-compromised maintainer credentials.
- Social engineering against maintainers or users.
- Issues in third-party services that are not controlled by this project.
- Vulnerabilities that only affect unsupported versions.
