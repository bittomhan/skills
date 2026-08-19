#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量校对替换脚本模板（联网勘定后的专有名词批量修正）

用法：
  1. 在 RULES 列表填入联网勘定后的 (原文误识, 修正) 对
     —— 长串/具体的规则放前面，避免部分替换冲突
  2. 设置 SRC（源文件）、MARKER（正文起始标记，替换仅作用于标记之后，不动对照表）
  3. 运行：/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 proofread_replace.py
  4. 看 [验证] 输出；若有残留，补充规则重跑或单独修补

特性：
  - NFKC 规范化：解决部分中文字符兼容变体（如"屈"的异体）导致匹配失败
  - body-only：只替换 MARKER 之后的正文，保留头部对照表展示原文
  - 残留验证：用 VERIFY 列表扫描正文，确认全部清除
"""
import unicodedata

# ============ 用户配置 ============
SRC = "/path/to/transcript.md"          # 待校对文件
MARKER = "## 带时间戳分段"                # 正文起始标记（替换仅作用于此后）；找不到则全文替换

# 校对规则（长串/具体优先；来自联网勘定）
# 示例（再鼎业绩会）：("Zosie","zoci"), ("韩国化疗","含铂化疗"), ("Furthing Class","First-in-Class")
RULES = [
    # ("原文误识", "修正"),
]

# 残留验证词（正文里不应再出现的错误词）
VERIFY = [
    # "Zosie", "韩国化疗", "Furthing",
]
# ===================================

def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # NFKC 规范化（统一全角/半角及兼容字符变体）
    text = unicodedata.normalize("NFKC", text)

    idx = text.find(MARKER)
    if idx == -1:
        head, body = "", text
        print("[WARN] 未找到 MARKER，全文替换")
    else:
        head, body = text[:idx], text[idx:]

    counts = {}
    for old, new in RULES:
        if old == new:
            continue
        n = body.count(old)
        if n > 0:
            counts[old] = n
            body = body.replace(old, new)

    out = head + body
    with open(SRC, "w", encoding="utf-8") as f:
        f.write(out)

    print("[INFO] 替换命中:")
    for old, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {old!r}: {n}")
    print(f"[INFO] 共修正 {sum(counts.values())} 处")

    # 残留验证
    remain = [w for w in VERIFY if w in body]
    print("\n[验证]", "✅ 正文残留全部清除" if not remain else f"⚠️ 仍有残留: {remain}")

if __name__ == "__main__":
    main()
