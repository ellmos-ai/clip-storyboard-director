"""Edge darf nicht mit --remote-allow-origins=* starten: sonst kann jede Webseite im
eingeloggten Cockpit-Profil per WebSocket auf den CDP-Port zugreifen."""

from clip_director import start_cockpit


def test_edge_and_shortcut_start_without_remote_allow_origins(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(start_cockpit, "ensure_server_running", lambda *a, **k: None)
    monkeypatch.setattr(start_cockpit, "DEFAULT_EDGE_PATH", str(tmp_path / "msedge.exe"))
    (tmp_path / "msedge.exe").write_bytes(b"")
    monkeypatch.setattr(start_cockpit.Path, "home", staticmethod(lambda: tmp_path))

    class FakeProc:
        pid = 1

    monkeypatch.setattr(start_cockpit.subprocess, "run", lambda cmd, **k: calls.append(cmd))
    monkeypatch.setattr(start_cockpit.subprocess, "Popen", lambda cmd, **k: calls.append(cmd) or FakeProc())

    project = tmp_path / "proj"
    project.mkdir()
    (project / "project.yaml").write_text("project: {name: p}\nshots: []\n", encoding="utf-8")

    start_cockpit.launch_edge_cockpit(str(project))

    flat = " ".join(" ".join(map(str, c)) for c in calls)
    assert "--remote-debugging-port" in flat, "Edge-Start und Verknuepfung muessen erfasst sein"
    assert "remote-allow-origins" not in flat


def test_cli_autopilot_passes_full_project_path(monkeypatch, tmp_path):
    from clip_director import cli

    seen = []
    monkeypatch.setattr("clip_director.auto_pilot.run_production_loop", lambda p: seen.append(p))

    class Args:
        project = str(tmp_path / "elsewhere" / "film")

    cli.cmd_autopilot(Args())
    assert seen == [Args.project]
