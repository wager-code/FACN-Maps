# 可复用地图玩法功能库（Steam 迁移候选）

**用途**：帮助 Codex 从真实地图中找到“选项定义 → 脚本读取 → 单位创建/波次逻辑”的完整实现，避免每张地图重新造轮子。**这里列出的参考来自用户上传的 `04槽位.zip` 静态检查，不代表 Steam 原版验证通过**。若地图未提供给 Codex，需先取得原始地图才能移植。

## 已发现的参考实现

| 地图文件夹 | 选项键 / 参考位置 | 作用 | 移植检查 |
| --- | --- | --- | --- |
| `Survival_BlackBox_10` | `opt_spawn_t1eng` | 开局额外一级工程师 | 每玩家阵营蓝图、空槽、生成位置 |
| 同上 | `opt_spawn_c` | 额外指挥官 | 胜负判定、默认 ACU 重复生成 |
| 同上 | `opt_spawn_sc` | 额外支援指挥官（SACU） | Steam 蓝图、死后判定 |
| 同上 | `opt_sacu_only` | 指挥官/支援指挥官专用规则 | 限制逻辑与其它模式是否冲突 |
| 同上 | `opt_startupTime`, `opt_waveTime` | 准备时间、波次间隔 | 秒数单位、短间隔性能风险 |
| 同上 | `opt_defenseObject`, `opt_smd_chrgd` | 防守目标与反导配置 | 不同胜利条件下是否有效 |
| `endless_survival_defense` | `opt_General_PrebuiltEngineers` | 不同级别工程师 / 初始单位 | 对应单位列表、玩家阵营 |
| 同上 | `opt_Survival_BuildTime`, `opt_Survival_Difficulty` | 生存准备时间与难度 | 独立 AI / 进攻节奏实现 |
| 同上 | `opt_Survival_AI_Pers_P1` ... `P4` | 各玩家敌军风格 | 小人数、空槽、数据传递 |
| `survival_5thdimension_practice` | `opt_Survival_Commander_One_Faction`（另有 Two/Three/Four） | 每个玩家自选指挥官阵营 | 数值映射 + 玩家槽位 + 单位 ID |
| `survival_horde_aeon_fixed` | `opt_HordeSpawnDelay` | 敌军刷怪延迟 | 默认值、首波启动时机 |
| 同上 | `opt_HordeHealthMultiplier`, `opt_HordeDamageMultiplier` | 敌军生命值/伤害调整 | 数值合法性，是否影响波次平衡 |
| 同上 | `opt_HordeAirWaves`, `opt_HordeAutoReclaim` | 空军波次与自动回收 | 开关真实生效、性能与残骸 |
| `Survival_Escape_v3ga` | `Difficulty`, `StartTime` | 难度与准备时间 | `pref` 键冲突、提前注入的缺省值 |

## 复制功能时必须追踪整条调用链

1. 在 `<map>_options.lua` 找到 `key`、`pref`、`default`、`values[].key`。
2. 在 `<map>_script.lua` 找 `ScenarioInfo.Options.<key>` 及所有间接读取。兼顾文件中 `src/Options.lua` 或包装器。
3. 沿代码查找选择值如何决定**单位 ID / 数量 / 阵营 / 坐标 / 生成时间 / 胜负条件**，标记所有相关引用。
4. 检查所有依赖的 `src/`、`vendor/`、波次表、单位蓝图是否能随地图独立工作。
5. 先验证目标 Steam 大厅确实传入自定义选项；否则这些功能只能算脚本实验，不能宣布可配置。
6. 对新增单位实施 `off / 最小值 / 最大值 / 多人 / 空槽` 五项回归测试；对波次实施至少首波、升级波、后期特殊波测试。

## 工程师与指挥官功能的实现边界

- **不要写死单位代码**。按参与者对应阵营，从 Steam 原版单位蓝图中建立 ACU / SACU / T1/T2/T3 工程师映射；未知阵营/单位应安全拒绝或回退。
- 确保与引擎默认 ACU、地图自带 `INITIAL` 单位不冲突。
- 可选择是否提供 0/1/2/4 名工程师，但实际数值方案必须按地图平衡设计，不强制所有地图一套。
- 某些生存地图的成功条件是“至少一位指挥官存活”，有些是“所有指挥官存活”或“保护建筑”。额外生成 ACU/SACU 不应无意改变原规则。
- 生成单位应在安全位置、属于正确 `army`，且只由 sim 侧产生一次；不可由每个客户端的 UI 分别生成。
- 所有新增选项默认 **保持原地图行为不变**；用户主动开启增强功能才改变玩法。

## 对“丰富地图功能”的建议次序

1. 先把原地图现有菜单选项修复到正常显示、读值、应用。
2. 优先实现准备时间、开局工程师、难度三类最有价值且可回滚的功能。
3. 随后处理阵营、额外 ACU/SACU、波次模式、无尽模式；任何会改写胜负规则的选项必须独立审查。
4. 在多人同步和后期波次通过之前，**不要一次性把所有高级选项加入所有地图**。

## 维护新增功能的方法

每新发现一种可复用玩法，在本文件附加记录：

```md
### 功能名称
- 来源地图/版本/哈希：
- 选项 key 与源文件/行号：
- Script 调用链（函数名）：
- Steam 原版所需 API 与蓝图：
- 需要一起带走的 src/vendor/波次文件：
- 哪些地图适用、哪些不适用：
- 默认兼容性与风险：
- 测试状态与日志/PR：
```

**注意**：`Survival_BlackBox_10` 中的 `opt_sacu_only` 不只是“新增单位”，还关联单位限制和规则变化；移植时不能省略配套限制函数。

## 可选模组池与原版降级（2026-10-16）

`desert_front_survival`、`survival_genesis`、`voodoo_battle_survival_new`、`survival_terror_lands`、`onixs_voodoo_survival` 的模组检测/条件导入可作为“原版可用+额外支持”的结构参考。必须连同初始化基础单位池、检测条件、空池保护、单位限制及玩法选项审查；不能把支持列表中的每个编号当成强制依赖。

原版降级不是通用玩法增强：替代单位的兵种、武器/技能、机动与平衡要在报告列明。小范围替换参考 [VANILLA_MIGRATION.md](VANILLA_MIGRATION.md)，多层英雄/外置波次模式不适合直接套此方法。来源哈希和当前路径见本轮摘要，不承诺跨版本兼容。

## 本轮可复用整合功能（2026-10-16，已修改待实测）

| 来源保留图 | 新选项/函数 | 正确迁移边界 |
| --- | --- | --- |
| Horde EE v22 | opt_FACN_HordeWaveSet；src/FACNWaveSelector.lua | 选择1为EE，2为Aeon Fixed；单位表/命令表必须配套，不能遗失路线与协助过滤。 |
| 黑日v2 | opt_FACN_TargetHealthMode | 1作者公式，2固定150000。只迁移生命规则，旧模型与传送门逻辑不带入。 |
| practice v9 | opt_FACN_EnemyScaling | 1固定4人，2仅统计已占用ARMY_1至4；原脚本人数也影响目标属性，须说明且测试空槽。 |
| Escape v4 | FACNCountSequentialMarkers / FACNDetectEscortMarkers | 分别检查WAYPOINT_0起、BOSS_BATTLE_1起、MAP_EXPANSION_1起；缺号回退，不能盲目count-1。 |

验证的是隔离真实函数/建表入口；实机和多人待测，不能将这些功能直接称为已发布组件。完整取舍与版本号见 [整合报告](CONSOLIDATION_2026-10-16.md)。


## 外部源码复核：四族开局单位选项（仅源码可证，Steam 待实测；2026-10-15）

| 来源地图 | 声明/实现在何处 | 源码证据和移植重点 |
| --- | --- | --- |
| [Genesis of the Order](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival) | [`Genesis_of_the_Order_Survival_options.lua`](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Genesis_of_the_Order_Survival_options.lua) `Option_AllFactions`; [`Utilities/AllFactions.lua`](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Utilities/AllFactions.lua); [`Functionality/GameSetup.lua`](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Functionality/GameSetup.lua) | 0关；1同族3工程师；2同族1 ACU；3其他三族工程师；4其他三族 ACU。取有效 PlayerArmies → Brain/GetFactionIndex/GetArmyStartPos → 对应蓝图 CreateUnitNearSpot。必须保留原胜负逻辑。 |
| [5th Dimension Center EE](https://github.com/SupremeCommanderMaps/Survival5thDimensionCenterEE) | [`*_options.lua`](https://github.com/SupremeCommanderMaps/Survival5thDimensionCenterEE/blob/master/survival_5th_dimension_center_ee_options.lua) `opt_CenterAllFactions` | 0关；1每玩家3工程师；2每玩家3 ACU。与 Genesis 的“1 ACU”不可混用；需查实际脚本读取链。 |

完整的 **选项 key/pref/default/values → 脚本取值 → 玩家槽/种族 → 生成坐标与单位数量 → ACU 失败规则 → 多人验证** 操作教程见 [ADVANCED_OPTIONS_REPAIR_GUIDE.md](ADVANCED_OPTIONS_REPAIR_GUIDE.md)。相关源代码接口表见 [API_EVIDENCE_MATRIX.md](API_EVIDENCE_MATRIX.md)。以上不是 Steam 原版大厅支持的证明；未实际运行地图，不可标记通过。
