import os
import shutil
import tempfile
import pytest
from pathlib import Path

from clip_director import __version__
from clip_director.storyboard_init import create_project
from clip_director.render_dashboard import render_project
from clip_director.render_cockpit import render_cockpit


def test_version():
    assert __version__ == "0.1.0"


def test_project_lifecycle(tmp_path):
    # 1. Init project in temp dir
    proj_dir = tmp_path / "test_clip"
    create_project("test_clip", "Test Film", total_duration=20, step_duration=10, out_dir=proj_dir)

    yaml_file = proj_dir / "project.yaml"
    assert yaml_file.exists(), "project.yaml should be created"

    # 2. Render dashboard
    html_dashboard = render_project(proj_dir)
    assert html_dashboard.exists(), "storyboard.html should be created"
    content = html_dashboard.read_text(encoding="utf-8")
    assert "test_clip" in content
    assert "Step 01" in content
    assert "Step 02" in content

    # 3. Render cockpit
    html_cockpit = render_cockpit(proj_dir)
    assert html_cockpit.exists(), "cockpit.html should be created"
    cockpit_content = html_cockpit.read_text(encoding="utf-8")
    assert "test_clip" in cockpit_content


def test_doctor():
    from clip_director.cli import cmd_doctor
    # Doctor should run without unhandled exceptions
    ret = cmd_doctor()
    assert ret in (0, 1)

