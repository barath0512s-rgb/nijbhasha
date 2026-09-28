"""The page the server sends must not load anything from the internet."""

import re

import config

HTML = (config.BASE_DIR / "frontend.html").read_text(encoding="utf-8")

# URLs that appear in the file but are never fetched:
#   the SVG XML namespace inside an inline data: image, and the JS fallback
#   address used when the page is opened straight from disk.
NOT_FETCHED = {"http://www.w3.org/2000/svg", "http://127.0.0.1:5000"}


def test_no_external_urls():
    urls = set(re.findall(r"https?://[^\s'\"()<>%]+", HTML))
    assert urls <= NOT_FETCHED, sorted(urls - NOT_FETCHED)


def test_no_remote_stylesheets_or_scripts():
    assert not re.search(r"<link[^>]+href=[\"']https?:", HTML)
    assert not re.search(r"<script[^>]+src=[\"']https?:", HTML)
    assert "@import" not in HTML


def test_every_font_face_file_exists():
    srcs = re.findall(r"url\('/static/fonts/([^']+)'\)", HTML)
    assert len(srcs) >= 5
    for name in srcs:
        assert (config.STATIC_DIR / "fonts" / name).exists(), name


def test_olchiki_font_is_in_every_text_stack():
    """Ol Chiki must never depend on the device having a system font for it."""
    for var in ("--deva", "--olck"):
        m = re.search(var + r":([^;]+)", HTML)
        assert m and "Noto Sans Ol Chiki" in m.group(1), var


def test_english_is_a_third_interface_language():
    # Hindi, Santali and English buttons; English hides only when /config says ui_english is false
    # (config.UI_ENGLISH), and evaluator mode (?evaluator=1) still shows it then.
    assert re.search(r'<button id="langEn"[^>]*>English</button>', HTML)
    assert not re.search(r'<button id="langEn"[^>]*\bhidden\b', HTML)
    assert "englishOption(c.ui_english)" in HTML and 'get("evaluator")' in HTML


def test_every_interface_string_has_english():
    """Every key of the Hindi table exists in the English one (a missing key would show Hindi)."""
    hi = HTML[HTML.index("\nhi: {"):HTML.index("\nsat: {")]
    en = HTML[HTML.index("\nen: {"):HTML.index("\n};", HTML.index("\nen: {"))]
    keys = lambda block: set(re.findall(r"(?m)(?:^|[,{\s])([a-z][a-z0-9_]*)\s*:", block))
    assert keys(hi) - keys(en) <= {"hi"}, sorted(keys(hi) - keys(en))


def test_config_offers_english():
    import config
    assert config.UI_ENGLISH is True


def test_the_page_runs_on_android_9_webview():
    """Android 9's stock WebView is Chrome 69 (the 2 GB emulator had 69.0.3497):
    no nullish/optional chaining, logical assignment, numeric separators or newer
    built-ins. One of them is a syntax error there and the whole page stops."""
    import re
    from pathlib import Path
    html = (Path(__file__).resolve().parent.parent / "frontend.html").read_text(encoding="utf-8")
    js = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"//[^\n]*", "", js)                         # comments may mention them
    banned = {r"\?\?": "??", r"\?\.(?!\d)": "?.", r"(\|\||&&)=": "logical assignment", r"(?<![\w$])\d+_\d": "numeric separator",
              r"\.replaceAll\(": "replaceAll", r"Object\.fromEntries": "Object.fromEntries",
              r"\.matchAll\(": "matchAll", r"allSettled": "Promise.allSettled", r"\.at\(": ".at()",
              r"globalThis": "globalThis", r"structuredClone": "structuredClone", r"Promise\.any": "Promise.any"}
    found = [name for pat, name in banned.items() if re.search(pat, js)]
    assert not found, f"not in Chrome 69: {found}"


def test_every_team_lesson_has_an_english_title():
    """Shown only in the English interface (titles only; the lesson lines stay Hindi)."""
    import json
    from pathlib import Path
    block = HTML[HTML.index("const TEAM_TITLE_EN = {"):HTML.index("};", HTML.index("const TEAM_TITLE_EN = {"))]
    mapped = set(re.findall(r'"([^"]+)":', block))
    team = json.loads((Path(__file__).parent.parent / "content" / "team_lessons.json").read_text(encoding="utf-8"))
    assert {l["title"] for l in team["lessons"]} <= mapped
    assert 'S.lang === "en" && TEAM_TITLE_EN[title]' in HTML
