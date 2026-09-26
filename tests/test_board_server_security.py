import http.client
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "clip_director"))

import board_server  # noqa: E402
from link_resolver import download_media  # noqa: E402


@pytest.fixture
def server(tmp_path, monkeypatch):
    (tmp_path / "project.yaml").write_text("project: {name: t}\nshots: []\n", encoding="utf-8")
    (tmp_path / "storyboard.html").write_text("<html>ok</html>", encoding="utf-8")
    # Ingest/Render sind hier nicht Gegenstand des Tests
    monkeypatch.setattr(board_server, "process_inbox", lambda *a, **k: None, raising=False)
    monkeypatch.setattr(board_server, "render_project", lambda *a, **k: None, raising=False)

    def handler(*args, **kwargs):
        return board_server.StoryboardHandler(*args, project_dir=tmp_path, **kwargs)

    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield srv.server_address[1], tmp_path
    srv.shutdown()
    srv.server_close()


def request(port, method, path, headers=None, body=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request(method, path, body=body, headers=headers or {})
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp, data


def test_own_origin_allowed_and_no_wildcard_cors(server):
    port, _ = server
    resp, _ = request(port, "GET", "/api/watcher/status")
    assert resp.status == 200
    assert resp.getheader("Access-Control-Allow-Origin") is None


def test_foreign_origin_post_rejected(server):
    port, _ = server
    resp, _ = request(port, "POST", "/api/open-folder", headers={"Origin": "https://evil.example"})
    assert resp.status == 403


def test_foreign_host_rejected(server):
    # DNS-Rebinding: fremder Hostname zeigt auf 127.0.0.1
    port, _ = server
    resp, _ = request(port, "GET", "/storyboard.html", headers={"Host": f"evil.example:{port}"})
    assert resp.status == 403


def test_upload_filename_cannot_escape_inbox(server):
    port, root = server
    resp, _ = request(
        port, "POST", "/api/upload-clip?step=1&filename=..%2F..%2Fescaped.mp4",
        headers={"Origin": f"http://127.0.0.1:{port}"}, body=b"data",
    )
    assert resp.status == 200
    assert (root / "_inbox" / "escaped.mp4").exists()
    assert not (root.parent / "escaped.mp4").exists()


def test_download_media_rejects_file_scheme(tmp_path):
    secret = tmp_path / "secret.txt"
    secret.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        download_media(secret.as_uri(), tmp_path / "out.mp4")
