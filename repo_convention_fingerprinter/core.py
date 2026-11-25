"""Core repository stack, package manager, and test-runner fingerprinter."""
from typing import Any, Dict, List


class RepoFingerprinter:
    """Infers developer tooling conventions from repository file paths."""

    def fingerprint(self, file_paths: List[str]) -> Dict[str, Any]:
        norm = {p.replace("\\", "/").lstrip("./") for p in file_paths}
        basenames = {p.split("/")[-1]: p for p in norm}

        language = "unknown"
        pkg_mgr = "unknown"
        test_cmd = "unknown"
        linters: List[str] = []

        if "pyproject.toml" in basenames or "setup.py" in basenames or any(p.endswith(".py") for p in norm):
            language = "python"
            if "uv.lock" in basenames:
                pkg_mgr = "uv"
            elif "poetry.lock" in basenames:
                pkg_mgr = "poetry"
            else:
                pkg_mgr = "pip"
            test_cmd = "pytest" if any("conftest.py" in p for p in norm) else "python -m unittest discover"
            if any("ruff" in p for p in norm):
                linters.append("ruff")
            if any("mypy" in p for p in norm):
                linters.append("mypy")
        elif "package.json" in basenames:
            language = "javascript/typescript"
            if "pnpm-lock.yaml" in basenames:
                pkg_mgr = "pnpm"
            elif "yarn.lock" in basenames:
                pkg_mgr = "yarn"
            else:
                pkg_mgr = "npm"
            test_cmd = f"{pkg_mgr} test"
            if any("eslint" in p for p in norm):
                linters.append("eslint")
        elif "Cargo.toml" in basenames:
            language = "rust"
            pkg_mgr = "cargo"
            test_cmd = "cargo test"
            linters.append("clippy")
        elif "go.mod" in basenames:
            language = "go"
            pkg_mgr = "go"
            test_cmd = "go test ./..."

        return {
            "language": language,
            "package_manager": pkg_mgr,
            "test_command": test_cmd,
            "linters": sorted(linters),
            "has_tests": any("test" in p.lower() for p in norm),
        }

    def to_agents_md(self, file_paths: List[str]) -> str:
        p = self.fingerprint(file_paths)
        return (
            "# Repository Conventions\n"
            f"- Language: {p['language']}\n"
            f"- Package Manager: {p['package_manager']}\n"
            f"- Test Command: `{p['test_command']}`\n"
            f"- Linters: {', '.join(p['linters']) or 'none'}\n"
        )
