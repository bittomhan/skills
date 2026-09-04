#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回滚上一轮「冗余副标题」清理中的误删：正式抬头/说明性副标题应保留。
仅保留对 TRM / Cyber 两处真正冗余副标题的删除。"""
import os, re

ROOT = "/Users/bittom/Desktop/GT"
BK = {"mpi": "/tmp/gt_backup_mpi", "cms": "/tmp/gt_backup_cms"}

# 当前文件 → (备份相对根, 备份内相对路径前缀)
RESTORE = [
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S4-01_最低资本金证明SM/GemTrust Stable｜Board Resolution — Capital Injection Undertaking & Support Letter（MPI-S4-01）.md", "mpi"),
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S4-01_最低资本金证明SM/GemTrust Stable｜Board Resolution — Capital Injection Undertaking & Support Letter（MPI-S4-01）_CN.md", "mpi"),
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S4-04_外部审计师委任函/GemTrust Stable｜Board Resolution — Appointment of External Auditor（MPI-S4-04）.md", "mpi"),
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S4-04_外部审计师委任函/GemTrust Stable｜Board Resolution — Appointment of External Auditor（MPI-S4-04）_CN.md", "mpi"),
 ("Gemtrust/CMS_Capital/递交前提交/CMS-S4-05_外部审计师委任函/GemTrust Capital｜Board Resolution — Appointment of External Auditor（CMS-S4-05）.md", "cms"),
 ("Gemtrust/CMS_Capital/递交前提交/CMS-S4-05_外部审计师委任函/GemTrust Capital｜Board Resolution — Appointment of External Auditor（CMS-S4-05）_CN.md", "cms"),
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S4-02_财务报表/GemTrust Stable｜Financial Statements & Financial Resources Adequacy（Explanatory Note）.md", "mpi"),
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S4-03_财务资源充足证明/GemTrust Stable｜Financial Statements & Financial Resources Adequacy（Explanatory Note）.md", "mpi"),
 ("Stable/Policy/GemTrust Stable｜Financial Statements & Financial Resources Adequacy（Explanatory Note）.md", "mpi"),
 ("Gemtrust/CMS_Capital/递交前提交/CMS-S8-01_商业计划书CMS口径/GemTrust Capital Business Plan - CMS Licence Application.md", "cms"),
 ("Capital/BP/GemTrust Capital Business Plan - CMS Licence Application.md", "cms"),
 ("Gemtrust/MPI_Stable/递交前提交/MPI-S8-05_企业风险评估/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md", "mpi"),
 ("Stable/Policy/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md", "mpi"),
]

# 备份内查找同名文件的辅助：按 basename 在备份树中搜索
def find_backup(broot, rel):
    base = os.path.basename(rel)
    for dp, dns, fns in os.walk(broot):
        if base in fns:
            return os.path.join(dp, base)
    return None

def h1_index(lines):
    for i, l in enumerate(lines):
        if l.startswith("# "):
            return i
    return None

def backup_subtitle(bpath):
    """取备份中 H1 之后的第一个 H2（即被误删的那行）"""
    lines = open(bpath, encoding="utf-8", errors="ignore").read().split("\n")
    i = h1_index(lines)
    if i is None:
        return None
    j = i + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j < len(lines) and lines[j].startswith("## "):
        return lines[j]
    return None

n = 0
for rel, key in RESTORE:
    cur = os.path.join(ROOT, rel)
    b = find_backup(BK[key], rel)
    if not b:
        print(f"  ⚠️  备份未找到，跳过: {os.path.basename(rel)}")
        continue
    sub = backup_subtitle(b)
    if not sub:
        print(f"  ⚠️  备份无副标题，跳过: {os.path.basename(rel)}")
        continue
    lines = open(cur, encoding="utf-8", errors="ignore").read().split("\n")
    i = h1_index(lines)
    if i is None:
        print(f"  ⚠️  当前无 H1，跳过: {os.path.basename(rel)}")
        continue
    # 若 H1 之后已有该 H2，则不重复插入
    j = i + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j < len(lines) and lines[j].strip() == sub.strip():
        continue
    lines.insert(i + 1, "")
    lines.insert(i + 2, sub)
    open(cur, "w", encoding="utf-8").write("\n".join(lines))
    n += 1
    print(f"  ✅ 已恢复: {os.path.basename(rel)[:52]}  ← {sub[:52]}")

print(f"\n共恢复 {n} 处")
