"""Tests for Repo Convention Fingerprinter."""
import unittest
from repo_convention_fingerprinter.core import RepoFingerprinter


class TestRepoFingerprinter(unittest.TestCase):
    def setUp(self):
        self.fp = RepoFingerprinter()

    def test_detects_python_uv_pytest(self):
        res = self.fp.fingerprint(["pyproject.toml", "uv.lock", "tests/conftest.py", ".ruff.toml"])
        self.assertEqual(res["language"], "python")
        self.assertEqual(res["package_manager"], "uv")
        self.assertEqual(res["test_command"], "pytest")
        self.assertIn("ruff", res["linters"])

    def test_detects_node_pnpm(self):
        res = self.fp.fingerprint(["package.json", "pnpm-lock.yaml", "eslint.config.js"])
        self.assertEqual(res["package_manager"], "pnpm")
        self.assertEqual(res["test_command"], "pnpm test")

    def test_renders_agents_md(self):
        md = self.fp.to_agents_md(["Cargo.toml", "src/main.rs"])
        self.assertIn("cargo test", md)
