from clip_director import __version__
from clip_director.render_cockpit import render_cockpit
from clip_director.render_dashboard import render_project
from clip_director.storyboard_init import create_project


def test_version():
    assert __version__ == "0.1.6"


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


def test_standalone_without_media_editor(monkeypatch):
    from clip_director.cli import cmd_doctor
    # Set to a non-existent path to verify standalone operation without ai-media-editor
    monkeypatch.setenv("AI_MEDIA_EDITOR_DIR", "C:/nonexistent/path/for/tests")
    ret = cmd_doctor()
    assert ret == 0, "Director doctor must pass even if ai-media-editor is not installed"


def test_cli_version_flag():
    import subprocess
    import sys
    for flag in ["--version", "-v"]:
        res = subprocess.run([sys.executable, "-m", "clip_director", flag], capture_output=True, text=True)
        assert res.returncode == 0
        assert "clip-director 0.1.6" in res.stdout or "clip-director 0.1.6" in res.stderr


def test_pep561_typing_marker_file():
    from pathlib import Path
    import clip_director
    pkg_dir = Path(clip_director.__file__).resolve().parent
    marker = pkg_dir / "py.typed"
    assert marker.is_file(), "src/clip_director/py.typed must exist for PEP 561 compliance"

