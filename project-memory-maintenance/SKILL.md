---
name: project-memory-maintenance
description: "Maintain and update a project's long-term MEMORY.md background file from daily work logs. Use when the user asks to review, update, organize, or regenerate the project MEMORY.md, or when comparing an old version against the current one. Provides a structured workflow for reading logs efficiently, verifying accuracy, tiering content by durability, separating signal from noise, managing length, and producing a curated background file. Trigger phrases: update MEMORY.md, 整理项目记忆, 审查 MEMORY, regenerate project memory, 更新项目背景文件."
agent_created: true
---

# Project Memory Maintenance

## Overview

Maintain a project's `MEMORY.md` — the curated long-term background file at
`{workspace}/.workbuddy/memory/MEMORY.md` — by reconciling it against daily work logs
(`{workspace}/.workbuddy/memory/YYYY-MM-DD.md`). The goal: any future session opens
MEMORY.md and immediately understands the project's red lines, structural facts, and
current operational state without re-reading every daily log.

### Three Memory Tiers (know where to write)

| Tier | File | Scope | When to write |
|------|------|-------|---------------|
| Cloud | Auto-injected profile | All projects, read-only | Never (server-managed) |
| User-level | `~/.workbuddy/MEMORY.md` | All projects, read/write | Cross-project habits, personal preferences |
| Workspace | `{workspace}/.workbuddy/memory/MEMORY.md` | Current project only | Project-specific decisions, conventions, state |

This skill addresses **workspace-level** MEMORY.md. If a fact applies across all projects
(e.g., "user prefers tables over prose"), write it to user-level instead.

### Language

MEMORY.md should follow the project's primary working language. If the user
communicates in Chinese, MEMORY.md content should be in Chinese (key terms may stay in
English). If in English, write in English. Match the tone of the project's existing
documents and daily logs.

## When to Use

- User asks to "update / review / organize / regenerate MEMORY.md" or "整理项目记忆".
- Significant work has accumulated in daily logs since the last update.
- User provides an older MEMORY.md version and asks what is missing or worth re-adding.
- Periodic maintenance (after 5-10 new daily logs, or when new log files collectively
  exceed ~50KB since last update).

### Interaction Modes

Distinguish two modes based on user intent:

- **Analysis mode** ("what should be updated?" / "有哪些值得更新?" / "看看有什么不足"):
  Read logs, compare against current MEMORY.md, present a structured findings report
  (what is stale, what is missing, what is redundant). Do NOT modify files. Wait for
  user confirmation before executing.

- **Execution mode** ("update it now" / "现在就补进去" / "更新 MEMORY"):
  Execute the full workflow below and produce the updated file directly.

Default to analysis mode when the user asks a question; switch to execution mode when
the user gives a command.

## File Roles

| File | Role | Granularity |
|------|------|-------------|
| `MEMORY.md` | Curated long-term background index | Decisions, red lines, structural facts, current state |
| `YYYY-MM-DD.md` | Daily work log (append-only) | Execution details, step-by-step, transient status |

MEMORY.md is an **index + essentials**, not a log dump. For execution details, consult
the daily log. For full deliverables, follow reference paths in MEMORY.md.

## Pre-Update: Efficient Log Reading

Reading 20+ daily logs one-by-one is token-expensive. Use this strategy:

1. **List first**: Glob `{workspace}/.workbuddy/memory/*.md` to get all log files
   sorted by modification time. Identify which are new since the last MEMORY.md update
   (check the update date in the MEMORY.md header).

2. **Batch by count**:
   - **Few (1-5 new logs)**: Read each in full with the Read tool.
   - **Moderate (6-15 new logs)**: Read each in full, but in parallel (multiple Read
     calls in a single message) to reduce round-trips.
   - **Many (16+ new logs)**: Dispatch an Explore subagent to read all new logs and
     return a structured summary (key decisions, status changes, new conventions, red
     lines added). Then read the full text only for logs flagged as containing P0/P1
     content.

3. **Read strategy**: Read each log in full — do not skip based on headers alone, as
   important decisions may be buried in execution details. Focus extraction on:
   decisions, conventions, red lines, status changes, structural facts.

## Two Update Workflows

### Workflow A — Full Regeneration

Use when updating MEMORY.md from scratch, doing a periodic full review, or when no
previous MEMORY.md exists. Execute the 7-step process below.

### Workflow B — Old Version Comparison

Use when the user provides a previous MEMORY.md version and asks what is missing.
Workflow B is a **pre-step** to Workflow A: it produces a gap analysis that the user
confirms, then the approved items are integrated via the 7-step process.

1. **Diff**: Read both the old and current MEMORY.md. Identify content present in the
   old version but absent from the current one.
2. **Categorize each diff item** into three buckets:
   - **Worth re-adding**: P1 structural content still valid (research conclusions,
     investor lists, operational models not yet superseded).
   - **Marginal**: Nice-to-have but may bloat (long-term vision notes, internal team
     dynamics, time-sensitive action items that may have expired).
   - **Correctly removed**: Stale, redundant, or superseded (outdated contact info,
     facts later corrected, content already covered elsewhere).
3. **Present findings**: Output a structured table (item / value assessment / source
   log / recommended action). Do NOT modify files until user confirms.
4. **Execute**: After user confirmation, integrate approved items into MEMORY.md via
   the 7-step process (Workflow A).

## 7-Step Generation Process

### Step 1 — Read Logs

Read daily logs from the **most recent backward** to the last MEMORY.md update point,
using the efficient reading strategy in "Pre-Update: Efficient Log Reading" above. For
structural facts that seem uncertain, trace back to earlier logs. Do not skip logs —
each may contain a decision that should persist.

### Step 2 — Verify Accuracy

Check every claim in the current MEMORY.md against the logs. Flag and fix:
- **Stale items**: status that has changed (e.g., "pending contact" now "replied").
- **Contradictions**: when logs disagree, trust the **latest and most detailed** log.
- **Errors**: facts that were later corrected in a subsequent log.

Example (business): if MEMORY says "Partner X — awaiting reply" but a later log records
"Partner X phone disconnected, downgraded to case-study evidence," update immediately.
Example (software): if MEMORY says "API v2 migration — in progress" but a later log
records "v2 rolled back due to breaking changes, reverted to v1.8," update immediately.

### Step 3 — Tier Content

Organize all content into four tiers by durability. **Upper tiers must never be lost
when condensing lower tiers.**

- **P0 — Never drop**: Red lines (title/role rules, confidentiality, communication
  style), conventions (file organization, reporting format, naming), hard compliance
  constraints. Persist for the project's lifetime.
- **P1 — Structural background**: Positioning, architecture, compliance blind spots,
  financing, entity structure research, operational models, investor/funnel playbooks,
  competitive positioning. For software: architecture decisions, tech debt inventory,
  dependency choices, design rationale. For research: methodology, validated findings,
  literature conclusions. Valid for months; **re-add priority** when previously dropped.
- **P2 — Current operational state**: Contact status, active workstreams, next-step
  actions. For software: feature progress, sprint status, blocker status. For research:
  experiment progress, data collection status, writing progress. **Refresh entirely
  each update** — replace old state, do not accumulate history (replace "pending send"
  with "sent, awaiting reply" — do not keep both).
- **P3 — Index**: Key contacts, reference document paths, open questions/blind spots.

### Step 4 — Signal vs Noise (also serves as Content Retention Rules)

**Include in MEMORY.md:**
- Decisions and their rationale
- Red lines and conventions
- Structural facts (entity models, regulatory conclusions, financing terms)
- Current state (contact status, active workstreams)
- Executable checklists (e.g., investor channels for BD, sprint backlog for software,
  experiment queue for research)
- Key contacts (people, emails, roles)

**Exclude from MEMORY.md** (keep in daily logs only):
- Email drafting process and iteration history
- File move/rename commands (sed, git mv, etc.)
- Temporary draft states ("draft on hold", "pending send")
- Single-task execution details (how a file was converted, which command was used)
- Personal/sensitive information (e.g., salary negotiations)
- Superseded conclusions (when a later log corrects an earlier one)

### Step 5 — Source-Tag

Tag each fact with a date and originating context so future updates can verify:
- Adapt the format to the project's language and conventions.
- Inline date after the fact: e.g., `(2026-07-10)` or `(Jul 2026)`.
- For research conclusions, reference the deliverable: e.g., `see path/to/file.md`.
- Do not over-tag trivial facts; reserve tags for non-obvious claims and research
  conclusions that may need verification.

### Step 6 — Resolve Contradictions

When daily logs contradict each other:
1. Identify the **latest** log that addresses the point.
2. Within that log, prefer the **most detailed / most corrected** statement.
3. If a later log explicitly says "corrects previous assessment" or equivalent, the
   correction wins.

Example: Log A says "Counsel scope includes 3 revision rounds"; Log B (later, more
detailed) says "maximum 2 revision rounds" — use 2.

### Step 7 — Refresh Time-Sensitive Content

For P2 content (operational state), **replace** the old state entirely:
- "pending send" becomes "sent, awaiting reply" (do not keep "pending send" as history)
- "replied, questionnaire required" replaces "sent, awaiting reply"
- Downgraded items (e.g., a contact found unreachable) get a one-line reason,
  not a full history of attempts.

Do not accumulate a timeline of state changes in MEMORY.md — that belongs in daily logs.

## Methodology Embed Pattern

Embed a condensed version of this maintenance methodology at the **top** of MEMORY.md
itself (after the title, before substantive content). This makes the file
self-documenting: any future agent opening MEMORY.md sees both the content AND the
process used to maintain it.

**What to embed** (condensed, ~15 lines):
- The 7-step process names (one line each)
- The P0-P3 tier definitions (one line each)
- The "replace, don't append" rule for P2

**What NOT to embed**: The full Skill text, examples, or pre-update reading strategy.
Keep the embed lean — it is a reminder, not a reproduction.

**Sync**: When this Skill is updated, check if the embedded methodology in any
project's MEMORY.md needs synchronization. The embed is a summary; this Skill is the
source of truth.

## Length Management

- **Target**: 60-120 lines for most projects. Below 40 = likely missing P1; above 150
  = likely accumulating noise or P2 history.
- **When too long**: First check if P2 history is accumulating (fix: replace, do not
  append). Then check if P1 items can be condensed (e.g., a 15-item detailed list —
  investor channels, tech debt items, literature references — can become "5 items
  identified, see {file path}" with only the top 3 named). If still too long, move
  detailed reference material to a separate file and keep a one-line pointer in
  MEMORY.md.
- **When P0 grows**: P0 red lines should never be shortened for length — they are hard
  rules. If P0 exceeds ~30 lines, consider splitting into "core red lines" (in
  MEMORY.md) and "detailed conventions" (in a reference file).
- **Tension resolution**: When "comprehensive" conflicts with "scannable", prioritize
  scannable for P2 (it refreshes every update) and comprehensive for P1 (it persists
  for months). P0 is always comprehensive — no trade-off.

## Structure Template

Adapt the section layout to the project type. The P0-P3 tier assignments are universal;
only section names and content focus change. Pick the closest template and further adapt
as needed.

### Business / BD Project (default)

1. **Title + update date**
2. **Maintenance methodology** (condensed embed — see Methodology Embed Pattern)
3. **Project positioning and entities** (P1: what each entity does, architecture, red
   lines on titles/roles)
4. **Current business state** (P2: contact status, strategic focus, active workstreams,
   next steps)
5. **Product/deal structure definitions** (P1: external communication baselines)
6. **External communication red lines** (P0: confidentiality, email style, capital
   discipline)
7. **File and reporting conventions** (P0: file organization, naming, reporting format)
8. **Quick facts** (P1: financing, legal counsel, competitor positioning, key specs)
9. **Key contacts** (P3: people, emails, roles)
10. **Reference docs and open questions** (P3: file paths, unresolved blind spots)

### Software Development Project

1. **Title + update date**
2. **Maintenance methodology** (condensed embed)
3. **Project overview and tech stack** (P1: what the project is, framework, key
   dependencies, architecture decisions and rationale)
4. **Current development state** (P2: feature progress, sprint/milestone status, blocker
   status, next steps)
5. **Architecture decisions and tech debt** (P1: key design choices, accepted trade-offs,
   tracked debt, migration plans)
6. **Coding conventions and constraints** (P0: naming rules, file organization, testing
   requirements, deployment rules, security constraints)
7. **Environment and infrastructure** (P1: version, env URLs, CI/CD status, key configs)
8. **Key contributors** (P3: names, roles, areas of ownership)
9. **Reference docs and open questions** (P3: design docs, API contracts, unresolved
   decisions)

### Research / Academic Project

1. **Title + update date**
2. **Maintenance methodology** (condensed embed)
3. **Research topic and scope** (P1: hypotheses, research questions, scope boundaries)
4. **Current research state** (P2: experiment progress, data collection status, writing
   progress, next steps)
5. **Methodology and key findings** (P1: methods, validated conclusions, literature
   synthesis)
6. **Research constraints and conventions** (P0: citation format, data handling rules,
   ethics constraints)
7. **Open questions and gaps** (P1: unresolved hypotheses, literature gaps, methodological
   limitations)
8. **Quick facts** (P1: funding status, timeline, key references, tools)
9. **Key collaborators** (P3: names, institutions, roles)
10. **Reference docs and open questions** (P3: file paths, datasets, pending reviews)

### Choosing the Right Template

- External partnerships, investors, regulatory compliance → Business / BD template.
- Primarily code, daily logs track features/bugs/deployments → Software Development template.
- Experiments, literature review, academic writing → Research template.
- Hybrid project → mix and match sections. P0-P3 tiers are universal; only section names
  adapt. When unsure, start with Business / BD (most general) and adjust.

## Post-Update Checklist

After writing the updated MEMORY.md, execute these steps:

1. **Daily log**: Append a brief note to today's `YYYY-MM-DD.md` recording what was
   updated (sections changed, items added/removed). If today's log does not exist,
   create it.
2. **Present to user**: Show the updated MEMORY.md to the user for review (e.g., via
   the platform's file presentation mechanism).
3. **User-level check**: Determine if any new facts are cross-project (e.g., a user
   preference discovered during the update). If so, write to `~/.workbuddy/MEMORY.md`.
4. **Automation check**: If the user has not set up periodic maintenance, suggest
   creating an automation (e.g., monthly MEMORY.md review reminder).
5. **Self-check**: Run through the checklist below.

### Post-Update Self-Check

- [ ] All P0 red lines and conventions are present and prominently visible?
- [ ] No P1 structural facts were accidentally dropped during condensation?
- [ ] P2 operational state reflects the LATEST status (no accumulated history)?
- [ ] No single-task execution details leaked from daily logs into MEMORY?
- [ ] No personal/sensitive information included?
- [ ] Every non-trivial fact has a source date or reference path?
- [ ] File length is within the 60-120 line target range?
- [ ] Maintenance methodology embed is present at the top?

## Maintenance Cadence

- **Trigger-based**: update when user requests, or after 5-10 new daily logs accumulate.
- **Quantitative trigger**: when new daily logs since last update collectively exceed
  ~50KB, proactively suggest an update even if not explicitly requested.
- **Monthly**: recommended full review even if not explicitly requested.
- **After major shifts**: update immediately when a strategic pivot, new red line, or
  significant status change occurs (do not wait for periodic review).
