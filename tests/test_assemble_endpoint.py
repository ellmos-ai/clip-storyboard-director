import sys

from test_board_server_security import request, server  # noqa: F401  (Fixture, setzt sys.path)

import assemble  # noqa: E402,F401


def test_assemble_failure_is_reported_as_error(server, monkeypatch):  # noqa: F811
    port, _ = server
    # assemble_project gibt bei fehlendem Hero-Take/FFmpeg-Fehler None zurueck
    monkeypatch.setattr(sys.modules["assemble"], "assemble_project", lambda *_: None)
    resp, body = request(port, "POST", "/api/assemble", headers={"Origin": f"http://127.0.0.1:{port}"})
    assert resp.status == 500
    assert b'"status": "error"' in body
