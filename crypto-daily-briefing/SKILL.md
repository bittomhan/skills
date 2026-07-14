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
- **【关联标的】** Relevant tokens/protocols

---

## 【今日观察】

Narrative synthesis — dominant themes, anomalies, watchlist

---

> *生成时间：YYYY-MM-DD HH:MM CST | 覆盖信源：WebSearch（The Block、CoinDesk、Bloomberg Crypto、财新等）*
```

### Step 5: Add Daily Observation

End with 【今日观察】 identifying the day's common narrative or anomaly worth watching.

## Output Specifications

- **Language**: Chinese with key English terms (T-Bill, NAV, mint/redeem, USDT, USDC, BUIDL, TVL)
- **Length**: ~3-minute morning read, concise
- **Tone**: Professional, direct, factual — no research report expansion
- **Color convention** (Chinese market): 🟢 bullish, 🔴 bearish, 🟡 neutral
- **Location**: `/Users/bittom/Desktop/DailyNews/briefings/crypto/YYYY-MM-DD.md`

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
