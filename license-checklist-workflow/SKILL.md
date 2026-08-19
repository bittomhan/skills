---
title: "牌照申请清单进度管理工作流"
summary: "四线牌照（CMS/MPI/RWA备案/RMO）申请材料的进度追踪、审核、Excel 更新与汇报工作流"
---

# 牌照申请清单进度管理工作流

## 适用场景
Tom 在四线牌照申请（CMS / MPI / RWA 备案 / RMO）过程中，拿到材料后放到对应子文件夹，Argo 审核并更新进度。

## 四线清单文件位置
- CMS：`Gemtrust/Compliance/CMS递交材料_Gemtrust Capital/Gemtrust Capital｜CMS牌照申请材料清单.md`
- MPI：`GTUSD/Compliance/MPI递交材料_Gemtrust Stable/GTUSD｜MPI稳定币牌照申请材料清单.md`
- RWA 备案：`RWA/合规/境内RWA境外发行监管备案材料清单.md`
- RMO：在 CMS 清单内（R01-R19，条件性）
- 汇总 Excel：`牌照申请材料清单汇总_2026-07-22.xlsx`（5 选项卡）
- 整体规划：`四线并行牌照申请整体时间规划_2026-07-22.md`
- 法源对照表：`三份清单法源出处对照表_2026-07-22.md`

## 收集文件夹
- CMS：`Gemtrust/Compliance/CMS递交材料_Gemtrust Capital/`（C01-C41 + R01-R19 子文件夹）
- MPI：`GTUSD/Compliance/MPI递交材料_Gemtrust Stable/`（M01-M44 + M17b + M43a/M43b 子文件夹）
- RWA：`RWA/合规/备案材料收集/`（R01-R47 子文件夹）

## 工作流步骤

### 1. Tom 放材料
Tom 拿到某项材料 → 放到对应编号子文件夹（如 `C04_Certificate-of-Incorporation/`）→ 告知 Argo。

### 2. Argo 审核
Argo 收到通知后：
1. 读取子文件夹中的文件
2. 对照清单该项的"说明"和"法源出处"列，审核是否满足要求
3. 记录审核结果（文件名/日期/是否合格/缺失点）
4. 更新对应清单 markdown 的看板状态（⬜→🟢 或 ⬜→🟡 如需补改）

### 3. Argo 更新 Excel
审核完成后，重新生成 `牌照申请材料清单汇总_2026-07-22.xlsx`：
```python
# 解析三份 markdown 看板 → 生成 5 选项卡 Excel
# 脚本模板见 /tmp/regen_final.py（已删除，每次重新编写）
# 关键：CMS 只匹配 C\d+，RMO 只匹配 R\d+（RMO 段落内），MPI 匹配 M\d+[a-z]?，RWA 匹配 R\d+
# EX.IO 选项卡从 RWA/Deals/EX.IO/EX.IO_checklist.xlsx 复制
```

### 4. Tom 每周汇报
Tom 根据更新后的看板状态，向俞总汇报进度：
- 本周完成项（⬜→🟢 的）
- 进行中项（🟡）
- 阻塞项（🔴）
- 下周计划

## 状态图例
🟢 就绪可递交 ｜ 🟡 进行中/需改写 ｜ ⬜ 未开始 ｜ 🔴 阻塞

## 看板规则（P0 约定）
- 看板**仅作进度展示**，不承载行动规划
- 行动规划在「快速准备路径」章节（四波分波）
- Tom 反馈进度时只更新看板状态
- 【公用】共用材料状态更新时须同步 CMS + MPI 两份清单

## 编号规则
- CMS：C01-C41（C 前缀）
- RMO：R01-R19（在 CMS 清单内，R 前缀，与 RWA 的 R 不同——RMO 在 CMS 文件内解析）
- MPI：M01-M44 + M17b + M43a/M43b（M 前缀，可带字母后缀）
- RWA 备案：R01-R47（R 前缀，在 RWA 文件内解析）

## 关键依赖链
- CMS：C41(律所) → C30-C33(意见书) → C18/C19(政策) → C01(递交)
- MPI：X-5(律所) → M27(意见书) → M17(AML) → M30(EA,递交前3月) → M01(递交)；M17b(Merkle Science) → M17 → M30
- RWA：R44(律所)+R01(客户) → R43(窗口) → R16(意见书) → R15-R21(七项) → 递交
