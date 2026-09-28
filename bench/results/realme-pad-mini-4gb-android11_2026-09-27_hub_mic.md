# Hub-mode microphone on the Realme Pad Mini (tablet browser via laptop hub, Wi-Fi)

- Date: 2026-09-27. Tablet: Realme Pad Mini (RMP2106), 4 GB, Android 11, Chrome, joined to the laptop's Mobile hotspot (192.168.137.0/24). Hub: this laptop, `app.py --https` on port 5443, CA certificate installed on the tablet.
- Speaker: one person from the team, saying the lesson line *दो आम और तीन आम मिलाओ। कुल कितने हुए? उंगलियों पर गिनो।* each time. One speaker, one sentence: not a benchmark of accuracy.
- Client time: measured by the tablet's browser from the end of speech (mic button released) to the reply audio starting to play; it includes the upload and download over Wi-Fi and playback start, which the laptop benchmarks do not. Server time: the hub's own time for recognition + translation + speech. Source: the hub's `latency_log` table (`tools/hub_mic_check.py`).
- Two runs of 3. The **first run** started about 5.7 min after the hub started, while its background pre-caching of 173 lesson sentences may still have been running (its completion line was not in the log, so this cannot be ruled out): reported, but not the headline figure. The **clean run** followed with the hub confirmed idle (its CPU time unchanged over 5 s).

| Run | Time | Path | ASR s | Translation s | Speech s | Server s | Network s | **Client s** |
|---|---|---|---|---|---|---|---|---|
| first (possible background load) | 15:08:12 | not matched: model translation, speech synthesised | 1.18 | 0.60 | 2.52 | 4.29 | 0.43 | **4.90** |
| first (possible background load) | 15:08:35 | matched to the lesson line; cached audio | 0.46 | 0.00 | 0.01 | 0.47 | 0.09 | **0.83** |
| first (possible background load) | 15:08:49 | matched to the lesson line; cached audio | 0.37 | 0.00 | 0.00 | 0.37 | 0.12 | **0.65** |
| clean (hub idle) | 15:14:54 | matched to the lesson line; cached audio | 1.31 | 0.00 | 0.00 | 1.31 | 0.14 | **1.71** |
| clean (hub idle) | 15:15:14 | matched to the lesson line; cached audio | 0.67 | 0.00 | 0.00 | 0.67 | 0.10 | **0.97** |
| clean (hub idle) | 15:15:30 | matched to the lesson line; cached audio | 0.57 | 0.00 | 0.00 | 0.58 | 0.13 | **0.87** |

- Clean run: 3 of 3 worked end to end (microphone, upload, the Santali reply audio started playing); client 1.71, 0.97, 0.87 s; all 3 matched the lesson line.
- First run: 3 of 3 worked; client 4.90, 0.83, 0.65 s. The first attempt was not matched to the lesson line (the hub does not store what it heard, so why is unknown) and went through the model with fresh speech synthesis: 4.90 s, over the 3 s target.
- Not measured: children's voices, a classroom (noise, several tablets), sentences outside the lessons from the tablet.
