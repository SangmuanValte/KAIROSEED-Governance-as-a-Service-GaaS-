# KAIROSEED Context and Workflow v0.1.0

**Classification:** documentation and local workflow prerelease.

This release provides a short, reusable starting context for code, documentation, preparation, memory, and release work. Start with `WORKING_CONTEXT.md` in the repository or ZIP.

## Contents

- Original `created-time-and-appointed-arrival.md`, preserved byte-for-byte.
- Small working context and a task-to-release guide.
- A concise session-handoff template.
- Standard-library Python validation, deterministic ZIP packaging, and archive checking.
- Scoped packaging tests and an exact-commit GitHub publication workflow.
- A per-file manifest and SHA256SUMS for the release assets.

The repository also corrects an older workflow's output from `INDEPENDENT_VERIFICATION=PASS` to `CI_VERIFICATION=PASS` and `INDEPENDENT_VERIFICATION=NOT_ASSESSED`. That older workflow is not executed by this release.

## Evidence and limits

The release workflow must pass the scoped packaging tests before publication. Inspect the actual workflow run for the observed result, Python version, and commit. The manifest binds packaged bytes to the release commit, and the ZIP includes its manifest.

**Independent verification: NOT ASSESSED.** These are project-operated tests of file selection, integrity checks, and packaging. They do not establish application correctness, AI governance enforcement, protected-state containment, formal proof, production readiness, certification, or divine timing.

The foundation's historical repository-status text is preserved as source material. Its inclusion in this release establishes publication of this document only; implementation verification remains a separate task. The full Master Data Pack has not been reassembled or verified by this release.

**Canonical specification: FROZEN — UNCHANGED.** No production deployment is performed.

## Reproduce and inspect

Check out the exact commit referenced by the release tag, then run:

```bash
python3 -m unittest discover -s tests -p test_context_release.py -v
python3 tools/context_release.py build --source-commit "$(git rev-parse HEAD)" --out dist/reproduction
python3 tools/context_release.py check dist/reproduction/context-workflow-v0.1.0.zip
```

Compare the resulting ZIP hash with the published SHA256SUMS. Identical bytes demonstrate reproducibility of this package, not correctness of broader research claims. Preserve a failed result and its conditions rather than editing the acceptance criteria after the fact.
