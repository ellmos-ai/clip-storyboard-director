"""prompt_builder.py - einzige Quelle der Wahrheit fuer Shot-Prompts.

Was im Cockpit/Storyboard angezeigt wird, was der Kopieren-Knopf liefert, was per CDP
injiziert wird und was im Desktop-Handoff steht, kommt ausschliesslich von hier.
Reine Funktionen, keine I/O.
"""

MODES = ("plain", "de", "en", "silent")
SILENT_DEFAULT = "Silent video with ambient environmental sound only, strictly no human voice"


def current_shot(shots):
    """Aktueller Shot = erster ohne Hero-Take (sonst der erste)."""
    return next((s for s in shots if not s.get("selected_take")), shots[0] if shots else {})


def active_prompt(shot):
    """(version, text) der aktiven Prompt-Version; faellt auf den ersten Prompt zurueck."""
    prompts = shot.get("prompts") or []
    v = shot.get("active_prompt_version", "v1")
    p = next((p for p in prompts if p.get("version") == v), None) or (prompts[0] if prompts else {})
    return p.get("version", v), p.get("text") or ""


def directive(shot, mode):
    """Audio-Direktive fuer den Modus ('' wenn keine zutrifft)."""
    voice = shot.get("voice") or {}
    d = voice.get("directives") or {}
    if mode == "de":
        text = voice.get("source_text") or voice.get("text")
        return d.get("german") or (f'Spoken dialogue in German (clear voice): "{text}"'
                                   if voice.get("enabled") and text else "")
    if mode == "en":
        en = voice.get("translated_text_en")
        return d.get("english") or (f'Spoken dialogue in English (clear voice): "{en}"' if en else "")
    if mode == "silent":
        return d.get("silent") or SILENT_DEFAULT
    return ""


def build_prompt(shot, mode="plain"):
    """Exakt der Text, der in die Zwischenablage / den Generator geht."""
    text = active_prompt(shot)[1]
    extra = directive(shot, mode)
    return f"{text}\n\n{extra}" if extra else text


def all_variants(shot):
    """Alle Modi vorberechnet (fuer Client-Daten und /api/cowork/focus)."""
    return {m: build_prompt(shot, m) for m in MODES}


def shot_prompt_data(shot):
    """Client-Daten pro Shot: aktive Version, fertige Varianten, Direktiven (Detailblatt)."""
    return {"prompt_version": active_prompt(shot)[0], "prompt_variants": all_variants(shot),
            "directives": {"de": directive(shot, "de"), "en": directive(shot, "en"),
                           "silent": directive(shot, "silent")}}
