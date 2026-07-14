---
name: work-report-infographic
agent_created: true
description: Convert a daily or weekly work report/summary into a clean PNG infographic suitable for sharing with leadership (e.g., on WeChat). Trigger when the user asks for a work summary in image, picture, infographic, or poster form.
---

# Work Report Infographic

## Overview

This skill generates a polished, one-page PNG infographic from a daily or weekly work report. It is designed for executive audiences (e.g., sharing a Friday summary with a chairman on WeChat) and uses Pillow (PIL) with system CJK fonts to guarantee crisp text rendering without relying on emoji fallbacks.

## When to Use

Use this skill when the user asks for phrases such as:

- "把本周工作总结生成图片"
- "今日工作汇报做成图片"
- "工作记录可视化 / 信息图 / 海报"
- "把汇报变成图片发微信"

If no work report markdown file exists, generate the report text first, then offer to convert it to an image.

## Workflow

### 1. Gather Source Material

- Read the requested markdown work report(s) from the project workspace (e.g., `今日工作汇报_YYYY-MM-DD.md`, `本周工作汇报_YYYY-MM-DD至YYYY-MM-DD.md`).
- If the user only says "weekly report image" without an existing file, read the week's daily memory logs (`/Users/bittom/Desktop/GT/.workbuddy/memory/YYYY-MM-DD.md`) and produce the markdown report first.

### 2. Extract Executive Highlights

Distill the report into visual building blocks:

- **Header**: report title, date range, reporter, recipient.
- **Top KPIs**: 3–4 quantified highlights (e.g., "11 platforms contacted", "3 research reports delivered").
- **Workstreams**: 2–4 themed sections (e.g., A. RWA platform outreach, B. GTUSD compliance, C. Governance).
- **Milestones/Timeline**: optional 5-day or key-event timeline.
- **Leadership asks**: 1–3 support items needing approval.
- **Footer**: company name + "internal report" marker.

### 3. Design Rules

- **Canvas**: width 1080 px (WeChat-friendly); height calculated from content.
- **Colors**: light gray background (#EEF1F6), white cards, navy header gradient (#0F2A52 → #1A4A8E), gold accent (#C9A24B), muted gray text.
- **Fonts**: use macOS system CJK fonts — `/System/Library/Fonts/Hiragino Sans GB.ttc` for body, `/System/Library/Fonts/STHeiti Medium.ttc` for headings. Fall back to `ImageFont.load_default()` if unavailable.
- **No emojis**: emoji fonts are unreliable in PIL. Use colored circles, rectangles, or text labels instead (e.g., draw a colored dot before region names, write "完成" instead of ✅).
- **Region accent bars**: draw thin vertical colored bars on the left edge of region/KPI cards (SG blue, HK purple, JP pink, KR green, abandoned gray).
- **Text wrapping**: implement character-by-character wrap for CJK so long lines break naturally within card width.

### 4. Build and Run the Script

Use or adapt the bundled script:

```bash
/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python \
  /Users/bittom/.workbuddy/skills/work-report-infographic/scripts/render_report_image.py \
  --input <path/to/report.md> --output <path/to/output.png>
```

The script is intentionally a template: for each new report, copy it into the workspace, edit the content data, run it, and delete or archive the temporary copy. The skill's canonical copy stays in the skill directory.

### 5. Verify and Deliver

- Read the generated PNG visually to confirm no text overflow, no broken glyphs, and no emoji fallback boxes.
- Present the PNG to the user via `present_files`.
- Save a note in the project memory that the image version was created.

## Reference Implementation

The canonical example used to generate reports for Gemtrust (2026-07-10) is stored at:

- `scripts/render_report_image.py` — generalized PIL renderer with header/KPI/section/timeline/ask helpers.

When adapting, keep these proven constants:

- `W = 1080`
- `BG = (238, 241, 246)`
- `CARD = (255, 255, 255)`
- Header gradient: `lerp((15,42,82), (26,74,142))`
- Accent: `GOLD = (201, 162, 75)`

## Notes

- Pillow's `rounded_rectangle` requires Pillow ≥ 12; the managed Python env already has Pillow 12.2.
- For non-macOS environments, adjust font paths or install a CJK font and update the skill script.
- Keep content concise; an infographic is a summary, not a full report.
