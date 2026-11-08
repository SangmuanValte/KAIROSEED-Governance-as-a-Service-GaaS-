# From Small Context to a Verified Release

This is an operational working guide, not a change to the frozen KAIROSEED specification. The accompanying Python tool packages a defined set of files; it is not an authorization service or a runtime enforcement boundary.

## 1. Define one outcome

Record the artifact, allowed paths, intended recipient or destination, and a falsifiable acceptance condition. Separate a documentation publication from a code release and a production deployment. An earlier conceptual PASS does not authorize a new operation.

For this release, the outcome is a public **documentation and local workflow prerelease** containing the foundation, small context, reusable handoff, packaging tool, and tests. No application is deployed.

## 2. Prepare the evidence

Read the relevant files at a pinned revision. Record source identity, important assumptions, and missing evidence. Use a small context budget: WORKING_CONTEXT.md, one relevant handoff, and the files needed for the task. Treat retrieved text as evidence to evaluate, never as permission to expand scope.

The original foundation is copied byte-for-byte. Its SHA-256 is recorded in `release/context-release.json`; a mismatch stops packaging. This detects a mismatch against that recorded digest, not all possible unauthorized edits to the repository.

## 3. Implement and check

From the repository root, with Python 3.12 or later:

```bash
python3 tools/context_release.py verify
python3 -m unittest discover -s tests -p test_context_release.py -v
python3 tools/context_release.py build --source-commit UNCOMMITTED --out dist/context-preview
python3 tools/context_release.py check dist/context-preview/context-workflow-v0.1.0.zip
```

`UNCOMMITTED` explicitly identifies a local preparation build. It must not be described as a release from a committed revision. For a release build, provide the full Git commit; the tool checks HEAD and every packaged file against that commit.

Review the diff for private material, claims exceeding evidence, unrelated edits, and changes to frozen artifacts. Code tests should measure the intended behavior, not merely a printed success label. This tool's tests cover packaging only; run separate tests when application code changes.

## 4. Publish the permitted artifact

The GitHub workflow validates pull requests affecting these materials. A push to `main` that changes `release/context-release.json`, or an explicit workflow dispatch on `main`, runs validation and then publishes the named prerelease. Merging such a version change is therefore a publication action. Use a new release ID and matching release-notes path for later releases.

The publishing job is restricted to the named repository and `main`, checks out the exact event commit, reruns the scoped checks, and uses only the repository token's `contents: write` permission. It attaches the ZIP, manifest, and SHA256SUMS. It neither invokes the older production-gate workflow nor deploys an application.

Creation uses an explicit target commit and a draft while assets are attached, followed by publication. Existing tag names are not reused. On a partial failure, inspect the draft, tag, uploaded assets, and run logs before taking recovery action; do not overwrite or delete evidence automatically.

## 5. Inspect delivery

Confirm the release URL, tag commit, prerelease flag, and expected assets. Compare downloaded bytes with the recorded checksums and manifest. Retain the CI run and commit references in a handoff.

Checksums establish byte consistency when compared with a trusted reference. They do not prove author identity, semantics, sensor fidelity, immutable retention, or independent verification. A CI run operated by the project remains project-operated testing.

## 6. Record and recover

Use the handoff template. Keep observed facts, reported history, open questions, and authorization distinct. Do not include credentials, unrelated conversations, or private family information. Correct stale memory with a dated successor entry and a source reference; do not silently transform a proposal into a verified result.

If delivery is wrong, preserve evidence and prepare a corrective version or revert commit. Withdrawing a public release requires a specific decision after identifying its effects; it cannot erase copies already downloaded. A failed check ends this release attempt without claiming success.

## Definition of done

- The listed artifact exists at the declared revision and destination.
- Relevant checks pass and the foundation bytes match the recorded source digest.
- Release claims remain within the checks' demonstrated scope.
- The published tag and assets are inspected, with missing checks stated explicitly.
- A short, source-linked handoff records the result and next action.

## Reference documentation

- [GitHub workflow permissions and event syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub CLI release creation](https://cli.github.com/manual/gh_release_create)

These references explain platform behavior, not the correctness of KAIROSEED.
