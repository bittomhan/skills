# -*- coding: utf-8 -*-
"""
Template: render a weekly + daily work-report infographic as PNGs using Pillow.
Edit the content data blocks below for each new report, then run:
  python render_report_image.py
Outputs are written to the workspace OUT directory.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/Users/bittom/Desktop/GT"
W = 1080

# ---- Fonts ----
HIRA = "/System/Library/Fonts/Hiragino Sans GB.ttc"   # body (CJK sans)
STHEITI = "/System/Library/Fonts/STHeiti Medium.ttc"  # heading (CJK medium)

def F(path, size, idx=0):
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception:
        return ImageFont.load_default()

f_title  = F(STHEITI, 52)
f_sub    = F(HIRA, 26)
f_h2     = F(STHEITI, 34)
f_h3     = F(STHEITI, 27)
f_body   = F(HIRA, 24)
f_small  = F(HIRA, 20)
f_kpi_n  = F(STHEITI, 58)
f_kpi_l  = F(HIRA, 21)
f_tag    = F(HIRA, 19)

# ---- Palette ----
BG       = (238, 241, 246)
CARD     = (255, 255, 255)
NAVY     = (15, 42, 82)
NAVY2    = (26, 74, 142)
GOLD     = (201, 162, 75)
INK      = (31, 41, 55)
MUTE     = (107, 114, 128)
LINE     = (224, 228, 235)
SG_C=(37,99,235); HK_C=(124,58,237); JP_C=(219,39,119); KR_C=(5,150,105)
ABAND_C=(156,163,175)

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def wrap(draw, text, font, maxw):
    out=[]
    for para in text.split("\n"):
        if para=="":
            out.append(""); continue
        line=""
        for ch in para:
            if draw.textlength(line+ch, font=font) <= maxw:
                line+=ch
            else:
                out.append(line); line=ch
        out.append(line)
    return out

def rr(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def header(draw, title, subtitle):
    for y in range(0, 150):
        t=y/150.0
        draw.line([(0,y),(W,y)], fill=lerp(NAVY, NAVY2, t))
    draw.text((48,40), title, font=f_title, fill=(255,255,255))
    draw.text((50,108), subtitle, font=f_sub, fill=(214,224,240))
    draw.rectangle([48,150,W,154], fill=GOLD)

def card(draw, x, y, w, h, fill=CARD):
    rr(draw,[x,y,x+w,y+h],16,fill=fill)
    rr(draw,[x,y,x+w,y+h],16,outline=LINE,width=1)

def section_title(draw, y, text, accent=GOLD, x=48, w=W-96):
    draw.text((x,y), text, font=f_h2, fill=INK)
    draw.rectangle([x, y+44, x+54, y+48], fill=accent)
    return y+72

def bullets(draw, x, y, items, w, font=f_body, gap=14, color=INK, marker="•", mcolor=GOLD):
    for it in items:
        # support (text, sub) tuples
        sub = None
        if isinstance(it, tuple):
            it, sub = it
        ml=wrap(draw, it, font, w-34)
        draw.text((x, y), marker, font=font, fill=mcolor)
        for i,ln in enumerate(ml):
            draw.text((x+28, y), ln, font=font, fill=color)
            y+=font.size+4
        if sub:
            sl=wrap(draw, sub, f_small, w-50)
            for ln in sl:
                draw.text((x+44, y), ln, font=f_small, fill=MUTE)
                y+=f_small.size+3
        y+=gap
    return y

# =====================================================================
# WEEKLY
# =====================================================================
img = Image.new("RGB",(W, 2230), BG)
d = ImageDraw.Draw(img)
header(d, "本周工作汇报", "2026.07.06 – 07.10  ·  汇报人 Tom Han  ·  汇报对象 俞总")

# KPI row
ky=180
kpi=[("11","家持牌平台已发出（四地）",SG_C),
     ("3","份区域调研报告",JP_C),
     ("1","份旗舰政策定稿\n（GTUSD 储备金 v1.2）",GOLD),
     ("完成","AltaX 初步合作意向",KR_C)]
kw=(W-48*2-3*20)//4
for i,(n,l,c) in enumerate(kpi):
    x=48+i*(kw+20)
    card(d,x,ky,kw,150)
    d.rectangle([x,ky,x+6,ky+150],fill=c)
    d.text((x+24,ky+18), n, font=f_kpi_n, fill=c)
    yy=ky+86
    for ln in wrap(d,l,f_kpi_l,kw-44):
        d.text((x+24,yy),ln,font=f_kpi_l,fill=MUTE); yy+=f_kpi_l.size+4

# Section A
y=370
y=section_title(d,y,"A · RWA 平台对接（本周主线）")
card(d,48,y,W-96,330)
ay=y+24
bullets(d,72,ay,[
 ("AltaX 07-06 视频会议达成初步合作意向；本周 4 轮跟进推进中（转回决策人 Khai Lin 问时间线）",None),
 ("战略升级：从单线追逐 AltaX → 四地 11 家平台全量发出（新/港/日/韩），暖引荐优先于冷邮件",None),
 ("放弃 3 家无回复平台：1EXCHANGE / ADDX / InvestaX",None),
 ("关键发现：SBI 证券+大和 07-08 完成跨境证券代币 PoC（以太坊+USDC，资产含「清酒 RWA」相邻品类），2027 上线，打通日本资金端",None),
],W-144)
y+=354

# Section B
y=section_title(d,y,"B · GTUSD 稳定币合规基建")
card(d,48,y,W-96,250)
bullets(d,72,y+24,[
 ("储备金管理政策定稿 v1.2（4合1，对标 Circle USDC，中文版完成；DBS 主托管+渣打备份，现金缓冲≥15%）",None),
 ("KGP Legal 律所对接：两份法律意见 USD 18,000，待 GTUSD 独立公司注册后签约",None),
 ("操作视频脚本 PPT 修正+精简（19 页，14 处修正 + 48 处精简）",None),
],W-144)
y+=274

# Section C
y=section_title(d,y,"C · 合规与文件治理")
card(d,48,y,W-96,270)
bullets(d,72,y+24,[
 ("俞总客户信息保密红线确立：仅引用「授权委托书」，不披露客户任何信息 — 本周全执行",None),
 ("文件夹重组：GTSPV 并入 RWA，新建 Gemtrust/Deals（客户交易执行层）",None),
 ("Exchange_Outreach 按地区前缀统一：SG/HK/JP/KR + X，13 个整合文件",None),
 ("中国侧律所意见书费用测算：建议先轻量备忘录 ¥8-15 万（可复用，非一次性支出）",None),
],W-144)
y+=294

# Timeline
y=section_title(d,y,"本周关键里程碑")
card(d,48,y,W-96,210)
tl=[("07-06","AltaX 会议 → 初步合作意向"),
    ("07-07","储备金政策审查修正 + 文件夹重组"),
    ("07-08","AltaX 跟进 Cecilia（已查看资料）"),
    ("07-09","保密红线确立 + 四地邮件全发出"),
    ("07-10","区域扫描 + 日/韩调研 + 11 家全量确认")]
ty=y+30
for i,(dt,txt) in enumerate(tl):
    x=72+i*((W-144)//5)
    d.rectangle([x,ty+6,x+12,ty+12],fill=GOLD)
    d.text((x,ty+22),dt,font=f_h3,fill=NAVY)
    ll=wrap(d,txt,f_small,(W-144)//5-10)
    yy=ty+58
    for ln in ll:
        d.text((x,yy),ln,font=f_small,fill=INK); yy+=f_small.size+3
y+=234

# 需俞总支持
y=section_title(d,y,"需俞总支持事项")
card(d,48,y,W-96,200,fill=(252,249,242))
bullets(d,72,y+22,[
 ("① 中国侧律所意见书费用：建议先出轻量备忘录（¥8-15 万级），可解锁 HydraX + 全平台通用信用背书，属可复用资产",None),
 ("② WebX 2026 参展确认（7/13-14 东京）：现场接触 ODX / SBI 日方高层",None),
 ("③ GTUSD 独立公司注册推进：KGP 签约前置条件",None),
],W-144,color=INK)
y+=224

footer_y=y+10
d.text((48,footer_y), "Gemtrust Pte. Ltd. · RWA 上链 + 验证 + 融资服务平台", font=f_small, fill=MUTE)
d.text((48,footer_y+28), "Generated 2026-07-10 · 内部汇报材料", font=f_small, fill=MUTE)

img.save(os.path.join(OUT,"本周工作汇报_2026-07-06至07-10.png"), "PNG")
print("weekly saved")

# =====================================================================
# DAILY
# =====================================================================
img2 = Image.new("RGB",(W, 1500), BG)
d2 = ImageDraw.Draw(img2)
header(d2, "今日工作汇报", "2026.07.10（周五）  ·  汇报人 Tom Han  ·  汇报对象 俞总")

# Highlight band
hy=180
card(d2,48,hy,W-96,120,fill=NAVY)
d2.text((72,hy+24), "今日核心成果", font=f_h3, fill=GOLD)
d2.text((72,hy+64), "四地 11 家持牌 RWA 平台联络全量发出", font=f_h2, fill=(255,255,255))

# Region cards
ry=330
regions=[("新加坡","5 家",["AltaX","HydraX","DigiFT","SDAX","AlphaLadder"],SG_C),
         ("中国香港","2 家",["HashKey","OSL"],HK_C),
         ("日本","2 家",["SBI Digital Markets","AsiaNext"],JP_C),
         ("韩国","2 家",["Seoul Exchange","Korbit·Mirae"],KR_C)]
col_w=(W-48*2-20)//2
for i,(name,cnt,plats,c) in enumerate(regions):
    x=48+(i%2)*(col_w+20)
    yy=ry+(i//2)*(300)
    card(d2,x,yy,col_w,285)
    d2.rectangle([x,yy,x+8,yy+285],fill=c)
    # colored circle
    d2.ellipse([x+24,yy+26,x+24+18,yy+44],fill=c)
    d2.text((x+50,yy+22),name,font=f_h3,fill=INK)
    d2.text((x+col_w-90,yy+22),cnt,font=f_h2,fill=c)
    by=yy+72
    for p in plats:
        d2.text((x+30,by),"•  "+p,font=f_body,fill=INK)
        by+=f_body.size+10
    # status tag
    d2.text((x+26,yy+285-34),"状态：已发出",font=f_tag,fill=MUTE)

# Abandoned
ay=ry+2*300+10
card(d2,48,ay,W-96,80,fill=(245,246,248))
d2.text((72,ay+26),"已放弃（多发无回复）：",font=f_body,fill=MUTE)
d2.text((72+250,ay+26),"1EXCHANGE  ·  ADDX  ·  InvestaX",font=f_body,fill=ABAND_C)

# key finding + next
ky2=ay+100
y=section_title(d2,ky2,"关键发现 & 下一步")
card(d2,48,y,W-96,300)
d2.text((72,y+24),"关键发现",font=f_h3,fill=GOLD)
ll=wrap(d2,"SBI 证券+大和证券 07-08 完成跨境证券代币 PoC（以太坊+USDC），资产类含「特色清酒」——与葡萄酒 RWA 直接相邻，新加坡为首目标市场，2027 上线。",f_body,W-144)
yy=y+64
for ln in ll: d2.text((72,yy),ln,font=f_body,fill=INK); yy+=f_body.size+5
yy+=10
d2.text((72,yy),"下一步",font=f_h3,fill=GOLD); yy+=44
ll=wrap(d2,"① 建立回复追踪表（首跟 5-7 工作日）  ② WebX 2026 参展（7/13-14 东京）  ③ 中国律所意见书并行推进  ④ 需求论证备忘录译英发 AltaX",f_body,W-144)
for ln in ll: d2.text((72,yy),ln,font=f_body,fill=INK); yy+=f_body.size+5

d2.text((48,yy+30),"Gemtrust Pte. Ltd. · 内部汇报材料 · Generated 2026-07-10", font=f_small, fill=MUTE)

img2.save(os.path.join(OUT,"今日工作汇报_2026-07-10.png"), "PNG")
print("daily saved")
