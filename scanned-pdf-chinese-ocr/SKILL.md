---
name: scanned-pdf-chinese-ocr
description: 中文扫描版 PDF 文字识别工作流（PyMuPDF 渲染 + tesseract OCR）。当用户要求把扫描版/图片型 PDF（无文本层）转成文字、提取中文扫描件内容、OCR 招标文件/合同/票据时使用。
agent_created: true
---

# 中文扫描版 PDF → 文字 工作流

> 来源：2026-08-25 鲁山粮库采购清单（42 页扫描件）实战验证。macOS 环境。

## 第零步：判断是否真的需要 OCR

先用 pypdf 试提取文本层，**有文本层就不要 OCR**：

```bash
python3 -c "
import pypdf
r = pypdf.PdfReader('文件.pdf')
print('pages:', len(r.pages))
print((r.pages[0].extract_text() or '')[:200])
"
```

输出为空/乱码 → 扫描件，走下面的流程。

## 推荐管线（已验证）

### 1. PyMuPDF 渲染每页为 PNG

```bash
/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python -c "
import fitz   # venv 已装 PyMuPDF；系统 python3 没有
doc = fitz.open('文件.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=120)          # 初筛用 120
    # 数量列等窄列要精读时重渲 dpi=250
    pix.save(f'/tmp/pages/p{i+1:02d}.png')
"
```

### 2. tesseract OCR（不要用 Vision 框架）

```bash
# 确认语言包（需 chi_sim）
tesseract --list-langs | grep chi_sim

cd /tmp/pages && for f in *.png; do
  b="${f%.png}"; tesseract "$f" "/tmp/${b}_out" -l chi_sim+eng --psm 6 2>/dev/null
done
cat /tmp/*_out.txt > /tmp/full_ocr.txt
```

**⚠️ 不要用 macOS Vision 框架（Swift VNRecognizeTextRequest）**：本机沙箱环境下 sanity 测试也返回 0 行（模型不可用），纯浪费时间。直接用 tesseract（homebrew 已装 tesseract + tesseract-lang）。

## 关键经验（踩过的坑）

1. **窄列（数量/单位）是最大失分区**。长参数列还原好，数量列数字经常错/丢。对策：
   - 精读页用 **dpi=250 重渲重跑**；
   - 用 `grep -n -E "(台|个|根|张|块|项|批|套)\s*[|｜]?\s*[0-9]+"` 批量抽取数量模式；
   - 同一份文档里多份同模板子表（如多个库点各一张相同清单）→ **横向交叉校验**：多数一致的值可信；单表独有差异先怀疑噪声再确认真差异；仍无法确定的标 ⚠️ 列入「待人工复核清单」，不要编造。
2. **先定位章节页码再精读**：`grep -l "章节标题" /tmp/p*_out.txt`，避免全量精读。
3. **--psm 6**（统一文本块）适合整页表格；个别页失败可试 psm 4。
4. 表格线会被 OCR 吃掉产生串行，**重建表格必须靠人读结构 + 数字交叉验证**，不能盲信行序。
5. 大 PDF（30MB+）渲染很慢的兜底：初筛 120dpi 全量 → 只对关键页 250dpi 重跑。
6. 向用户交付时必须附「OCR 质量声明」：哪些字段可信、哪些待人工复核——**宁可标注不确定，不可静默给错数**。
