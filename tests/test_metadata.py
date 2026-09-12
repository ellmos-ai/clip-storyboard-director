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
    """Verify version 0.1.4 parity across code, manifests, and documentation."""
    expected_version = "0.1.4"

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
        "https://img.shields.io/badge/version-0.1.4",
        "https://img.shields.io/badge/llms.txt-Discovery%20Context-informational",
        "https://img.shields.io/badge/security%20SLA-48h%20response",
        "https://img.shields.io/badge/code%20style-ruff-000000.svg",
        "https://img.shields.io/badge/last%20checked-2026--09--12-informational",
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
        assert len(anchor_links) == 16, f"Expected exactly 16 quick nav links in {filename}, got {len(anchor_links)}"

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


def test_gitignore_hygiene_patterns():
    """Verify .gitignore contains canonical locks, multi-host conflict patterns, and caches."""
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    required_patterns = [
        "LOCK",
        "LOCK.*",
        "*.lock",
        "LOCK*.txt",
        "LOCK.permissions.json",
        "uv.lock",
        "*-conflict-*",
        "*.sync-temp-*",
        "*.sync-conflict-*",
        "*-ASUS-GEI.*",
        "*-WORKSTATION-LG.*",
        "*-WORKSTATION.*",
        "* (kopie)*",
        "* (copy)*",
        "coverage/",
        "wheelhouse/",
        ".wheel-smoke/",
    ]
    for pattern in required_patterns:
        assert pattern in gitignore, f"Pattern {pattern} missing in .gitignore"


def test_pytest_configuration_and_flags():
    """Verify pyproject.toml defines standardized pytest options."""
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.pytest.ini_options]" in pyproject
    assert 'addopts = "-ra -v"' in pyproject


def test_ci_workflow_pytest_flags():
    """Verify CI workflow executes pytest with standardized -ra -v flags."""
    ci_file = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "pytest -ra -v" in ci_file


def test_changelog_recent_pfad_a_entry():
    """Verify CHANGELOG.md contains the 0.1.3 Pfad A technical hygiene release entry."""
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.1.3] - 2026-09-10" in changelog


def test_changelog_recent_pfad_b_entry():
    """Verify CHANGELOG.md contains the 0.1.4 Pfad B marketing and discoverability release entry."""
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.1.4] - 2026-09-12" in changelog


def test_target_personas_and_discoverability_section():
    """Verify target personas and bilingual keywords in both English and German READMEs."""
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "## Target Personas & Discoverability" in readme_en
    assert "## Zielgruppen & Auffindbarkeit" in readme_de

    # English personas and pain points
    assert "AI Filmmakers & Narrative Directors" in readme_en
    assert "Generative Media Engineers" in readme_en
    assert "Content Creators & YouTubers" in readme_en
    assert "Autonomous Coding Agents" in readme_en

    # German personas and pain points
    assert "KI-Filmschaffende & Narrative Regisseure" in readme_de
    assert "Generative Medien-Entwickler" in readme_de
    assert "Content Creator & YouTuber" in readme_de
    assert "Autonome Coding-Agenten" in readme_de

    # High-Intent search queries
    assert "High-Intent Search Queries" in readme_en
    assert "Suchbegriffe mit hoher Absicht" in readme_de


def test_third_party_licenses_section_and_invariants():
    """Verify third-party licenses section and invariant guarantees in both READMEs."""
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "## Third-Party Licenses & Transparency" in readme_en
    assert "## Drittanbieter-Lizenzen & Transparenz" in readme_de

    for content in [readme_en, readme_de]:
        assert "PyYAML" in content
        assert "edge-tts" in content
        assert "websocket-client" in content
        assert "requests" in content
        assert "INV-LOCAL-01" in content
        assert "INV-UNPRIV-02" in content
        assert "THIRD_PARTY_LICENSES.md" in content


def test_pep621_extended_project_urls():
    """Verify pyproject.toml defines extended PEP 621 URLs for discoverability."""
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"Third-Party Licenses"' in pyproject
    assert '"Marketing-Log"' in pyproject
    assert '"LLM-Ready"' in pyproject
    assert "THIRD_PARTY_LICENSES.md" in pyproject
    assert "MARKETING-LOG.txt" in pyproject
    assert "llms.txt" in pyproject


def test_third_party_licenses_file_contract():
    """Verify THIRD_PARTY_LICENSES.md inventory, audit date, and compliance invariants."""
    licenses_doc = (ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    assert "Audit Date:** 2026-09-12" in licenses_doc
    assert "GPL-3.0" in licenses_doc
    assert "LGPL" in licenses_doc
    assert "INV-LOCAL-01" in licenses_doc
    assert "INV-UNPRIV-02" in licenses_doc
    assert "INV-LOOPBACK-03" in licenses_doc


def test_marketing_log_contract():
    """Verify local MARKETING-LOG.txt contains personas, 5-way matrix, invariants, and latest audit."""
    marketing_log = (ROOT / "MARKETING-LOG.txt").read_text(encoding="utf-8")
    assert "TARGET PERSONAS & AUDIENCE PROFILES" in marketing_log
    assert "HIGH-INTENT SEARCH QUERIES" in marketing_log
    assert "5-WAY COMPETITIVE DIFFERENTIATION MATRIX" in marketing_log
    assert "GOVERNANCE & RUNTIME INVARIANTS" in marketing_log
    assert "SIBLING ECOSYSTEM & PARTNER MATRIX" in marketing_log
    assert "2026-09-12 — Pfad B" in marketing_log
    assert "INV-LOCAL-01" in marketing_log
    assert "INV-SLA-10" in marketing_log
