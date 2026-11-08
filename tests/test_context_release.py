import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("context_release", ROOT / "tools/context_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ContextReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "source"
        config = json.loads((ROOT / release.CONFIG).read_text())
        for name in config["files"]:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def build(self, out="output"):
        return Path(release.build(self.root, self.base / out, "UNCOMMITTED")["archive"])

    def test_reproducible_package_and_readback(self):
        first, second = self.build("one"), self.build("two")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        result = release.check_archive(first, release.digest(first.read_bytes()))
        self.assertEqual(result["integrity"], "PASS")
        self.assertEqual(result["source_commit"], "UNCOMMITTED")

    def test_unlisted_private_file_is_excluded(self):
        (self.root / "private-session.txt").write_text("must not be published")
        with zipfile.ZipFile(self.build()) as z:
            self.assertNotIn("private-session.txt", z.namelist())

    def test_missing_input_blocks(self):
        (self.root / "WORKING_CONTEXT.md").unlink()
        with self.assertRaises(release.ReleaseError):
            self.build()

    def test_changed_foundation_blocks(self):
        path = self.root / "docs/foundations/created-time-and-appointed-arrival.md"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
        with self.assertRaises(release.ReleaseError):
            self.build()

    def test_symlink_input_blocks(self):
        path = self.root / "WORKING_CONTEXT.md"
        path.unlink()
        outside = self.base / "private.txt"
        outside.write_text("private")
        path.symlink_to(outside)
        with self.assertRaises(release.ReleaseError):
            self.build()

    def test_traversal_input_blocks(self):
        path = self.root / release.CONFIG
        config = json.loads(path.read_text())
        config["files"].append("../private.txt")
        path.write_text(json.dumps(config))
        with self.assertRaises(release.ReleaseError):
            self.build()

    def test_false_commit_binding_blocks(self):
        with self.assertRaises(release.ReleaseError):
            release.build(self.root, self.base / "out", "0" * 40)

    def test_real_commit_binding_and_dirty_input(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.DEVNULL)
        git("init")
        git("add", ".")
        git("-c", "user.name=Release Test", "-c", "user.email=test@example.invalid", "commit", "-m", "fixture")
        sha = git("rev-parse", "HEAD").decode().strip()
        result = release.build(self.root, self.base / "bound", sha)
        self.assertEqual(release.check_archive(result["archive"])["source_commit"], sha)
        (self.root / "WORKING_CONTEXT.md").write_text("uncommitted change")
        with self.assertRaises(release.ReleaseError):
            release.build(self.root, self.base / "dirty", sha)

    def rewrite_archive(self, additions):
        original = self.build()
        changed = self.base / "changed.zip"
        with zipfile.ZipFile(original) as src, zipfile.ZipFile(changed, "w") as dst:
            for name in src.namelist():
                dst.writestr(name, additions.pop(name, src.read(name)))
            for name, content in additions.items():
                dst.writestr(name, content)
        return changed

    def test_modified_archive_member_blocks(self):
        with self.assertRaises(release.ReleaseError):
            release.check_archive(self.rewrite_archive({"WORKING_CONTEXT.md": b"changed"}))

    def test_unexpected_archive_member_blocks(self):
        with self.assertRaises(release.ReleaseError):
            release.check_archive(self.rewrite_archive({"extra.txt": b"unexpected"}))

    def test_external_digest_mismatch_blocks(self):
        with self.assertRaises(release.ReleaseError):
            release.check_archive(self.build(), "0" * 64)

    def test_output_cannot_overlap_inputs(self):
        with self.assertRaises(release.ReleaseError):
            release.build(self.root, self.root / "docs", "UNCOMMITTED")


if __name__ == "__main__":
    unittest.main()
