"""The int8 translation guards (nmt_guard.py), on the run-on outputs actually seen
(no models needed)."""

from pathlib import Path

from nmt_guard import cut_stem_loop, length_cap, stem_loop


def test_the_int8_stem_loop_is_cut():
    # bench/results/latency_steps_onnx-int8-t6.csv, a 25-word FLEURS sentence
    seen = ("ᱥᱟᱯᱷᱟᱨᱤ ᱥᱟᱯᱷᱟᱹᱨᱤ ᱥᱟᱯᱷᱚᱨᱤ ᱥᱟᱯᱷᱮᱨᱤ ᱥᱟᱯᱷᱷᱟᱨᱤ ᱥᱟᱯᱷᱛᱨᱤ ᱥᱟᱯᱷᱚᱛᱤ ᱥᱟᱯᱷᱛᱤ ᱥᱟᱯᱷᱤᱛᱤ ᱥᱟᱯᱷᱤᱛ")
    out, cut = cut_stem_loop(seen)
    assert cut and out == "ᱥᱟᱯᱷᱟᱨᱤ"


def test_the_fp32_loops_found_on_the_test_sets_are_cut():
    # data/eval/hyp_flores_sat_Olck-hin_Deva.txt (fp32), cut off by the length cap mid-loop
    hi = ("उदाहरण के लिए, लोअर वैली, रेन वैली हॉर्ट, हैप्पी डेन्यूब में एक लोकप्रिय स्थान हैप्पी, हैवी, हैव, हैम, "
          "हैव्ह, हैवन, हैवे, हैवो, हैवा, हैवान, हैवां, हैवान्, हैवॉ, हैवाना, हैवानी, हैविया, हैव्यू, हैवास्ट, हैवाः "
          "हैवोड, है वोइस, हैवॊड, हैंवोड और हैवोडकॉ, हैव्डकॉम्ब, है")
    out, cut = cut_stem_loop(hi)
    assert cut and out.endswith("हैम, हैव्ह,") and len(out.split()) == 19


def test_a_repeated_word_is_not_a_loop():
    # fp32 output for a counting line: the source repeats the word, so may the output
    text = "ᱢᱤᱫ, ᱢᱤᱫ, ᱜᱮᱞ, ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ, ᱛᱩᱨᱩᱭ ᱜᱮᱞ, ᱢᱤᱫ ᱜᱮᱞ, ᱢᱤᱫᱴᱟᱝ ᱜᱮᱞ, ᱵᱟᱨᱭᱟ ᱾"
    assert cut_stem_loop(text) == (text, False)
    assert not stem_loop("ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ".split())


def test_normal_sentences_pass():
    for text in ("ᱟᱢᱟᱜ ᱛᱤ ᱨᱮᱭᱟᱜ ᱫᱟᱜ ᱫᱚ ᱵᱤᱞᱟᱹᱛ ᱨᱮᱭᱟᱜ ᱯᱚᱨᱤᱢᱟᱱ ᱥᱟᱞᱟᱜ ᱠᱟᱹᱢᱤᱼᱟ ᱾",
                 "आज हम जोड़ना सीखेंगे। एक और एक मिलाओ।"):
        assert cut_stem_loop(text) == (text, False)


def test_length_cap():
    assert length_cap(8) == 26
    assert length_cap(40) == 90
    assert length_cap(100) == 128


# ── script guard (nmt_guard.foreign_letters) ─────────────────────────────────
def test_foreign_letters_finds_other_scripts_in_santali_output():
    from nmt_guard import foreign_letters
    # real outputs from the 26 Sep content pack (docs/fln_translation_sample.md)
    assert foreign_letters("ᱢᱤᱫᱴᱟᱝ ᱟᱛᱳ ᱨᱮ ᱢᱤᱫᱴᱟᱝ ᱠᱷᱮᱹᱞᱚᱜ ᱠᱟᱱ ꯎꯆꯦꯛ ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ ᱾")      # Meetei Mayek
    assert foreign_letters("ᱛᱮᱦᱮᱧ ᱫᱚ اتوار ᱾")                                         # Urdu
    assert foreign_letters("ᱰᱟᱣun ᱰᱟᱣୂନ")                                              # Latin, Odia
    assert foreign_letters("ᱛᱮᱦᱮᱸᱡ ᱟᱞᱮ ᱢᱤᱫ ᱠᱷᱚᱱ ᱜᱮᱞ ᱛᱩᱨᱩᱭ ᱜᱤᱱᱛᱤ ᱥᱮᱪᱮᱫᱟ।") == ""
    assert foreign_letters("᱓ + ᱔ = ? 7, ᱾ ?") == ""                                    # digits, punctuation
    assert foreign_letters("") == "" and foreign_letters(None) == ""


def test_the_pipeline_flags_foreign_script_model_output():
    src = (Path(__file__).resolve().parent.parent / "pipeline.py").read_text(encoding="utf-8")
    assert "nmt_guard.foreign_letters(out)" in src and 'result["review_reason"] = "script"' in src
    kt = (Path(__file__).resolve().parent.parent /
          "android/app/src/main/java/org/team8bitpool/app/core/Api.kt").read_text(encoding="utf-8")
    assert kt.count("foreignLetters(out)") == 2       # typed and spoken replies on the tablet
