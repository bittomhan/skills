#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一人名为标准式（Tom 09-01 指令）：
  俞晓鹏 / Yu Xiaopeng ；韩悠阳 / Han Youyang
  （Ma Qing / Li Hua 一并按 BP 既有标准式统一，避免同包内大小写混用）
中文文档中补中文全名，格式：中文名（English Name）
仅处理递交材料与政策树；ACRA/护照逐字记录（公司信息/）不动。
"""
import os, re, shutil

ROOT = "/Users/bittom/Desktop/GT"

SCOPES = [
    "Gemtrust/MPI_Stable/递交前提交",
    "Gemtrust/CMS_Capital/递交前提交",
    "Stable/Policy",
    "Capital/Policy",
    "Stable/BP",
    "Capital/BP",
]

EXCLUDE_DIR_MARK = ("_归档", "归档")
EXCLUDE_FILE = ("GemTrust｜MPI递交材料缺口清单.md", "GemTrust｜CMS递交材料缺口清单.md")

def is_cn(path):
    """CN 文档判定：文件名以 _CN 结尾，或正文中文字符占比高"""
    base = os.path.basename(path)
    if base.endswith("_CN.md"):
        return True
    if base.endswith("_CN.pdf"):
        return True
    t = open(path, encoding="utf-8", errors="ignore").read()
    cn = len(re.findall(r"[\u4e00-\u9fff]", t))
    total = max(len(re.sub(r"\s", "", t)), 1)
    return cn / total > 0.25

def fix(text, cn_doc):
    orig = text

    # ---- 1) 大小写统一（先做，便于后续补中文名） ----
    text = re.sub(r"\bHAN Youyang\b", "Han Youyang", text)
    text = re.sub(r"\bYU Xiaopeng\b", "Yu Xiaopeng", text)
    text = re.sub(r"\bMA QING\b", "Ma Qing", text)
    text = re.sub(r"\bMA Qing\b", "Ma Qing", text)
    text = re.sub(r"\bLI HUA\b", "Li Hua", text)

    if cn_doc:
        # ---- 2) 中文文档补中文全名 ----
        # 俞晓鹏：若 "Yu Xiaopeng" 前后 6 字符内尚无「俞晓鹏」，则补为 俞晓鹏（Yu Xiaopeng）
        def add_yu(m):
            s = m.group(0)
            return s  # 占位，下面用 lookaround 处理
        # 已有中文名在右侧：Yu Xiaopeng（俞晓鹏）→ 俞晓鹏（Yu Xiaopeng）
        text = re.sub(r"\bYu Xiaopeng（俞晓鹏）", "俞晓鹏（Yu Xiaopeng）", text)
        text = re.sub(r"\bYu Xiaopeng（俞总）", "俞晓鹏（Yu Xiaopeng）", text)
        # 已有中文名在左侧：俞晓鹏（Yu Xiaopeng）保持不动
        # 裸英文名 → 补中文名（避免已在括号内 / 已有中文名相邻时重复）
        text = re.sub(r"(?<![\u4e00-\u9fff])Yu Xiaopeng(?![\u4e00-\u9fff])(?!（)", "俞晓鹏（Yu Xiaopeng）", text)
        # 韩悠阳：已有「韩悠阳（Han Youyang）」不动；裸英文补中文
        text = re.sub(r"(?<![\u4e00-\u9fff])Han Youyang(?![\u4e00-\u9fff])(?!（)", "韩悠阳（Han Youyang）", text)

    return text, (text != orig)

changed = []
for scope in SCOPES:
    d = os.path.join(ROOT, scope)
    if not os.path.isdir(d):
        continue
    for dp, dns, fns in os.walk(d):
        if any(m in dp for m in EXCLUDE_DIR_MARK):
            continue
        for fn in sorted(fns):
            if not fn.endswith(".md") or fn in EXCLUDE_FILE:
                continue
            p = os.path.join(dp, fn)
            t = open(p, encoding="utf-8", errors="ignore").read()
            cn = is_cn(p)
            nt, ch = fix(t, cn)
            if ch:
                open(p, "w", encoding="utf-8").write(nt)
                changed.append((scope, fn, "CN" if cn else "EN"))

print(f"已修改 {len(changed)} 份：")
cur = None
for scope, fn, lang in changed:
    if scope != cur:
        print(f"\n  [{scope}]")
        cur = scope
    print(f"      ({lang}) {fn[:70]}")
