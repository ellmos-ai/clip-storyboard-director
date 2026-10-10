"""Eine Quelle der Wahrheit fuer Prompts: Anzeige, Kopieren, Injektion, Handoff."""
import http.client
import json
import re
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
import yaml

SRC = Path(__file__).resolve().parents[1] / "src" / "clip_director"
sys.path.insert(0, str(SRC))

import board_server  # noqa: E402
from prompt_builder import all_variants, build_prompt, current_shot  # noqa: E402
from render_dashboard import render_project  # noqa: E402

SHOT = {
    "step_nr": 1, "slug": "a", "active_prompt_version": "v2",
    "prompts": [{"version": "v1", "text": "alt"}, {"version": "v2", "text": "neu"}],
    "voice": {"enabled": True, "text": "Hallo", "translated_text_en": "Hello"},
}


def test_builder_active_version_and_modes():
    assert build_prompt(SHOT) == "neu"
    # voice.text allein genuegt (frueher: JS ignorierte es, Handoff nicht)
    assert build_prompt(SHOT, "de").endswith('German (clear voice): "Hallo"')
    assert build_prompt(SHOT, "en").endswith('English (clear voice): "Hello"')
    assert "Silent video" in build_prompt(SHOT, "silent")
    assert build_prompt({**SHOT, "voice": {"enabled": False, "text": "x"}}, "de") == "neu"


def test_builder_missing_version_falls_back_to_first_prompt():
    shot = {**SHOT, "active_prompt_version": "v9"}
    assert build_prompt(shot) == "alt"


def test_current_shot_is_first_without_hero():
    shots = [{"step_nr": 1, "selected_take": "t"}, {"step_nr": 2}]
    assert current_shot(shots)["step_nr"] == 2


def _project(tmp_path):
    (tmp_path / "project.yaml").write_text(yaml.safe_dump(
        {"project": {"name": "t"}, "shots": [SHOT]}, allow_unicode=True), encoding="utf-8")
    return tmp_path


def test_dashboard_embeds_server_built_variants(tmp_path):
    render_project(_project(tmp_path))
    html = (tmp_path / "storyboard.html").read_text(encoding="utf-8")
    m = re.search(r"const PROJECT_DATA = (.*?);\n", html)
    data = json.loads(m.group(1).replace("\u003c", "<").replace("\u003e", ">").replace("\u0026", "&"))
    assert data["shots"]["1"]["prompt_variants"] == all_variants(SHOT)
    # keine zweite Zusammenbau-Logik in den Vorlagen
    for name in ("dashboard_template.html", "cockpit_template.html"):
        tpl = (SRC / name).read_text(encoding="utf-8")
        assert "active_prompt_version" not in tpl
        assert "Spoken dialogue in" not in tpl


@pytest.fixture
def server(tmp_path):
    _project(tmp_path)
    render_project(tmp_path)

    def handler(*a, **k):
        return board_server.StoryboardHandler(*a, project_dir=tmp_path, **k)

    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield srv.server_address[1], tmp_path
    srv.shutdown()
    srv.server_close()


def _focus(port):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    c.request("GET", "/api/cowork/focus")
    return json.loads(c.getresponse().read())


def test_focus_matches_builder_and_follows_yaml_edit(server):
    port, tmp = server
    f1 = _focus(port)
    assert f1["prompt_variants"] == all_variants(SHOT)
    # Handbearbeitung von project.yaml: Fokus und Storyboard ziehen sofort nach
    data = yaml.safe_load((tmp / "project.yaml").read_text(encoding="utf-8"))
    data["shots"][0]["prompts"][1]["text"] = "geaendert"
    (tmp / "project.yaml").write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    f2 = _focus(port)
    assert f2["prompt_variants"]["plain"] == "geaendert"
    assert f2["revision"] != f1["revision"]
    assert "geaendert" in (tmp / "storyboard.html").read_text(encoding="utf-8")
