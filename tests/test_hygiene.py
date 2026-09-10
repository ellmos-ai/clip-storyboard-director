"""Tests for repository hygiene, path neutrality, metadata parity, and gate standards."""

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_version_parity():
    """Ensure versions match across pyproject.toml, package, and ellmos-module manifest."""
    import clip_director

    pkg_version = clip_director.__version__

    pyproject_path = REPO_ROOT / "pyproject.toml"
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    m = re.search(r'version\s*=\s*"([^"]+)"', pyproject_text)
    assert m is not None, "Version not found in pyproject.toml"
    pyproject_version = m.group(1)

    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_version = manifest_data.get("version")

    assert pkg_version == pyproject_version == manifest_version == "0.1.3"


def test_llms_txt_structure():
    """Ensure llms.txt exists and contains standard discoverability headers."""
    llms_path = REPO_ROOT / "llms.txt"
    assert llms_path.is_file()
    content = llms_path.read_text(encoding="utf-8")
    assert "# clip-storyboard-director" in content
    assert "System Overview" in content
    assert "Key Invariants" in content
    assert "CLI Quick Reference" in content


def test_todo_status_table():
    """Ensure TODO.md exists with a valid STATUS table."""
    todo_path = REPO_ROOT / "TODO.md"
    assert todo_path.is_file()
    content = todo_path.read_text(encoding="utf-8")
    assert "STATUS" in content.upper()
    assert "| Category" in content or "| category" in content


def test_no_hardcoded_personal_paths_in_source():
    """Ensure source and templates do not leak personal Windows user paths."""
    forbidden = [
        re.compile(r"C:[\\/]+Users[\\/]+(?:lukas|User)(?=[\\/]|$)", re.IGNORECASE),
        re.compile(r"/c/Users/(?:lukas|User)(?=/|$)", re.IGNORECASE),
    ]
    scan_extensions = {".py", ".html", ".sh", ".json", ".yaml", ".yml"}

    for dirpath, _, filenames in os.walk(REPO_ROOT):
        # Skip git directory
        if ".git" in dirpath:
            continue
        for filename in filenames:
            ext = Path(filename).suffix.lower()
            if ext not in scan_extensions:
                continue
            filepath = Path(dirpath) / filename
            text = filepath.read_text(encoding="utf-8", errors="ignore")
            for pattern in forbidden:
                assert not pattern.search(text), f"Personal path found in {filepath}"


def test_gitignore_contains_required_gate_entries():
    """Ensure .gitignore has all minimum entries required by the release gate."""
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.is_file()
    text = gitignore_path.read_text(encoding="utf-8")
    required = ["__pycache__", "*.pyc", ".env", "*.db", ".venv/", ".idea/", ".vscode/", "data/"]
    for entry in required:
        assert entry in text, f"Missing required gitignore entry: {entry}"
