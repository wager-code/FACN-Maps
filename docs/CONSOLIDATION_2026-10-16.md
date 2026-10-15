> **后续当前状态：62张。** 用户于2026-10-16要求删除9张确认需专用模组的地图，已备份并删除；本页71/83张为历史阶段。见[专用模组地图删除记录](MOD_MAP_REMOVAL_2026-10-16.md)。未新增游戏实测。

# 生存地图整合、淘汰与升版报告

2026-10-16。按用户明确授权：保留推荐版本；移入可兼容的优点；无法稳妥兼容的部分允许舍弃并删除旧目录。用户同时要求新版本号不得低于保留前或淘汰版。

## 完成范围

- 地图包由83张整理为 **71张**，淘汰 **12张**，修改/整合/升版 **23张**。
- 原槽位52张、待测试10张、需专用模组9张。Omega替换两个后期单位后从模组区移回3槽位；仍需游戏验证。
- 所有23张新map_version均**严格高于**比较组的旧配置版本；已知显示版本提示也纳入保守下限，地图显示名同步。历史源码/文件名中的作者版本保留作为来源，不重命名内部虚拟路径。
- 83张原始地图2522个文件已完整归档并逐项校验。淘汰目录从活动地图包删除，备份在工作区，不会被地图选择器扫描。
- 没有绘制或改写.scmap，没有拼接资源点、地形或出生点。近似图的独有地形明确作为取舍，不伪称完全重复。

## 已兼容保留的优点

| 保留图 | 实际整合 | 默认行为 |
| --- | --- | --- |
| 黑日防守 v2 | 新增“防守目标生命规则”：作者1.0公式/旧版固定150000 | 默认仍为作者1.0公式；准备时间菜单已有旧版2分钟选项。 |
| Horde EE v22 | 并入Aeon Fixed完整单位表和命令表，新增“敌军波次版本” | 默认EE；切换万古时同时切换单位/命令，生命伤害/回收/空军等设置照常适用。 |
| 5th Dimension practice v9 | 新增固定4人/按已占用防守槽人数缩放 | 默认固定4人；保留阵营选择和缺人补指挥官。人数还影响原脚本目标生命/回血/能量，帮助已注明。 |
| Survival Escape v4 | 移入路点/首领/扩区自动识别，校验连续编号 | 当前存档仍识别11/5/2；编号缺口或为空时回退原设计，不移植v3ga整套护送强化。 |

## 淘汰12张：保留了什么，舍弃了什么

| 淘汰来源 | 保留目标 | 来源优点 / 处理结果 | 明确舍弃 |
| --- | --- | --- | --- |
| BSD 0.9 - Black Sun Defense Health fix<br>`04槽位/BBF_BSD_09` | Black Sun Defense v2<br>`04槽位/BBF_BlackSunDefense` | 旧版固定150000目标生命。并为可选项；默认沿用作者v1.0生命公式，2分钟准备时间原菜单已有。 | 旧目标模型ope6006和旧单体传送门不移入；保留新版uec1901目标与成对门击杀/胜利逻辑。 |
| Survival Escape v3ga<br>`04槽位/Survival_Escape_v3ga` | Survival Escape v4<br>`04槽位/Survival_Escape` | 自动统计路点、首领点、地图扩区。移入带连续编号校验和缺口回退的识别方法。 | 舍弃v3ga目标生命/视野/速度强化、线程重排和模组向平衡，不拼接整套护送逻辑。 |
| Survival EXtreme Desert V2fA<br>`04槽位/Survival_ExtremeDesertV2fA` | Survival EXtreme Desert v3<br>`04槽位/Survival_ExtremeDesert` | 同系沙漠规则与地形布置。常规版保留ExtremeDesert，挑战玩法仍保留独立Insane。 | V2fA的独立地形、波表与目标平衡不混入；常规和挑战已有入口，避免第三套近似版本。 |
| Survival Horde<br>`04槽位/survival_horde` | Survival Horde EE v22<br>`04槽位/survival_horde_ee` | 经典Horde的波次基础和准备节奏。EE本来已继承经典波次体系；延迟/生命/伤害设置可选旧强度。 | 旧脚本硬编码、独立提示及部分时间/支援细节不恢复，不声称完全复刻经典版。 |
| Survival Horde Aeon<br>`04槽位/survival_horde_aeon` | Survival Horde EE v22<br>`04槽位/survival_horde_ee` | 万古阵营防守波次。通过较完整Aeon Fixed的单位表+命令表移入EE的万古选项。 | 旧Aeon单独初始化/硬编码数值舍弃；采用修正版和EE的设置框架。 |
| Survival Horde Aeon Fixed<br>`04槽位/survival_horde_aeon_fixed` | Survival Horde EE v22<br>`04槽位/survival_horde_ee` | 完整万古单位表与协助/路线命令。原样移入WaveTable_Aeon.lua与WaveOrders_Aeon.lua；同一个选项同时切换两者。 | 只有独立地图包装被淘汰；不会只复制单位表而遗失命令过滤。 |
| Survival_Mayhem&BlackOps_3D<br>`需专用模组/07槽位/survival_mayhem&blackops_3d` | Survival_Mayhem&BO_3D v89<br>`需专用模组/07槽位/survival_mayhem&bo_3d` | 旧版7槽海陆空防守体系。较新3D v88已保留同系海陆空、进攻槽与波次暂停；本次改为v89。 | 舍弃512尺寸旧地形、旧波次时刻和历史单位组合；不把旧表直接叠进1024版改变路线。模组依赖保留。 |
| Survival 5th Dimension Center v6<br>`08槽位/Survival_5thdim_center` | Survival 5th Dimension Center EE v7<br>`08槽位/survival_5th_dimension_center_ee` | 原Center防守目标与基础波次。Center EE已继承基础玩法，并提供更多目标/经济/回收设置。 | 旧终局强度、特殊炮核波与旧目标平衡不回填；采用EE的终局和远程舰目标处理。 |
| survival_5thdimension<br>`08槽位/survival_5thdimension` | survival_5thdimension_practice v9<br>`04槽位/survival_5thdimension_practice` | 按参与人数调整刷兵强度。移入practice为可选人数缩放；保留practice的阵营选择和缺人补指挥官。 | 旧图5～8号大厅AI槽及其操作方式不保留；新图仍是4个正常防守槽，不伪装8人版。 |
| voodoo battle v1 survival<br>`08槽位/voodoo_battle_v1_survival` | voodoo battle survival new v4<br>`08槽位/voodoo_battle_survival_new` | 原Voodoo防守布局、固定波次。选择新版18项设置和条件模组单位池作为保留基准。 | 旧73个质量点布局、旧固定波次与DRLK001依赖不拼入25标记新版；这些属于另一套经济/生成核心。 |
| Survival EpischeLAN Redone<br>`12槽位/survival_epischelan_redone` | Survival EpischeLAN v6<br>`12槽位/survival_epischelan` | 重做地形和资源摆位。脚本/菜单没有独有改进可移植，采用原EpischeLAN v5并升为v6。 | 舍弃Redone的高度、摆位和部分SpawnWithArmy变更，避免拼接两套地形；原图数量/布局不改。 |
| survival_voodoo_no_mods<br>`待测试_依赖与资源核对/08槽位/survival_voodoo_no_mods` | survival_生存AN_voodoo_no_mods v4<br>`待测试_依赖与资源核对/08槽位/survival_voodoo_AN_no_mods` | 与AN版几乎相同的无模组Voodoo。保留AN版正确的UAA0304限制，并将共同缺失的DRLK001换成URL0205。 | 旧版不存在的UAA0314限制不保留；没有发现其他独有有益代码。 |

## 按人数或独立玩法继续保留

Mycelium 3槽/4槽、沙漠5th 4槽/6槽、真正8人/16人5th、Navy 4槽/8槽、Insane挑战版、NorthSouth/Insane NvS、DDDX RPG等保留各自独立玩法。Omega与Light只是复制外置图，Onix与Navy只是外置图重用，均没有因此删除；Omega和Onix外置图已从各自.scmap导出。

MayhemEdition、3D新版、DDDX RPG、Voodoo Double、Swarm和Eternals等共9张仍在模组区。没有将它们强行清空波表或删除技能来冒充完整原版版。

## 13张小范围原版兼容修改与损失

Omega：BEL0402→UEL0401、BRL0401→XRL0403，失去原BlackOps实验单位的模型、武器、技能和原平衡。

其余12张当前保留图：Dreamy Survival v16、Fort Ictus Survival v9、Sexy Survival v13、Broad Front Survival v8、Center Arena Survival v18、Aeon Illuminate Survival v12、deadzone survival v9、Survival Stranded v22、Dune Survival v2、Survival Temple v5、survival_生存AN_voodoo_no_mods v4、Tomb Guard Survival v4。FAF T3防空改为对应阵营原版T2防空，强度/射程/模型改变；ZAB9601/ZEB9501改同科技普通工厂，失去FAF支援工厂/HQ体系；XRB2309改XRB2308，部署/隐蔽与水深仍待测。不是所有地图都涉及全部替换。

各图新增FACN_CHANGELOG.md记录修订与取舍；原作者信息保留。两张被淘汰的旧Voodoo不再单独应用之前候选补丁。

## 版本号与内容中心上传清单

实际上传版本读取scenario的 **map_version**，不是文件名里的v1/v6片段。以下均已将显示名同步为新版本；23张整合目标全部严格升版。

| 地图 | 保留前map_version | 比较旧版上限 | 新map_version |
| --- | ---: | ---: | ---: |
| Survival Omega v3 | 1 | 2（显示版本下限2） | **3** |
| Black Sun Defense v2 | 1 | 1（显示版本下限1） | **2** |
| Dreamy Survival v16 | 15 | 15（显示版本下限0） | **16** |
| Fort Ictus Survival v9 | 8 | 8（显示版本下限0） | **9** |
| Sexy Survival v13 | 12 | 12（显示版本下限0） | **13** |
| survival_5thdimension_practice v9 | 3 | 8（显示版本下限8） | **9** |
| Survival Escape v4 | 1 | 1（显示版本下限3） | **4** |
| Survival EXtreme Desert v3 | 1 | 1（显示版本下限2） | **3** |
| Survival Horde EE v22 | 21 | 21（显示版本下限21） | **22** |
| Broad Front Survival v8 | 7 | 7（显示版本下限0） | **8** |
| Center Arena Survival v18 | 17 | 17（显示版本下限0） | **18** |
| Survival 5th Dimension Center EE v7 | 6 | 6（显示版本下限6） | **7** |
| voodoo battle survival new v4 | 1 | 3（显示版本下限3） | **4** |
| naval survival onix v70 | 69 | 69（显示版本下限69） | **70** |
| Survival EpischeLAN v6 | 5 | 5（显示版本下限5） | **6** |
| Aeon Illuminate Survival v12 | 11 | 11（显示版本下限0） | **12** |
| deadzone survival v9 | 8 | 8（显示版本下限0） | **9** |
| Survival Stranded v22 | 21 | 21（显示版本下限0） | **22** |
| Survival_Mayhem&BO_3D v89 | 88 | 88（显示版本下限88） | **89** |
| Dune Survival v2 | 1 | 1（显示版本下限0） | **2** |
| Survival Temple v5 | 4 | 4（显示版本下限0） | **5** |
| survival_生存AN_voodoo_no_mods v4 | 3 | 3（显示版本下限3） | **4** |
| Tomb Guard Survival v4 | 3 | 3（显示版本下限0） | **4** |

71张当前名称、目录、版本及状态见 [当前地图与版本元数据](data/survival_consolidation_2026-10-16.json)。这只是上传元数据清单；本轮没有上传或发布地图。

不同人数的地图仍有既有安装文件夹同名（如Mycelium、survival_5thdimension、Navy）。它们是不同内容，内容中心应按独立地图身份/人数区分；安装器不能把不同条目仅按同一目录名互相覆盖。本轮保留既有地图身份与内部路径，没有擅改内容中心规则。

## 验证结果与边界

- 46个新增/修改Lua文件全部通过与Steam字节相同的LuaPlus运行库编译。
- 71张最终场景/存档/菜单数据加载通过，23张版本和显示名逐项核验。
- 13张原版替换图的活动波表/存档单位池均在本机Steam蓝图索引中存在。
- 执行真实Horde建表入口与捐赠版本对照：2种模式×32种路线占用，64用例；单位表与命令表全部一致。
- 黑日生命规则14用例；真实练习版初始化10用例（含空槽/零防守者），真实Escape初始化4用例（含实际标记/空/缺号/新连续编号）。
- 测试环境替代引擎单位/地形/线程接口，没有启动Steam游戏，也未验证模型、弹道、完整胜负、中文显示或多人同步。因此修改图状态均为 **已修改待实测**。

## 原始备份与恢复

完整原始备份：`本地工作区/整合前83张地图原始备份.zip`。ZIP内按整合前的槽位/分类目录保存83张原图；2522个原文件均已校验。

旧根目录报告和清单保存在工作区`原索引/`；本轮精确修改/移动/淘汰清单是`执行计划.json`，另有`整合前清单.json`、`验证摘要.json`与最终文件哈希。恢复时须先核对当前文件，避免覆盖后续改动；之前“仅移动模组目录”的还原脚本不适用于本轮整合。

本轮删除和取舍来自用户本次明确授权，不代表以后任意AI可不经授权批量删除新地图。知识库将同步本轮方法、版本规则、保留项与损失。


仓库只发布文档与核验元数据；地图源码、图像、备份ZIP均未上传。
