import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "clip_director"))

from render_dashboard import render_project  # noqa: E402

EVIL = "x');alert(1);//</script><script>alert(2)</script>"


class _Attrs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.handlers = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.scripts += 1
        for k, v in attrs:
            if k in ("onclick", "ondragstart") and ("copyBibleItem" in v or "onAssetDragStart" in v):
                self.handlers.append(v)


def test_yaml_values_cannot_break_out_of_script_or_handlers(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "ref.png").write_bytes(b"png")
    data = {
        "project": {"name": "t", "title": "T", "fps": "<b>24</b>"},
        "consistency_bible": [
            {"id": EVIL, "name": EVIL, "category": "c", "description": EVIL, "reference_image": "assets/ref.png"},
        ],
        "shots": [{"step_nr": 1, "slug": "a", "prompts": [{"version": "v1", "text": EVIL}], "takes": []}],
    }
    (tmp_path / "project.yaml").write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")

    out = render_project(tmp_path).read_text(encoding="utf-8")

    parser = _Attrs()
    parser.feed(out)
    # Genau der eine Script-Block des Templates – kein eingeschleuster
    assert parser.scripts == 1
    assert "<b>24</b>" not in out
    # Nach HTML-Dekodierung muss das JS-Argument ein gueltiges, vollstaendiges String-Literal sein
    assert parser.handlers
    for handler in parser.handlers:
        arg = re.search(r"\((?:event, this, )?(.*)\)$", handler).group(1)
        assert json.loads(arg) == EVIL
