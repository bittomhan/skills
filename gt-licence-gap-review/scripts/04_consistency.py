#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨文档共享参数一致性核查"""
import os, re

ROOT = "/Users/bittom/Desktop/GT"
TREES = {"MPI": "Gemtrust/MPI_Stable/递交前提交", "CMS": "Gemtrust/CMS_Capital/递交前提交"}

# 共享参数：名称 -> 正则
PARAMS = {
    "赎回 5 个工作日": r"five business days|5 business days|5 个工作日|T\+5",
    "记录保存 5 年": r"five years|5 years|五年|5 年",
    "投诉确认 1 个工作日(MPI)": r"1 business day|one business day|1 个工作日",
    "投诉回复 15 个工作日(MPI)": r"15 business days|15 个工作日",
    "投诉确认 2 个工作日(CMS)": r"2 business days|two business days|2 个工作日",
    "投诉回复 10 个工作日(CMS)": r"10 business days|10 个工作日",
    "事件通报 1 小时": r"1 hour|one hour|1 小时",
    "根因报告 14 日": r"14 days|14 日|fourteen days",
    "RTO 4 小时": r"4 hours|four hours|4 小时|RTO",
    "月度 attestation": r"monthly attestation|月度鉴证|月度保证",
    "年度储备审计": r"annual audit|年度审计",
    "次月底前报 MAS": r"end of the following month|次月底",
    "最低赎回额 US$100k": r"100,000|10 万|100k",
    "冻结三情形": r"three circumstances|三情形|三种情形",
}

def scan(tag, rel):
    d = os.path.join(ROOT, rel)
    out = {}
    for dp, dns, fns in os.walk(d):
        if "_归档" in dp:
            continue
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            if "缺口清单" in fn:
                continue
            p = os.path.join(dp, fn)
            t = open(p, encoding="utf-8", errors="ignore").read()
            is_cn = bool(re.search(r"[\u4e00-\u9fff]", t)) and len(re.findall(r"[\u4e00-\u9fff]", t)) > 200
            lang = "CN" if is_cn else "EN"
            for name, pat in PARAMS.items():
                if re.search(pat, t, re.I):
                    out.setdefault((name, lang), []).append(os.path.relpath(p, d))
    return out

for tag, rel in TREES.items():
    print("=" * 88)
    print(f"【{tag} 递交树】共享参数命中分布")
    print("=" * 88)
    res = scan(tag, rel)
    for (name, lang), files in sorted(res.items()):
        print(f"\n  · {name} [{lang}] — {len(files)} 份")
        for f in sorted(files):
            print(f"        {f}")

print()
print("=" * 88)
print("【EN / CN 版本对称性检查】")
print("=" * 88)
for tag, rel in TREES.items():
    d = os.path.join(ROOT, rel)
    ens, cns = set(), set()
    for dp, dns, fns in os.walk(d):
        if "_归档" in dp:
            continue
        for fn in fns:
            if not fn.endswith(".md") or "缺口清单" in fn:
                continue
            base = fn[:-3]
            if base.endswith("_CN"):
                cns.add(base[:-3])
            else:
                ens.add(base)
    only_en = sorted(x for x in ens if x not in cns)
    only_cn = sorted(x for x in cns if x not in ens)
    print(f"\n  [{tag}] EN {len(ens)} 份 / CN {len(cns)} 份")
    if only_en:
        print(f"     ⚠️ 仅有 EN 无 CN（{len(only_en)}）：")
        for x in only_en:
            print(f"        {x}")
    if only_cn:
        print(f"     ⚠️ 仅有 CN 无 EN（{len(only_cn)}）：")
        for x in only_cn:
            print(f"        {x}")
