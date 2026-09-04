#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""源↔副本 新旧方向判定 + 源文件夹命名扫描"""
import os, re, hashlib, datetime

ROOT = "/Users/bittom/Desktop/GT"
TREES = {"CMS": "Gemtrust/CMS_Capital/递交前提交", "MPI": "Gemtrust/MPI_Stable/递交前提交"}
SRC = {"CMS": "Capital/Policy", "MPI": "Stable/Policy"}

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def norm(s):
    s = re.sub(r"Gemtrust(?!\s)", "GemTrust", s)
    s = re.sub(r"（(英文版|中文版|中文对照版|中文|EN版|CN版)）", "_CN", s)
    s = re.sub(r"·中文", "_CN", s); s = re.sub(r"·EN", "", s)
    s = s.replace("_CN_CN", "_CN")
    return s

srcidx = {}
for tag, rel in SRC.items():
    d = os.path.join(ROOT, rel)
    for dp, dns, fns in os.walk(d):
        for fn in fns:
            if fn.endswith(".md"):
                srcidx.setdefault((tag, norm(fn)), []).append(os.path.join(dp, fn))

print("=" * 100)
print("【C2】源↔副本 新旧方向（同一文档两个副本 mtime 对比）")
print("=" * 100)
cnt_newer_copy = cnt_newer_src = 0
for tag, rel in TREES.items():
    d = os.path.join(ROOT, rel)
    for dp, dns, fns in os.walk(d):
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            cands = srcidx.get((tag, norm(fn)))
            if not cands:
                continue
            sp = cands[0]
            if md5(sp) == md5(p):
                continue
            mt_c = os.path.getmtime(p); mt_s = os.path.getmtime(sp)
            f = lambda t: datetime.datetime.fromtimestamp(t).strftime("%m-%d %H:%M")
            who = "副本新" if mt_c > mt_s else "源新"
            if mt_c > mt_s: cnt_newer_copy += 1
            else: cnt_newer_src += 1
            print(f"  [{tag}] {who}  副本 {f(mt_c)} | 源 {f(mt_s)}  {os.path.relpath(p, rel)}")
print(f"\n  → 副本较新 {cnt_newer_copy} 份 / 源较新 {cnt_newer_src} 份")

print()
print("=" * 100)
print("【A2】源文件夹（Capital/Policy、Stable/Policy）命名规范违规")
print("=" * 100)
bad = 0
for tag, rel in SRC.items():
    d = os.path.join(ROOT, rel)
    for dp, dns, fns in os.walk(d):
        for fn in sorted(fns):
            issues = []
            if re.search(r"Gemtrust(?!\s)", fn):
                issues.append("品牌拼写Gemtrust")
            if re.search(r"（(英文版|中文版|中文对照版|中文)）|·中文|·EN", fn):
                issues.append("版本后缀")
            if issues:
                bad += 1
                print(f"  [{tag}] {','.join(issues)}: {fn}")
print(f"  → 合计 {bad} 项")

print()
print("=" * 100)
print("【E】源文件夹内 md 是否含版本痕迹 / 生效日期行")
print("=" * 100)
n = 0
for tag, rel in SRC.items():
    d = os.path.join(ROOT, rel)
    for dp, dns, fns in os.walk(d):
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            t = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
            head = "\n".join(t.split("\n")[:10])
            eff = bool(re.search(r"(生效日期|Effective date|Effective Date)", head))
            ver = bool(re.search(r"(Version\s*[0-9]|版本\s*v?[0-9]\.[0-9]|DRAFT|初稿|待律所审查|Correction Log|修正记录)", t))
            if not eff or ver:
                n += 1
                print(f"  [{tag}] 生效日期={eff} 版本痕迹={ver}  {fn}")
print(f"  → 异常 {n} 项")
