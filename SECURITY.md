# Security Policy

## Scope

This repository contains reference governance implementations for AI-agent authorization and simulated execution.

Security reports should focus on:

- authorization bypasses;
- execution paths that bypass the documented gate;
- invariant violations;
- evidence integrity failures;
- unsafe default behavior;
- sensitive-data exposure introduced by the project.

## Do not include secrets

Do not submit API keys, credentials, private tokens, personal data, or other sensitive material in public issues.

For a suspected vulnerability involving sensitive information, use the repository owner's private GitHub security-reporting mechanism if enabled. If private reporting is unavailable, contact the maintainer through the account associated with this repository and provide only the minimum necessary detail.

## Report contents

Include:

1. affected commit/version;
2. affected component/path;
3. exact reproduction steps;
4. expected authorization boundary;
5. observed behavior;
6. whether a consequential side effect occurred;
7. minimal test case, if safe to provide.

Preserve the original artifact. Do not silently modify the reproduction.

## Security posture

This project is not currently presented as production-certified. Security reports may reveal gaps between documented and actual behavior; those gaps are treated as evidence requiring investigation, not as proof of universal security.
