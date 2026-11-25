"""CLI for Repo Convention Fingerprinter."""
import argparse
import json
import os
from .core import RepoFingerprinter


def main():
    parser = argparse.ArgumentParser(description="Repo Convention Fingerprinter CLI")
    parser.add_argument("--path", default=".", help="Repository directory to scan")
    parser.add_argument("--markdown", action="store_true", help="Output AGENTS.md format")
    args = parser.parse_args()

    files = []
    for root, _, names in os.walk(args.path):
        if ".git" in root or "__pycache__" in root:
            continue
        for n in names:
            files.append(os.path.relpath(os.path.join(root, n), args.path))

    fp = RepoFingerprinter()
    if args.markdown:
        print(fp.to_agents_md(files))
    else:
        print(json.dumps(fp.fingerprint(files), indent=2))


if __name__ == "__main__":
    main()
