#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取「递交树独有内容块」——以段落为单位，找出源树中不存在的递交树正文"""
import os, re, sys, difflib

ROOT = "/Users/bittom/Desktop/GT"

def blocks(p):
    t = open(p, encoding="utf-8", errors="ignore").read()
    out = []
    cur = []
    for line in t.split("\n"):
        if line.strip():
            cur.append(line.rstrip())
        else:
            if cur:
                out.append("\n".join(cur))
            cur = []
    if cur:
        out.append("\n".join(cur))
    return out

def norm(s):
    s = re.sub(r"^#+ ", "", s)
    s = re.sub(r"[\s\-—–|]", "", s).lower()
    return s

def unique_blocks(src_p, dst_p, thresh=0.62):
    """返回 dst 中源树没有的块（按块整体相似度判断）"""
    sb, db = blocks(src_p), blocks(dst_p)
    sn = [norm(b) for b in sb]
    uniq = []
    for b in db:
        nb = norm(b)
        if len(nb) < 25:      # 太短（表格分隔/单行标题）跳过
            continue
        best = 0
        for x in sn:
            r = difflib.SequenceMatcher(None, nb, x).ratio()
            if r > best:
                best = r
            if best >= 0.95:
                break
        if best < thresh:
            uniq.append((b, round(best, 2)))
    return uniq

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    sp, dp = os.path.join(ROOT, src), os.path.join(ROOT, dst)
    print(f"源树: {os.path.basename(src)}")
    print(f"递交: {os.path.basename(dst)}")
    print("=" * 90)
    u = unique_blocks(sp, dp)
    print(f"递交树独有块：{len(u)} 个\n")
    for i, (b, sim) in enumerate(u, 1):
        print(f"--- [{i}] 最似源树 {sim} ---")
        print(b[:700])
        print()
