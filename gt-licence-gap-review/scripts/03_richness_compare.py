#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""源 vs 副本 内容量对比（判断哪一侧更完整）"""
import os, re, difflib

ROOT = "/Users/bittom/Desktop/GT"
PAIRS = [
    ("CMS-S8-03 合规手册", "Capital/Policy/GemTrust Capital｜Compliance Manual（CMS-S8-03）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-03_合规手册/GemTrust Capital｜Compliance Manual（CMS-S8-03）.md"),
    ("CMS-S8-04 AML", "Capital/Policy/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-04_AML-CFT政策AMLOMA/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）.md"),
    ("CMS-S8-05 RMF", "Capital/Policy/GemTrust Capital｜Risk Management Framework（CMS-S8-05）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-05_风险管理框架/GemTrust Capital｜Risk Management Framework（CMS-S8-05）.md"),
    ("CMS-S8-05 RMF_CN", "Capital/Policy/GemTrust Capital｜风险管理框架（CMS-S8-05·中文）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-05_风险管理框架/GemTrust Capital｜风险管理框架（CMS-S8-05·中文）.md"),
    ("CMS-S8-10 TRM", "Capital/Policy/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-10_技术风险管理政策TRM/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）.md"),
    ("CMS-S8-11 Cyber", "Capital/Policy/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-11_网络卫生文件/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）.md"),
    ("CMS-S8-06 COI", "Capital/Policy/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-06_利益冲突政策/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）.md"),
    ("CMS-S8-07 Complaints", "Capital/Policy/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-07_投诉处理政策/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）.md"),
    ("CMS-S8-08 IA", "Capital/Policy/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-08_内部审计安排/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）.md"),
    ("CMS-S8-09 Outsourcing", "Capital/Policy/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-09_外包政策登记/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）.md"),
    ("CMS-S10-01 F&P", "Capital/Policy/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S10-01_Fit-Proper声明/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）.md"),
    ("CMS-S4-03 FinRes", "Capital/Policy/GemTrust Capital｜Financial Resources Adequacy（CMS-S4-03）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S4-03_财务资源充足证明/GemTrust Capital｜Financial Resources Adequacy（CMS-S4-03）.md"),
    ("MPI-S8-05 EWRA", "Stable/Policy/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-05_企业风险评估/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md"),
    ("MPI-S8-07 合规手册", "Stable/Policy/GemTrust Stable｜Compliance Manual（MPI-S8-07）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-07_合规手册/GemTrust Stable｜Compliance Manual（MPI-S8-07）.md"),
    ("MPI-S8-08 COI", "Stable/Policy/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-08_利益冲突政策/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）.md"),
    ("MPI-S8-09 Complaints", "Stable/Policy/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-09_投诉处理政策/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）.md"),
    ("MPI-S8-10 IA", "Stable/Policy/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-10_内部审计安排/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）.md"),
    ("MPI-S8-11 Outsourcing", "Stable/Policy/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-11_外包政策登记/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）.md"),
    ("MPI-S8-22 Custody", "Stable/Policy/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-22_客户资产保障与密钥管理/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy.md"),
    ("MPI-S8-23 Disclosure", "Stable/Policy/GemTrust Stable｜Disclosure & Regulatory Reporting Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Disclosure & Regulatory Reporting Policy.md"),
]

def wc(p):
    t = open(p, encoding="utf-8", errors="ignore").read()
    cn = len(re.findall(r"[\u4e00-\u9fff]", t))
    en = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", re.sub(r"[\u4e00-\u9fff]", " ", t)))
    return cn + en

print(f"{'文档':<26} {'源':>7} {'副本':>7} {'差':>7}   判定")
print("-" * 78)
tot_src = tot_cpy = 0
for name, s, c in PAIRS:
    sp, cp = os.path.join(ROOT, s), os.path.join(ROOT, c)
    if not os.path.exists(sp):
        print(f"{name:<26} {'—':>7} {'?':>7}  (源路径不存在)")
        continue
    if not os.path.exists(cp):
        print(f"{name:<26} {'?':>7} {'—':>7}  (副本路径不存在)")
        continue
    ws, wc_ = wc(sp), wc(cp)
    tot_src += ws; tot_cpy += wc_
    d = wc_ - ws
    verdict = "副本更完整" if d > 60 else ("源更完整" if d < -60 else "近似")
    print(f"{name:<26} {ws:>7} {wc_:>7} {d:>+7}   {verdict}")
print("-" * 78)
print(f"{'合计':<26} {tot_src:>7} {tot_cpy:>7} {tot_cpy-tot_src:>+7}")
