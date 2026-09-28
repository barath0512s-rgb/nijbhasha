# reading_guide.py — a Devanagari reading guide for Santali (Ol Chiki) output.
#
# A Hindi-medium teacher cannot read Ol Chiki. The guide writes the same
# Santali in Devanagari so the teacher can read it aloud and, over time, learn
# it: a bridge, not only a translator. It is the transliteration the offline
# voice already speaks (translit/olchiki.py, 125 reference cases); its phonetic
# choices await native review, so the page and the lesson plan call it a guide.

from translit.olchiki import has_olchiki, to_devanagari


def reading_guide(text):
    """Devanagari for Santali text, numbers as Santali number words; None when the
    text has no Ol Chiki (Hindi output, empty text)."""
    if not text or not has_olchiki(text):
        return None
    return to_devanagari(text)
