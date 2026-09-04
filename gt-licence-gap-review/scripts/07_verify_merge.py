#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并完整性核验：逐份检查必须保留的内容标记 + EN/CN 章节数对齐"""
import os, re

ROOT = "/Users/bittom/Desktop/GT"

# (显示名, EN 路径, CN 路径, [必须存在的标记(正则, 不区分大小写)])
DOCS = [
 ("MPI TRM", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-06_技术风险管理政策/GemTrust Stable｜Technology Risk Management Policy（FSM-N13）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-06_技术风险管理政策/GemTrust Stable｜Technology Risk Management Policy（FSM-N13）_CN.md",
  ["risk register", "KRI", "multi-signature|multisig", "timelock", "HSM", "CertiK",
   "one \\(1\\) hour", "fourteen \\(14\\)", "RTO", "Immutable|offline backup", "Tier 1",
   "Forward alignment", "cryptographic assets", "unscheduled downtime"]),
 ("MPI AML", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-03_AML-CFT政策PSN02/GemTrust Stable｜AML-CFT Policy（PSN02）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-03_AML-CFT政策PSN02/GemTrust Stable｜AML-CFT Policy（PSN02）_CN.md",
  ["CDD", "beneficial owner", "EDD", "1,500", "Merkle", "travel rule", "STR"]),
 ("MPI CM", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-07_合规手册/GemTrust Stable｜Compliance Manual（MPI-S8-07）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-07_合规手册/GemTrust Stable｜Compliance Manual（MPI-S8-07）_CN.md",
  ["obligations register", "monitoring plan", "licence condition", "filing calendar|regulatory calendar", "20 business days|twenty business days"]),
 ("MPI COI", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-08_利益冲突政策/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-08_利益冲突政策/GemTrust Stable｜Conflict of Interest Policy（MPI-S8-08）_CN.md",
  ["conflicts register|conflict register", "related.party", "gift", "annual attestation"]),
 ("MPI EWRA", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-05_企业风险评估/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-05_企业风险评估/GemTrust Stable｜Enterprise-Wide Risk Assessment（MPI-S8-05）_CN.md",
  ["5\\s*[x×]\\s*5", "R1", "R7", "inherent", "residual"]),
 ("MPI Cyber", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-12_网络卫生文件/GemTrust Stable｜Cyber Hygiene Policy（FSM-N14）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-12_网络卫生文件/GemTrust Stable｜Cyber Hygiene Policy（FSM-N14）_CN.md",
  ["C1", "C6", "administrative account", "patch", "anti-malware|malware", "multi-factor|MFA", "self-assessment|annual"]),
 ("MPI Outsourcing", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-11_外包政策登记/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-11_外包政策登记/GemTrust Stable｜Outsourcing Policy & Register（MPI-S8-11）_CN.md",
  ["materiality", "concentration", "sub-contract|subcontract", "cloud", "exit"]),
 ("MPI IA", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-10_内部审计安排/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-10_内部审计安排/GemTrust Stable｜Internal Audit Arrangements（MPI-S8-10）_CN.md",
  ["charter", "co-sourc", "three.year|three-year", "QAIP", "independen"]),
 ("MPI Complaints", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-09_投诉处理政策/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-09_投诉处理政策/GemTrust Stable｜Complaints Handling Policy（MPI-S8-09）_CN.md",
  ["1 business day|one business day", "15 business days|fifteen business days", "FIDReC", "root cause"]),
 ("MPI Reserve", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-18_储备管理政策/GemTrust Stable｜Reserve Management Policy.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-18_储备管理政策/GemTrust Stable｜Reserve Management Policy_CN.md",
  ["AA–|AA-", "three months|3 months", "mark-to-market", "monthly attestation", "annual audit",
   "following month", "WAM", "SVB", "Record Retention Plan", "asset class", "US\\$756 million"]),
 ("MPI Redemption", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-20_赎回政策/GemTrust Stable｜Redemption Policy.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-20_赎回政策/GemTrust Stable｜Redemption Policy_CN.md",
  ["par", "five business days|5 business days", "burn", "100,000"]),
 ("MPI Custody", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-22_客户资产保障与密钥管理/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-22_客户资产保障与密钥管理/GemTrust Stable｜Customer Asset Safeguarding & Key Management Policy_CN.md",
  ["multi-signature|multisig", "timelock", "cold", "key ceremony"]),
 ("MPI Disclosure", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Disclosure & Regulatory Reporting Policy.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Disclosure & Regulatory Reporting Policy_CN.md",
  ["factsheet", "whitepaper", "transparency", "MAS"]),
 ("MPI ToS", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Terms of Service.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Terms of Service_CN.md",
  ["100,000", "suspend|freeze"]),
 ("MPI Privacy", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Privacy Policy.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Privacy Policy_CN.md",
  ["PDPA", "three calendar days|3 calendar days", "DNC", "retention"]),
 ("MPI RiskDisc", "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Risk Disclosure.md",
  "Gemtrust/MPI_Stable/递交前提交/MPI-S8-23_披露与监管申报/GemTrust Stable｜Risk Disclosure_CN.md",
  ["0\\.87", "depeg|de-peg", "smart contract"]),
 ("CMS AML", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-04_AML-CFT政策AMLOMA/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-04_AML-CFT政策AMLOMA/GemTrust Capital｜AML-CFT Policy（CMS-S8-04）_CN.md",
  ["AMLOM", "accredit", "CDSA", "s\\.39", "on-chain"]),
 ("CMS CM", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-03_合规手册/GemTrust Capital｜Compliance Manual（CMS-S8-03）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-03_合规手册/GemTrust Capital｜Compliance Manual（CMS-S8-03）_CN.md",
  ["obligations register", "marketing", "274", "275", "three lines of defence|three lines"]),
 ("CMS RMF", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-05_风险管理框架/GemTrust Capital｜Risk Management Framework（CMS-S8-05）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-05_风险管理框架/GemTrust Capital｜Risk Management Framework（CMS-S8-05）_CN.md",
  ["KRI|key risk indicator", "risk appetite", "control matrix"]),
 ("CMS COI", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-06_利益冲突政策/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-06_利益冲突政策/GemTrust Capital｜Conflict of Interest Policy（CMS-S8-06）_CN.md",
  ["conflict register|conflicts register", "allocation", "information barrier|wall"]),
 ("CMS Complaints", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-07_投诉处理政策/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-07_投诉处理政策/GemTrust Capital｜Complaints Handling Policy（CMS-S8-07）_CN.md",
  ["2 business days|two business days", "10 business days|ten business days"]),
 ("CMS IA", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-08_内部审计安排/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-08_内部审计安排/GemTrust Capital｜Internal Audit Arrangements（CMS-S8-08）_CN.md",
  ["s\\.37", "co-sourc", "three.year|three-year", "QAIP"]),
 ("CMS Outsourcing", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-09_外包政策登记/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-09_外包政策登记/GemTrust Capital｜Outsourcing Policy & Register（CMS-S8-09）_CN.md",
  ["materiality", "concentration", "cloud", "exit", "register"]),
 ("CMS TRM", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-10_技术风险管理政策TRM/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-10_技术风险管理政策TRM/GemTrust Capital｜Technology Risk Management Policy（CMS-S8-10）_CN.md",
  ["one \\(1\\) hour", "fourteen \\(14\\)", "RTO", "immutable|offline backup", "multi-signature|multisig",
   "Forward alignment", "FSM-N21", "cryptographic assets"]),
 ("CMS Cyber", "Gemtrust/CMS_Capital/递交前提交/CMS-S8-11_网络卫生文件/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S8-11_网络卫生文件/GemTrust Capital｜Cyber Hygiene Policy（CMS-S8-11）_CN.md",
  ["C1", "C6", "administrative account", "patch", "anti-malware|malware", "multi-factor|MFA"]),
 ("CMS F&P", "Gemtrust/CMS_Capital/递交前提交/CMS-S10-01_Fit-Proper声明/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）.md",
  "Gemtrust/CMS_Capital/递交前提交/CMS-S10-01_Fit-Proper声明/GemTrust Capital｜Fit & Proper Declaration（CMS-S10-01）_CN.md",
  ["honesty|integrity", "reputation", "financial", "competence", "FSG-G01"]),
]

def nsec(p):
    t = open(p, encoding="utf-8", errors="ignore").read()
    return len(re.findall(r"^## ", t, re.M)), len(re.findall(r"^#{1,3} ", t, re.M))

print("=" * 92)
print("【A】内容标记核验（EN 版；CN 版仅查文件存在与章节对齐）")
print("=" * 92)
problems = []
for name, en, cn, marks in DOCS:
    pe, pc = os.path.join(ROOT, en), os.path.join(ROOT, cn)
    if not os.path.exists(pe):
        problems.append(f"{name}: EN 缺失"); continue
    if not os.path.exists(pc):
        problems.append(f"{name}: CN 缺失")
    t = open(pe, encoding="utf-8", errors="ignore").read()
    miss = [m for m in marks if not re.search(m, t, re.I)]
    if miss:
        problems.append(f"{name} 缺标记: {miss}")
        print(f"  ❌ {name:<16} 缺: {', '.join(miss)[:70]}")
    else:
        print(f"  ✅ {name:<16} 全部 {len(marks)} 项标记在位")

print()
print("=" * 92)
print("【B】EN / CN 章节数对齐")
print("=" * 92)
for name, en, cn, _ in DOCS:
    pe, pc = os.path.join(ROOT, en), os.path.join(ROOT, cn)
    if not (os.path.exists(pe) and os.path.exists(pc)):
        print(f"  ⚠️  {name}: 文件缺失，跳过"); continue
    (he, ae), (hc, ac) = nsec(pe), nsec(pc)
    flag = "✅" if he == hc else "⚠️ "
    if he != hc:
        problems.append(f"{name}: EN {he} 章 vs CN {hc} 章")
    print(f"  {flag} {name:<16} H2: EN {he:>3} / CN {hc:>3}    全部标题: EN {ae:>3} / CN {ac:>3}")

print()
print("=" * 92)
if problems:
    print(f"⚠️  共 {len(problems)} 项待处理：")
    for p in problems:
        print("   -", p)
else:
    print("✅ 全部通过")
