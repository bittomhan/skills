#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MPI/CMS 政策套件一致性扫描（只读，不修改任何文件）"""
import os, re, hashlib, datetime

ROOT = "/Users/bittom/Desktop/GT"
TREES = {
    "CMS": os.path.join(ROOT, "Gemtrust/CMS_Capital/递交前提交"),
    "MPI": os.path.join(ROOT, "Gemtrust/MPI_Stable/递交前提交"),
}
# 源树 = {Capital,Stable}/Policy/ + {Capital,Stable}/BP/（项目约定：两者都是源树）
# 09-02 修正：原脚本只扫 Policy/，导致 BP、白皮书、记录保留计划等被误报「无源」
SRC = {
    "CMS": [os.path.join(ROOT, "Capital/Policy"), os.path.join(ROOT, "Capital/BP")],
    "MPI": [os.path.join(ROOT, "Stable/Policy"), os.path.join(ROOT, "Stable/BP")],
}

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def wc(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    cn = len(re.findall(r"[\u4e00-\u9fff]", t))
    # 去掉中文后统计英文单词
    en_only = re.sub(r"[\u4e00-\u9fff]", " ", t)
    en = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", en_only))
    return cn + en, cn, en

print("=" * 100)
print("【A】命名规范违规扫描")
print("=" * 100)
bad_suffix = re.compile(r"（(英文版|中文版|中文对照版|中文|EN版|CN版)）|·中文|·EN")
bad_brand = re.compile(r"Gemtrust(?! )")  # Gemtrust 后不是空格（即 GemtrustX）
viol = []
for tag, d in TREES.items():
    for dp, dns, fns in os.walk(d):
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, ROOT)
            if bad_suffix.search(fn):
                viol.append((tag, "版本后缀", rel))
            if re.search(r"Gemtrust(?!\s)", fn):
                viol.append((tag, "品牌拼写", rel))
for tag, kind, rel in sorted(viol):
    print(f"  [{tag}] {kind}: {rel}")
print(f"  → 合计 {len(viol)} 项")

print()
print("=" * 100)
print("【B】md ↔ PDF 同步（PDF 早于 md 即为落后）")
print("=" * 100)
stale = []
for tag, d in TREES.items():
    for dp, dns, fns in os.walk(d):
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            mdp = os.path.join(dp, fn)
            pdf = mdp[:-3] + ".pdf"
            if not os.path.exists(pdf):
                print(f"  [{tag}] 缺 PDF: {os.path.relpath(mdp, ROOT)}")
                continue
            mt_md = datetime.datetime.fromtimestamp(os.path.getmtime(mdp))
            mt_pdf = datetime.datetime.fromtimestamp(os.path.getmtime(pdf))
            if mt_pdf < mt_md:
                stale.append((tag, os.path.relpath(mdp, ROOT),
                              mt_md.strftime("%m-%d %H:%M"), mt_pdf.strftime("%m-%d %H:%M")))
for tag, rel, a, b in stale:
    print(f"  [{tag}] PDF落后: {rel}  md {a} > pdf {b}")
print(f"  → 落后合计 {len(stale)} 项")

print()
print("=" * 100)
print("【C】源(Capital|Stable/Policy) ↔ 递交副本 内容差异")
print("=" * 100)
# 建源索引：按 basename 归一化
def norm(s):
    s = s.replace("Gemtrust", "GemTrust")
    s = re.sub(r"（(英文版|中文版|中文对照版|中文|EN版|CN版)）", "_CN", s)
    s = re.sub(r"_CN_CN", "_CN", s)
    return s

srcidx = {}
for tag, dirs in SRC.items():
    for d in dirs:  # 09-02: SRC 值为目录列表（Policy + BP）
        if not os.path.isdir(d):
            continue
        for dp, dns, fns in os.walk(d):
            for fn in fns:
                if fn.endswith(".md"):
                    srcidx.setdefault(norm(fn), []).append((tag, os.path.join(dp, fn)))

diffs = []
missing_src = []
for tag, d in TREES.items():
    for dp, dns, fns in os.walk(d):
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            key = norm(fn)
            cands = srcidx.get(key) or srcidx.get(norm(fn.replace("_CN", "_CN")))
            if not cands:
                missing_src.append((tag, os.path.relpath(p, ROOT)))
                continue
            # 取同 tag 的源
            same = [c for c in cands if c[0] == tag] or cands
            sp = same[0][1]
            if md5(sp) != md5(p):
                diffs.append((tag, os.path.relpath(p, ROOT), os.path.relpath(sp, ROOT)))
for tag, rel in sorted(missing_src):
    print(f"  [{tag}] 无源: {rel}")
print()
for tag, rel, srel in sorted(diffs):
    print(f"  [{tag}] 内容不一致:\n      副本 {rel}\n      源   {srel}")
print(f"  → 无源 {len(missing_src)} 项 / 不一致 {len(diffs)} 项")

print()
print("=" * 100)
print("【D】递交树 md 字数（中文字符+英文单词）+ 生效日期行检查")
print("=" * 100)
hdr_bad = []
for tag, d in TREES.items():
    rows = []
    for dp, dns, fns in os.walk(d):
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            t = open(p, encoding="utf-8", errors="ignore").read()
            head = "\n".join(t.split("\n")[:12])
            has_eff = bool(re.search(r"(生效日期|Effective date|Effective Date)", head))
            has_ver = bool(re.search(r"(Version\s*[0-9]|版本\s*v?[0-9]|DRAFT|初稿|待律所审查)", t))
            if not has_eff or has_ver:
                hdr_bad.append((tag, os.path.relpath(p, ROOT), has_eff, has_ver))
            rows.append((fn, wc(p)))
    print(f"\n--- {tag} 树 ---")
    for fn, (tot, cn, en) in rows:
        print(f"  {tot:>6}  (CN {cn:>5} / EN {en:>5})  {fn}")
print()
print("  头部/版本标记异常：")
for tag, rel, he, hv in sorted(hdr_bad):
    print(f"  [{tag}] 生效日期={he} 含版本痕迹={hv}  {rel}")
print(f"  → 异常 {len(hdr_bad)} 项")
