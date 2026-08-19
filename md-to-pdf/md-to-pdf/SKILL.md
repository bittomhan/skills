---
name: md-to-pdf
description: Convert Markdown documents (with Chinese content, tables, code blocks) to formatted PDF. This skill should be used when the user asks to generate a PDF from a Markdown file, or convert .md to .pdf.
agent_created: true
---

# Markdown → PDF Converter

Convert Markdown files to professionally formatted PDF documents with Chinese font support (Noto Sans CJK SC).

## Font Configuration (Updated 2026-08-06)

**Primary font: Noto Sans CJK SC** (思源黑体, open-source, cross-platform compatible)

Previously used PingFang SC (macOS proprietary). Switched to Noto Sans CJK SC because:
- PingFang SC is Apple-proprietary; its CFF subset data caused compatibility issues on some PDF viewers (e.g., WeChat's built-in viewer on Android)
- Noto Sans CJK SC is open-source with standardised CFF data, better character coverage, and broader viewer compatibility
- Fonts are installed at `~/Library/Fonts/NotoSansCJKsc-Regular.otf` and `NotoSansCJKsc-Bold.otf` (downloaded via jsdelivr CDN from github.com/notofonts/noto-cjk)

**Font fallback chain** (in CSS): `"Noto Sans CJK SC", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif`

## Prerequisites

The conversion script requires **weasyprint** and **markdown** Python libraries on the **system Python** (not WorkBuddy's isolated Python), because weasyprint needs system-level pango/gobject libraries.

```bash
/opt/homebrew/bin/pip3 install --break-system-packages weasyprint markdown
```

**Font installation** (one-time, if Noto Sans CJK SC is not already installed):

```bash
mkdir -p ~/Library/Fonts
curl -L -o ~/Library/Fonts/NotoSansCJKsc-Regular.otf "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf"
curl -L -o ~/Library/Fonts/NotoSansCJKsc-Bold.otf "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf"
```

> Use jsdelivr CDN (not raw GitHub) — much faster in China.

## Usage

Run the script with the system Python:

```bash
/opt/homebrew/bin/python3 scripts/md_to_pdf.py <input.md> [output.pdf]
```

If `output.pdf` is omitted, it uses the same basename as the input file.

### Example

```bash
/opt/homebrew/bin/python3 scripts/md_to_pdf.py \
  "/path/to/document.md" \
  "/path/to/document.pdf"
```

## What It Does

1. Reads the Markdown file with `markdown` library (extensions: tables, fenced_code, toc, nl2br, sane_lists)
2. Wraps the HTML with **inline CSS** (defined in the script itself; `assets/pandoc_chinese.css` is a standalone copy kept for reference)
3. Renders to PDF with weasyprint using **Noto Sans CJK SC** as the primary Chinese font (embedded as CFF subset via FontFile3)

## PDF Styling

- A4 page size, 2cm margins
- Blue (#2563eb) table headers, alternating row colors
- Dark background code blocks (#1e293b)
- Blue left-border blockquotes with light background
- Page breaks before each H1 (except the first)
- h2/h3 headings: `break-after: avoid` (headings never orphaned at page bottom)
- Tables: `table-layout: fixed` + **script auto-generates `<colgroup>`: content-driven floors + water-filling allocation of remaining width**（2026-08-16 v4 终版；weasyprint 对 `table-layout:auto` 支持弱，长文本列会把窄列压成单字竖排——「竖排文字」问题的标准解法即 fixed + 显式列宽 + `word-break: break-word`，详见 Troubleshooting）
- Tables: `page-break-inside: auto` + `thead: table-header-group` (long tables break across pages with repeated headers; short tables stay on one page)
- `tr: page-break-inside: avoid` (individual rows never split across pages)

## When to Use

- User asks to "generate PDF" or "convert to PDF" from a Markdown file
- User wants a formatted export of an analysis document, report, or memo
- File contains Chinese text, tables, or code blocks

## 底稿版 vs 汇报版（双版工作流，2026-08-15 Tom 确认）

调研报告的 **Markdown 底稿**与**对外汇报 PDF** 是两个产物，不得直接把底稿转 PDF 对外。**全流程：底稿 md → （汇报版）.md → 原名.pdf**，只此一条产物链，不生成"底稿 PDF"（底稿 md 足够用于内部追溯与后续迭代）：

- **底稿（工作文档，`原名.md`）**：保留完整审计痕迹——`依据`（引用来源清单）、`修正记录`（审查改动日志）、正文中的「初稿引用…⚠️更正」标注。这些是内部质量控制用的，对外暴露审查过程不合适。
- **汇报版（中间文档，`原名（汇报版）.md`）**：转 PDF 前先生成，剥离六类内容。**文件存放位置由调用方 skill 或项目交付约定决定，本 skill 不规定**（2026-08-16 Tom 确认：存放是交付组织策略，不同场景不同——项目级交付可用源文档结构、新闻深挖类平铺每日简报文件夹——由调用方决定；本 skill 专注转换与剥离规范）。剥离内容：
  1. 头部 `依据` 行与 `修正记录` 块；
  2. 正文内嵌的审查痕迹（「初稿写…⚠️更正」改为直接陈述更正后的事实；「勘误声明」「关键纠正：首版误判…」等草稿历史叙述整段删除——其事实性结论应在正文以直接陈述存在）；
  3. 内部指代（如「（Tom 确认）」「待一线核实」等面向内部流程的标注，酌情保留或删）；
  4. **面向内部的「使用提示/说明」整节**（2026-08-17 Tom 确认）：凡标题为「内部使用提示」「对外使用提示」「注意事项」等、内容为写作者自用的节——对接人姓名核实、公文格式规范、表述红线、保密提示等——**整节删除，不进入对外版本与 PDF**；此类节中的政府/监管对接人具体姓名等敏感信息，底稿中也应脱敏（用职务简称替代），防止底稿被误转发。
  5. **头部背景/撰写缘起引用块**（2026-08-17 Tom 确认）：文档头部说明「应某部门/某人咨询而写」的背景块、名称辨析导语、撰写方式说明等内部上下文，对外版一并剥离——对外 PDF 直接以标题+分析时间行+正文开始；必要信息（如名称对应关系）应在正文以直接陈述存在。
  6. **名称辨析/勘误类条目**（2026-08-17 Tom 确认）：口径说明等节中的名称纠错条目（「X（音）=Y」的同音/拆字辨析、"两种写法并存"的考据、"回复 XX 方时建议用全称"等）属**勘误内容**——自己调研的底稿可以存在，对外 PDF 一律删除；正文中的品牌名/主体名直接用正确名称陈述，不出现辨析过程。同类一并清理：「建议 XX 时标注/建议以…为准」等写作者自用建议、「待核实」内部行动标记、「若 XX 方追问/向 XX 方说明」的对接场景引用（含小节标题）。
  - **注意区分**：✅/⚠️/❌ 三态状态标注、口径时点标注（如「2022-10 披露」「泰乾方披露口径」）是**信息内容**，必须保留，不属于审查痕迹。
- **最终 PDF 命名用原名（`原名.pdf`），不带「（汇报版）」等任何后缀**——后缀只用于中间 md 区分底稿，不进入最终交付物名称。转换命令：`md_to_pdf.py "原名（汇报版）.md" "原名.pdf"`。
- 底稿 md 永远不动；中间 md 保留（便于后续改稿重转）；最终 PDF 就是唯一对外交付物。
- 若用户只说「生成 PDF」且文档含修正记录/依据块，默认走双版工作流，并告知用户。

## 分享场景规范（2026-08-16 Tom 确认，必读）

**Tom 的投资调研 PDF 是分享给朋友的，不是给领导/同事的汇报**。生成 PDF 时：

1. **禁止自造"汇报"封面章节**：不加「XX调研汇报」标题页、不加「汇报日期/汇报对象/致XX」头页、不加「本汇报经X轮审查勘误后定稿」等过程说明。多份报告合并转 PDF 时也**不造封面页**——直接以第一份报告的 H1 开头（正文从第一页顶部开始），后续报告的 H1 自动分页即可。
   - 历史教训：2026-08-14 生泰尔报告合并时自造了"汇报"封面（H1+日期引用块，仅3行），叠加 CSS `h1 { page-break-before: always }` 导致第一篇正文强制另起页，**首页出现大范围空白**。根因=封面内容过少+H1强制分页。
2. **文档标题与文件名不带修改过程说明**：禁止「（含重大纠错）」「（二轮审查修订版）」「（勘误版）」类后缀——改完不需要告诉读者。允许带**信息量关键词**（如「（动保/宠物药，A股港股标的梳理）」）帮助读者快速定位主题。
3. 对朋友的分享版语气：直接给结论与证据链，不需要"汇报体"措辞（不必出现"汇报"二字）。

## Troubleshooting

- **ModuleNotFoundError: weasyprint** → Run the `pip3 install --break-system-packages weasyprint markdown` command above
- **OSError: cannot load library 'libgobject-2.0-0'** → Script is running on WorkBuddy's isolated Python. Must use system Python (`/opt/homebrew/bin/python3`)
- **PDF has garbled Chinese characters** → Check: (1) Noto Sans CJK SC fonts installed in `~/Library/Fonts/`; (2) fonts are embedded in the PDF (use `pikepdf` to verify FontFile3 in FontDescriptor → DescendantFonts); (3) CSS font-family includes `"Noto Sans CJK SC"` as first choice
- **WeChat garbled text** → Ensure fonts are embedded (not just referenced). Noto Sans CJK SC's standardised CFF data has better cross-viewer compatibility than PingFang SC. If issues persist on Android WeChat, consider switching to a TrueType-format font (e.g., system STHeiti which is TrueType-based)
- **Font download slow** → Use jsdelivr CDN URL (above), not raw GitHub. GitHub raw is very slow in China.
- **表格窄列文字竖排（单字一行）/ 标签列过宽 / 短内容列大片空白**（2026-08-16 两轮修复，weasyprint 表格列宽完整经验）→
  根因：weasyprint 对 `table-layout:auto` 支持弱，列宽分配不可控。脚本内置三层修复，已验证的三类症状与解法：
  1. **窄列竖排**（长文本列把标签列压到单字宽）：`table-layout:fixed` + 脚本自动生成 `<colgroup>`（按列内容显示宽度分配：CJK=1.0、ASCII=0.6，权重上限14防长列独大）+ `word-break:break-word`；
  2. **标签列过宽、内容列拥挤**（2列概况表典型）：列宽**下限必须内容驱动**——每列保底=该列最长单行内容所需宽度换算%，且不超过等分，**不能用"等分×0.8"这类固定下限**（会把2列表的标签列抬到40%）；
  3. **列宽上限不能用固定值（如35%）**：会把2列表的内容列从70%压到35%、标签列反被撑宽。正确上限=**100%减去其他各列下限之和**（保证各列拿到保底的同时，内容列可自由占大头）。

  **2026-08-16 第三轮追加（v4 终版算法，两个隐蔽陷阱）**：
  4. **"钳制后归一化"会侵蚀下限**：若先算目标比例、再对每列做下限/上限钳制、最后除以总和（>100%）归一——归一化除法会把已满足下限的列重新压到保底以下。症状：4字公司名仍换行成 3+1 字、长名单里最长的名字（如"中国动物保健品"6+1字）反而换行而短名不换。**正解=注水法（water-filling）分配**：每列先精确拿到下限，剩余空间按 `(目标比例-下限)` 的差值比例分配、逐列受上限约束，**分配完成后绝不再归一化**；若有残余空间（全部列触顶）才均分。
  5. **pt 换算必须留安全余量**：9pt 字号下 CJK 实际步进约 9.03pt，若按理论值取整（9.0pt）则 4 字名需要 36.1pt 而列宽恰好 36pt——差 0.1pt 就换行。脚本取 `CHAR_PT=9.6`（步进+余量）、`PAD_PT=16`（cell 内边距约9pt+边框1.5pt+余量）、`TABLE_PT=470`（A4 595pt − 2×2.2cm 边距）。
  6. **竖排检测器阈值**：单字符行扫描的行距阈值必须 **<18pt**（用 <16pt 会漏检恰好 16pt 行距的换行，产生假阴性）；且按 y 坐标聚合行时不能用 y 做 dict key（同一行不同列的线会互相覆盖），应收集全部线段再去重。验证方法：PyMuPDF 提取表格竖线x坐标测实际列宽 + 上述单字符行扫描。
- **文档头部信息行规范（2026-08-16 Tom 确认）** → 分享版 PDF 的头部信息行固定为 `> 分析时间: YYYY-MM | 分析人: Tom Han`——**"分析时间"必须有、"分析人：Tom Han"并列署名；"更新模式"等内部流程字段不出现**（读者不关心谁更新的）。
