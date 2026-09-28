// Finale deck for Nijbhasha (SIH26042). Every number is from the repository; the
// source line on each slide names the file. Run: node build_final_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const A = f => path.join(__dirname, "assets", f);

const C = { navy: "14324D", ink: "1F2A37", mute: "5B6573", line: "D9D2C5", paper: "FBF8F3",
            saffron: "D9822B", teal: "1E7A6E", green: "1E7A45", blue: "1F6FB2", red: "B03A2E", white: "FFFFFF" };
const HF = "Arial", BF = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.33 x 7.5 in
pres.author = "Team 8-bitPool";
pres.title = "Nijbhasha — SIH26042 finale deck";

let n = 0;
function base(opts = {}) {
  const s = pres.addSlide();
  n += 1;
  s.background = { color: opts.dark ? C.navy : C.white };
  if (!opts.dark) {
    s.addText("Nijbhasha · SIH26042 · Team 8-bitPool", { x: 0.5, y: 7.05, w: 5, h: 0.3, fontFace: BF, fontSize: 9, color: C.mute, margin: 0, isTextBox: true });
    s.addText(String(n), { x: 12.3, y: 7.05, w: 0.5, h: 0.3, fontFace: BF, fontSize: 9, color: C.mute, align: "right", margin: 0, isTextBox: true });
  }
  return s;
}
function title(s, text, sub) {
  s.addText(text, { x: 0.5, y: 0.35, w: 12.3, h: 0.95, fontFace: HF, fontSize: 28, bold: true, color: C.navy, margin: 0, valign: "top", isTextBox: true });
  if (sub) s.addText(sub, { x: 0.5, y: 1.3, w: 12.3, h: 0.4, fontFace: BF, fontSize: 15, color: C.mute, margin: 0, isTextBox: true });
}
function source(s, text) {
  s.addText("Source: " + text, { x: 5.6, y: 7.05, w: 6.6, h: 0.3, fontFace: BF, fontSize: 8.5, color: C.mute, italic: true, align: "right", margin: 0, isTextBox: true });
}
function tile(s, x, y, w, h, big, small, color) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: color || C.navy }, line: { color: color || C.navy }, rectRadius: 0.12 });
  s.addText(big, { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: h * 0.5, fontFace: HF, fontSize: 30, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(small, { x: x + 0.15, y: y + h * 0.55, w: w - 0.3, h: h * 0.4, fontFace: BF, fontSize: 12.5, color: C.white, align: "center", valign: "top", margin: 0, isTextBox: true });
}
function chip(s, x, y, w, text, color) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.32, fill: { color }, line: { color }, rectRadius: 0.16 });
  s.addText(text, { x, y, w, h: 0.32, fontFace: BF, fontSize: 10.5, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function bullets(s, items, x, y, w, h, size) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })),
    { x, y, w, h, fontFace: BF, fontSize: size || 16, color: C.ink, valign: "top", paraSpaceAfter: 8, margin: 0, isTextBox: true });
}
function box(s, x, y, w, h, head, body, color) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: C.paper }, line: { color: C.line, width: 1 }, rectRadius: 0.1 });
  s.addText(head, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.4, fontFace: HF, fontSize: 15, bold: true, color: color || C.navy, margin: 0, isTextBox: true });
  s.addText(body, { x: x + 0.2, y: y + 0.58, w: w - 0.4, h: h - 0.7, fontFace: BF, fontSize: 12.5, color: C.ink, valign: "top", margin: 0, isTextBox: true });
}
function arrow(s, x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: color || C.mute, width: 2, endArrowType: "triangle" } });
}

// ── F1 Title ────────────────────────────────────────────────────────────────
{
  const s = base({ dark: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.2, y: 0.3, w: 2.8, h: 1.38, fill: { color: C.white }, line: { color: C.white }, rectRadius: 0.12 });
  s.addImage({ path: A("sih_logo.png"), x: 10.35, y: 0.4, w: 2.5, h: 1.18 });
  s.addText("Nijbhasha", { x: 0.8, y: 1.9, w: 9, h: 1.2, fontFace: HF, fontSize: 60, bold: true, color: C.white, margin: 0, isTextBox: true });
  s.addText("निजभाषा", { x: 0.8, y: 3.05, w: 9, h: 0.7, fontFace: "Nirmala UI", fontSize: 30, color: "F2C27B", margin: 0, isTextBox: true });
  s.addText("A Hindi-medium teacher teaches in Santali. Offline, on a tablet.", { x: 0.8, y: 3.95, w: 11, h: 0.6, fontFace: BF, fontSize: 24, color: C.white, margin: 0, isTextBox: true });
  s.addText("SIH26042 · Smart Education · Software   |   Team 8-bitPool (VITV) · Team ID 168531", { x: 0.8, y: 6.3, w: 11.5, h: 0.4, fontFace: BF, fontSize: 14, color: "C9D3DE", margin: 0, isTextBox: true });
  s.addNotes("Good morning. We are 8-bitPool, and this is Nijbhasha, which means 'one's own language'. In one line: a Hindi-medium teacher in Jharkhand runs a lesson in Santali, on a tablet, with no internet. Everything we show today is running code, and every number has a file behind it in our public repository.\n\nLikely question: Why the name change from VaaniSetu? Answer: another team used that name; we renamed on 26 September to avoid confusion.");
}

// ── F2 Problem ──────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "Children are taught in a language many do not speak at home", "Jharkhand, Grade 1: the teacher speaks Hindi; the child may speak Santali, Ho or Mundari.");
  tile(s, 0.5, 2.1, 3.9, 2.0, "~98%", "of surveyed schools teach in Hindi", C.navy);
  tile(s, 4.72, 2.1, 3.9, 2.0, "17 · 13 · 7 %", "Ho · Santali · Mundari: Grade 1 home languages", C.teal);
  tile(s, 8.94, 2.1, 3.9, 2.0, "5,000+", "tribal-area primary schools named in the problem statement", C.saffron);
  s.addText("PALASH shows mother-tongue teaching works; it cannot find enough teachers who speak these languages.",
    { x: 0.5, y: 4.6, w: 12.3, h: 0.8, fontFace: BF, fontSize: 18, color: C.ink, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 5.55, w: 12.3, h: 1.1, fill: { color: C.paper }, line: { color: C.line }, rectRadius: 0.12 });
  s.addText([{ text: "A child who cannot answer ", options: {} }, { text: "“दो और तीन कितने होते हैं?”", options: { bold: true, fontFace: "Nirmala UI" } },
             { text: " may not be failing at addition, but at Hindi.", options: {} }],
    { x: 0.8, y: 5.55, w: 11.7, h: 1.1, fontFace: BF, fontSize: 18, color: C.ink, valign: "middle", margin: 0, isTextBox: true });
  source(s, "JEPC Language Mapping Survey Ph. 1 (2024), pp. 17-18 (8,244 schools, 7 districts); SIH26042 brief");
  s.addNotes("The JEPC language-mapping survey of 8,244 schools found that about 98 percent teach in Hindi, while Grade 1 children's home languages include Ho 17.03 percent, Santali 13.07 percent and Mundari 7.32 percent. The problem statement names more than 5,000 tribal-area schools. PALASH shows mother-tongue teaching helps, but there are not enough teachers who speak these languages. A child who cannot answer 'two plus three' may not be failing at addition; they may not understand the Hindi question.\n\nLikely question: Are those percentages from your own data? Answer: No, from the JEPC survey report, pages 17 and 18; the brief gives the 5,000+ figure.");
}

// ── F3 Insight ──────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "Not a translator: a bridge the teacher can use tomorrow");
  const cols = [["Teacher speaks Hindi", "No Santali training needed", C.navy],
                ["Child hears Santali", "Text in Ol Chiki and speech, in under a second on the tablet", C.teal],
                ["Teacher reads it back", "Devanagari reading guide; lesson plan to print", C.saffron]];
  cols.forEach(([h, b, c], i) => {
    const x = 0.5 + i * 4.2;
    s.addShape(pres.shapes.OVAL, { x: x + 1.55, y: 1.75, w: 0.8, h: 0.8, fill: { color: c }, line: { color: c } });
    s.addText(String(i + 1), { x: x + 1.55, y: 1.75, w: 0.8, h: 0.8, fontFace: HF, fontSize: 26, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(h, { x, y: 2.75, w: 3.9, h: 0.5, fontFace: HF, fontSize: 20, bold: true, color: C.navy, align: "center", margin: 0, isTextBox: true });
    s.addText(b, { x: x + 0.2, y: 3.3, w: 3.5, h: 0.9, fontFace: BF, fontSize: 14, color: C.mute, align: "center", margin: 0, isTextBox: true });
    if (i < 2) arrow(s, x + 3.75, 2.15, x + 4.55, 2.15, C.mute);
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.5, y: 4.8, w: 10.3, h: 1.1, fill: { color: C.paper }, line: { color: C.line }, rectRadius: 0.12 });
  s.addText("The community corrects it; every doubtful line is flagged, never played as right.",
    { x: 1.7, y: 4.8, w: 9.9, h: 1.1, fontFace: BF, fontSize: 18, color: C.ink, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("Our insight: the teacher does not need a translator app; they need a bridge they can use in tomorrow's lesson. The teacher speaks Hindi; the child hears Santali, in Ol Chiki and in speech; and the teacher gets the Santali back in Devanagari to read aloud, so over time they learn it too. Teachers correct lines, corrections spread to other tablets, and anything the system is unsure about is flagged instead of played.\n\nLikely question: Why not just use Google Translate? Answer: it needs the internet, gives no lesson structure or worksheets, and has no way to mark doubtful output for a teacher.");
}

// ── F4 Architecture ────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "One pipeline, two devices, no internet after the first sync");
  // hub
  box(s, 0.5, 1.55, 4.3, 2.55, "Laptop hub (optional)", "Speech: IndicConformer 600M\nTranslation: IndicTrans2 320M, direct\nVoice: Piper (offline)\nMakes worksheets, flashcards, lesson plans\nSQLite: corrections, sessions", C.navy);
  box(s, 8.5, 1.55, 4.3, 2.55, "Android tablet (Android 9+)", "Speech: IndicConformer 120M int8\nTranslation: IndicTrans2 int8\nVoice: Piper via sherpa-onnx\nLesson-line matcher; PDFs from the pack\nRuns in airplane mode", C.teal);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.2, y: 1.85, w: 2.9, h: 0.7, fill: { color: C.saffron }, line: { color: C.saffron }, rectRadius: 0.1 });
  s.addText("Signed content + model packs", { x: 5.2, y: 1.85, w: 2.9, h: 0.7, fontFace: BF, fontSize: 12.5, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
  arrow(s, 4.85, 2.2, 5.15, 2.2, C.saffron); arrow(s, 8.12, 2.2, 8.45, 2.2, C.saffron);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.2, y: 3.05, w: 2.9, h: 0.7, fill: { color: C.green }, line: { color: C.green }, rectRadius: 0.1 });
  s.addText("Signed teacher corrections", { x: 5.2, y: 3.05, w: 2.9, h: 0.7, fontFace: BF, fontSize: 12.5, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
  arrow(s, 8.45, 3.4, 8.12, 3.4, C.green); arrow(s, 5.15, 3.4, 4.85, 3.4, C.green);
  // voice pipeline strip
  const steps = [["Mic", C.navy], ["Speech recognition", C.navy], ["Teacher fix → glossary → cache → model", C.blue], ["Guards: loop · round trip · script", C.red], ["Speech + reading guide", C.teal], ["Speaker", C.teal]];
  const w = [1.1, 1.9, 2.9, 2.55, 2.1, 1.25];
  let x = 0.5;
  steps.forEach(([t, c], i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.75, w: w[i], h: 0.95, fill: { color: c }, line: { color: c }, rectRadius: 0.1 });
    s.addText(t, { x, y: 4.75, w: w[i], h: 0.95, fontFace: BF, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle", margin: 2, isTextBox: true });
    if (i < steps.length - 1) arrow(s, x + w[i] + 0.02, 5.22, x + w[i] + 0.16, 5.22, C.mute);
    x += w[i] + 0.18;
  });
  s.addText("The same page (frontend.html) runs on both; the same 24-case REST contract is tested on both.", { x: 0.5, y: 6.05, w: 12.3, h: 0.45, fontFace: BF, fontSize: 14, color: C.mute, margin: 0, isTextBox: true });
  source(s, "README §4; contract/rest_contract.json; android/");
  s.addNotes("Two set-ups. The laptop hub runs the larger models and makes printable material; it is optional. The Android tablet runs smaller int8 models on the device. Content and models reach the tablet as signed packs; teacher corrections come back as signed files. The voice path is the same on both: speech recognition, then four translation layers where a teacher's correction or a verified sentence wins over the model, then three guards, then speech plus a Devanagari reading guide. One web page and one tested REST contract serve both devices.\n\nLikely question: Do you need the laptop? Answer: No for lessons, spoken lesson lines, typed translation and worksheets; yes for free-form speech and making new content packs.");
}

// ── F5 R1 ──────────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "R1: every lesson line in Santali text and speech, with a trust tier");
  bullets(s, ["Human first: teacher correction → verified sentence → cache → model",
              "Direct Hindi → Santali (IndicTrans2), Ol Chiki script",
              "Speech offline; Devanagari reading guide for the teacher",
              "Tier A human-written · B model · C flagged"], 0.5, 1.6, 5.2, 3.2, 16);
  tile(s, 0.5, 4.9, 2.5, 1.65, "32.2", "chrF++ Hindi → Santali, IN22-Conv (n = 1,503)", C.navy);
  tile(s, 3.2, 4.9, 2.5, 1.65, "119", "lesson lines checked: script, numbers, flags", C.teal);
  s.addImage({ path: A("keep_ui_guide_en.png"), x: 6.0, y: 1.6, w: 6.85, h: 3.1 });
  s.addText("Live page: Santali (Ol Chiki), reading guide in Devanagari, badge \"B · Model\".", { x: 6.0, y: 4.78, w: 6.85, h: 0.4, fontFace: BF, fontSize: 12, color: C.mute, italic: true, margin: 0, isTextBox: true });
  s.addText("Santali is spoken by a Hindi voice reading our transliteration: no offline Santali voice exists; two alternatives lost on a pre-set rule.",
    { x: 6.0, y: 5.35, w: 6.85, h: 0.9, fontFace: BF, fontSize: 13, color: C.ink, margin: 0, isTextBox: true });
  source(s, "eval/results/benchmarks.md; docs/fln_translation_sample.md; bench/results/voice_rule_finale.md");
  s.addNotes("R1. Every lesson line has Santali in Ol Chiki and offline speech. Translation goes human-first: a teacher's correction, then our verified sentences, then the cache, then the model, IndicTrans2, direct from Hindi with no English in between. On a public test set the model scores 32.2 chrF++ Hindi to Santali. Each reply shows where it came from as a tier: A human-written, B model, C flagged. Under the Santali, the teacher sees it in Devanagari to read aloud. We are open about the voice: a Hindi voice reads our transliteration, because no offline Santali voice exists; our own fine-tuned voice and Indic Parler-TTS both lost to it on a rule we fixed before testing.\n\nLikely question: Is 32 chrF++ good? Answer: It is the published model's level for Santali (the paper's average into Santali is 30.4 on the same set); we do not claim it is good enough alone, which is why the tiers and flags exist.");
}

// ── F6 R2 ──────────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "R2: spoken lesson lines on the tablet take 0.70 s (median), 1.27 s at p95");
  const labels = ["Realme tablet, lesson lines", "2 GB emulator, lesson lines", "Laptop hub, free speech ≤17 words"];
  s.addChart([
    { type: pres.charts.BAR, data: [
        { name: "p50", labels, values: [0.70, 0.50, 2.04] },
        { name: "p90", labels, values: [1.20, 0.82, 2.90] },
        { name: "p95", labels, values: [1.27, 0.93, 3.29] }],
      options: { barGrouping: "clustered", chartColors: [C.teal, C.blue, C.navy] } },
    { type: pres.charts.LINE, data: [{ name: "3 s limit", labels, values: [3, 3, 3] }],
      options: { chartColors: [C.red], lineSize: 2, lineDataSymbol: "none", showValue: false } }],
    { x: 0.5, y: 1.55, w: 7.6, h: 4.9, valAxisMaxVal: 3.5, valAxisMinVal: 0, valAxisMajorUnit: 0.5,
      valAxisTitle: "seconds", showValAxisTitle: true, valAxisTitleFontSize: 11,
      catAxisLabelFontSize: 11, valAxisLabelFontSize: 11, showLegend: true, legendPos: "b", legendFontSize: 11,
      showValue: true, dataLabelFontSize: 9, dataLabelFormatCode: "0.00",
      valGridLine: { color: "E5E1D8", size: 0.5 }, catGridLine: { style: "none" } });
  s.addText("Laptop hub, per stage (median)", { x: 8.5, y: 1.6, w: 4.3, h: 0.4, fontFace: HF, fontSize: 15, bold: true, color: C.navy, margin: 0, isTextBox: true });
  s.addChart(pres.charts.BAR, [{ name: "ms", labels: ["Recognition", "Translation", "Speech"], values: [861, 846, 360] }],
    { x: 8.4, y: 2.0, w: 4.45, h: 2.3, barDir: "bar", chartColors: [C.blue], showValue: true, dataLabelFontSize: 10,
      catAxisLabelFontSize: 11, valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false });
  s.addText("Honest tail: on the laptop, 8 of 96 free-speech sentences took over 3 s (p95 3.29 s). Free speech stays on the laptop; the tablet matches lesson lines and refuses anything else.",
    { x: 8.5, y: 4.5, w: 4.3, h: 1.9, fontFace: BF, fontSize: 13, color: C.ink, margin: 0, isTextBox: true });
  source(s, "bench/results/latency_percentiles.md (50 lines per device; 3 hub runs × 32 sentences, FLEURS)");
  s.addNotes("R2, the three-second limit. On the tablet, a spoken lesson line takes 0.70 seconds median and 1.27 seconds at the 95th percentile on the Realme Pad Mini, and 0.93 seconds at p95 on a 2 GB Android 9 emulator: measured over 50 lines each, in airplane mode, from the end of speech to the reply audio being ready. On the laptop hub, free Hindi speech of up to 17 words takes 2.04 seconds median, 2.90 at p90, but 3.29 at p95: eight of 96 sentences went over three seconds. We show that. Recognition and translation take about 0.85 seconds each, speech 0.36.\n\nLikely question: Is this with children's voices and classroom noise? Answer: No. Public adult speech and synthetic lesson lines; children's speech is the first thing we would measure in a pilot.");
}

// ── F7 R3 ──────────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "R3: each lesson prints a worksheet, flashcards and a teacher plan, tagged to NIPUN");
  const pics = [["ws-1.png", "Worksheet: count, match, fill, circle, trace; answer key"], ["fc-1.png", "Cut-out flashcards, mirrored backs, review mark"], ["lp-1.png", "Teacher's plan: Hindi, Santali, reading guide, answers"]];
  pics.forEach(([f, cap], i) => {
    const x = 0.5 + i * 4.2;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 3.9, h: 4.35, fill: { color: C.white }, line: { color: C.line, width: 1 } });
    s.addImage({ path: A(f), x: x + 0.45, y: 1.65, w: 3.0, h: 4.15, sizing: { type: "contain", w: 3.0, h: 4.15 } });
    s.addText(cap, { x, y: 5.97, w: 3.9, h: 0.5, fontFace: BF, fontSize: 12, color: C.mute, align: "center", margin: 0, isTextBox: true });
  });
  chip(s, 0.5, 6.55, 5.6, "NIPUN-G1-NUM-2: Perform simple addition and subtraction", C.green);
  chip(s, 6.3, 6.55, 3.3, "18 lessons · every Lakshya", C.navy);
  source(s, "docs/samples/; nipun/lakshya.py (Ministry text, 2021)");
  s.addNotes("R3. For every lesson the app produces a bilingual worksheet with five kinds of exercise and an answer key, cut-out flashcards with Santali on the front and Hindi on the back, and new this week, a teacher's lesson plan with the Santali in Ol Chiki and in Devanagari to read aloud, plus the accepted answers. Every lesson is tagged with the Ministry's NIPUN Lakshya, quoted word for word. Eighteen lessons from Balvatika to Grade 3 cover every Lakshya; teachers can add their own from Hindi text.\n\nLikely question: Who checked the mapping to NIPUN? Answer: we did, per lesson, marking full or partial fit; it has not been reviewed by a teacher yet, and we say so.");
}

// ── F8 R4 ──────────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "R4: airplane mode, 24 of 24 checks on a 2 GB Android 9 emulator and a real tablet");
  tile(s, 0.5, 1.6, 2.6, 1.45, "Android 9+", "minSdk 28", C.navy);
  tile(s, 3.3, 1.6, 2.6, 1.45, "72 MB", "release APK", C.navy);
  tile(s, 0.5, 3.25, 2.6, 1.45, "361 MB", "model pack, int8, signed", C.teal);
  tile(s, 3.3, 3.25, 2.6, 1.45, "38 MB", "content pack, signed", C.teal);
  s.addText("Tested: Realme Pad Mini (4 GB, Android 11) and a 2 GB Android 9 emulator. Not yet: a real 2 GB tablet, a 32-bit build.",
    { x: 0.5, y: 4.95, w: 5.4, h: 1.2, fontFace: BF, fontSize: 13.5, color: C.ink, margin: 0, isTextBox: true });
  s.addText("Peak memory (app + WebView), GB", { x: 6.4, y: 1.6, w: 6.4, h: 0.4, fontFace: HF, fontSize: 15, bold: true, color: C.navy, margin: 0, isTextBox: true });
  const ml = ["Lessons, packs (Realme)", "Spoken lesson lines (2 GB emu)", "Typing new sentences (2 GB emu)"];
  s.addChart([
    { type: pres.charts.BAR, data: [{ name: "peak", labels: ml, values: [0.30, 0.75, 1.30] }], options: { barDir: "bar", chartColors: [C.teal] } },
    { type: pres.charts.LINE, data: [{ name: "2 GB device RAM", labels: ml, values: [2, 2, 2] }], options: { chartColors: [C.red], lineSize: 2, lineDataSymbol: "none", showValue: false } }],
    { x: 6.3, y: 2.0, w: 6.5, h: 3.4, barDir: "bar", valAxisMaxVal: 2.2, valAxisMinVal: 0, valAxisMajorUnit: 0.5, showValue: true, dataLabelFormatCode: "0.00",
      dataLabelFontSize: 10, catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, showLegend: true, legendPos: "b", legendFontSize: 10,
      valGridLine: { color: "E5E1D8", size: 0.5 }, catGridLine: { style: "none" } });
  s.addText("Translation (1.3 GB) loads only when needed; the recogniser is released first.", { x: 6.4, y: 5.55, w: 6.4, h: 0.6, fontFace: BF, fontSize: 13, color: C.ink, margin: 0, isTextBox: true });
  source(s, "bench/results/realme-…-rc2_2026-09-28_m1.md; emulator-2gb-android9_2026-09-26_{m1,voice,nmt_memfix}.md");
  s.addNotes("R4. The app targets Android 9 and up. In airplane mode, all 24 contract checks pass on a real tablet, the Realme Pad Mini, and on a 2 GB Android 9 emulator. Models arrive once as a 361 MB signed int8 pack, content as a 38 MB signed pack; a changed pack is refused. Memory: lessons need about 0.3 GB, spoken lesson lines 0.75 GB, typing new sentences 1.3 GB, so translation is loaded only when needed. What we have not done: a real 2 GB tablet, and a 32-bit ARM build, which many cheap tablets need. Both are first on our list.\n\nLikely question: Will 1.3 GB fit on a 2 GB tablet with Android running? Answer: it ran on the 2 GB emulator; free-form speech did not (13.5 s, models swapped), so that stays on the laptop hub.");
}

// ── F9 Novelty stack ───────────────────────────────────────────────────────
{
  const s = base();
  title(s, "Eight things a classroom needs that a translator does not do");
  const items = [["Teacher corrections", "reused first; synced between tablets as signed files", "built", C.green],
                 ["Devanagari reading guide", "the teacher can read the Santali aloud", "new", C.saffron],
                 ["Trust tiers + 3 guards", "loop, round trip, script; C is never auto-played", "built", C.green],
                 ["Local-context lessons", "teachers import village examples; app translates", "sample", C.blue],
                 ["Lesson plans", "daily script with pronunciation guide and answers", "new", C.saffron],
                 ["Progress per NIPUN Lakshya", "by week; CSV and PDF; no names", "built", C.green],
                 ["Community voice corpus", "adults only, consent, stays on the laptop", "new", C.saffron],
                 ["Low-resource bootstrapping", "glossary-first; Mundari by LoRA (preview)", "built", C.green]];
  items.forEach(([h, b, st, c], i) => {
    const col = i % 4, row = Math.floor(i / 4), x = 0.5 + col * 3.1, y = 1.6 + row * 2.55;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.9, h: 2.3, fill: { color: C.paper }, line: { color: C.line }, rectRadius: 0.1 });
    chip(s, x + 0.2, y + 0.2, 1.0, st, c);
    s.addText(h, { x: x + 0.2, y: y + 0.65, w: 2.5, h: 0.7, fontFace: HF, fontSize: 15, bold: true, color: C.navy, valign: "top", margin: 0, isTextBox: true });
    s.addText(b, { x: x + 0.2, y: y + 1.35, w: 2.5, h: 0.85, fontFace: BF, fontSize: 12, color: C.ink, valign: "top", margin: 0, isTextBox: true });
  });
  source(s, "docs/feature_traceability.md");
  s.addNotes("Our novelty is not one model; it is what a classroom needs around the model. Teacher corrections are reused first and shared between tablets. The Devanagari reading guide lets the teacher say the Santali themselves. Tiers and three guards stop doubtful output from being played. Teachers can import lessons with village examples. A printed daily plan with pronunciation. Progress per NIPUN goal, with no names. A voice corpus where adults from the community record lines, with consent, to grow better voices. And a low-resource strategy: human-written sentences first, and new languages by light fine-tuning, as we did for Mundari.\n\nLikely question: Which of these are new this week? Answer: the reading guide, the tiers, the lesson plans and the voice corpus; each has tests in the repository.");
}

// ── F10 Trust ──────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "No native speaker yet: so nothing doubtful is played as if it were right");
  s.addImage({ path: A("ui_tierC_en.png"), x: 0.5, y: 1.6, w: 6.6, h: 2.99 });
  s.addText("A flagged line: tier C, a warning, no auto-play, the nearest verified sentence offered.", { x: 0.5, y: 4.68, w: 6.6, h: 0.45, fontFace: BF, fontSize: 12, italic: true, color: C.mute, margin: 0, isTextBox: true });
  bullets(s, ["Round-trip check: a caution, not a score",
              "Script guard: catches words in other scripts",
              "Every Santali line on a native-review list",
              "No cloud, no names; reading audio deleted"], 7.4, 1.6, 5.45, 3.0, 16);
  tile(s, 0.5, 5.3, 3.2, 1.55, "13 of 119", "lesson lines with Urdu / Meetei letters: now tier C", C.red);
  tile(s, 3.9, 5.3, 3.2, 1.55, "0.46 / 0.45", "round-trip flag precision / recall", C.navy);
  source(s, "eval/results/roundtrip_flag.md; docs/fln_translation_sample.md; docs/native_review.md");
  s.addNotes("We have no native Santali speaker on the team, and we treat that as a design constraint, not a secret. Human-written sentences come first. Model output is checked three ways: a loop guard, a round-trip check (a weak signal: precision 0.46, recall 0.45, so we call it a caution), and a new script guard. That guard came from auditing our own content pack: 13 of 119 lesson lines had words in Urdu or Meetei Mayek script, and six of them had passed the round-trip check. Flagged lines are tier C: a warning, no auto-play, and the nearest verified sentence. Children's data never leaves the device.\n\nLikely question: So how accurate is it on your lessons? Answer: not measured, because that needs native speakers; it is the first thing we ask a pilot for.");
}

// ── F11 Comparison ─────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "Where we win: the classroom job, not the translation model");
  const H = (t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 12 } });
  const Y = (t) => ({ text: t, options: { color: C.green, bold: true, fontSize: 12 } });
  const rows = [
    [H(""), H("Nijbhasha"), H("Translate wrapper"), H("Online-only app"), H("Text-only tool"), H("LLM chatbot")],
    ["Works with no internet", Y("Yes, tablet in airplane mode"), "No", "No", "Sometimes", "No"],
    ["Voice to voice", Y("Both ways; 0.70 s on tablet"), "Some apps", "Network-bound", "No", "Slow, online"],
    ["Santali in Ol Chiki", Y("Yes; Mundari preview"), "Santali only", "Varies", "Varies", "Unreliable"],
    ["NIPUN lessons + worksheets", Y("18 lessons, every Lakshya"), "No", "Rarely", "Sometimes", "Ad hoc"],
    ["Flags doubtful output", Y("Tiers + 3 guards"), "No", "Rarely", "Rarely", "No"],
    ["Child data stays local", Y("Yes"), "Cloud", "Cloud", "—", "Cloud"],
  ];
  s.addTable(rows, { x: 0.5, y: 1.6, w: 12.3, colW: [2.6, 2.7, 1.75, 1.75, 1.75, 1.75], fontFace: BF, fontSize: 12, color: C.ink,
    border: { type: "solid", pt: 0.5, color: C.line }, rowH: 0.62, valign: "middle" });
  s.addText("We do not claim better translation quality than any of these.", { x: 0.5, y: 6.25, w: 12.3, h: 0.4, fontFace: BF, fontSize: 13, italic: true, color: C.mute, margin: 0, isTextBox: true });
  source(s, "docs/audit_2026-09-28.md §5; Google Translate added Santali in 2024 (docs/sources.md)");
  s.addNotes("Against the likely alternatives. A translate wrapper or an online app stops without internet, which rules out many target schools, and sends children's voices to the cloud. Text-only tools do not speak. A chatbot needs the internet and can invent. Where we win is the classroom job: offline on the tablet, both directions by voice, Santali in its own script, NIPUN lessons and worksheets, and flags on doubtful output. We deliberately do not claim better raw translation than any of them.\n\nLikely question: Bhashini supports Santali; why not use it? Answer: it is an online service; we need the classroom to work without a network, and we need the lesson loop around the translation.");
}

// ── F12 Impact and scale ───────────────────────────────────────────────────
{
  const s = base();
  title(s, "Built for PALASH scale: 1,041 schools today, 5,000+ in the brief");
  tile(s, 0.5, 1.6, 2.9, 1.7, "1,041", "PALASH schools, 8 of 24 districts", C.navy);
  tile(s, 3.6, 1.6, 2.9, 1.7, "5,000+", "tribal-area schools in the brief", C.saffron);
  tile(s, 0.5, 3.5, 2.9, 1.7, "1 tablet", "per classroom; laptop optional", C.teal);
  tile(s, 3.6, 3.5, 2.9, 1.7, "₹0", "licence or per-use fees", C.green);
  s.addText("How it grows", { x: 7.0, y: 1.6, w: 5.8, h: 0.45, fontFace: HF, fontSize: 17, bold: true, color: C.navy, margin: 0, isTextBox: true });
  bullets(s, ["Santali now → Mundari (our LoRA, preview) → Ho once text exists",
              "Same pipeline for other Munda and low-resource languages",
              "Content = signed packs a district can build and send",
              "Proposed first step: a PALASH classroom pilot (not yet agreed)"], 7.0, 2.15, 5.8, 3.3, 15);
  s.addText("Assumptions: hardware and training costs are not estimated; school counts are PALASH's and the brief's, not our reach.",
    { x: 0.5, y: 5.6, w: 12.3, h: 0.6, fontFace: BF, fontSize: 12.5, italic: true, color: C.mute, margin: 0, isTextBox: true });
  source(s, "JEPC State Project Director to PTI (Jan 2026); SIH26042 brief; languages.json");
  s.addNotes("Scale. PALASH runs in 1,041 schools across 8 of Jharkhand's 24 districts, according to JEPC in January 2026; the brief names more than 5,000 tribal-area schools. A classroom needs one Android tablet; the laptop hub is optional. There are no licence or per-use fees. Languages grow along one path: Santali now, Mundari as a preview from our own LoRA adapters, Ho once there is text to train on. We propose a PALASH classroom pilot as the first step; nothing is agreed yet, and we do not estimate hardware cost here.\n\nLikely question: What does a tablet cost? Answer: we have not priced it; any Android 9+ tablet the school has, or a low-cost one, and we would size that with the department.");
}

// ── F13 Roadmap ────────────────────────────────────────────────────────────
{
  const s = base();
  title(s, "Roadmap: close the known gaps first, then grow with the community");
  const cols = [["30 days", C.navy, ["Native review of the 18 lessons", "32-bit ARM build; a real 2 GB tablet", "Demo video; APK release"]],
                ["90 days", C.teal, ["Proposed PALASH pilot, 5 classrooms", "Children's speech benchmark", "Mundari on the tablet"]],
                ["180 days", C.saffron, ["Ho content with native writers", "Voice from the community corpus", "Resumable pack download"]]];
  cols.forEach(([h, c, its], i) => {
    const x = 0.5 + i * 4.2;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.6, w: 3.9, h: 0.6, fill: { color: c }, line: { color: c }, rectRadius: 0.1 });
    s.addText(h, { x, y: 1.6, w: 3.9, h: 0.6, fontFace: HF, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.35, w: 3.9, h: 2.7, fill: { color: C.paper }, line: { color: C.line }, rectRadius: 0.1 });
    bullets(s, its, x + 0.25, 2.55, 3.45, 2.4, 15);
  });
  s.addText("Sustained by: open models and MIT code; lessons as editable JSON; corrections and the voice corpus grow with use.",
    { x: 0.5, y: 5.4, w: 12.3, h: 0.7, fontFace: BF, fontSize: 15, color: C.ink, margin: 0, isTextBox: true });
  source(s, "docs/audit_2026-09-28.md §7 (checklist)");
  s.addNotes("Our roadmap starts with the gaps we have told you about. In 30 days: native review of the lessons, a 32-bit build and a real 2 GB tablet, and the demo video. In 90 days, if a pilot is agreed: five classrooms, a children's speech benchmark, and Mundari on the tablet. In 180 days: Ho content written with native speakers, a better Santali voice from the community corpus, and resumable downloads. It sustains itself because the models and code are open, lessons are editable files, and every correction and recording improves it.\n\nLikely question: Who pays for maintenance? Answer: there are no licence fees; the ongoing work is content and review, which fits the existing PALASH teacher-training structure; that is a proposal, not an agreement.");
}

// ── F14 Demo and close ─────────────────────────────────────────────────────
{
  const s = base({ dark: true });
  s.addText("See it run: airplane mode, the timer on screen", { x: 0.6, y: 0.5, w: 12, h: 0.8, fontFace: HF, fontSize: 30, bold: true, color: C.white, margin: 0, isTextBox: true });
  const steps = ["Tablet in airplane mode: lessons load", "Teacher says a lesson line → Santali in 0.7 s", "Reading guide under the Santali", "A doubtful line: tier C, not played", "Worksheet, flashcards, lesson plan print"];
  steps.forEach((t, i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: 1.65 + i * 0.85, w: 0.55, h: 0.55, fill: { color: C.saffron }, line: { color: C.saffron } });
    s.addText(String(i + 1), { x: 0.6, y: 1.65 + i * 0.85, w: 0.55, h: 0.55, fontFace: HF, fontSize: 16, bold: true, color: C.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(t, { x: 1.35, y: 1.65 + i * 0.85, w: 6.8, h: 0.55, fontFace: BF, fontSize: 17, color: C.white, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addImage({ path: A("qr_repo.png"), x: 9.4, y: 1.55, w: 2.6, h: 2.6 });
  s.addText("github.com/barath0512s-rgb/nijbhasha", { x: 8.4, y: 4.25, w: 4.6, h: 0.4, fontFace: BF, fontSize: 13, color: "C9D3DE", align: "center", margin: 0, isTextBox: true, hyperlink: { url: "https://github.com/barath0512s-rgb/nijbhasha" } });
  s.addText("Demo video: [add link after recording]", { x: 8.4, y: 4.7, w: 4.6, h: 0.4, fontFace: BF, fontSize: 13, color: "F2C27B", align: "center", margin: 0, isTextBox: true });
  s.addText("Our ask: a native Santali reviewer and one PALASH classroom.", { x: 0.6, y: 6.2, w: 12, h: 0.6, fontFace: HF, fontSize: 22, bold: true, color: "F2C27B", margin: 0, isTextBox: true });
  s.addNotes("Here is what the live demo shows, in order: the tablet in airplane mode loading lessons; the teacher speaking a lesson line and the child hearing Santali in about 0.7 seconds, with the timer on screen; the Devanagari reading guide; a doubtful line flagged as tier C and not played; and the worksheet, flashcards and lesson plan. The code, tests and every number are in the repository behind the QR code. Our ask is simple: a native Santali reviewer, and one PALASH classroom to measure it with real children. Thank you.\n\nLikely question: Can we try it now? Answer: yes, the tablet is in airplane mode; say any lesson line.");
}

// ── Appendix ───────────────────────────────────────────────────────────────
function appendix(t, sub) { const s = base(); title(s, t, sub); return s; }
const tbl = (s, rows, colW, y, fs) => s.addTable(rows.map((r, i) => r.map(c => i === 0 ? { text: c, options: { bold: true, color: C.white, fill: { color: C.navy } } } : c)),
  { x: 0.5, y: y || 1.6, w: 12.3, colW, fontFace: BF, fontSize: fs || 11, color: C.ink, border: { type: "solid", pt: 0.5, color: C.line }, valign: "middle", rowH: 0.46 });

{ const s = appendix("A1 · Data sources and licences");
  tbl(s, [["What", "Used for", "Licence"],
    ["AI4Bharat IndicConformer 600M / 120M", "Speech recognition (hub / tablet)", "MIT"],
    ["AI4Bharat IndicTrans2 indic-indic 320M", "Translation, hub fp32 and tablet int8", "MIT"],
    ["Piper hi_IN-pratham-medium", "Speech (Hindi, and Santali via transliteration)", "CC BY-NC-SA 4.0"],
    ["sherpa-onnx 1.13.8 (with espeak-ng)", "On-device speech", "Apache-2.0 (espeak-ng GPL-3.0: APK under GPL-3.0)"],
    ["Meta MMS voices mms-tts-unr / -hoc", "Mundari and Ho voices (preview)", "CC BY-NC 4.0"],
    ["MMLoSo 2025 Hindi-Mundari data", "Mundari LoRA (18,978 training pairs)", "CC BY-SA 4.0"],
    ["IN22-Gen, IN22-Conv; FLORES-200", "Evaluation only (leakage-guarded)", "CC BY 4.0; CC BY-SA 4.0"],
    ["FLEURS (Hindi), IndicVoices (Santali valid.)", "Speech benchmarks, adult", "CC BY 4.0"],
    ["OpenMoji; Noto fonts", "Pictures; Devanagari and Ol Chiki type", "CC BY-SA 4.0; OFL"],
    ["Our code", "Everything else", "MIT"]], [4.3, 4.6, 3.4], 1.6, 14);
  source(s, "THIRD_PARTY_LICENSES.md; docs/sources.md; languages.json");
  s.addNotes("All models and data are public, with licences listed in THIRD_PARTY_LICENSES.md. Test sets are used only for evaluation; a leakage guard stops any training script from seeing them. The default voice is non-commercial, which suits a free government programme; the APK is under GPL-3.0 because of espeak-ng.");
}
{ const s = appendix("A2 · Benchmarks (all offline)");
  tbl(s, [["Measure", "Setting", "Result"],
    ["Voice to voice, lesson lines", "Realme Pad Mini, n = 50", "p50 0.70 · p90 1.20 · p95 1.27 s"],
    ["Voice to voice, lesson lines", "2 GB Android 9 emulator, n = 50", "p50 0.50 · p90 0.82 · p95 0.93 s"],
    ["Hindi → Santali, free speech ≤ 17 words", "Laptop hub, 3 runs × 32 (FLEURS)", "p50 2.04 · p90 2.90 · p95 3.29 s; 8 of 96 > 3 s"],
    ["Santali → Hindi, upload to reply", "Laptop hub, 80 answers per run", "p90 2.52–2.60 s"],
    ["Typed new sentence on the tablet", "Realme / 2 GB emulator", "p50 1.50 s / 0.60 s"],
    ["Translation quality hi → sat", "IN22-Gen / IN22-Conv / FLORES-200", "chrF++ 31.3 / 32.2 / 27.4"],
    ["Mundari preview (our LoRA)", "Held-out 5 % of MMLoSo, n = 1,021", "chrF++ hi→unr 30.92 · unr→hi 35.97"],
    ["Speech recognition, WER (normalised)", "Hub 600M: Hindi / Santali", "12.5 % / 31.0 %"],
    ["Peak memory", "Lessons / lesson-line voice / typing", "0.30 / 0.75 / 1.30 GB"]], [4.0, 4.1, 4.2], 1.6, 14);
  source(s, "bench/results/latency_percentiles.md; eval/results/benchmarks.md; README §6; STATUS.md");
  s.addNotes("The full numbers, each from a results file. Adult public speech and synthetic lesson lines only; children's speech is not measured.");
}
{ const s = appendix("A3 · How we keep the numbers honest");
  bullets(s, ["332 automated tests pass without models; 38 more need the models; CI on every push",
              "A test fails if the README quotes a number with no evidence file",
              "Model choices by rules written before the results (voice, decoding, int8)",
              "Leakage guard: no benchmark sentence can reach training",
              "Same 24-case REST contract tested on the hub and the tablet",
              "Every figure printed by a script: tools/deck_numbers.py, tools/latency_percentiles.py"], 0.5, 1.7, 12.3, 4.8, 20);
  source(s, "tests/; .github/workflows/tests.yml; tests/test_claims.py; docs/voice_rule_finale.md; eval/leakage.py");
  s.addNotes("If a judge doubts a number, it can be re-derived from a script in the repository. We fixed decision rules before running the comparisons, so we could not pick the winner after seeing the results.");
}
{ const s = appendix("A4 · Security and privacy");
  bullets(s, ["No cloud at run time; network sockets blocked in the offline test",
              "Packs signed (Ed25519) and verified on the tablet; a changed pack is refused",
              "Progress reports: no names, no audio",
              "Reading check: consent box; the recording is deleted after scoring",
              "Voice corpus: adults only, consent, no names; export only from the laptop, only with consent to share",
              "Hub over HTTPS with its own local certificate for tablet microphones"], 0.5, 1.7, 12.3, 4.8, 20);
  source(s, "tests/test_offline.py; core/Pack.kt; progress.py; orf.py; corpus.py; tools/make_cert.py");
  s.addNotes("Children's data never leaves the classroom device. The only recordings we keep are from consenting adults in the voice corpus, and they stay on the laptop.");
}
{ const s = appendix("A5 · Limitations we disclose");
  bullets(s, ["No native-speaker review yet of Santali, Mundari or Ho output, or of the voice",
              "Santali voice is a Hindi voice reading a transliteration",
              "No real 2 GB tablet; no 32-bit ARM build",
              "Free-form speech on the laptop only; p95 3.29 s there",
              "Children's speech and classroom noise not measured",
              "Ho: voice only; Mundari: preview on the laptop",
              "NIPUN mapping not reviewed by a teacher"], 0.5, 1.7, 12.3, 5.0, 20);
  source(s, "docs/audit_2026-09-28.md; README §13");
  s.addNotes("These are the gaps a judge would find; we list them first.");
}
{ const s = appendix("A6 · Real lesson lines, as the app shows them", "Hub output from the content pack (26 Sep); not reviewed by a native speaker.");
  s.addImage({ path: A("fln_table.png"), x: 0.5, y: 1.85, w: 12.3, h: 4.23 });
  source(s, "docs/fln_translation_sample.md");
  s.addNotes("Seven real lines. The last row is one the new script guard catches: an Urdu word inside the Santali, now tier C.");
}
{ const s = appendix("A7 · Questions we expect");
  tbl(s, [["Question", "Short answer"],
    ["Is the Santali correct?", "Not measured without native speakers; human-written first, doubtful lines flagged, review list ready"],
    ["Does it run on 2 GB?", "2 GB Android 9 emulator yes; real 2 GB tablet not yet; typing needs 1.3 GB, loaded on demand"],
    ["Under 3 s?", "Tablet lesson lines p95 1.27 s; laptop free speech p95 3.29 s (8 of 96 over)"],
    ["Children's voices?", "Not measured; first pilot benchmark"],
    ["Ho and Mundari?", "Mundari translation preview (our LoRA); Ho voice only, no licensed text"],
    ["Why not an LLM?", "Needs internet or far more memory; can invent"],
    ["Cost?", "No licence or per-use fees; hardware not estimated"],
    ["Privacy?", "No cloud; no names; reading audio deleted; corpus adults-only with consent"]], [3.2, 9.1], 1.6, 15);
  source(s, "docs/winning_narrative.md (15 questions in full)");
  s.addNotes("The full set of fifteen questions and answers is in docs/winning_narrative.md.");
}

pres.writeFile({ fileName: path.join(__dirname, "..", "final_deck.pptx") }).then(f => console.log("wrote", f, n, "slides"));
