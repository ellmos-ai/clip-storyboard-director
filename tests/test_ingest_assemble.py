import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "clip_director"))

from assemble import ensure_voice_audio  # noqa: E402
from ingest import process_inbox  # noqa: E402


def _project(tmp_path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    data = {
        "project": {"name": "t"},
        "shots": [
            {"step_nr": 1, "takes": []},
            {"step_nr": 2, "takes": []},
        ],
    }
    (tmp_path / "project.yaml").write_text(yaml.dump(data), encoding="utf-8")
    return tmp_path


def test_ingest_keeps_master_and_creates_missing_video_dir(tmp_path):
    proj = _project(tmp_path)
    (proj / "t_master.mp4").write_bytes(b"master")
    (proj / "_temp_stitched.mp4").write_bytes(b"tmp")
    (proj / "_inbox").mkdir()
    (proj / "_inbox" / "shot01.png").write_bytes(b"png")

    process_inbox(proj, auto_advance=False)

    assert (proj / "t_master.mp4").exists(), "Master-Video darf nicht als Take einsortiert werden"
    assert (proj / "_temp_stitched.mp4").exists()
    assert (proj / "video" / "shot01_v01.png").exists()
    shots = yaml.safe_load((proj / "project.yaml").read_text(encoding="utf-8"))["shots"]
    assert [t["file"] for t in shots[0]["takes"]] == ["video/shot01_v01.png"]
    assert shots[1]["takes"] == []


def test_recorded_voice_wins_over_tts(tmp_path):
    (tmp_path / "voice").mkdir()
    rec = tmp_path / "voice" / "shot01_user_voice.mp3"
    rec.write_bytes(b"mp3")
    shot = {"step_nr": 1, "voice": {"enabled": True, "text": "Hallo", "rendered_file": "voice/shot01_user_voice.mp3"}}
    assert ensure_voice_audio(tmp_path, shot) == rec


def test_desktop_handoff_finds_shot_by_step_nr(tmp_path):
    from desktop_handoff import handoff_step

    proj = _project(tmp_path / "proj")
    desk = tmp_path / "desk"
    # vorher: Suche nach "step" statt "step_nr" -> sys.exit(1) mitten im Ingest-Thread
    handoff_step(proj, 2, desk, force=True)
    assert any(desk.iterdir())
