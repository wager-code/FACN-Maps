# 2026-10-16 生存地图同图版本复核

范围为本次当前存在的 83 张；不是此前 86/93 张历史目录。11 张模组图移入 `需专用模组/`，原槽位61张，原待测试目录11张，地图内容2522个文件哈希均未变。没有删除旧版，没有合并玩法。

以下15组包含精确重复预览、近似图以及同系改版，证据逐组区分。外置图像、内嵌预览、完整 .scmap、高度数据、存档、主脚本、菜单和独立模块不能互相替代。

[完整摘要与哈希](data/survival_audit_2026-10-16.json) · [模组发现](KNOWN_MAP_FINDINGS.md) · [迁移方法与损失](VANILLA_MIGRATION.md)

## 1. 黑日防守

成员：Black Sun Defense - v1.0（`04槽位/BBF_BlackSunDefense`；配置版本1，大厅4槽）；BSD 0.9 - Black Sun Defense Health fix（`04槽位/BBF_BSD_09`；配置版本1，大厅4槽）

证据：地形、内嵌图和存档逐字节相同；脚本与准备时间不同。

建议与差异：优先留 BBF_BlackSunDefense（作者 v1.0）。旧版不是纯副本：防守物为 ope6006、固定 150000 血；v1.0 改为 uec1901，生命公式 getDifValueDESC(130000)+20000，传送门改为成对生成并联动击杀，准备首项 150 秒而旧版 120 秒。没有 Steam 实战前，不建议直接删除 0.9。

## 2. Mycelium 3 槽与 4 槽

成员：SH1R3_Mycelium2_Survival（`03槽位/SH1R3_Mycelium2_Survival`；配置版本1，大厅3槽）；SH1R3_Mycelium2_Survival（`04槽位/sh1r3_mycelium2_survival`；配置版本2，大厅4槽）

证据：高度数据相同，内嵌图近似；完整地形文件与起点、资源布置不同。

建议与差异：按人数保留：3 槽和 4 槽均有用途。配置和联盟/玩家处理分别适配对应人数；静态资源标记为 42 与 56 个质量点。不能因 4 槽版本号较大就替代 3 槽。

## 3. 5th Dimension 沙漠版

成员：survival_5thdimension v6（`04槽位/survival_5thdimension`；配置版本1，大厅4槽）；survival_5thdimension v8（`06槽位/survival_5thdimension`；配置版本1，大厅6槽）；Survival_5.thD_MayhemEdition（`需专用模组/06槽位/survival_5.thd_mayhemedition`；配置版本5，大厅6槽）

证据：三者 .scmap 和内嵌图完全相同；存档和波次不同。

建议与差异：纯原版优先 6 槽 survival_5thdimension v8；4 槽 v6 按人数另留。v6/v8 都给前四军队各预置 8 名指挥官；v8 多出第 39 分钟波组，目标时间由 2400 改为 2700 秒，目标视野由 350 改为 380，资源标记由 80 质量/0 碳氢变成 108/2。MayhemEdition 为独立模组玩法，静态资源为 114/6，预置友方 Paragon；放入模组区。

## 4. 5th Dimension 原图、练习与扩人数

成员：survival_5thdimension（`08槽位/survival_5thdimension`；配置版本1，大厅8槽）；survival_5thdimension_practice（`04槽位/survival_5thdimension_practice`；配置版本3，大厅4槽）；survival_5thdimension 8 player（`08槽位/survival_5thdimension_8_player`；配置版本4，大厅8槽）；survival_5thdimension 16 player（`16槽位/survival_5thdimension_16_player`；配置版本8，大厅16槽）

证据：原图与 practice 地形、内嵌图、存档相同；8 player 与 16 player 为相近地形扩展。

建议与差异：1～4 人练习优先 practice（4 个阵营选择、缺人补充指挥官逻辑，固定按 4 人计敌军）；原版保留其 1～4 人+被囚 AI 槽规则。真正 8 人选 8_player，16 人选 16_player；后两者质量点都是 128，碳氢分别 8/16，出生点与人数逻辑不同。不要把原版 8 个大厅槽误当 8 名人类玩家。

## 5. 5th Dimension Center

成员：Survival 5th Dimension Center v6（`08槽位/Survival_5thdim_center`；配置版本6，大厅8槽）；Survival 5th Dimension Center EE（`08槽位/survival_5th_dimension_center_ee`；配置版本6，大厅8槽）

证据：完整地形与内嵌图相同；主脚本和模块、选项不同。

建议与差异：优先 Center EE v6：9 项设置，原 Center v6 只有 3 项；EE 增加自动回收、全阵营、能量奖励、目标生命/回血/视野，并重做终局和远程舰射击目标。目标和最终波次平衡不同，旧版仅作经典玩法来源；不能只对比同为 v6 的数字。

## 6. Horde 四版本

成员：Survival Horde（`04槽位/survival_horde`；配置版本5，大厅4槽）；Survival Horde Aeon（`04槽位/survival_horde_aeon`；配置版本8，大厅4槽）；Survival Horde Aeon Fixed（`04槽位/survival_horde_aeon_fixed`；配置版本21，大厅4槽）；Survival Horde EE（`04槽位/survival_horde_ee`；配置版本21，大厅4槽）

证据：四者 .scmap 完全相同。Aeon、Aeon Fixed、EE 的存档也相同。

建议与差异：EE 与 Aeon Fixed 分别保留：虽然主脚本相同，23 个 src 文件中的 WaveTable.lua 与 WaveOrders.lua 不同，EE 首波 URL0107，Aeon Fixed 首波 UAL0201，协助命令过滤单位也随阵营变化。原 Horde 留作经典规则；旧 Aeon 可优先用 Aeon Fixed 替代（由 1 项扩为 6 项设置），实测前不删除。

## 7. Survival Escape

成员：Survival Escape（`04槽位/Survival_Escape`；配置版本1，大厅4槽）；Survival Escape v3ga（`04槽位/Survival_Escape_v3ga`；配置版本1，大厅4槽）

证据：完整地形、内嵌图、存档完全相同；主脚本不同。

建议与差异：纯原版先选原 Survival_Escape；v3ga 面向 Total Veterancy/BlackOps 的平衡但未发现强制外部单位。v3ga 自动统计路点/首领标记，改变护送目标生命、视野与移动节奏，原独立追踪线程结构也改变。模组推荐不等于开局必需，两个版本不是简单新旧副本。

## 8. Extreme Desert / Insane

成员：Survival EXtreme Desert（`04槽位/Survival_ExtremeDesert`；配置版本1，大厅4槽）；Survival EXtreme Desert V2fA（`04槽位/Survival_ExtremeDesertV2fA`；配置版本1，大厅4槽）；Survival Insane (Beta1)（`04槽位/Survival_Insane_Beta1`；配置版本1，大厅4槽）

证据：V2fA 与 Insane 高度数据相同，内嵌图极近；完整文件不同。普通 ExtremeDesert 也近似但地形不相同。

建议与差异：经典沙漠防守优先 ExtremeDesert；V2fA 与 Insane 按规则另留。Insane 新增 HealthBuff/UnitCountMult、重做地面/空军波表与难度节奏，默认准备/目标等也不同，不能只看同一沙漠缩略图。

## 9. NorthSouth / Insane NvS

成员：Survival North and South Barrens（`04槽位/survival_NorthSouth_Barrens`；配置版本1，大厅4槽）；Survival Insane NvS (Beta1)（`04槽位/Survival_Insane_NvS_Beta1`；配置版本1，大厅4槽）

证据：高度数据相同；内嵌预览和完整地形不同，NvS 带限制区域标识。

建议与差异：常规防守优先 NorthSouth_Barrens；Insane NvS 留作挑战版。波表、准备/间隔、目标选项以及可玩区域设计不同，旧修复只处理了 NorthSouth 的强制难度和军队计数，没有合并 Insane 玩法。

## 10. Navy 与 Onix

成员：Survival EXtreme NavyV2（`04槽位/Survival_ExtremeNavy`；配置版本1，大厅4槽）；Survival EXtreme NavyV28（`08槽位/Survival_ExtremeNavy`；配置版本1，大厅8槽）；naval survival onix（`09槽位/naval_survival_onix`；配置版本69，大厅9槽）

证据：4 槽与 8 槽为人数扩展；8 槽 Navy 与 Onix 的外置 PNG 完全相同，但内嵌预览与完整地形不同。

建议与差异：4 人选 NavyV2，8 人优先 NavyV28。Onix 主脚本/选项与 8 槽版同系，但地形、起点、初始海军/工事和资源不同（44 质量/8 碳氢对 52/16）。Onix 还把 ARMY_SUPERWEAPON 同时列入大厅与 ExtraArmies，需核实特殊槽使用，不能把 9 槽当 9 名正常合作玩家。相同外图属于沿用预览，不能据此删地图。

## 11. Voodoo Battle 两版

成员：voodoo battle v1 survival（`08槽位/voodoo_battle_v1_survival`；配置版本3，大厅8槽）；voodoo battle survival new（`08槽位/voodoo_battle_survival_new`；配置版本1，大厅8槽）

证据：高度数据相同，内嵌图极近；完整地形和存档不同。

建议与差异：优先 voodoo_battle_survival_new 作为设置丰富的候选：18 项、按已启用模组装载单位表，有原版分支；v1 只有 3 项且活动波表仍含 DRLK001。两版资源布局明显不同（73 对 25 个静态质量标记），换新版会改变经济和波次；并非无损替代。

## 12. Voodoo no_mods 与 AN

成员：survival_voodoo_no_mods（`待测试_依赖与资源核对/08槽位/survival_voodoo_no_mods`；配置版本3，大厅8槽）；survival_生存AN_voodoo_no_mods（`待测试_依赖与资源核对/08槽位/survival_voodoo_AN_no_mods`；配置版本3，大厅8槽）

证据：完整地形、内嵌图、存档、菜单相同；主脚本只有一条单位限制差异。

建议与差异：优先 AN 版：将不存在的 categories.uaa0314 改为原版存在的 categories.uaa0304，恢复该单位限制。两者仍在后期波表使用 DRLK001，名字 no_mods 不能证明可在纯 Steam 原版完整运行。已准备两版的 DRLK001 替换候选，未写回。

## 13. EpischeLAN 两版

成员：Survival EpischeLAN（`12槽位/survival_epischelan`；配置版本5，大厅12槽）；Survival EpischeLAN Redone（`12槽位/survival_epischelan_redone`；配置版本1，大厅12槽）

证据：预览相似但完整地形与高度数据不同；主脚本和菜单规范化后相同。

建议与差异：稳定基准优先原 EpischeLAN v5；Redone 作为地形改版保留。两者静态资源数量同为 144 质量/24 碳氢，但 Redone 改地形高度、位置和部分 SpawnWithArmy 绑定。不能把它当脚本升级版，是否更好取决于重做后的通路/布置实测。

## 14. Omega 与 Light：复制外置图

成员：Survival Omega（`需专用模组/03槽位/Survival Omega`；配置版本1，大厅3槽）；Survival Light 2a（`08槽位/Survival Light 2a`；配置版本2，大厅8槽）

证据：外置 DDS/large/small PNG 像素相同，实际 .scmap 与内嵌图不同；只有平坦高度数据相同。

建议与差异：两张都保留，玩法完全不同。Omega 为 3 槽、经典波次且后期需 BlackOps；Light 为 8 槽、12 项设置、指挥官/预建工厂规则。应分别重建匹配的外置预览，不应因复制缩略图删除地图。本轮仅记录，不改预览。

## 15. Mayhem 3D 与 DDDX RPG

成员：Survival_Mayhem&BlackOps_3D（`需专用模组/07槽位/survival_mayhem&blackops_3d`；配置版本9，大厅7槽）；Survival_Mayhem&BO_3D_v1（`需专用模组/07槽位/survival_mayhem&bo_3d`；配置版本88，大厅7槽）；DDDX RPG survival（`需专用模组/07槽位/dddx_rpg_survival`；配置版本156，大厅7槽）

证据：可辨认的同系地形改作；尺寸/完整地形/脚本不相同。

建议与差异：追求完整模组生存优先 1024 尺寸的 3D v88 作为测试候选，512 尺寸 v9 留作较旧规则。RPG v156 单独保留，英雄槽、升级、技能使其成为独立玩法，不能被普通 3D 版替代；三者均放入模组区。

## 未确认的内容

本轮没有确认可直接删除的全量副本。配置版本字段可能曾为管理补值，不能代替作者版本说明。大厅槽可能包含被囚 AI 或特殊军队，不是人类玩家数的可靠直接表达。原预览图可在用户本地可视报告查看，仓库未上传地图图片或资源。

没有运行 Steam 引擎/多人对局；建议均为代码与结构层面的选择依据，淘汰旧版需保留可恢复来源并实际验证。
