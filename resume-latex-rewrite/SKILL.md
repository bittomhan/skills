---
name: resume-latex-rewrite
description: 把简陋简历（PDF/docx）改写为 billryan resume LaTeX 模板精装版（中/英文 .tex）。当用户要求"帮某人生成简历/改写简历/做成 LaTeX 简历"并给出简历源文件时使用。固化版式（与 Tom 本人简历同款）、内容纪律（不虚构）、交付方式（只交 .tex，Tom 自行 Overleaf 编译）。
---

# 简历 LaTeX 改写（billryan resume 模板）

## 触发
- 「帮 XX 生成简历」「改写简历」「简历太简陋，按模板改」，源通常是 PDF（docx 转的）。
- 已做案例：刘欢（2026-08-18，中文版）、马清（2026-08-19，中英文双版）。

## 模板与参照
- 模板：billryan/resume（XeLaTeX；resume.cls + zh_CN-Adobefonts_external.sty + linespacing_fix.sty + fontawesome + fonts/ 目录）。
- 版式真源：`~/Desktop/韩悠阳资料/resume/TomHan.tex` 及编译效果 `韩悠阳+2605.pdf`（同名目录）。
- 用户 Overleaf 上已有该模板工程：交付 .tex 后，用户把内容整体替换主 .tex 文件、XeLaTeX 编译即可。
- **本机无 TeX 环境（无 xelatex/tectonic），不要搭建、不要安装**（2026-08-18 Tom 明确确认）。

## 结构模板
1. preamble 原样保留（\documentclass{resume} + zh_CN-Adobefonts_external + linespacing_fix + cite + fontawesome，含注释行）。
2. `\name{姓名 拼音大写}`；`\basicInfo`：\email{} · \phone{} · \faMapMarker\ 现居 · \faBriefcase\ 求职意向/头衔。
3. 分节顺序（图标仅用 FA4 安全集）：\faUser 综合能力（加粗定位句 + 3–5 个「维度加粗 + 成果导向」条目）→ \faInstitution 工作经历（\datedsubsection 倒序，职责领域加粗）→ \faTasks 项目业绩（可选；金额放右侧日期位，按金额降序）→ \faCogs 技能 → \faGraduationCap 教育经历收尾。
4. 文件顶部加注释说明 Overleaf 用法。

## 内容纪律（重要）
- 数字、客户、金额、日期只用源简历已有内容，**不虚构、不加料**；外部信息（如任职公司集团）即使已知也先问用户是否纳入。
- 源简历流水账压缩为「职责领域加粗 + 一句成果导向」；空话填充（"积极参加活动"类）可删或轻量保留。
- 日期空档与重叠按原样保留，并在回复中标注提醒。
- **不把 Tom 自己 tex 里的私人策略注释复制进他人简历。**
- 修正源简历明显拼写错误（案例：MANDARIAN→Mandarin、PNUEMATIC→Pneumatic、NEGOTITION→negotiation）。
- **英文版公司名一律从中文音译（拼音），不意译**（2026-08-19 Tom 确认；案例：风动机械厂→Fengdong Machinery Factory、经营贸易公司→Jingying Trading Company、珠江商贸→Zhujiang Trading Co., Ltd.）。
- 回复末尾明确列出所有推断项（现居地、任职起始时间、公司英文名等）请 Tom 核实。

## 流程
1. 提取源 PDF 文本：`/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python` + pymupdf（fitz），逐页 `page.get_text()`。
2. 按结构模板写 .tex（中文/英文各一份，按用户要求）。
3. `present_files` 交付；回复中简述改写要点 + 待核实清单。

## 链接同步（2026-08-21 经验，改写已有 .tex 时必用）
- 当源是**已含大量 `\href` 的 .tex**（如 TomHan.tex 有 161 条 notion/长 URL）时，**禁止手抄链接 ID**——32 位 ID 手抄必错位。标准做法：
  1. 先正则提取全部 `\href{...}` 到编号清单（H01…Hnn）作真源；
  2. 新 tex 中链接处写 `{{Hxx}}` 占位符；
  3. 脚本按 token 回填并校验：tokens used / missing / unreplaced 全零 + CJK 残留扫描（英文版应为空）。
- 源 tex 中被注释掉的内容块不纳入新版（提取真源时注意区分注释行）。
