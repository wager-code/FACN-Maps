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


## 62张玩法组件检索（2026-10-16）

新增[逐图代码地图册](SURVIVAL_CODE_ATLAS_2026-10-16.md)：每图给函数文件/行号、核心调用线索、菜单值/消费者和SHA-256。后续用当前哈希核对版本再移植。

- 第一层可研究：Omega/5th practice的固定波次、目标死亡与准备计时。
- 配套迁移：Horde的成对波表/命令、BlackSun的阶段/门、Escape/Run的路点/扩区；不要只提取一段刷兵。
- 复杂系统：Endless的收入驱动、Anerle的队伍资源与竞争、Rainmakers/Order/Stranded的目标/事件模块；应按完整状态机理解。
- 普通大厅AI布局和空初始化图不是内置波次模板。备用库未进入调用链也不能当作已经游戏验证的通用组件。
- 本轮只修既有偏好键和原生API，不改变玩法、不新增全图菜单。未来制作的技术路线见[AI地图制作](AI_MAP_AUTHORING.md)。

## 当前安装生存图可借鉴的布局与高级选项（2026-10-20）

本轮研究35张生存/AOD、235活动选项；只读源码/本机Lua隔离，不冒称所有组合游戏验证。详见[SURVIVAL_DEFENSE_OPTIONS_COMPARISON](SURVIVAL_DEFENSE_OPTIONS_COMPARISON_2026-10-20.md)。

| 来源 | 可复用机制 | 必须先核对 |
| --- | --- | --- |
| 5iver Land/Naval | 门/远程火炮/特殊敌军独立守备档，陆空海数量、生命、老练、科技时间分开 | 预设覆盖、占地相交、反核弹药接口、显示值与key；Swarm守备固定不在菜单 |
| Run/Attack/Escape | 编辑器GROUP存整套防线，难度/区域/随机组合启用 | INITIAL与GROUP区分、Run GROUP_6非法type=5、全路线和空区测试 |
| Horde EE v22 | buffDamage按Damage×(倍率−1)追加，生命/空军/回收独立 | 生存创建回调范围、5级老练、回收上限、射弹自定义覆盖 |
| Grand Barrens v13 | 整波/持续、起始波、Boss、残骸、成长、开局资源和工程师 | 伤害“×2”当前附加原值得×3（普通无其它加成）、成长表达式与文案不一致 |
| Endless v17 | 质量预算、6种AI风格、T2/3/4时间或收入门槛、7种Boss开关 | 活动路径；BaseSpanwer圆环仅DEBUG=false测试入口，不能宣称正常启用 |
| AOD及survival_vs_4player | 密排地防/防空维持波次路线 | 其不可击杀性质；不能直接套到玩家应能反攻的敌方核心 |

先定义数量、生命、伤害、盾量/恢复、科技计时、人数缩放分别作用于谁，再加菜单；新增选项须接入创建和更新路径，而非只加options表。
