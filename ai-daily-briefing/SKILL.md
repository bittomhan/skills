---
name: ai-daily-briefing
description: >
  AI industry daily briefing generator for Tom. Collects and formats AI news
  covering LLMs/models, Agents/toolchains, compute/GPUs, and applications. This
  skill should be used when the user asks for "AI日报", "AI简报", "daily AI
  briefing", "today's AI news", or when the daily automation runs.
agent_created: true
disable: true
---

# AI Daily Briefing

## Overview

Generate a structured daily AI industry briefing covering LLM models, Agents & toolchains,
compute & GPUs, and AI applications. Output is a Chinese-language markdown file with
exactly 15 news items ranked by importance, formatted to the user's spec.

## When to Use

- User asks for "AI日报", "AI简报", "AI每日新闻"
- Daily automation triggers at 8:00 AM Beijing time
- User asks "今天AI圈有什么" or similar broad queries

## Workflow

### Step 1: Collect News from aihot API (Primary Source)

Load the `aihot` skill and call the aihot API for curated AI news from the past 24 hours:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&since=$since&take=50"
```

The API returns structured items with: title, source, publishedAt, summary, category, score, url.

### Step 2: Supplement with WebSearch

Use WebSearch (topic=news) to fill coverage gaps in these areas:

1. **Compute/GPUs**: "NVIDIA H200 B200 GB200 shipment TSMC CoWoS AI chip news"
2. **Agent toolchain**: "Cursor Claude Code Copilot AI coding agent MCP A2A protocol update"
3. **China AI chips**: "国产算力 昇腾 寒武纪 海光 AI芯片 最新消息"
4. **Model releases**: "OpenAI Anthropic Google DeepMind AI model release news"
5. **Applications**: "AI search office companion application commercial news"

Fetch 2-3 key articles via WebFetch for richer detail when needed.

### Step 3: Rank and Select

- Select exactly 15 items
- Rank by importance: major model releases > compute/ASIC news > regulatory/policy > application news > academic papers
- Prioritize: official blogs, earnings reports, founder X posts, Reuters/Bloomberg Tech
- Deprioritize: pure KOL commentary, clickbait titles

### Step 4: Format Output

Save to `briefings/ai/YYYY-MM-DD.md` using this EXACT format for each item:

```markdown
## N. [Title in Chinese or concise translation]

- **【信源】** Media / Official / Earnings / On-chain source
- **【一句话事实】** One-sentence factual summary
- **【影响判断】** 🟢/🔴/🟡 bias direction with target segment (model/compute/application)
- **【关联标的】** US stocks (NVDA/MSFT/GOOG...) and/or A-shares (寒武纪/海光...)
```

### Step 5: Add Daily Observation

Append a 【今日观察】 section at the end identifying the dominant narrative of the day.

## Output Specifications

- **Language**: Chinese with key English terms preserved (token, context window, FLOPs, CUDA, MoE, etc.)
- **Length**: ~3-minute morning read
- **Tone**: Professional, direct, factual — no research report expansion
- **Color convention**: 🟢 bullish, 🔴 bearish, 🟡 neutral — for AI sector or specific sub-segments
- **Location**: `/Users/bittom/Desktop/DailyNews/briefings/ai/YYYY-MM-DD.md`

## Coverage Scope

| Category | Topics |
|----------|--------|
| LLM Models | OpenAI, Anthropic, Google, xAI, DeepSeek, 智谱, MiniMax, Kimi |
| Agents & Tools | Cursor, Claude Code, Copilot, MCP/A2A protocol, browser agents, multi-agent frameworks |
| Compute | NVDA/AMD/Broadcom/ASIC (Trainium/TPU), H20/B200/GB200, TSMC CoWoS, 国产算力 (昇腾/寒武纪/海光) |
| Applications | AI search, AI office, AI companion/character |

## Source Priority

1. **Preferred**: Company official blogs, earnings reports, founder X/Twitter, Reuters Tech, Bloomberg Tech, The Information
2. **Secondary**: TechCrunch, Benzinga AI, 36kr, 机器之心, 量子位, 晚点LatePost
3. **Deprioritized**: Pure KOL commentary, clickbait "XX already surpassed GPT-5" pieces
