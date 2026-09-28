"""C3: the Mundari translation preview on the hub (mundari_nmt.py, POST /preview/translate)."""

import importlib

import pytest

import config
import mundari_nmt

NUKTA_ESCAPED = "ड\\u093C"          # ड + the six characters ़, as the adapters write it


def test_directions_and_label():
    assert set(mundari_nmt.DIRECTIONS) == {"hi-to-unr", "unr-to-hi"}
    assert mundari_nmt.DIRECTIONS["hi-to-unr"][1:] == ("hin_Deva", "brx_Deva")      # surrogate tag, as trained
    assert mundari_nmt.LABEL == ("held-out 5% of the MMLoSo 2025 training file, n=1,021 pairs, greedy, "
                                 "Mundari preview, not reviewed by a native speaker")
    assert not mundari_nmt.available("hi-to-sat")


def test_output_is_cleaned_and_labelled(monkeypatch):
    class Fake:
        def translate(self, text, src, tgt):
            assert (src, tgt) == ("hin_Deva", "brx_Deva")
            return "प" + NUKTA_ESCAPED + "हा", [2]
    monkeypatch.setattr(mundari_nmt, "_engine", lambda d: Fake())
    r = mundari_nmt.translate("पड़हा", "hi-to-unr")
    assert r["translated_text"] == "पड़हा"
    assert r["maturity"] == "preview" and r["needs_review"] is True and r["label"] == mundari_nmt.LABEL
    with pytest.raises(ValueError):
        mundari_nmt.translate("x", "hi-to-sat")


needs_hub = pytest.mark.skipif(
    not (config.ASR_DIR / "model_onnx.py").exists() or not (config.NMT_DIR / "config.json").exists(),
    reason="model files not downloaded")


@pytest.fixture(scope="module")
def client():
    app_module = importlib.import_module("app")
    app_module.app.testing = True
    return app_module.app.test_client()


@needs_hub
def test_route_flag_missing_model_and_bad_input(client, monkeypatch, tmp_path):
    monkeypatch.setattr(config, "MUNDARI_NMT_PREVIEW", False)
    r = client.post("/preview/translate", json={"text": "आज", "direction": "hi-to-unr"})
    assert r.status_code == 404 and r.get_json()["code"] == "disabled"
    unr = [l for l in client.get("/languages").get_json()["languages"] if l["code"] == "unr"][0]
    assert unr["stages"]["nmt"]["maturity"] == "not available"          # the page hides the button

    monkeypatch.setattr(config, "MUNDARI_NMT_PREVIEW", True)
    assert client.post("/preview/translate", json={"text": "", "direction": "hi-to-unr"}).status_code == 400
    assert client.post("/preview/translate", json={"text": "आज", "direction": "hi-to-sat"}).status_code == 400
    monkeypatch.setattr(config, "MUNDARI_NMT_DIR", tmp_path / "none")
    r = client.post("/preview/translate", json={"text": "आज", "direction": "hi-to-unr"})
    assert r.status_code == 503 and r.get_json()["code"] == "engine_missing"


@needs_hub
@pytest.mark.skipif(not mundari_nmt.available("hi-to-unr") or not mundari_nmt.available("unr-to-hi"),
                    reason="Mundari model not installed (tools/install_mundari_nmt.py)")
def test_route_translates_both_ways(client, monkeypatch):
    monkeypatch.setattr(config, "MUNDARI_NMT_PREVIEW", True)
    for direction, text in (("hi-to-unr", "यही पड़हा पत्थर तो, नया-नया से ही शुरू हुआ है।"),
                            ("unr-to-hi", "नेअःगे पड़हा दिरि दो, नवा नवागे एटेःआकना।")):
        r = client.post("/preview/translate", json={"text": text, "direction": direction})
        assert r.status_code == 200, r.get_json()
        d = r.get_json()
        assert d["translated_text"].strip() and "\\u" not in d["translated_text"]
        assert d["maturity"] == "preview" and d["needs_review"] is True
    unr = [l for l in client.get("/languages").get_json()["languages"] if l["code"] == "unr"][0]
    assert unr["stages"]["nmt"]["maturity"] == "preview"


def test_no_repeat_can_be_switched_off_per_engine():
    import nmt_onnx
    assert nmt_onnx.OnnxNMT._banned([5, 6, 5, 6, 5], 0) == set()          # the Mundari engine: off
    assert nmt_onnx.OnnxNMT._banned([5, 6, 5, 6, 5], 3) == {6}            # Santali default: unchanged


@pytest.mark.skipif(not list((config.BASE_DIR / "data" / "mmloso").glob("*.csv")) if (config.BASE_DIR / "data" / "mmloso").exists() else True,
                    reason="MMLoSo training file not in data/mmloso/ (git-ignored)")
def test_the_rebuilt_split_matches_the_notebook():
    import sys
    sys.path.insert(0, str(config.BASE_DIR / "eval"))
    import mundari_split
    r = mundari_split.check()
    assert r["held_out"] == 1021 and r["hindi_not_in_leakage_set"] == 0 and r["mundari_not_in_leakage_set"] == 0, r
