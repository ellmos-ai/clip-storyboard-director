import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "clip_director"))

from auto_pilot import resolve_project_path  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def test_resolves_bundled_project_by_name():
    # vorher: src/projects/sternenseufzer (existiert nicht)
    assert resolve_project_path("sternenseufzer") == REPO / "projects" / "sternenseufzer"
    assert (resolve_project_path("sternenseufzer") / "project.yaml").exists()


def test_accepts_explicit_project_dir(tmp_path):
    (tmp_path / "project.yaml").write_text("shots: []\n", encoding="utf-8")
    assert resolve_project_path(str(tmp_path)) == tmp_path.resolve()
