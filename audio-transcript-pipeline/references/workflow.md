# 详细工作流（6 阶段）

> 加载本文档以获取每阶段的命令、参数、陷阱与实例。SKILL.md 是精简版流程指引。

---

## 阶段 0 — 环境检查（每次开始前）

```bash
# 1. 音频时长
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<AUDIO_PATH>"
# 2. Whisper 模型缓存
ls ~/.cache/whisper/
# 3. Whisper + MPS 可用性
/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 -c "import whisper, torch; print('whisper ok, mps:', torch.backends.mps.is_available())"
```

- Whisper 缺失：`/Users/bittom/.workbuddy/binaries/python/envs/default/bin/pip install openai-whisper`
- 模型未缓存：首次运行自动下载 `medium.pt`（~1.5GB）到 `~/.cache/whisper/`
- MPS 不可用（Intel Mac）：改 `DEVICE="cpu"`，速度慢约 3-5 倍

---

## 阶段 1 — Whisper 转写

编辑 `scripts/whisper_transcribe.py` 顶部常量后运行。要点：

- **强制语言**（`language="zh"`）：比自动检测更快更准，避免中英混合音频被误判。
- **幻觉调优参数**（中文关键）：
  - `compression_ratio_threshold=2.4`（默认 2.4）：低于此值更易放过重复段；中文可保持 2.4
  - `no_speech_threshold=0.6`（默认 0.6）：调高可避免静音段被误判为有内容；中文长段建议 0.6
  - `logprob_threshold=-0.8`（默认 -1.0）：调高（-0.8）更严格，减少低置信度胡编
- **运行方式**：必须后台运行（`run_in_background=true`），等待 task-notification，**不要轮询**。
- **速度波动**：MPS 在中段可能因散热降频变慢（40 帧/秒），后段恢复（250 帧/秒），属正常，让其跑完。
- **输出**：两段式——「完整文字」连续文本 + 「带时间戳分段」`**[MM:SS]** 文本` 逐行。

---

## 阶段 2 — 联网校对

### 2.1 识别错误

通读转写稿，标注以下类别的可疑错误：
- **英文药名/代号**（最易错）：Whisper 对英文术语音译失真严重（"Zosie"→zoci、"Furthing Class"→First-in-Class、"Athmo"→ESMO）
- **机构名**："安静"→安进(Amgen)、"柏林格英格汗"→勃林格殷格翰(BI)
- **医学术语**："客观缓决率"→客观缓解率(ORR)、"特音性皮炎"→特应性皮炎、"韩国化疗"→含铂化疗
- **中文同音误识**："故事的底部"→估值的底部、"回难"→回暖、"采报"→财报
- **数字/时间**：核对财报原文
- **发言人身份/在职状态**（易被忽略的高频错误）：转写稿里的发言人姓名多为音译误识（"亚进"→Josh/陈娅静）；**必须联网核实当前在职状态**——高管可能在会议前已离职。典型坑：某高管已离职但仍按旧认知标注为发言人。核实信源：公司近期 IR 公告（"leadership changes"/"appoints"/"no longer be with"）、高管变动新闻。

### 2.2 联网勘定（信源优先级）

1. **公司官网/IR 公告**（最高可信度）：管线代号、产品商品名、财务数据、临床进度
2. **合作方/收购方公告**：AbbVie/Daiichi Sankyo/Merck 等收购与合作公告
3. **临床数据库**：ClinicalTrials.gov、ASCO/ESMO/WCLC/AACR 会议摘要
4. **券商研报/行业数据库**（中等可信度）：Insight、医药魔方

### 2.3 标注规范

- 已确认修正：直接替换
- **推断但未 100% 确认**：标 `[?]`（如推断的研究代号、人名音译）
- 矛盾信息：优先采信公司官方信源

### 2.4 实例（再鼎业绩会）

| 转写错误 | 勘定为 | 信源 |
|---|---|---|
| Zosie/ZoC/Docie | zoci（zocilurtatug pelitecan，曾用名 ZL-1310）| 再鼎 IR 公告 |
| AppleG | Apogee Therapeutics | AbbVie 收购公告（109 亿美金）|
| IDFD/IDXD | I-DXd（ifinatamab deruxtecan）| 第一三共/默沙东公告，PDUFA 2026-10-10 |
| 他买的 006 | ABBV-706（艾伯维 SEZ6 ADC）| 2026 ELCC 摘要 |

---

## 阶段 3 — 多轮批量修正

### 3.1 批量替换原则

- **长串优先**：先替换"客观环绝率COR2"→"确认的客观缓解率"，再替换"客观环绝率"→"客观缓解率"，避免部分替换冲突
- **body-only**：只替换正文（MARKER 之后），不动头部对照表展示的原文
- **NFKC 规范化**：部分中文字符有兼容变体（如"屈"的异体 U+5C48 vs U+FA1C），直接 replace 失败；先 `unicodedata.normalize("NFKC", text)` 再替换

### 3.2 多轮修补流程

1. **Pass 1**（bulk）：`scripts/proofread_replace.py` 应用全部规则
2. **Grep 残留扫描**：用 Grep 工具扫描正文，找未命中的错误词模式
3. **Pass 2-N**（patch）：针对残留写小脚本补充替换，每轮后 Grep 验证
4. **验证**：用 VERIFY 词表扫描正文，确认全部清除

### 3.3 常见残留陷阱

- 字符编码变体（NFKC 解决）
- 规则顺序冲突（长串优先解决）
- 触发词边界（"PT-1加zoci Chemo" 应在 "PT-1加zoci" 之前替换）
- 冗余（"经确认的"+"确认的客观缓解率"→"经确认的确认的客观缓解率"，需去冗余）

---

## 阶段 4 — 语义段落重排

运行 `scripts/reformat_paragraphs.py`。要点：

- **触发词需按会议类型定制**：业绩会=分析师自报+交接+Q&A标志；访谈=主持人/嘉宾切换
- **MAX_SENT**：每段最多句数（默认 9），超过强制分段，避免段落过长
- **章节划分**：按时间边界归入章节，需根据实际议程定义 CHAPTERS
- **段首时间戳**：保留该段第一句的时间，便于定位回放

---

## 阶段 5 — 终版格式化

参见 `format_template.md`。关键：

- **精华摘要手写**：这是最大价值增量，需基于全文提炼 4-6 个主题 + 速览表
- **发言人映射**：按时间戳区间定义 SPEAKERS 列表（秒→发言人），无通用自动检测，需逐录音构建
- **议题式章节标题**：比角色式更清晰（"三、何珊：zoci 管线详述" > "三、何珊发言"）
- **附录**：对照表（阶段2成果）+ 联网核实记录（编号信源列表）

---

## 阶段 6 — PDF 导出

```bash
/opt/homebrew/bin/python3 /Users/bittom/.workbuddy/skills/md-to-pdf/md-to-pdf/scripts/md_to_pdf.py "<input.md>" "<output.pdf>"
```

- 必须用**系统 Python**（`/opt/homebrew/bin/python3`），不能用隔离 Python（weasyprint 依赖系统 pango/gobject）
- 字体：Noto Sans CJK SC（思源黑体），已嵌入，微信端无乱码
- 按用户偏好：仅在用户明确要求"生成 PDF"时执行

---

## 清理约定

终版确认后，用户可能要求仅保留终版：
- 中间稿件（原始转写稿/校对字幕版/段落版）`mv` 到 `~/.Trash/`（可恢复）
- 保留终版 `.md` + `.pdf`
- **不要用 `rm`**，用 `mv` 到废纸篓保证可恢复
