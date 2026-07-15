---
name: crypto-daily-briefing
description: >
  Crypto daily briefing generator for Tom — focused on Stablecoin + RWA (Real World Assets)
  sectors. Collects news covering stablecoin regulation, RWA tokenization (T-Bills, precious
  metals, carbon credits, stocks, funds), and compliance frameworks in Singapore/HK/US/EU/Japan.
  This skill should be used when the user asks for "加密日报", "稳定币简报", "crypto briefing",
  "RWA日报", or when the daily automation runs.
agent_created: true
---

# Crypto Daily Briefing — Stablecoin + RWA

## Overview

Generate a structured daily briefing covering Stablecoin and RWA (Real World Assets) sectors.
Output is a Chinese-language markdown file with max 10 news items ranked by importance.

**视角多样性（Verbalized Sampling）**：为避免简报"观点坍塌"，每条新闻除主解读外，用 Verbalized Sampling (VS) 额外给出 2–3 条备选解读角度及其概率；【今日观察】也产出多条叙事框架而非单一视角。原理与用法见速查卡 `verbalized-sampling-cheatsheet.md`。

## When to Use

- User asks for "加密日报", "稳定币简报", "crypto briefing", "RWA新闻"
- Daily automation triggers at 9:00 AM Beijing time
- User asks "今天稳定币有什么新闻" or similar queries

## Workflow

### Step 1: Collect News via WebSearch

No crypto-specific API is available. Use WebSearch (topic=news) in 4 parallel groups:

**Group 1 — Stablecoin Regulation (4 queries)**:
1. "USDT USDC stablecoin regulation license legislation"
2. "GENIUS Act stablecoin bill Congress progress"
3. "稳定币 香港 新加坡 监管 牌照 最新进展"
4. "MiCA stablecoin EU regulation compliance June 2026"

**Group 2 — RWA Tokenization (4 queries)**:
5. "BlackRock BUIDL tokenized treasury fund update June 2026"
6. "Ondo Finance RWA tokenization real world assets"
7. "Securitize tokenized assets real world assets 2026"
8. "真实世界资产 代币化 美债 RWA June 2026"

**Group 3 — Protocol & Market Data (6 queries)**:
9. "Ethena USDe stablecoin yield update news"
10. "MakerDAO Sky stablecoin USDS Endgame"
11. "stablecoin market cap USDT USDC supply change June 2026"
12. "tokenized treasuries on-chain T-Bill market size 2026"
13. "new stablecoin launch announce 2026 consortium"
14. "新稳定币 发布 推出 上线 consortium"

**Group 4 — Chinese Sources (2 queries)**:
13. "财新 稳定币 加密货币 监管 RWA"
14. "21世纪经济报道 数字资产 代币化"

### Step 2: Deep Dive

WebFetch the 5-8 most promising articles for richer detail. Prioritize:
- Official announcements / press releases
- SEC filings / regulatory documents
- The Block, CoinDesk, Bloomberg Crypto
- RWA.xyz, DefiLlama data references

### Step 3: Rank and Select

Select max 10 items, ranked by importance:
1. Major new stablecoin launches or protocol-level announcements (new stablecoin debuts, consortium formations, issuer M&A)
2. Major regulatory/legislative milestone (GENIUS Act, MiCA updates, new jurisdiction licenses)
3. Major protocol launch/upgrade (Ethena, Maker/Sky, Frax, Ondo, new stablecoin launches)
4. Institutional RWA deployment (BlackRock, Goldman, JPM, Franklin Templeton)
5. TVL/on-chain data anomalies or significant market cap changes
6. Advisory/opinion pieces (lowest priority)

Deprioritize: pure KOL reposts, unsigned hype articles, "XX暴涨" sensationalism.

### Step 3.5: VS Multi-Angle Interpretation (Verbalized Sampling)

For each selected news item, apply **Verbalized Sampling** so the briefing does not collapse onto a single typical framing. For every item, generate **2–3 interpretation angles with probabilities**, e.g.:

> "Generate 3 different interpretation angles for this news and their corresponding probabilities:
> (1) typical/mainstream read, (2) an alternative read a sharp analyst would push, (3) a contrarian or overlooked read."

Rules:
- Keep it compact — one short line per angle + a probability (e.g., `典型解读 60% / 另类解读 30% / 被忽视视角 10%`). Do NOT expand into a research report.
- Angles must be factually grounded in the sourced article; never invent facts to force diversity.
- This step only reshapes *interpretation*, not the factual summary from Step 2/3.

### Step 4: Format Output

Save to `briefings/crypto/YYYY-MM-DD.md`:

```markdown
# 加密每日简报 — YYYY年MM月DD日（周X）

> 过去 24h | 稳定币 + RWA 赛道 | 共 N 条 | 按重要度降序

---

## N. 【标题】
- **【信源】** Source
- **【一句话事实】** One-sentence factual summary
- **【影响判断】** 🟢/🔴/🟡 impact assessment
- **【多角度解读 · VS】** 典型解读 60% / 另类解读 30% / 被忽视视角 10%
- **【关联标的】** Relevant tokens/protocols

---

## 【今日观察】

Narrative synthesis — dominant themes, anomalies, watchlist

---

> *生成时间：YYYY-MM-DD HH:MM CST | 覆盖信源：WebSearch（The Block、CoinDesk、Bloomberg Crypto、财新等）*
```

### Step 5: Add Daily Observation (VS Multi-Framing)

End with 【今日观察】. Instead of a single collapsed "dominant narrative", use **Verbalized Sampling (VS-Multi style)** to surface **2–3 distinct narrative framings** of the day, each with a one-line rationale and an implicit/shared probability, e.g.:

> 框架 A（主流）：监管落地驱动机构加速入场 — 60%
> 框架 B（另类）：市场已 price-in，真正变量是链上流动性 — 30%
> 框架 C（被忽视）：新兴市场主权采用才是中期拐点 — 10%

Then keep a short **【值得关注】** watchlist. Stay concise — this is a 3-minute morning read, not an essay.

## Output Specifications

- **Language**: Chinese with key English terms (T-Bill, NAV, mint/redeem, USDT, USDC, BUIDL, TVL)
- **Length**: ~3-minute morning read, concise
- **Tone**: Professional, direct, factual — no research report expansion
- **Color convention** (Chinese market): 🟢 bullish, 🔴 bearish, 🟡 neutral
- **Location**: `/Users/bittom/Desktop/DailyNews/briefings/crypto/YYYY-MM-DD.md`

## Verbalized Sampling (VS) 使用约定

- **是什么**：零训练、推理时的提示技巧——让模型把 K 个候选及其概率一起说出，恢复被对齐"压掉"的多样性（论文 arXiv:2510.01171v3）。
- **模板**：`Generate {K} {items} about {topic} and their corresponding probabilities.`（中文：`生成 K 条关于{topic}的{items}及各自概率。`）
- **候选数 K**：每条新闻多角度解读取 **K=3**；【今日观察】框架取 **K=3**。
- **仅在强模型上启用**：VS 收益随模型能力上升而显著增大。优先在 GPT-4.1 / Gemini-2.5-Pro / Claude 级模型运行；若运行模型为小模型（Mini/Flash 级），可省略多角度块以免噪声。
- **成本/延迟**：每轮生成多个候选，推理成本与延迟更高；在保持 ≤10 条、3 分钟晨读的长度约束下使用。
- **不牺牲事实**：VS 只重塑"解读/叙事框架"，不改动【一句话事实】与信源；概率是对"哪种解读更可能成立"的主观估计，非市场预测。
- **完整模板与场景**：见 `verbalized-sampling-cheatsheet.md`。

## Coverage Scope

| Category | Topics |
|----------|--------|
| Stablecoins | USDT, USDC, DAI/USDS, FDUSD, Ethena USDe, Frax, PYUSD, RLUSD, Open USD; new stablecoin launches & consortium formations; jurisdiction licensing (HK/Singapore/EU/Japan/UAE); GENIUS Act, MiCA, stablecoin legislation |
| RWA Tokenization | BlackRock BUIDL, Ondo Finance (OUSG/USDY), Securitize, Franklin Templeton BENJI; T-Bill tokenization, precious metals, carbon credits, stock/fund tokenization |
| Regulatory Frameworks | Singapore MAS, Hong Kong SFC/HKMA, US SEC/CFTC, EU MiCA, Japan FSA; compliance requirements, sandbox programs |
| Market Data | Stablecoin market cap trends, DeFi TVL related to RWA, on-chain anomaly monitoring |

## Source Priority

1. **Preferred**: Project official X/announcements, SEC filings, TreasuryDirect, DefiLlama TVL changes, ARKM on-chain anomalies
2. **Secondary**: The Block, CoinDesk, Bloomberg Crypto, 财新, 21世纪经济报道
3. **Deprioritized**: Pure KOL reposts, unsigned hype articles
