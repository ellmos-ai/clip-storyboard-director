"""Automated metadata, documentation parity, and security contract test suite.

Ensures that READMEs, SECURITY.md, pyproject.toml, llms.txt, CI workflows, and source
invariants remain strictly synchronized and adhere to ecosystem standards.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_required_root_documents_exist():
    """Verify that all standard governance and documentation files are present."""
    required = [
        "README.md",
        "README_de.md",
        "SECURITY.md",
        "LICENSE",
        "THIRD_PARTY_LICENSES.md",
        "CHANGELOG.md",
        "MARKETING-LOG.txt",
        "llms.txt",
        "pyproject.toml",
        "ellmos-module.v2.json",
        ".github/workflows/ci.yml",
    ]
    for rel_path in required:
        target = ROOT / rel_path
        assert target.is_file(), f"Missing required file: {rel_path}"


def test_version_parity():
    """Verify version 0.1.2 parity across code, manifests, and documentation."""
    expected_version = "0.1.2"

    # 1. Python package __version__
    import clip_director

    assert clip_director.__version__ == expected_version

    # 2. pyproject.toml
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'version\s*=\s*"([^"]+)"', pyproject_text)
    assert m is not None, "Version not found in pyproject.toml"
    assert m.group(1) == expected_version

    # 3. ellmos-module.v2.json
    manifest_data = json.loads((ROOT / "ellmos-module.v2.json").read_text(encoding="utf-8"))
    assert manifest_data.get("version") == expected_version

    # 4. llms.txt
    llms_content = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f"Version: {expected_version}" in llms_content

    # 5. CHANGELOG.md
    changelog_content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## [{expected_version}]" in changelog_content


def test_readme_badges_parity():
    """Verify Shields.io badges in both English and German READMEs."""
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (ROOT / "README_de.md").read_text(encoding="utf-8")

    expected_badges = [
        "https://github.com/ellmos-ai/clip-storyboard-director/actions/workflows/ci.yml/badge.svg",
        "https://img.shields.io/badge/pytest-passing",
        "https://img.shields.io/badge/python-3.10",
        "https://img.shields.io/badge/ecosystem-ellmos--ai-purple",
        "https://img.shields.io/badge/umbrella-open--bricks-blueviolet",
        "https://img.shields.io/badge/version-0.1.2",
        "https://img.shields.io/badge/llms.txt-Discovery%20Context-informational",
        "https://img.shields.io/badge/security%20SLA-48h%20response",
        "https://img.shields.io/badge/code%20style-ruff-000000.svg",
        "https://img.shields.io/badge/last%20checked-2026--09--09-informational",
        "license-MIT",
    ]

    for badge in expected_badges:
        assert badge in readme_en, f"Missing badge in README.md: {badge}"
        assert badge in readme_de, f"Missing badge in README_de.md: {badge}"


def test_quick_navigation_anchors():
    """Verify quick navigation links resolve to headers in READMEs."""
    for filename in ["README.md", "README_de.md"]:
        content = (ROOT / filename).read_text(encoding="utf-8")
        assert "Quick Navigation" in content or "Schnellnavigation" in content

        # Extract markdown anchor links [Text](#anchor)
        anchor_links = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", content)
        assert len(anchor_links) >= 12, f"Expected at least 12 quick nav links in {filename}"

        # Extract headers ## Header Title
        headers = re.findall(r"^#{2,4}\s+(.+)$", content, re.MULTILINE)
        normalized_headers = [
            re.sub(r"[^\w\s-]", "", h).strip().lower().replace(" ", "-") for h in headers
        ]

        for _text, anchor in anchor_links:
            assert anchor in normalized_headers or any(
                anchor in nh for nh in normalized_headers
            ), f"Anchor #{anchor} in {filename} does not match any header"


def test_mermaid_diagrams_syntax():
    """Verify Mermaid diagrams in both READMEs are present and well-formed."""
    for filename in ["README.md", "README_de.md"]:
        content = (ROOT / filename).read_text(encoding="utf-8")
        diagrams = re.findall(r"```mermaid\n(.*?)```", content, re.DOTALL)
        assert len(diagrams) >= 2, f"Expected at least 2 Mermaid diagrams in {filename}"
        assert any("flowchart TD" in d for d in diagrams), f"Missing flowchart TD in {filename}"
        assert any("sequenceDiagram" in d for d in diagrams), f"Missing sequenceDiagram in {filename}"


def test_governance_invariants_table():
    """Verify all 10 governance and runtime invariants are documented."""
    invariants = [
        "INV-LOCAL-01",
        "INV-UNPRIV-02",
        "INV-LOOPBACK-03",
        "INV-SANDBOX-04",
        "INV-CONTINUITY-05",
        "INV-CLUEFRAME-06",
        "INV-STANDALONE-07",
        "INV-MULTIOS-08",
        "INV-SYNC-09",
        "INV-SLA-10",
    ]
    for filename in ["README.md", "README_de.md"]:
        content = (ROOT / filename).read_text(encoding="utf-8")
        for inv in invariants:
            assert inv in content, f"Missing invariant {inv} in {filename}"


def test_sibling_ecosystem_matrix():
    """Verify sibling ecosystem tools are linked in both READMEs."""
    siblings = [
        "ai-media-editor",
        "system-auditor",
        "system-explorer",
        "ellmos-voice-io",
        "ellmos-controlcenter-mcp",
        "open-bricks",
    ]
    for filename in ["README.md", "README_de.md"]:
        content = (ROOT / filename).read_text(encoding="utf-8")
        for sibling in siblings:
            assert sibling in content, f"Missing sibling {sibling} in {filename}"


def test_security_policy_contract():
    """Verify SECURITY.md contains bilingual policy, SLAs, and contact points."""
    security_file = ROOT / "SECURITY.md"
    assert security_file.is_file()
    content = security_file.read_text(encoding="utf-8")

    assert "English" in content
    assert "Deutsch" in content
    assert "48" in content
    assert "triage" in content.lower() or "5" in content
    assert "security@ellmos.ai" in content
    assert "security@open-bricks.org" in content
    assert "0.1.x" in content


def test_ci_workflow_contract():
    """Verify GitHub Actions CI workflow contains required testing matrix and gates."""
    ci_file = ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_file.is_file()
    content = ci_file.read_text(encoding="utf-8")

    assert "cancel-in-progress: true" in content
    assert "ubuntu-latest" in content
    assert "windows-latest" in content
    assert "macos-latest" in content
    assert "3.10" in content
    assert "3.11" in content
    assert "3.12" in content
    assert "3.13" in content
    assert "ruff check" in content
    assert "compileall" in content
    assert "pytest" in content
