#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""建立源树↔递交树文档映射，并列出递交树独有章节（需补入源树基底的内容）"""
import os, re, difflib

ROOT = "/Users/bittom/Desktop/GT"

PAIRS = [
    # (主题, 源EN, 源CN, 递交EN, 递交CN)
    ("CMS-AML", "Capital/Policy/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）.md",
     "Capital/Policy/GemTrust Capital｜反洗钱与反恐怖融资政策（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-04_AML-CFT政策AMLOMA/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-04_AML-CFT政策AMLOMA/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）_CN.md"),
    ("CMS-CM", "Capital/Policy/GemTrust Capital｜Compliance Manual（CMS-S8-03）.md",
     "Capital/Policy/GemTrust Capital｜合规手册（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-03_合规手册/GemTrust Capital｜Compliance Manual（CMS-S8-03）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-03_合规手册/GemTrust Capital｜Compliance Manual（CMS-S8-03）_CN.md"),
    ("CMS-RMF", "Capital/Policy/GemTrust Capital｜Risk Management Framework（CMS-S8-05）.md",
     "Capital/Policy/GemTrust Capital｜风险管理框架（CMS-S8-05·中文）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-05_风险管理框架/GemTrust Capital｜Risk Management Framework（CMS-S8-05）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-05_风险管理框架/GemTrust Capital｜风险管理框架（CMS-S8-05·中文）.md"),
    ("CMS-COI", "Capital/Policy/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）.md",
     "Capital/Policy/GemTrust Capital｜利益冲突政策（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-06_利益冲突政策/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-06_利益冲突政策/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）_CN.md"),
    ("CMS-Complaints", "Capital/Policy/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）.md",
     "Capital/Policy/GemTrust Capital｜投诉处理政策（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-07_投诉处理政策/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-07_投诉处理政策/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）_CN.md"),
    ("CMS-IA", "Capital/Policy/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）.md",
     "Capital/Policy/GemTrust Capital｜内部审计安排（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-08_内部审计安排/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-08_内部审计安排/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）_CN.md"),
    ("CMS-Outsourcing", "Capital/Policy/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）.md",
     "Capital/Policy/GemTrust Capital｜外包政策与登记册（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-09_外包政策登记/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-09_外包政策登记/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）_CN.md"),
    ("CMS-TRM", "Capital/Policy/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）.md",
     "Capital/Policy/GemTrust Capital｜技术风险管理政策（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-10_技术风险管理政策TRM/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-10_技术风险管理政策TRM/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）_CN.md"),
    ("CMS-Cyber", "Capital/Policy/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）.md",
     "Capital/Policy/GemTrust Capital｜网络卫生政策（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-11_网络卫生文件/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S8-11_网络卫生文件/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）_CN.md"),
    ("CMS-FP", "Capital/Policy/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）.md",
     "Capital/Policy/GemTrust Capital｜适当人选声明（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S10-01_Fit-Proper声明/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S10-01_Fit-Proper声明/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）_CN.md"),
    ("CMS-FinRes", "Capital/Policy/GemTrust Capital｜Financial Resources Adequacy（CMS-S4-03）.md",
     "Capital/Policy/GemTrust Capital｜财务资源充足证明（中文对照版）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S4-03_财务资源充足证明/GemTrust Capital｜Financial Resources Adequacy（CMS-S4-03）.md",
     "Gemtrust/CMS_Capital/递交前提交/CMS-S4-03_财务资源充足证明/GemTrust Capital｜Financial Resources Adequacy（CMS-S4-03）_CN.md"),
    ("MPI-AML", "Stable/Policy/Gemtrust Stable｜AML-CFT Policy（PSN02）.md",
     "Stable/Policy/GemTrust Stable｜反洗钱与反恐怖融资政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-03_AML-CFT政策PSN02/GemTrust Stable｜AML-CFT Policy（PSN02）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-03_AML-CFT政策PSN02/GemTrust Stable｜AML-CFT Policy（PSN02）_CN.md"),
    ("MPI-EWRA", "Stable/Policy/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md",
     "Stable/Policy/GemTrust Stable｜企业风险评估EWRA（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-05_企业风险评估/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-05_企业风险评估/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）_CN.md"),
    ("MPI-TRM", "Stable/Policy/Gemtrust Stable｜Technology Risk Management Policy（FSM-N13）.md",
     "Stable/Policy/GemTrust Stable｜技术风险管理政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-06_技术风险管理政策/GemTrust Stable｜Technology Risk Management Policy（FSM-N13）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-06_技术风险管理政策/GemTrust Stable｜Technology Risk Management Policy（FSM-N13）_CN.md"),
    ("MPI-CM", "Stable/Policy/GemTrust Stable｜Compliance Manual（MPI-S8-07）.md",
     "Stable/Policy/GemTrust Stable｜合规手册（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-07_合规手册/GemTrust Stable｜Compliance Manual（MPI-S8-07）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-07_合规手册/GemTrust Stable｜Compliance Manual（MPI-S8-07）_CN.md"),
    ("MPI-COI", "Stable/Policy/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）.md",
     "Stable/Policy/GemTrust Stable｜利益冲突政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-08_利益冲突政策/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-08_利益冲突政策/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）_CN.md"),
    ("MPI-Complaints", "Stable/Policy/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）.md",
     "Stable/Policy/GemTrust Stable｜投诉处理政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-09_投诉处理政策/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-09_投诉处理政策/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）_CN.md"),
    ("MPI-IA", "Stable/Policy/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）.md",
     "Stable/Policy/GemTrust Stable｜内部审计安排（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-10_内部审计安排/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-10_内部审计安排/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）_CN.md"),
    ("MPI-Outsourcing", "Stable/Policy/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）.md",
     "Stable/Policy/GemTrust Stable｜外包政策与登记册（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-11_外包政策登记/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-11_外包政策登记/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）_CN.md"),
    ("MPI-Cyber", "Stable/Policy/Gemtrust Stable｜Cyber Hygiene Policy（FSM-N14）.md",
     "Stable/Policy/GemTrust Stable｜网络卫生政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-12_网络卫生文件/GemTrust Stable｜Cyber Hygiene Policy（FSM-N14）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-12_网络卫生文件/GemTrust Stable｜Cyber Hygiene Policy（FSM-N14）_CN.md"),
    ("MPI-Reserve", "Stable/Policy/Gemtrust Stable｜Reserve Management Policy（英文版）.md",
     "Stable/Policy/Gemtrust Stable｜储备金管理政策（中文版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-18_储备管理政策/GemTrust Stable｜Reserve Management Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-18_储备管理政策/GemTrust Stable｜Reserve Management Policy_CN.md"),
    ("MPI-Redemption", "Stable/Policy/Gemtrust Stable｜Redemption Policy.md",
     "Stable/Policy/GemTrust Stable｜赎回政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-20_赎回政策/GemTrust Stable｜Redemption Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-20_赎回政策/GemTrust Stable｜Redemption Policy_CN.md"),
    ("MPI-Custody", "Stable/Policy/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy.md",
     "Stable/Policy/GemTrust Stable｜客户资产保障与密钥管理政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-22_客户资产保障与密钥管理/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-22_客户资产保障与密钥管理/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy_CN.md"),
    ("MPI-Disclosure", "Stable/Policy/GemTrust Stable｜Disclosure & Regulatory Reporting Policy.md",
     "Stable/Policy/GemTrust Stable｜披露与监管申报政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Disclosure & Regulatory Reporting Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Disclosure & Regulatory Reporting Policy_CN.md"),
    ("MPI-ToS", "Stable/Policy/Gemtrust Stable｜Terms of Service.md",
     "Stable/Policy/GemTrust Stable｜服务条款（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Terms of Service.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Terms of Service_CN.md"),
    ("MPI-Privacy", "Stable/Policy/Gemtrust Stable｜Privacy Policy.md",
     "Stable/Policy/GemTrust Stable｜隐私政策（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Privacy Policy.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Privacy Policy_CN.md"),
    ("MPI-RiskDisc", "Stable/Policy/Gemtrust Stable｜Risk Disclosure.md",
     "Stable/Policy/GemTrust Stable｜风险披露（中文对照版）.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Risk Disclosure.md",
     "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Risk Disclosure_CN.md"),
]

def heads(p):
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", errors="ignore").read()
    return [l.strip() for l in t.split("\n") if re.match(r"^#{1,3} ", l)]

def wc(p):
    t = open(p, encoding="utf-8", errors="ignore").read()
    cn = len(re.findall(r"[\u4e00-\u9fff]", t))
    en = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", re.sub(r"[\u4e00-\u9fff]", " ", t)))
    return cn + en

print("=" * 100)
print("【映射完整性 + 字数对比】")
print("=" * 100)
missing = 0
for name, se, sc, de, dc in PAIRS:
    row = []
    for label, p in (("源EN", se), ("源CN", sc), ("递EN", de), ("递CN", dc)):
        full = os.path.join(ROOT, p)
        if os.path.exists(full):
            row.append(f"{label}={wc(full)}")
        else:
            row.append(f"{label}=缺失")
            missing += 1
    print(f"  {name:<16} " + "  ".join(row))

print()
print("=" * 100)
print("【递交树独有章节】（源树基底未覆盖、需补入的内容）")
print("=" * 100)
for name, se, sc, de, dc in PAIRS:
    for label, sp, dp in (("EN", se, de), ("CN", sc, dc)):
        spf, dpf = os.path.join(ROOT, sp), os.path.join(ROOT, dp)
        if not (os.path.exists(spf) and os.path.exists(dpf)):
            continue
        sh, dh = heads(spf), heads(dpf)
        # 归一化标题以比对
        def norm(hs):
            out = set()
            for h in hs:
                s = re.sub(r"^#+ ", "", h).strip().lower()
                s = re.sub(r"[^a-z\u4e00-\u9fff ]", " ", s)
                out.add(" ".join(s.split()))
            return out
        ns, nd = norm(sh), norm(dh)
        only_d = []
        for h in dh:
            s = re.sub(r"^#+ ", "", h).strip().lower()
            s = " ".join(re.sub(r"[^a-z\u4e00-\u9fff ]", " ", s).split())
            # 判断源树是否有语义相近标题
            if s in ns:
                continue
            close = any(difflib.SequenceMatcher(None, s, x).ratio() > 0.75 for x in ns)
            if not close:
                only_d.append(h)
        if only_d:
            print(f"\n  ▸ {name} [{label}] 递交树独有 {len(only_d)} 项：")
            for h in only_d:
                print(f"       {h}")
print(f"\n缺失文件数：{missing}")
