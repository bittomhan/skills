---
name: academic-literature-validation
description: >-
  Validate investment research claims with peer-reviewed academic literature using
  WebSearch + WebFetch, without paid tools. This skill should be used when performing
  academic cross-validation of existing investment research reports — specifically
  when upgrading [low] credibility personal analysis to [high] credibility peer-reviewed
  sources. Triggers: "学术验证", "文献验证", "cross-validate with academic sources",
  "verify with literature", "upgrade credibility", or when updating tracking research
  files with [high] confidence citations. Applicable to biotech/pharma investment
  research where clinical trial data, competitive landscape, and mechanism validation
  require peer-reviewed sourcing.
agent_created: true
---

# Academic Literature Validation

## Overview

This skill validates investment research claims by systematically searching peer-reviewed
academic literature using Argo's built-in WebSearch + WebFetch tools — no paid
subscriptions required. It bridges the credibility gap between [low] personal analysis
(e.g., Fan Junqing's Snowball posts) and [high] peer-reviewed sources (NEJM, JCO,
Blood, mAbs, etc.) by leveraging open-access ecosystems like PubMed Central (PMC).

## When to Use

- Updating any company tracking file (`[公司名]_跟踪调研/`) with academic validation
- Before catalyst events (conference presentations, BLA/NDA filings) to establish
  academic baselines
- When a research claim from [low] source needs independent verification
- When competitive landscape analysis requires comprehensive literature mapping
- Periodic credibility audits of existing research files

## Key Principle

**Biotech/pharma literature is disproportionately open-access.** PMC hosts full-text
articles for all NIH-funded research and many journal submissions. Conference abstracts
(ASCO/ESMO/WCLC/ASH) are free. bioRxiv/medRxiv preprints are free. ClinicalTrials.gov
provides trial designs and results. This means Argo can access a large majority of
relevant literature without paid tools.

## Workflow

### Step 1: Extract Claims to Validate

Read the existing research file and extract all claims with [low] or [medium]
credibility tags. Organize into categories:

- **Clinical data claims**: ORR, DCR, PFS, OS numbers and their sources
- **Mechanism claims**: "overcomes toxicity", "first-in-class", "best-in-class"
- **Competitive claims**: "global first", "ORR highest in class", pipeline status
- **Market claims**: "SOC survival X months", "no approved drugs for indication"
- **Strategic claims**: "IO 2.0", "platform technology", "BD potential"

Record each claim with its original source and credibility tag.

### Step 2: Systematic Academic Search

Use WebSearch with targeted queries. Search patterns that work well:

```
"[drug name] [target] clinical trial results [journal/conference] [year]"
"[drug name] NCT[number] published results"
"[target] bispecific antibody review [year]"  (for competitive landscape)
"[indication] standard of care survival [year]"  (for SOC comparison)
"[competitor drug] safety adverse events"  (for head-to-head comparison)
```

Run 3-5 searches per validation target. Prioritize:
1. Specific drug name + clinical trial identifier (NCT number)
2. Target/mechanism + review articles (for competitive landscape)
3. Indication + standard of care (for SOC comparison)
4. Competitor drug + safety profile (for head-to-head)

### Step 3: Fetch Full Text / Abstracts

Use WebFetch on search results, prioritizing in this order:

1. **PMC full-text articles** (pmc.ncbi.nlm.nih.gov) — complete peer-reviewed papers
2. **PubMed abstracts** (pubmed.ncbi.nlm.nih.gov) — key data in abstract
3. **Conference abstracts** (ascopubs.org, ashpublications.org) — meeting presentations
4. **ClinicalTrials.gov** — trial designs, enrollment, status
5. **Journal pages** (aacrjournals.org, frontiersin.org) — may have open access

WebFetch prompt pattern for extraction:
```
Extract: 1) Is this peer-reviewed? What journal? 2) Does it mention [drug]?
3) What are the key efficacy data (ORR/DCR/PFS/OS)? 4) What are the safety data?
5) Is full text available? 6) List comparison data in table format.
```

### Step 4: Cross-Validate Claims

For each extracted claim, compare with academic data:

| Outcome | Action | Credibility Adjustment |
|---------|--------|----------------------|
| Academic data matches claim | Confirm | [low]→[high] or [med]→[high] |
| Academic data contradicts claim | Flag discrepancy | Keep original, add [high] correction |
| Academic data partially supports | Nuance | [low]→[med], note what needs modification |
| No academic data found | Note gap | Keep original credibility, mark "unverified" |
| Claim is a prediction/extrapolation | Distinguish fact from prediction | Keep [low], mark as "prediction" |

### Step 5: Write Validation Document

Create a new file: `[公司名]_跟踪调研/学术文献验证.md`

Structure:
1. **Clinical data validation** — table comparing original vs academic data
2. **Mechanism/safety claims** — academic evidence for/against
3. **Competitive landscape** — comprehensive comparison table from review articles
4. **SOC comparison** — academic baseline data for indication
5. **Credibility upgrade summary** — table of all claims with before/after ratings
6. **Key corrections** — list of claims that need modification in original report
7. **New [high] source list** — DOI/PMID/NCT numbers for traceability

Rules:
- **Never modify the original research file** — the validation document is additive
- Every [high] citation must include DOI, PMID, or NCT number
- Distinguish between "verified" (data matches) and "corrected" (data differs)
- Mark predictions/extrapolations explicitly as "prediction, not fact"

### Step 6: Update README

Update the company folder's README.md:
- Add the validation file to the document index
- Update coverage status (e.g., "竞品对比" from ⚠️ to ✅ if competitive landscape now covered)
- Update "最后更新" date

## Open Access Quick Reference

| Source | Access | URL Pattern | Coverage |
|--------|--------|-------------|----------|
| PubMed Central (PMC) | Full text FREE | pmc.ncbi.nlm.nih.gov/articles/PMCXXXXX | NIH-funded + open access journals |
| PubMed | Abstracts FREE | pubmed.ncbi.nlm.nih.gov | All biomedical literature |
| ASCO abstracts | FREE | ascopubs.org/doi/10.1200/JCO | ASCO annual meeting |
| ASH abstracts | FREE | ashpublications.org/blood | ASH annual meeting (Blood journal) |
| ClinicalTrials.gov | FREE | clinicaltrials.gov/study/NCTXXXXX | All US-registered trials |
| bioRxiv/medRxiv | Full text FREE | biorxiv.org, medrxiv.org | Preprints |
| Frontiers | Full text FREE | frontiersin.org | Open access journal |
| mAbs (Taylor & Francis) | Full text FREE | tandfonline.com/loi/kmab20 | Antibody therapeutics |
| J Clin Med (MDPI) | Full text FREE | mdpi.com/journal/jcm | Open access journal |
| AACR journals | Abstract FREE | aacrjournals.org | Cancer Research, Clinical Cancer Research |

## Search Strategy Tips

- **Drug name variants**: Search both generic name and code (e.g., "LBL-024" AND "opamtistomig")
- **NCT numbers**: If a trial number is known, search it directly — most precise
- **Review articles**: Search "[target] review [year]" to find comprehensive competitive landscapes
- **Conference names**: Search "[drug] ASCO 2025" or "[drug] ASH 2025" for latest presentations
- **Chinese sources**: For Chinese companies, also search 良药汇 / 医药魔方 / pharmcube for Chinese-language reports
- **Citation chains**: When a review article mentions a drug, check its reference list for primary sources

## Output Quality Standards

- Every [high] source must be traceable (DOI/PMID/NCT/URL)
- Safety data must distinguish "all-grade" vs "Grade ≥3"
- Efficacy data must note sample size and follow-up duration
- Competitive comparisons must note patient baseline differences
- Predictions must be labeled as predictions, not facts
- "First-in-class" / "best-in-class" claims must be verified against global pipeline

## Limitations

- **Paywalled full text**: NEJM, Lancet, Nature may require subscription; abstracts are free but may lack detailed data
- **Chinese journals**: Limited coverage in PubMed; supplement with Chinese databases if needed
- **Search depth**: Each WebSearch returns 5-10 results; may need multiple iterations for comprehensive coverage
- **No citation graph traversal**: Unlike Undermind, cannot automatically follow citation chains — must manually identify and fetch referenced papers
- **Real-time monitoring**: No automatic alerts for new publications; must periodically re-search

## Relationship to Credibility Framework

This skill implements the cross-validation mechanism defined in
`OnlineInvest/_framework/信息来源可信度分级规范.md`:

- [低] personal analysis → validated by [高] academic source → upgrade to [中] or [高]
- [中] sell-side research → validated by [高] academic source → upgrade to [高]
- Contradictions between [低] and [高] → [高] takes precedence, flag discrepancy
- Mark upgrades with: `(来源:XXX | 可信度:[低]→经[高]学术验证,提升为[中])`
