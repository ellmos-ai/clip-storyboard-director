"""Regression tests for the two `clip-director cockpit` startup bugs reported
2026-09-27: an ImportError (start_cockpit exported no such name) and a doubled
"projects/projects/..." path when the caller already passed a "projects/<name>"
path (the default for every other subcommand)."""

from clip_director import cli
from clip_director.start_cockpit import SKILL_ROOT, launch_edge_cockpit, resolve_project_path


def test_cli_imports_the_real_cockpit_entrypoint():
    # cmd_cockpit used to import a non-existent `start_cockpit` name from the
    # start_cockpit module; this simply confirms the name it now imports
    # actually exists as a callable.
    assert callable(launch_edge_cockpit)


def test_resolve_project_path_bare_name():
    assert resolve_project_path("sternenseufzer") == SKILL_ROOT / "projects" / "sternenseufzer"


def test_resolve_project_path_does_not_double_projects_prefix():
    # This is the exact input every other subcommand's --project default uses.
    assert resolve_project_path("projects/sternenseufzer") == SKILL_ROOT / "projects" / "sternenseufzer"


def test_resolve_project_path_absolute_passthrough(tmp_path):
    assert resolve_project_path(str(tmp_path)) == tmp_path


def test_cmd_cockpit_calls_launch_edge_cockpit_with_resolved_args(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "clip_director.start_cockpit.launch_edge_cockpit",
        lambda project_name, server_port=None: calls.append((project_name, server_port)),
    )

    class Args:
        project = "projects/sternenseufzer"
        port = 8765

    cli.cmd_cockpit(Args())
    assert calls == [("projects/sternenseufzer", 8765)]


def test_known_desktop_folder_uses_shgetknownfolderpath_on_windows(tmp_path, monkeypatch):
    import ctypes
    from types import SimpleNamespace

    from clip_director import desktop_handoff

    known_dir = tmp_path / "CustomOneDrive" / "Desktop"
    fallback_home = tmp_path / "UnusedHome"
    freed = []

    class FakeShell32:
        def SHGetKnownFolderPath(self, rfid, flags, token, out_ptr):
            assert len(rfid.raw) == 16
            out_ptr._obj.value = str(known_dir)
            return 0

    class FakeOle32:
        def CoTaskMemFree(self, p):
            freed.append(p)

    monkeypatch.setattr(desktop_handoff.sys, "platform", "win32")
    monkeypatch.setattr(desktop_handoff.Path, "home", classmethod(lambda cls: fallback_home))
    monkeypatch.setattr(
        ctypes,
        "windll",
        SimpleNamespace(shell32=FakeShell32(), ole32=FakeOle32()),
        raising=False,
    )

    assert desktop_handoff.get_default_desktop() == known_dir
    assert len(freed) == 1


def test_known_desktop_folder_falls_back_safely_when_api_unavailable(tmp_path, monkeypatch):
    from clip_director import desktop_handoff

    monkeypatch.setattr(desktop_handoff.sys, "platform", "linux")
    monkeypatch.setattr(desktop_handoff.Path, "home", classmethod(lambda cls: tmp_path))

    assert desktop_handoff.get_default_desktop() == tmp_path / "Desktop"

    onedrive_desktop = tmp_path / "OneDrive" / "Desktop"
    onedrive_desktop.mkdir(parents=True)
    assert desktop_handoff.get_default_desktop() == onedrive_desktop


def test_create_desktop_shortcut_uses_known_desktop_folder(tmp_path, monkeypatch):
    from clip_director import desktop_handoff, start_cockpit

    known_desktop = tmp_path / "KnownDesktop"
    known_desktop.mkdir()
    monkeypatch.setattr(desktop_handoff, "get_default_desktop", lambda: known_desktop)

    captured = []
    monkeypatch.setattr(
        start_cockpit.subprocess,
        "run",
        lambda cmd, **kw: captured.append(cmd),
    )

    start_cockpit.create_desktop_shortcut()
    assert len(captured) == 1
    assert str(known_desktop / "STORYBOARD COCKPIT (Edge).lnk") in captured[0][-1]
