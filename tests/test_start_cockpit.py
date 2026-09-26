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
