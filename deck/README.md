# Decks

| File | What | Slides |
|---|---|---|
| `final_deck.pptx` (+ `.pdf`) | Finale / presentation-round deck: problem, approach, architecture, R1-R4 proof slides, novelty, trust, comparison, impact, roadmap, demo; appendix with sources and licences, benchmarks, evidence, privacy, limitations, real lesson lines, judge questions. Speaker notes on every slide (script + likely question and answer) | 14 + 7 appendix |
| `../docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx` (+ `.pdf`) | The idea submission in the SIH template (SIH limit: 6 slides including the title) | 6 |

Every number has a source line on its slide; `../docs/deck/SOURCES.md` and `../docs/feature_traceability.md`
map numbers and features to files. The only placeholder is the demo video link (slide 14 and submission slide 6).

The PDFs are LibreOffice exports for preview; export the upload PDF from PowerPoint.

Rebuild the finale deck: `cd deck/build && npm install pptxgenjs && node build_final_deck.js` (assets are the
screenshots of the current page taken on 28 Sep, pages of `docs/samples/`, and the repository QR code).
Devanagari text uses the Nirmala UI font (Windows); Ol Chiki appears only inside images, so it displays everywhere.
