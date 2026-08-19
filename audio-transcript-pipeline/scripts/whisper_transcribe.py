#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Whisper 语音转文字脚本（medium + MPS 加速 + 中文优化）
将音频转为带时间戳分段的 Markdown 文字稿。

用法：
  1. 修改下方 AUDIO_PATH / OUTPUT_MD / LANGUAGE 常量
  2. /Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 whisper_transcribe.py
  3. 建议后台运行（run_in_background），46分钟音频约需37分钟

可配置项：
  - MODEL_NAME: medium（中文平衡）/ large-v3（最高精度，~3GB）/ small（快速草稿）
  - DEVICE: mps（Apple Silicon GPU）/ cpu
  - LANGUAGE: zh（中文）/ en（英文）/ ja... 强制语言可提升精度与速度
"""
import sys
import time
import warnings

warnings.filterwarnings("ignore")

# ============ 用户配置（按需修改）============
AUDIO_PATH = "/path/to/audio.m4a"          # 音频文件路径
OUTPUT_MD = "/path/to/output.md"            # 输出 Markdown 路径
MODEL_NAME = "medium"                       # 模型：medium / large-v3 / small
DEVICE = "mps"                              # 设备：mps（Apple Silicon）/ cpu
LANGUAGE = "zh"                             # 强制语言：zh / en / ja ...
TITLE = "音频文字稿"                          # 输出文档标题
# ===========================================

def fmt_ts(seconds):
    seconds = int(round(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def main():
    t0 = time.time()
    print(f"[INFO] 加载 Whisper 模型: {MODEL_NAME} (device={DEVICE})", flush=True)
    import whisper
    model = whisper.load_model(MODEL_NAME, device=DEVICE)
    print(f"[INFO] 模型加载完成，耗时 {time.time()-t0:.1f}s", flush=True)

    t1 = time.time()
    print(f"[INFO] 开始转写: {AUDIO_PATH}", flush=True)
    print(f"[INFO] 强制语言识别 (language={LANGUAGE})", flush=True)
    result = model.transcribe(
        AUDIO_PATH,
        language=LANGUAGE,
        task="transcribe",
        verbose=False,
        # 中文场景幻觉调优（减少重复/胡编，避免长段误截断）
        compression_ratio_threshold=2.4,
        no_speech_threshold=0.6,
        logprob_threshold=-0.8,
    )
    print(f"[INFO] 转写完成，耗时 {time.time()-t1:.1f}s", flush=True)

    segments = result.get("segments", [])
    full_text = result.get("text", "").strip()
    lang = result.get("language", LANGUAGE)

    lines = []
    lines.append(f"# {TITLE}")
    lines.append("")
    lines.append(f"> **音频文件**: `{AUDIO_PATH.split('/')[-1]}`")
    lines.append(f"> **识别语言**: {lang}")
    lines.append(f"> **转写模型**: OpenAI Whisper `{MODEL_NAME}` ({DEVICE} 加速)")
    lines.append(f"> **转写时间**: {time.strftime('%Y-%m-%d')}")
    lines.append(f"> **转写耗时**: {time.time()-t1:.1f}s")
    lines.append("")
    lines.append("> ⚠️ 本文字稿由 AI 自动语音识别生成，可能存在识别错误（尤其专有名词、数字、英文术语）。")
    lines.append("> 关键数据请以官方公告/回放为准。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 完整文字")
    lines.append("")
    lines.append(full_text)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 带时间戳分段")
    lines.append("")
    for seg in segments:
        start = fmt_ts(seg["start"])
        text = seg["text"].strip()
        if text:
            lines.append(f"**[{start}]** {text}")
            lines.append("")

    md = "\n".join(lines)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[INFO] 已保存: {OUTPUT_MD}", flush=True)
    print(f"[INFO] 分段数: {len(segments)}", flush=True)
    print(f"[DONE] 全部完成", flush=True)

if __name__ == "__main__":
    main()
