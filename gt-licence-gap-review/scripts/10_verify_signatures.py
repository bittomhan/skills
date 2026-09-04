#!/usr/bin/env python3
"""
GT 项目 · PDF 签名核验标准工具（v1，2026-09-02）

背景（血泪教训，勿删）：
  09-02 核验 S4-01 三份函件签署状态时，只查了 page.get_images()（位图），
  报告「LI Hua 未签、需补签」——**完全错误**。LI Hua 的签名是 PDF 矢量路径
  （电子签名板 → filled Path），不在 images 数组里。
  Tom 指出「Li Hua 喜欢这种签名方式」——即她习惯用电子签名板生成矢量签名。

结论（永久规则）：
  PDF 有【图像 / 文字 / 矢量 Path】三层，签名可能落在任意一层。
  核验签署必须【三层同时查】，只看一层 = 必然漏签。

签名形态对照（本项目已观察到的两种）：
  · MA Qing —— 手写后扫描 → **位图**（page.get_images()，xref 图像）
  · LI Hua  —— 电子签名板 → **矢量**（page.get_drawings() 中 type='f' 的填充路径）

用法：
  /Users/bittom/.workbuddy/binaries/python/envs/default/bin/python3 \
      10_verify_signatures.py <pdf1> [<pdf2> ...]

输出：每份 PDF 的位图签名数、矢量签名数、日期填写情况与总判定。
"""
import sys
import fitz


def verify(path: str, sig_y_range=None, min_path_area=200.0):
    """核验单个 PDF 的签名情况。

    sig_y_range: 签名栏纵向范围（pt）。**默认 None = 全页扫描**（v1.1 起）。
                 教训：Board Resolution 的签名在 y≈312（页中），不在页尾，
                 固定范围会漏检。故默认扫全页，改靠几何特征过滤装饰元素。
    min_path_area: 矢量路径最小面积（pt²），过滤极小的表格线。
    """
    doc = fitz.open(path)
    result = {"file": path.split("/")[-1], "pages": doc.page_count,
              "bitmap_sigs": [], "vector_sigs": [], "text_dates": []}

    for pno in range(doc.page_count):
        pg = doc.load_page(pno)
        ph = pg.rect.height
        pw = pg.rect.width
        y0_min, y0_max = sig_y_range if sig_y_range else (0, ph)

        # ---- 层 1：位图签名（手写扫描 / 插入图片）----
        for img in pg.get_images(full=True):
            xref = img[0]
            rects = pg.get_image_rects(xref)
            if not rects:
                continue
            for r in rects:
                if not (y0_min <= r.y0 <= y0_max):
                    continue
                # 过滤整页背景图：宽或高超过页面的 90%
                if (r.x1 - r.x0) > pw * 0.9 or (r.y1 - r.y0) > ph * 0.9:
                    continue
                result["bitmap_sigs"].append({
                    "page": pno + 1,
                    "rect": (round(r.x0), round(r.y0), round(r.x1), round(r.y1)),
                    "size": f"{img[2]}x{img[3]}",
                })

        # ---- 层 2：矢量签名（电子签名板 → filled Path）----
        for dr in pg.get_drawings():
            if dr.get("type") != "f":          # f = fill（填充）；s = stroke（描边，通常是线条）
                continue
            r = dr.get("rect")
            if not r:
                continue
            if not (y0_min <= r.y0 <= y0_max):
                continue
            h = r.y1 - r.y0
            w = r.x1 - r.x0
            area = w * h
            if area < min_path_area:
                continue                        # 过滤极小表格线/项目符号
            if h < 3 or (w / max(h, 0.01)) > 40:
                continue                        # 过滤横向分隔线（极扁）
            if w > pw * 0.6:
                continue                        # 过滤通栏/半栏装饰条与页眉色块
                                                # （实测：真签名宽≈98pt；页眉装饰宽≈459pt）
            if area > 150000:
                continue                        # 过滤大面积背景块
            if h < 20:
                continue                        # 过滤高度过小的分隔线/下划线
            result["vector_sigs"].append({
                "page": pno + 1,
                "rect": (round(r.x0), round(r.y0), round(r.x1), round(r.y1)),
                "area": round(area),
            })

        # ---- 层 3：文字层（检查 Date 是否已填）----
        txt = pg.get_text()
        for line in txt.split("\n"):
            if "Date" in line and any(ch.isdigit() for ch in line):
                result["text_dates"].append(line.strip()[:60])

    result["total"] = len(result["bitmap_sigs"]) + len(result["vector_sigs"])
    doc.close()
    return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    for p in sys.argv[1:]:
        try:
            r = verify(p)
        except Exception as e:
            print(f"\n### {p.split('/')[-1]}\n  [错误] {e}")
            continue
        print(f"\n### {r['file']}  (pages={r['pages']})")
        print(f"  位图签名 (MA Qing 型): {len(r['bitmap_sigs'])} 个")
        for s in r["bitmap_sigs"]:
            print(f"    - p{s['page']} rect={s['rect']} size={s['size']}")
        print(f"  矢量签名 (LI Hua 型): {len(r['vector_sigs'])} 个")
        for s in r["vector_sigs"]:
            print(f"    - p{s['page']} rect={s['rect']} area={s['area']}")
        print(f"  Date 文字行: {len(r['text_dates'])} 条")
        for d in r["text_dates"]:
            print(f"    - {d}")
        total = r["total"]
        if total >= 2:
            verdict = "✅ 双签齐全"
        elif total == 1:
            verdict = "⚠️ 仅 1 个签名 —— 需确认是否漏签"
        else:
            verdict = "❌ 未检出签名（可能签名栏在 sig_y_range 之外，请调整参数后重跑）"
        print(f"  >>> 判定：{verdict}")


if __name__ == "__main__":
    main()
