---
name: audio-transcript-pipeline
description: Convert audio recordings (earnings calls, phone conferences, interviews) into polished, publication-ready transcripts with timestamps, speaker labels, and PDF export. Covers the full pipeline: Whisper speech-to-text transcription (MPS-accelerated), web-search proofreading of proper nouns/drug codes/medical terms, multi-pass cleanup, semantic paragraph reformatting, final real-transcript formatting (executive summary + topic chapters + speaker labels + appendices), and PDF generation. Use this skill when the user provides an audio file (m4a/mp3/wav) of a meeting/call/interview and wants a readable, proofread transcript or PDF; or when the user says "转写"/"转录"/"语音转文字"/"transcribe"/"会议实录"/"业绩会文字稿".
agent_created: true
---

# Audio Transcript Pipeline

## Overview

Convert an audio recording into a publication-ready, proofread transcript (Markdown + PDF). The pipeline runs six stages: Whisper transcription → web-search proofreading → multi-pass cleanup → semantic paragraph reformatting → final real-transcript formatting → PDF export. Designed for Chinese earnings calls / investor calls / interviews but adaptable to any language.

## Prerequisites (environment check)

Before starting, verify the environment once:

1. **Whisper + ffmpeg**: Whisper Python package pre-installed in the isolated venv `/Users/bittom/.workbuddy/binaries/python/envs/default/`; ffmpeg at `/opt/homebrew/bin/ffmpeg`. If Whisper is missing, install: `/Users/bittom/.workbuddy/binaries/python/envs/default/bin/pip install openai-whisper`.
2. **Model cache**: Whisper models cached at `~/.cache/whisper/`. For Chinese, `medium.pt` (~1.5GB) is the recommended balance of accuracy and speed. If not cached, the first run downloads it.
3. **MPS acceleration**: Apple Silicon GPU. Verify `torch.backends.mps.is_available()` returns True.
4. **PDF generation**: md-to-pdf skill available (weasyprint + Noto Sans CJK SC, system Python `/opt/homebrew/bin/python3`).

Run environment check:
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<AUDIO_PATH>"
ls ~/.cache/whisper/
/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 -c "import whisper, torch; print('whisper ok, mps:', torch.backends.mps.is_available())"
```

## Workflow (6 stages)

### Stage 1 — Whisper Transcription

Run `scripts/whisper_transcribe.py` to transcribe the audio into a timestamped Markdown file.

- **Model**: `medium` (cached); **Device**: `mps`; **Language**: force the target language (e.g. `zh`) for better accuracy and speed.
- **Hallucination tuning for Chinese**: `compression_ratio_threshold=2.4` (reduce repetition/fabrication), `no_speech_threshold=0.6` (avoid false truncation of long segments), `logprob_threshold=-0.8`.
- **Output**: a Markdown file with two sections — "完整文字" (full continuous text) and "带时间戳分段" (timestamped segments, `[MM:SS]` per line).
- **Runtime**: ~real-time to 2x on Apple Silicon MPS for `medium` model; a 46-min audio takes ~37 min. Run in background (`run_in_background=true`) and wait for the task-notification — do NOT poll in a loop.

```bash
# Edit AUDIO_PATH / OUTPUT_MD / LANGUAGE at top of script, then:
/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 scripts/whisper_transcribe.py
```

> If thermal throttling slows the middle section, speed usually recovers later — let it finish.

### Stage 2 — Web-Search Proofreading

Read the full transcript, identify errors in proper nouns / drug codes / company names / medical terms / numbers, then web-search to verify each.

- **Sources to search (priority)**: company official site / IR press releases, partner/acquirer announcements (e.g. AbbVie, Daiichi Sankyo, Merck), clinical-trial databases (ClinicalTrials.gov), conference data (ASCO/ESMO/WCLC/AACR).
- **Common Whisper error patterns for Chinese**: English drug codes (e.g. "Zosie"→zoci, "Furthing Class"→First-in-Class), institution names ("安静"→安进/Amgen, "韩国化疗"→含铂化疗), medical terms ("客观缓决率"→客观缓解率/ORR, "特音性皮炎"→特应性皮炎), homophone Chinese ("故事的底部"→估值的底部).
- **Mark uncertain inferences** with `[?]` (e.g. inferred speaker name, study code) — do not assert unverified guesses.
- Build a **proofreading mapping table** grouped by category (drugs/pipelines, companies/people, medical terms, Chinese homophones).

See `references/workflow.md` §2 for the full search strategy and worked examples.

### Stage 3 — Multi-Pass Cleanup

Apply the mapping table as batch string replacements, then iteratively scan for residuals and patch.

- **Pass 1 — bulk replace** (`scripts/proofread_replace.py` template): ordered rules, **longer/more-specific strings first** to avoid partial-replacement conflicts. Only replace in the body (after a marker), never in the mapping-table display itself.
- **Pass 2 — NFKC normalization**: some Chinese characters have compatibility variants that block exact matching (e.g. "屈" variants). Apply `unicodedata.normalize("NFKC", text)` before replacing.
- **Pass 3+ — residual scan**: use Grep to scan the body for known error patterns; each found residual gets a targeted patch. Typical rounds: 3-5.
- **Verify**: after each pass, Grep a verification word list against the body — confirm all cleared before stopping.

```bash
/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 scripts/proofread_replace.py
```

See `references/workflow.md` §3 for ordering rules, NFKC pitfalls, and a residual-scan word list.

### Stage 4 — Semantic Paragraph Reformatting

Convert the subtitle-style one-line-per-timestamp file into readable semantic paragraphs.

- Run `scripts/reformat_paragraphs.py`: parse all `[MM:SS]` segments, split into paragraphs at **speaker-switch / Q&A-boundary triggers** (analyst self-introductions like "我是中金/中信", handoff phrases like "下面我把时间交给", Q&A markers like "好的，这个问题我来回答", closings like "总结来说"), cap each paragraph at ~9 sentences.
- Each paragraph keeps the **start timestamp** at its head.
- Group paragraphs into chapters by time range.

### Stage 5 — Final Real-Transcript Formatting

Produce the publication-ready version following the standard real-transcript format (see `references/format_template.md`):

1. **Header**: title + topic + duration + attendees + proofreading note (preserve spoken style, `[?]` for uncertain).
2. **Executive summary** (手写, the key value-add): 4-6 themed sections distilling core viewpoints + a product/asset quick-reference table.
3. **Body**: topic-based chapter titles (e.g. "三、何珊：zoci 管线详述") + **speaker labels** per paragraph (`**杜莹（CEO）：**`) + `[MM:SS]` timestamp at paragraph head. Derive speaker labels from a time-range→speaker mapping (define per recording based on content).
4. **Appendix I**: proofreading mapping table (the categories from Stage 2).
5. **Appendix II**: web-verification record (numbered list of verified facts with sources).

The executive summary and appendices are hand-written; the body is generated by mapping speaker labels onto Stage-4 paragraphs via a time-range table.

### Stage 6 — PDF Export

Generate PDF from the final Markdown using the **md-to-pdf** skill (weasyprint + Noto Sans CJK SC, system Python).

```bash
/opt/homebrew/bin/python3 /Users/bittom/.workbuddy/skills/md-to-pdf/md-to-pdf/scripts/md_to_pdf.py "<input.md>" "<output.pdf>"
```

- A4, 2cm margins, blue table headers, page breaks before H1, Noto Sans CJK SC embedded (WeChat-safe).
- Per user preference: only generate PDF when explicitly requested ("生成 PDF").

## Cleanup convention

After the final version is approved, the user may ask to keep only the final file. Move intermediate files (raw transcript, proofread subtitle version, paragraph version) to `~/.Trash/` via `mv` (recoverable), keeping only the final `.md` and `.pdf`.

## Resources

### scripts/
- `whisper_transcribe.py` — Whisper transcription (medium + MPS + language-forced + hallucination tuning). Edit AUDIO_PATH/OUTPUT_MD/LANGUAGE constants at top, then run.
- `proofread_replace.py` — batch proofreading replacement template (ordered rules, long-first, NFKC, body-only, residual verify).
- `reformat_paragraphs.py` — subtitle→semantic-paragraph reformatting (speaker-switch/Q&A triggers, chapter grouping).

### references/
- `workflow.md` — detailed 6-stage workflow with commands, parameters, pitfalls, and worked examples (load when executing a specific stage in depth).
- `format_template.md` — final real-transcript format template (header / executive summary / chapter / speaker label / appendix structure).

## Adaptation notes

- **Language**: set `LANGUAGE` in the transcribe script; for English audio use `language="en"` and skip Chinese-specific hallucination tuning.
- **Speaker mapping**: must be rebuilt per recording — read the transcript, identify speaker switches, define a time-range→speaker list. There is no generic auto-detection.
- **Proofreading scope**: domain-specific. For pharma earnings calls, verify drug codes/pipelines/targets; for tech calls, verify product names/acquisitions; for interviews, verify person/institution names. Always web-search rather than guess.
- **Model choice**: `medium` for Chinese balance; `large-v3` for best accuracy (slower, ~3GB); `small` for fast drafts.
