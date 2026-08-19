#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字幕式稿件 → 语义段落版重排脚本

将一行一句的字幕稿按语义合并为段落，段首保留开始时间戳。
分段依据：发言人切换 / 问答边界触发词 + 每段最大句数。

用法：
  1. 设置 SRC（字幕式稿件）、DST（段落版输出）
  2. 按需调整 TRIGGER_STARTS（发言人切换/问答边界触发词，句子开头匹配）
     和 CHAPTERS（章节时间边界→标题）
  3. 运行：/Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 reformat_paragraphs.py

分段触发词需根据会议类型调整：
  - 业绩会：分析师自报家门（"我是中金/中信/国泰/UBS"）、交接语、Q&A标志
  - 访谈：主持人/嘉宾切换标志
"""
import re

# ============ 用户配置 ============
SRC = "/path/to/transcript_subtitle.md"   # 字幕式稿件（含 **[MM:SS]** 文本 行）
DST = "/path/to/transcript_paragraph.md"  # 段落版输出
MAX_SENT = 9                              # 段落最大句数，超过强制分段

# 分段触发词：句子以这些开头 → 新起一段（发言人切换/问答边界）
TRIGGER_STARTS = [
    # 分析师自报家门
    "我是中金", "我是中信", "我是国泰", "我是UBS",
    # 交接
    "下面我把时间交给", "下面我来为大家介绍", "下面我们进入",
    # Q&A 提问
    "好 谢谢公司", "好 谢谢领导", "感谢公司给我提问", "现在有请", "接下来有请",
    "我这边有两个", "我这边有几个", "第一个问题", "第二个问题",
    # Q&A 回答
    "好的 这个问题我来回答", "好的 我可以来回答", "这个问题我来回答", "我来回答吧",
    # 交接回应
    "谢谢张静", "谢谢杜总", "谢谢何珊", "谢谢何总", "明白明白",
    # 收尾
    "总结来说", "总的来说", "本场会议的时间就差不多了", "感谢各位拨冗",
]
# 包含触发（句子中包含即分段）
TRIGGER_CONTAINS = ["给我一个提问机会", "给我提问的机会"]

# 章节划分（开始秒→标题），按会议实际流程定义
CHAPTERS = [
    (0, "一、开场"),
    # (120, "二、致辞"),
    # (324, "三、管线介绍"),
    # (767, "四、财务"),
    # (995, "五、投资者问答（Q&A）"),
]
# ===================================

def is_trigger(content):
    for t in TRIGGER_STARTS:
        if content.startswith(t):
            return True
    for t in TRIGGER_CONTAINS:
        if t in content:
            return True
    return False

def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # 解析 **[MM:SS]** 文本
    line_re = re.compile(r"^\*\*\[(\d{1,2}:\d{2})\]\*\*\s*(.*)$", re.MULTILINE)
    segs = []
    for m in line_re.finditer(text):
        tstr, content = m.group(1), m.group(2).strip()
        p = tstr.split(":")
        secs = int(p[0]) * 60 + int(p[1])
        if content:
            segs.append((tstr, secs, content))

    # 分段
    paragraphs = []
    cur, cur_start, cur_tstr = [], None, None
    for tstr, secs, content in segs:
        if not cur:
            cur, cur_start, cur_tstr = [content], secs, tstr
        elif is_trigger(content) or len(cur) >= MAX_SENT:
            paragraphs.append((cur_tstr, cur_start, cur))
            cur, cur_start, cur_tstr = [content], secs, tstr
        else:
            cur.append(content)
    if cur:
        paragraphs.append((cur_tstr, cur_start, cur))

    # 输出
    out = ["# 文字稿（段落版）", "", "> 按语义分段，段首保留开始时间戳。", "", "---", ""]
    printed = set()
    for tstr, secs, contents in paragraphs:
        # 章节
        ci = 0
        for i, (s, name) in enumerate(CHAPTERS):
            if s <= secs:
                ci = i
            else:
                break
        if ci not in printed and CHAPTERS:
            out.append(f"## {CHAPTERS[ci][1]}")
            out.append("")
            printed.add(ci)
        out.append(f"**[{tstr}]** {''.join(contents)}")
        out.append("")

    with open(DST, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"[INFO] {len(segs)} 个分段 → {len(paragraphs)} 个语义段落")
    print(f"[INFO] 已保存: {DST}")

if __name__ == "__main__":
    main()
