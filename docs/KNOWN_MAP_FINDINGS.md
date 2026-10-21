> **当前维护包数量：62张。** 全局数量、修改统计和测试边界以 [CURRENT_STATE.md](CURRENT_STATE.md) 为准。2026-10-16删除了9张当时已确认依赖专用模组的地图，但后续发现保留地图中仍有强制依赖证据（例如 Brainsucka）；“需专用模组”分类目录已移除不等于剩余地图零依赖。见[专用模组地图删除记录](MOD_MAP_REMOVAL_2026-10-16.md)及[Brainsucka专项](BRAINSUCKA_LUAC_AND_REQUIRED_MOD_2026-10-20.md)。未因此新增游戏实测。

> **历史阶段：71张整合快照。** 2026-10-16曾按用户授权整合为71张，淘汰12张、升版23张。见 [整合与升版记录](CONSOLIDATION_2026-10-16.md)。下文引用的83张/30张清单、哈希与路径均是历史证据，不自动适用于当前文件。

# 04槽位.zip 静态审计：已知问题、重复地形与待验证事项

**数据来源**：用户在 2026-10-15 对话中提供的 `04槽位.zip`（原始归档未上传到本仓库）。静态读取 ZIP 文件表、Lua 文本以及 SHA-256；未启动 Steam SCFA。**所有条目默认“静态确认”或“待调查”，绝不是游戏实测通过**。如果后续拿到不同版本 ZIP，应重新核对哈希与行号。

统计：30 个顶层地图文件夹、31 个 `.scmap` 文件、26 种不同 SHA-256 的 `.scmap` 数据；因此**地形完全重复组为3组**，但不能推出整个地图玩法重复。

## P0：选项定义 / 读取存在静态可定位的问题

### A. Survival_Escape 与 Survival_Escape_v3ga 的 StartTime 复用了 Difficulty 偏好键
- 证据：`Survival_Escape/Survival_Escape_options.lua` 第26–27行，`Survival_Escape_v3ga/Survival_Escape_v3ga_options.lua` 第26–27行：
  - `key = 'StartTime'`
  - `pref = 'Difficulty'`
- 风险：在会读取 `pref` 的大厅实现中，准备时间的偏好项可能与难度混淆或污染；**具体运行影响需验证**。
- 修复候选：在保留 `key='StartTime'` 的前提下将 `pref` 独立为 `StartTime`；先查加载器 `pref` 行为和存档迁移，再测试 Steam/FAF 大厅，不可直接推断 Steam 一定支持此选项。
- 状态：**静态确认，待修改/实测**。

### B. survival_sea_fleet 的 Wreckage 选项 key / pref 拼写不一致
- 证据：`survival_sea_fleet/survival_sea_fleet_options.lua` 第52–53行：`key='opt_Survival_Wreckage'`，`pref='opt_Survival_Wreckages'`。
- 修复候选：核查原设计意图和解析器后统一键名；脚本所有读取位置一起核对。
- 状态：**静态确认，待修改/实测**。

### C. survival_horde_aeon_fixed / survival_horde_ee 默认值定义疑似冲突
- `survival_horde_aeon_fixed_options.lua`：`opt_HordeSpawnDelay` 的 `default=8`，选项值列表依次为 1、10、20、30、40、60、70、80…；最前面“1秒”文本写着“默认”。
- `opt_HordeHealthMultiplier` 与 `opt_HordeDamageMultiplier` 选项的 `default=7`，其第七项为 1.0，但最前面“10%”仍标注“默认”。
- `survival_horde_aeon_fixed_script.lua` 第5–11行额外注入缺省值：延迟1、生命值0.1、伤害0.1（并非必然等于大厅选中的默认值）。
- `survival_horde_ee` 的选项 Lua 与 fixed 版本 SHA-256 完全相同，同类问题一并审查。
- **不要直接把 default=8 改成1**：必须先确认所用大厅解析器将 `default` 解释为 **条目序号** 还是 **value key**，并与原地图作者的期望玩法核对。
- 状态：**静态确认“定义不一致”，影响待实测**。

### D. Survival_Escape_v3ga 多段 fallback 互相覆盖
- `Survival_Escape_v3ga_script.lua` 第5–8行的 `__SurvivalApplyLobbyDefaults` 首先将缺失的 `Difficulty` 补为1；后面第154–157行 `if Difficulty == nil then Difficulty = 4`。
- 由于前面的补值函数已执行，在通常情况下后面的 `4` 回退不会触发；同时 `_options.lua` 为 `Difficulty` 声明 `default=4`，可见文本中“极其简单”仍标为“默认”。
- **精确结论**：既存在提前注入的1，也存在后段的4，不应只说“默认一定是1”或“一定是4”；Steam 实际取值要结合大厅和注入调用顺序验证。
- 修复候选：明确原设计默认难度，并统一选项/提示/无大厅回退值；修改前记录难度各档行为。
- 状态：**静态确认，待实测**。

### E. survival_5thdimension_practice 的指挥官阵营缺省值不一致
- `survival_5thdimension_practice_script.lua` 第10行提前设置 `opt_Survival_Commander_One_Faction=1`；第879–880行仅在 nil 时又会将其设置为2。
- 两段回退意图不一致；其他玩家阵营选项也应逐一验证。
- 状态：**静态确认，待核对选项含义**。

## P1：高风险兼容性审计（不能未经日志直接认定故障）

| 地图 | 静态事实 | 为什么要查 | 下一步 |
| --- | --- | --- | --- |
| `Supreme_survival` | `_script.lua` 第16–17行在地图脚本导入 `/lua/ui/uiutil.lua`、`/lua/ui/game/gamemain.lua` | sim 与 UI 环境混用风险 | Steam 实测导入时机/堆栈；找 sim 内可用实现 |
| `5iver Survival Brainsucka` | 使用 `_script.luac`、`_save.luac`、`Functions.luac`、`Hooks.luac` | 字节码版本 / 可维护性 / 源码来源 | 搜来源、版本与合法授权；目标引擎实际加载测试 |
| `endless_survival_defense` | Scenario 含 `AdaptiveMap = true`，主脚本使用自带 `vendor/EntropyLib` | FAF 自适应地图功能和 Steam 的加载差异 | 分别核对本地依赖完整性、Steam 大厅与脚本功能 |
| `survival_horde_aeon_fixed` | 脚本从 `/maps/survival_horde_aeon_fixed/src/`、`vendor/EntropyLib/src/` 导入 | 重命名/合并容易破坏绝对虚拟路径 | 保持目录或同步更新全部 `import`；按各波次测试 |

## 已确认地形哈希完全相同的3组

下列只是 **`.scmap` SHA-256 相同**（不是整个文件夹相同），同组地图仍可能有不同规则与波次。

| 组别 | 地图文件夹 | 保留建议 |
| --- | --- | --- |
| Horde | `survival_horde`、`survival_horde_aeon`、`survival_horde_aeon_fixed`、`survival_horde_ee` | 先选一版为**整合基底候选**；核查 Fixed 与 EE 的波次表/阵营，不建议未经对战测试删除其他版本 |
| Black Sun Defense | `BBF_BlackSunDefense`、`BBF_BSD_09` | `_save.lua` 哈希相同；脚本不同，候选保留 `BBF_BlackSunDefense`，**稳定性未验证** |
| Escape | `Survival_Escape`、`Survival_Escape_v3ga` | `_save.lua` 哈希相同；脚本不同，可先以 v3ga 为整合基底，检查 MOD 适配及选项异常 |

可核对的重复数据：
- Horde 4个 `.scmap` 完全一致；`survival_horde_aeon`、`survival_horde_aeon_fixed`、`survival_horde_ee` 三者的 `_save.lua` 完全一致；fixed 和 ee 的 `_options.lua` 完全一致。
- Black Sun 两个 `_save.lua` 完全一致。
- Escape 两个 `_save.lua` 完全一致。
- **独立 `WaveTable.lua` / 其他 `src` 仍可能不同**：合并时必须遍历整个脚本依赖图，而非仅核对四个标准地图文件。

## 地形近似但不是哈希完全一致（尚未做结构级确认）

- `Survival_Insane_Beta1` ↔ `Survival_ExtremeDesertV2fA`
- `Survival_Insane_NvS_Beta1` ↔ `survival_NorthSouth_Barrens`
- `survival_5thdimension` ↔ `survival_5thdimension_practice`（同系列，练习玩法）

这三对当前**不得列入“可删除重复文件夹”**。需逐项比地形图、资源点、出生点、逻辑、难度和实际玩法。

## 需要检查的冗余 / 构建文件

- `survival_defense_atoll` 同目录附带 `Survival_Defense_Atoll_Old.scmap` 和 `Survival_Defense_Atoll_script_Old.lua`；先核对所有 `Scenario` / `import` 引用，再考虑从**正式包**排除，旧版原始归档保留。
- 有些地图文件夹自带 `.git/` 开发历史。正式分发可排除内部 Git 元数据，但保留开发源仓与可回滚记录；不要将 `src/` 或 `vendor/` 一并误删。

## 审计范围：压缩包的30个顶层目录

```text
5iver Survival Brainsucka
BBF_BSD_09
BBF_BlackSunDefense
Desert_Swarm_v1c_Beta
Supreme_survival
Survival Run
Survival_BlackBox_10
Survival_Escape
Survival_Escape_v3ga
Survival_Extreme
Survival_ExtremeDesert
Survival_ExtremeDesertV2fA
Survival_ExtremeNavy
Survival_Insane_Beta1
Survival_Insane_NvS_Beta1
dreamy_survival
endless_survival_defense
fort_ictus_survival
sexy_survival
sh1r3_mycelium2_survival
survival attack
survival_5thdimension
survival_5thdimension_practice
survival_NorthSouth_Barrens
survival_defense_atoll
survival_horde
survival_horde_aeon
survival_horde_aeon_fixed
survival_horde_ee
survival_sea_fleet
```

## Codex 后续每次更新的格式

```md
### [状态] 地图目录 / 问题短标题
- 来源/版本/哈希：
- 现象（Steam 版本、人数、选项）：
- 静态证据（文件+行号）：
- 游戏日志/复现步骤：
- 根因（确认 or 假设）：
- 修改路径/差异：
- 回归测试（默认+非默认、单人+多人）：
- 能否合并 / 淘汰其他文件夹：
- 未解决问题：
- PR / commit：
```

不要把“问题线索”自动标记为“已修复”。

---

## 2026-10-16：当前83张地图增量复核

此前04槽位ZIP与本次当前目录是不同快照。历史选项疑点不可直接自动套到当前文件；必须先核对来源哈希、目标大厅和实际消费路径。以下记录按当前文件重新核验。

## 证据与适用范围

2026-10-16 新增记录来自用户电脑当前 `02_生存与波次防守` 的 83 张实际地图，目标对照为本机 Steam 游戏安装。仓库没有上传这些地图源码/资源。下列为静态确认或隔离数据验证，不是 Steam 实机测试。此前 README 提及的 `04槽位.zip` 历史发现不能据此自动补造。

文件级 SHA-256、实际配置版本、当前路径及非原版单位证据见 [本轮摘要数据](data/survival_audit_2026-10-16.json)。原始本地快照 2522 个文件在移动前后均核验一致；共移动 11 张地图，未改地图内容。

## F001：单位编号正则漏检（静态确认）

旧扫描只认“若干字母 + 四位数字”，漏掉 `BRNT1EXMOB`、`BRMT3BM2MK2` 等 Total Mayhem 编号，也漏掉 `DRLK001`、`DALK003` 等 FAF 编号。应从有效单位使用位置提取任意蓝图 ID，再与目标游戏实际加载的蓝图表比较。不要仅放宽正则后把颜色、UID、注释或可选模组列表当作强制依赖。

- 症状：首波能刷不代表后期可运行；按固定编号正则会错误宣布零依赖。
- 修复方法：核对活动波表、存档、直接/间接创建与条件分支；纯数据表可在目标 Lua 中隔离求值，不能执行未知游戏入口。
- 剩余风险：动态字符串拼接、运行时蓝图克隆、字节码、MOD 挂载顺序仍需独立追踪。

## F002：明确需配套模组的 11 张（静态确认）

此分类表示完整玩法依赖，不表示每张都会在进入地图瞬间失败。Swarm/Eternals 可能只加载出空地形，单位模组图可能到后期才失败。

| 地图 / 当前相对位置 | 依赖与证据 |
| --- | --- |
| Survival Omega<br>`需专用模组/03槽位/Survival Omega` | BlackOps 单位包（后期波次）。38 分钟波表开始直接抽取 BEL0402，45 分钟加入 BRL0401；无模组检测。能开局不代表能完成后期波次。 |
| Survival_5.thD_MayhemEdition<br>`需专用模组/06槽位/survival_5.thd_mayhemedition` | Total Mayhem v1.35。作者说明明确要求；活动波表直接引用 40 种非 Steam 单位，含 BRNT1EXMOB 等长编号。BlackOps 只推荐。 |
| Survival_Mayhem&BlackOps_3D<br>`需专用模组/07槽位/survival_mayhem&blackops_3d` | Total Mayhem v1.35 + BlackOps Unleashed v14。作者明确要求两者；地面、空军和海军波表均直接使用外部单位。 |
| survival_voodoo_double<br>`需专用模组/08槽位/survival_voodoo_double` | Extreme Wars + Some Mods 2.1（作者原要求）。说明明确要求两者；7 分钟波表已含 URLEW0001，12 分钟含四族太空舰；另有 FAF 单位 DRLK001。历史模组具体版本仍需核对。 |
| eternals survival dimension<br>`需专用模组/09槽位/eternals_survival_dimension` | Mayhem Eternals Survival。作者说明为该模组制作；本地图脚本只有初始化及禁止传送，没有刷兵与完整生存胜负系统。不开模组可进入地形，但不会运行原生存玩法。 |
| swarm survival mk4<br>`需专用模组/09槽位/swarm_survival_mk4` | Swarm Survival。作者说明指定 Swarm Survival；脚本只有 InitializeArmies 和空 OnStart，波次由外置模组提供。 |
| swarm survival 10 players<br>`需专用模组/11槽位/swarm_survival_10_players` | Swarm Survival。说明为 10 人对抗 AI 的 Swarm Survival 图；11 个大厅槽含对手槽，地图内没有波次系统。 |
| Survival Unit Mayhem<br>`需专用模组/04槽位/survival_unit_mayhem` | Total Mayhem v1.35。作者明确要求；活动波表有 43 种非 Steam 单位，含 FAF 防空单位；BlackOps 只是兼容。 |
| Survival Beach Ramp Mayhem<br>`需专用模组/06槽位/survival_beach_ramp_mayhem` | Total Mayhem v1.35。说明明确要求；活动波表与 MayhemEdition 使用相同外部单位体系；BlackOps 是推荐搭配。 |
| DDDX RPG survival<br>`需专用模组/07槽位/dddx_rpg_survival` | Survival Mayhem&BO Balance + Total Mayhem + BlackOps Unleashed；BlackOps ACUs 仅需安装。作者区分启用与仅安装；除波次外，还有英雄、技能、升级、额外炮塔及资源建筑等专用单位。 |
| Survival_Mayhem&BO_3D_v1<br>`需专用模组/07槽位/survival_mayhem&bo_3d` | Total Mayhem v1.36 + BlackOps Unleashed v14；Balance 为推荐且部分功能需要。说明明确要求前两者；Balance 解锁额外资源和史诗内容，不能混称所有模组都是开局必需。 |

Omega 直接单位引用证据：`需专用模组/03槽位/Survival Omega/Survival Omega_script.lua:558`、`需专用模组/03槽位/Survival Omega/Survival Omega_script.lua:580`。BEL0402 位于 38 分钟波组，BRL0401 位于 45 分钟波组；时间是波表的相对时刻，仍受准备时间和脚本流程影响。模组归属可与同包 `survival_genesis/units/Units_BlackOps.lua` 中的分组对照。

## F003：FAF 单位缺失不能自动归为专用模组（静态确认）

| 地图 | 缺失蓝图及首次有效引用位置 |
| --- | --- |
| Dreamy Survival | `drlk001`：`04槽位/dreamy_survival/dreamy_survival_script.lua:1403` |
| Fort Ictus Survival | `drlk001`：`04槽位/fort_ictus_survival/Fort_Ictus_Survival_script.lua:516` |
| Sexy Survival | `dalk003`：`04槽位/sexy_survival/sexy_survival_script.lua:945`；`delk002`：`04槽位/sexy_survival/sexy_survival_script.lua:943`；`drlk001`：`04槽位/sexy_survival/sexy_survival_script.lua:944`；`dslk004`：`04槽位/sexy_survival/sexy_survival_script.lua:946` |
| Broad Front Survival | `drlk001`：`06槽位/broad_front_survival/Broad_Front_Survival_script.lua:501` |
| Center Arena Survival | `drlk001`：`08槽位/center_arena_survival/center_arena_survival_script.lua:372` |
| voodoo battle v1 survival | `drlk001`：`08槽位/voodoo_battle_v1_survival/voodoo_battle_v1_survival_script.lua:475` |
| Aeon Illuminate Survival | `dalk003`：`待测试_依赖与资源核对/05槽位/aeon_illuminate_survival/Aeon_Illuminate_Survival_save.lua:2628`；`zab9601`：`待测试_依赖与资源核对/05槽位/aeon_illuminate_survival/Aeon_Illuminate_Survival_save.lua:2852` |
| deadzone survival | `drlk001`：`待测试_依赖与资源核对/06槽位/deadzone_survival/deadzone_survival_script.lua:501` |
| Survival Stranded | `dslk004`：`待测试_依赖与资源核对/06槽位/survival_stranded/survival_stranded_save.lua:4715`；`xrb2309`：`待测试_依赖与资源核对/06槽位/survival_stranded/survival_stranded_save.lua:8871` |
| Dune Survival | `zeb9501`：`待测试_依赖与资源核对/08槽位/dune_survival/Dune_Survival_save.lua:2242` |
| Survival Temple | `drlk001`：`待测试_依赖与资源核对/08槽位/survival_temple/survival_temple_script.lua:372` |
| survival_生存AN_voodoo_no_mods | `drlk001`：`待测试_依赖与资源核对/08槽位/survival_voodoo_AN_no_mods/survival_voodoo_AN_no_mods_script.lua:424` |
| survival_voodoo_no_mods | `drlk001`：`待测试_依赖与资源核对/08槽位/survival_voodoo_no_mods/survival_voodoo_no_mods_script.lua:424` |
| Tomb Guard Survival | `drlk001`：`待测试_依赖与资源核对/12槽位/tomb_guard_survival/tomb_guard_survival_script.lua:501` |

特别是 `survival_voodoo_no_mods` 与 AN 版仍有活动 `DRLK001` 引用；作者的 no mods 名称并非 Steam 原版资源证明。Aeon Illuminate、Dune、Stranded 的部分引用在存档，不能只检查主脚本。建议替换与损失见 [纯原版迁移指南](VANILLA_MIGRATION.md)。

## F004：主脚本相同不代表完整玩法相同（静态确认）

Horde Aeon Fixed 与 Horde EE 的地形、存档、主脚本和菜单相同，但 23 个 `src/` 文件中 `WaveTable.lua`、`WaveOrders.lua` 不同。前者首波 `ual0201`，后者 `url0107`；协助命令的单位过滤也不同。不得只凭主脚本归并或删除；按阵营玩法分别保留。

## F005：重复预览不等于重复地图（静态确认）

Omega 与 Light 2a 的外置 DDS/large/small PNG 像素相同，地形文件和内嵌图不同；两者平坦高度数据相同不足以证明地形完全相同。NavyV28 与 Onix 的外置 PNG 相同，地形、存档和内嵌图不同。处理方法是按各自 `.scmap` 重建/选择正确预览，保留玩法，不靠缩略图去重。

## F006：Voodoo 两版限制差异（静态确认）

AN 版 `待测试_依赖与资源核对/08槽位/survival_voodoo_AN_no_mods/survival_voodoo_AN_no_mods_script.lua:938` 使用真实 `uaa0304`；另一版相同位置为目标原版没有的 `uaa0314`。这是一项有效单位限制差异，不是两版完全重复的证据，也不解决共同的 DRLK001 依赖。原注释把该限制称为实验空军，不能据注释重新推断或更改兵种意图。

## F007：特殊军队误列普通大厅槽（静态确认，影响待实测）

`09槽位/naval_survival_onix/naval_survival_onix_scenario.lua` 将 `ARMY_SUPERWEAPON` 同时放入 teams.armies 和 ExtraArmies。大厅 9 槽不应直接说明为 9 名人类合作版。应验证这一特殊槽的作者意图、占用行为、联盟/胜负与计数；本轮只记录，未删除该槽。

## F008：外置生存模式与可选 MOD 支持要分开（静态确认/待调查）

- Swarm mk4、Swarm 10 players、Eternals 的地图内没有完整波次/生存胜负实现，需要外部模式提供。删除模组后能进入地形不等于能游玩生存。
- Zhunas Crater Swarm Survival 名称与空脚本提示外置模式，但无明确模组声明，状态为 **待调查**，未移动成已确认模组图。
- desert_front、Genesis、Voodoo Battle new、Terror Lands、Onix Voodoo 按模组检测导入单位表，有原版分支。指定“仅模组单位”模式的需要不能扩大为整图必需。
- `pass_survival_aix` 的 AIX 与 TeamPlayAI 的 AI 推荐不能机械视为专用生存模组依赖。

## 证据限制

83 个场景/菜单/存档数据用例通过目标 Lua 的隔离加载，15 个候选文件编译与 15 个迁移数据用例通过；没有运行 Steam 游戏，没有实机截图、多人日志或完整引擎初始化。具体分类与保留建议见 [本轮同图复核](SURVIVAL_AUDIT_2026-10-16.md)。

## F009：本轮整合与功能兼容（已修改待实测）

- Horde EE v22：同时导入Aeon Fixed的WaveTable与WaveOrders，新增一个配对选择器；默认仍EE。只换单位表会使协助命令的阵营过滤不一致，因此必须配对。
- 黑日v2：保留作者1.0目标/成对门逻辑，增加旧版固定150000目标生命作为可选项；默认不改原公式。
- practice v9：增加已占用ARMY_1至4的人数缩放；默认固定4人。人数还影响目标生命/回血/能量，选项文字必须说明；零玩家不能向nil军队补发指挥官。
- Escape v4：移入连续路点/首领/扩区识别。缺号或为空回退原值；不能把v3ga的TotalMapExpansions误当原版TotalExpansionPoints。
- 原版单位替换13张写回，Omega移回3槽位；两张淘汰Voodoo不再另修。损失见整合报告，未宣称完整等价。
- Omega/Onix外置预览从各自scmap直接导出，不重绘地形。

本轮用户明确接受舍弃不可兼容内容，故从活动包删除12个已完整归档目录；71张最终2295个文件校验通过。此授权不自动覆盖以后删除。精确变更与版本见 [本轮元数据](data/survival_consolidation_2026-10-16.json)。

## F010：升版工具必须完整处理多位数字（静态确认，工具已修正）

部分简化Lua词法器将15拆成字符token 1和5。若只替换第一个token为16，会得到165而非16。应按完整数值字面量跨度修改，并在目标Lua中实际读取ScenarioInfo.map_version校验；不要只检查文本包含新数字。此次23张均完成实际求值和版本上限检查。Lua格式`version=3`保持原值。

## F011：同名安装目录不是版本比较的唯一身份（静态确认，内容中心集成待核对）

Mycelium、沙漠5th、Navy仍按人数保留不同内容，但既有目录名存在相同项。内容中心须以独立地图身份/人数区分；安装器不能仅按目录名互相覆盖。未经确认，不为解决上传元数据而擅改全部内部路径、地形资源路径。此次只更新map_version/显示名，未声称已验证内容中心安装或更新行为。


## F012：62张当前代码研究与明确修正（2026-10-16）

7张选项pref与key不一致：Escape的StartTime误指Difficulty；Sea Fleet、Desert Front、Genesis、Voodoo New、Terror Lands、Onix Voodoo的Wreckage偏好多了s。已按消费者使用的key统一，保留default和值；支持pref的大厅偏好混用/错拼被修正，不能扩称Steam全部自定义菜单已解决。

Genesis of the Order的`Functionality/PlayableArea.lua:10–12`与Stranded的`PlayableArea.lua:13`调用不存在的ScenarioFramework.SetIgnorePlayableRect。本机Steam模块中没有此方法；官方X1CA_001_script.lua:209使用全局接口，Steam二进制也存在该名称。已改用全局接口并传入GetArmyBrain取得的数值army index，保留AI边界豁免，不用空函数忽略错误。

9张27文件修订及严格升版见[本轮9张修正](CODE_MAINTENANCE_2026-10-16.md)；37项编译/隔离模块/偏好/版本用例通过。62张2234文件已验证。当前累计28张有改动，状态均不因这些检查升级为游戏实测通过。

## F013：全量编译失败必须区分运行文件和备用素材

627份Lua/字节码中622编译通过；Rainmakers的`info-theme.lua`是辅助数据格式，未发现活动引用；四份EventDispatcher.lua在Endless/Horde/Center EE/Aeon的vendor库中使用`...`转发，目标旧Lua不能编译，但只找到vendor测试引用，未发现生产Lua引用。它们是未来启用的兼容风险，不是已证实的地图启动失败。未为使统计全绿删除或改写这些来源文件。

## F014：保留的玩法边界和资源疑点

Zhuna没有内置生存链，来源外置模式待调查；AIX TeamPlayAI/Pass AIX是大厅AI对战布局，不应补写固定生存波次来改变原设计。Onix特殊army重叠问题仍待实测。

`.scmap`ASCII路径扫描在目标Steam/当前包未找到DDay的`/env/Seraphim II/Props/Floe_prop.bp`、Temple的`/env/Seraphim II/Props/Floe_Floe_specteam.dds`。未证明其他所有动态资产均完整，未改二进制。完整格式解析和游戏画面对照仍有必要。

## F015：AI制图参考目录与外部问题研究

[62张代码地图册](SURVIVAL_CODE_ATLAS_2026-10-16.md)包含逐图62卡片、2833个函数定义的核心位置及361个选项。25张字面量经典波次75个首波隔离用例无错误；其余复杂模块只按数据/编译和明确专项范围报告。可复用工具`tools/scan_scfa_maps.py`已在当前包运行，纯只读。

FAF与Steam共享基础但挂载/脚本/蓝图/美术资源不同，不能断言所有地图互不兼容。没有本机FAF完整资源/运行结果，不捏造贴图数量差或双端通过。已检索作者/开发者的Rainmakers任务UI、运输机击杀质量、海岸轰炸及编辑器资源/对称问题，含已关闭状态；见[外部研究](EXTERNAL_MAPPING_RESEARCH_2026-10-16.md)，不把网上Issue直接认作本包故障。

## F016：Fort Ictus中途结束后空白结算表（2026-10-18，待调查）

用户截图与补充确认：本人+3名AI，实时分数正常，中途结束后4行结算表空白。包内/本机安装v9脚本一致，未发现地图改写结算模块；中途结束由游戏tabs.EndGame调用score.CreateDialog，并非地图胜负分支。

原版score.UpdateData压缩可见军队行号，UpdateDisplay又按该行号读原始分数；隔离测试确认隐藏/稀疏军队的错配/缺项风险，但尚无证据确定本局因此触发。没有日志就不能将UI异常归咎某地图/模组，更不能冒称修好。已准备只加/log的本地启动入口，地图不变、版本仍v9。

证据位置、源文件哈希、测试范围及下一步见[专项记录](FORT_ICTUS_SCORE_INVESTIGATION_2026-10-18.md)。未自动对其他地图或全局游戏UI打补丁。

## F017：Fort Ictus第4槽是特殊堡垒，不能按4个普通队友修复（2026-10-18）

用户确认第4槽外置且开局明显更多东西；存档求值得INITIAL396条记录，前三槽0。另有ALLY/ENEMY两支ExtraArmies。用户反馈敌对，而脚本把第4槽列入防守人数和共同胜负，存在设计/运行冲突；尚未证明是3人合作加敌堡的作者原意。结盟前uaa0314无效限制可能中断初始化，须日志证实。先前v10强制合作候选未采用，两处地图仍v9且逐文件不变，不能仅修变量后宣称游戏修好。见[完整玩法调查](FORT_ICTUS_GAMEPLAY_2026-10-18.md)。

### F017恢复更新（2026-10-19）

包内v9七文件保持；此前安装图目录已缺失，两份备份完整。用户无日志。旧联盟用例跳过限制接口，不能证明初始化成功；新增573蓝图类别夹具在真实Lua封装中追踪到nil传参，但原生接口仍是记录桩，不认定实机根因。最新边界及取证工具见[恢复记录](FORT_ICTUS_RECOVERY_2026-10-19.md)。

## F018：地图目录名、基础显示名与版本号混用（2026-10-19；命名维护规则）

**问题性质：地图定位/管理问题，不是已确认的运行故障。** 用户确认本轮提供的两个原始地图都已在游戏中测试并能正常运行；当前需要解决的是按游戏名称无法快速找到对应文件夹。

- 示例 A：文件夹 `Supreme_survival`，游戏基础显示名 `Survival of the Fittest`，版本单独显示为 `Version: 1`。
- 示例 B：文件夹 `survival_5thdimension`，游戏基础显示名当前带有 `v6` 后缀，界面另显示 `Version: 1`。用户明确要求：若 `v6` 表示版本号，就不应重复放在文件夹名或基础显示名中；目标基础名称为 `survival_5thdimension`，版本应由 `map_version` 字段表达。
- **规范**：文件夹名与场景配置 `name` 字段的基础地图名一致；`map_version` 单独保存数值版本，游戏负责显示版本信息。移除版本尾缀前，必须确认它确实表示版本，而非正式地图名称的一部分。
- **改目录前检查**：备份；检查目标目录重名；审计场景 `map/save/script` 虚拟路径、导入、资源路径和硬编码旧目录引用；仅更新必要的目录前缀，不要无必要地重命名内部文件。
- **状态边界**：用户实测只确认原始目录结构能运行。本条记录的是命名规范；本仓库未修改这两个地图包，重命名后的实际加载状态尚未验证。若将 `v6` 迁移为数值版本 6，仍须核对来源历史及本仓库的升版下限规则。
## F019：Fort Ictus Survival FAF v8 的单位依赖与 Steam 迁移边界（2026-10-19）

- 上传包 `fort_ictus_survival.v0008.zip` 的 SHA-256 为 `cea02527a8cc7f73762e44031abb244ac46f6fa531a80a9c37c6257623831bf4`；ZIP 完整性检查通过，包含 5 个实际文件。
- **专用 MOD 判断**：场景/脚本没有 `/mods/`、`src/`、`vendor/` 或外置依赖包引用；只导入 `/lua/sim/ScenarioUtilities.lua`、`/lua/ScenarioFramework.lua`、`/lua/utilities.lua`。因此没有证据表明地图强制要求某个具名独立 MOD，但不能据此说它零依赖。
- 活动波次表含 `DRLK001` 13 次；该蓝图在仓库既有 Steam 蓝图索引中缺失，而 FAF 源码中存在。它是 FAF 单位资源依赖。已有候选替换为 `URL0205`，但会改变原单位强度/科技等级，必须回归后期波次和难度。
- `Fort_Ictus_Survival_script.lua:1063` 引用 `categories.uaa0314`；目标 Steam 蓝图索引未找到此项，本次可检索的 FAForever/fa 也未找到。它不在刷兵表中，属于缺失/未知的限制类别；可能向限制 API 传入 nil。实际原生 API 是否报错仍未由游戏日志确认，不能写成已证实崩溃，也不能简单判定为专用 MOD 依赖。
- `QEL01112`（第116行）、`LDUC260`（第120行）及另一个 `DRLK001`（第118行）只在注释示例中，不构成活动依赖。
- v8 的 `_save.lua` SHA-256 与维护卡 v9 完全一致；但 v8 的 `_scenario.lua`、`_options.lua`、`_script.lua` 与 v9 指纹不同，且 v8 使用 `fort_ictus_survival.v0008` 虚拟路径。不能用旧 v8 直接替代当前 v9，也不能将 v8 内容冒充新版本。
- 当前 v9 维护卡的波次单位清单已全部映射到 Steam 索引中存在的单位，但 `uaa0314` 限制仍是独立待调查风险。优先基于最新 v9 做最小修改。
- 详细文件哈希、证据边界与回归计划见 [FAF v8 → Steam 静态审计](FORT_ICTUS_FAF_V8_STEAM_AUDIT_2026-10-19.md)。本轮没有修改地图本体，也没有 Steam 实机测试。
## F020：Fort Ictus v8 派生 Steam 候选（2026-10-19）

- 候选文件：`Fort_Ictus_Survival_Steam_Candidate_v11.zip`，SHA-256 `4ac2f416230ab6439bcfbaea8b85303fe748eecb98b9b2cdfa9adf6d4fe175c3`。
- 来源仍是上传的 v8（源 ZIP SHA-256 `cea02527a8cc7f73762e44031abb244ac46f6fa531a80a9c37c6257623831bf4`），不是当前维护版 v9；v9 完整包不在当前工作目录/仓库，不能声称此候选继承了 v9 全部修订。
- 独立场景名 `Fort Ictus Survival Steam Candidate`，`map_version = 11`，虚拟目录 `fort_ictus_survival_steam_candidate`，防止覆盖现有版本。11 是隔离测试候选版本号，不是正式发布。
- 13 处活动波次 `DRLK001` 替换为 `URL0205`。这把 FAF T3 防空替换成 Cybran T2 防空，明确会降低原单位科技/强度并改变波次平衡。
- `categories.uaa0314` 调用增加 `if categories.uaa0314 then` guard，避免缺失类别作为 nil 传给限制 API；没有将第4槽结盟、人数、胜负或结算逻辑纳入此补丁。
- 静态验收：ZIP `testzip()` 通过、5 个成员、三个虚拟路径指向独立目录、活动 `DRLK001` 残留 0、guard 存在、SCMAP 哈希与原始一致。
- 状态：**已修改待实测**。未执行 Steam 编译或游戏测试。第4槽阵营/人数冲突、菜单默认值、结算表空白仍是独立风险。
- 详细记录见 [专项静态审计](FORT_ICTUS_FAF_V8_STEAM_AUDIT_2026-10-19.md)。只有取得当前 v9 完整包后，才可将最小补丁移植到 v9 并做新候选。

## F021：X1CA_TUT官方教程共享地形被独立包规则拦截（2026-10-19）

教程4文件195755字节，scenario.map引用SCMP_019/SCMP_019.scmap；与被引用地形及原对战配置共8文件均匹配Steam副本。这是正常官方依赖，不是损坏或重复玩法。当前仅教程目录不构成地形完整包，不能只取消检查。建议中心支持内置依赖清单或保持虚拟路径的合包；campaign教程与skirmish分别启动。scenario只有Lua格式version=3，没有map_version，界面显示3的来源需中心源码确认。详细证据与方案见[专项分析](X1CA_TUT_PUBLICATION_2026-10-19.md)。未改原图或实际上传。
## F022：Fort Ictus v9 炮兵 marker 前缀拼写不一致（2026-10-19）

- 来源：用户上传本机地图 fort_ictus_survival.rar，RAR SHA-256 e615d864586d2e391a2cfad6421fc52a92be6188348d8bdca20d45a793d7ad87。
- 场景读取逻辑使用 GetMarker("SURVIVAL_ARTY_" .. i)，但 Fort_Ictus_Survival_save.lua 中 4 个标记实际命名为 SURVIVAL_ATY_1..4（漏掉字母 R）。这不是地图没有炮兵点，而是脚本与存档名称不匹配。
- 原 Survival_GetPOS 对空 marker 列表直接调用 math.random(1, table.getn(...))，在炮兵特殊波次中可能触发 math.random(1, 0)。
- v10 候选修复四个 marker 名称，并为炮兵 marker 列表空/耗尽增加回退到普通出生点的保护。
- 同一候选还修正内层联盟判断变量、把玩家人数计算改为统计 ARMY_1..ARMY_4、对 categories.uaa0314 加存在性 guard，并把三项大厅默认选项对齐到第一项。
- 候选 ZIP SHA-256：1fdfc61347b65705ff558e56c7170abda341938877f09b4a4a4b95940362076b；地图文件夹与场景基础名统一为 Fort Ictus Survival，map_version = 10。
- 地形 .scmap 哈希保持不变。静态 ZIP/路径/marker/代码条件检查通过；没有执行 Steam 游戏，人数、默认选项、炮兵波次和多人联盟仍待实测。
- 详细报告：[Fort Ictus v10 Steam 修复候选](FORT_ICTUS_V10_STEAM_REPAIR_2026-10-19.md)。

## F023：Survival Omega历史地形使目录计数预检失败（2026-10-19）

安装目录含当前Survival Omega.scmap（512×256）和old.scmap（256×256），并非相同文件；scenario只引用前者。3个出生标记x=430.5，84个标记x>256，不能替换成小地形。发布宜按已选scenario闭包，未引用old另归档而非随机取首个文件。当前安装修订1仍含BlackOps单位，不能套用维护包v3结论；本次未删、未同步、未实机/上传。见[双地形分析](OMEGA_EXTRA_TERRAIN_2026-10-19.md)。

### F023后续：用户授权删除未引用旧地形（2026-10-19）

已先在工作区外部备份并核对旧文件SHA，再仅删除安装目录Survival Omega old.scmap；9→8文件，剩余1个当前SCMAP，其余8文件哈希完全不变。未改修订或玩法，未修改地图包v3。满足单SCMAP计数条件，上传结果待重新扫描；见[删除记录](OMEGA_EXTRA_TERRAIN_2026-10-19.md)。

## F024：Omega外置预览与地形内嵌预览不一致（2026-10-20，已修改待界面验证）

删除old后保留8文件的哈希与删除前相同；红色外置DDS/PNG与灰色星空背景内嵌预览原先就不同。scenario.preview为空，原版mapselect/lobby会从当前SCMAP回退取图。已先备份后仅同步3张外置预览为活动SCMAP内嵌图；DDS载荷/大图像素/小图参考缩放核验通过，SCMAP与四个Lua保持。未实测实时缓存刷新，也未升级安装副本v1的玩法。详见[来源与修正](OMEGA_PREVIEW_MISMATCH_2026-10-20.md)。

## F025：Fort Ictus v8在用户maps目录中有解压目录与ZIP（2026-10-20）

E:/SCFA/maps没有对应条目；实际位于个人Documents/My Games/Gas Powered Games/Supreme Commander Forged Alliance/maps：fort_ictus_survival.v0008目录和同名ZIP。去掉ZIP顶层包装目录后5文件SHA完全相同，两份scenario均为同名v8。SupComDataPath会挂载用户maps的目录与ZIP，原版maputil从虚拟/maps枚举scenario，能解释同名条目。未实测运行时VFS，未移动/删除；维护v9/候选不能当作此处v8。见[确切来源与路径](FORT_ICTUS_DUPLICATE_SOURCES_2026-10-20.md)。


## F026：Brainsucka的luac真实存在却被发布预检误报缺失（2026-10-20）

实际三条引用均存在，8文件SHA与10月15日一致。FACN客户端和网关仅接受_save.lua/_script.lua，客户端还把后缀不符报为缺失；打包枚举不排除luac。两端源码补齐lua/luac并保留路径、ZIP与哈希保护。隔离核心476、网关65及实际地图专项45项通过；正式EXE与真实上传未验证。见[专项](BRAINSUCKA_LUAC_AND_REQUIRED_MOD_2026-10-20.md)。

## F027：Brainsucka强制模组检测被此前文本分类漏检（2026-10-20）

主脚本SHA5196bac1…未变，目标LuaPlus实际OnStart缺少UID d36d33e5-3927-499f-8990-55555b000001时不调用正常任务初始化，提示线程还会调用缺失CreateDialogue。测试UID令其进入初始化记录桩，不等于拥有模组。已纠正04卡片及地图册；62张保留数不变，不能再据此前分类断言全部无强制依赖。没有地图修改、删除或新游戏测试。详见同一[专项](BRAINSUCKA_LUAC_AND_REQUIRED_MOD_2026-10-20.md)。


## F028：Survival Horde EE v22中途退出直接跳过结算（2026-10-20）

用户确认中途退出直接回大厅。主脚本848行Sync.CampaignMode=true，经schook UserSync进入UI；原版tabs.EndGame在战役模式下传midGame=true，score.CreateDialog直接ExitGame并return，不创建普通结算表。包/安装44文件SHA一致；与Steam安装的5种相关原始代码逐一SHA相同，目标LuaPlus5项检查通过，包含实际退出分支对照。未实机点击退出、未验证自然胜负或FAF当前版。不能将其与Fort Ictus的空白表混为一谈，也不能只关闭战役模式或导入UI模块来假装修复。独立失败条件`or "ARMY_5"`真值问题另记，未改地图。见[专项](HORDE_EE_MANUAL_EXIT_2026-10-20.md)。


## F029：Insane Beta1默认目标无武器令刷兵与分数同步均未启动（2026-10-20，已修改待实测）

Steam4玩家默认准备、10分钟无波次且结算空白。UEC1902无Weapon，setupGame在旧769–773行却按第1件武器调整射程；OnStart在启动刷兵前中断，原版schook BeginSession在地图返回后才创建统计线程。实际蓝图/完整地图/原生统计函数模型复现此链。已仅为射程调用加蓝图条目和武器对象guard，包及安装升v2，36项隔离＋3项落盘Lua核验通过；SCMAP/save/options/预览不变。外围8传送门不带炮塔，另8斯卡萨在错误前已创建；用户记不清外形，未据此加炮塔。真实UI/游戏/多人待测。见[专项](INSANE_BETA1_STARTUP_SCORE_FIX_2026-10-20.md)。

## F030：Sea Fleet同队AI敌对、刷兵不启动与空白结算（2026-10-20，用户实测确认正常）

v7主脚本462–465行墙体类别为大写键，480行xsb2406未见于本机573蓝图；按实际原版蓝图小写墙体和Yolona Oss xsb2401作最小修正，升v8。初始化若在此处异常会阻断其后的大厅队伍恢复及分数采集；原ArmyToPlayerID是槽位函数，已包含AI，联盟/人数/胜负无需重写。两处11文件一致、8个地形/数据/图像资产不变，16＋2项目标Lua检查通过。用户在部署后明确回复“没问题了”，记录为用户对本次问题的实测确认；无修复前日志，不将模型断言当作原生错误栈，也不扩大为全波次/多人/FAF通过。见[修复与方法](SEA_FLEET_ALLIANCE_STARTUP_SCORE_2026-10-20.md)。


## F031：Insane Beta1按用户要求加入传送门堡垒v3（2026-10-20，已修改待实测）

截图确认v2传送门周围没有驻防塔；这是原设计，不是本次再发现初始化丢单位。用户明确要求直接增强。已在每门加入4地面炮、4防空、双盾、雷达和反战术导弹，中档升级2SAM，高档增2XEB2306重炮，共96/112。每单位复制盾规格为直径80，保留原血量耗能；共享蓝图不变，刷兵区留空，重复生成防护、v2修复和8门胜利保留。包/安装升v3，50项隔离＋3项落盘Lua检查通过；真实战斗、寻路、盾表现及多人未验收。见[设计与边界](INSANE_GATE_FORTRESS_V3_2026-10-20.md)。

## F032：Insane v3据点太疏，按用户反馈迭代为v4（2026-10-20，已修改待实测）

用户截图确认v3建筑已出现，但要求更密集并增加地面炮、防空和盾。v4每门8炮/8防空/4盾/2反导/1雷达，23座；中档4SAM，高档另4重炮，全图184/216。收进52×52中心范围，以四主方向保留原世界坐标刷兵方框和正面出口；四盾独立规格80，不改共享蓝图。v2修复、波次与8门胜利保持。50项隔离＋3项实际落盘Lua通过，包/安装7文件一致，其他61条清单不变；用户尚未测试v4真实战斗/寻路/性能/结算。见[v4设计和边界](INSANE_GATE_FORTRESS_V4_2026-10-20.md)。

## F033：Insane v4难度、绝对时间与防区密度复核（2026-10-20，仅分析）

用户允许后续把兵刷到塔外，要求本轮先分析。9档HealthBuff为0.25/0.5/1/1.5/2/2.5/3/3.5/4，陆军每玩家10～50；门25k～400k，斯卡萨射程300～500；塔/盾/斯卡萨本体生命和普通武器无统一难度倍率。波次连续GetHealth存在低档当前血量截断歧义，两个模型结果不同，待原生验证。科技用整局时间＋5秒容差，20分准备会首刷地5/空3；菜单default字段不决定本机地图面板首选。原门10×10、盾6×6、近防2×2；本机GetSkirtRect解释与先前保守包围不同。已研究约30～31宽门防区及边界火炮向内防区，16处模型无重叠/越界、可用原盾44覆盖；另查出原核心死亡借ACU的30/40半径核爆，密集化有连锁风险。1＋36项只读隔离通过，两处v4七文件/清单不变；详见[完整分析](INSANE_DIFFICULTY_LAYOUT_ANALYSIS_2026-10-20.md)。

## F034：安装目录仍有3张全英文高级菜单（2026-10-20，只读核对）

用户要求检查E:/SCFA/maps，官方和系统不要动。排除61官方配置，检查42自定义/34活动菜单共243项，42项本机LuaPlus场景菜单求值通过。5iver Survival Land有23个、5iver Survival Land Naval有25个、5iver_survival_landnaval-swarm有7个英文标题及大量英文值/帮助，合计55项；其余31主体中文，8无自带高级设置。Grand Barrens有5处Boss，Practice有一处ARMY标识帮助。Adaptive/Endless注释中的英文不算活动菜单；AI/T1/UEF等缩写/专名不误报整图未译。960文件路径/SHA结束前后全部一致，没有翻译、删除、升版或动SCD；安装清单不替代62张维护包。详见[报告](INSTALLED_ADVANCED_OPTIONS_CHINESE_AUDIT_2026-10-20.md)。

### F034后续：三张英文菜单已汉化并各升一级（2026-10-20）

按用户明确授权，安装Land1→2、Land Naval1→2、landnaval-swarm11→12。55项菜单296显示字段汉化，6守备组合增中文帮助；key/pref/default/数值表达式/重复项和顺序保持。9项候选语义/加载＋3项实际落盘求值通过，960文件仅6个options/scenario改变、954保持，官方/系统与62维护包不动。三图26原文件完整归档SHA核验，真实UI/游戏未测。上方3张英文为历史审计状态，见[完成记录](THREE_5IVER_OPTIONS_LOCALIZATION_2026-10-20.md)。

## F035：安装生存图防区与难度菜单跨图对比（2026-10-20，仅分析）

读取42自定义，生存/AOD35张235项；排除61官方，7普通/Adaptive/TeamPlayAI仅旁证，不覆盖62维护包。5iver原函数实跑0～5档：Land/oxtreme最高32守备、Naval/Swarm24；共同4盾/8地防/8SAM，门与火炮共用模板。基于本机完整Footprint/Offset，4盾与10×10门/角炮有8对已知Skirt相交，不能把紧凑示例等同无碰撞布局。Swarm守备固定5/5/0，极端最大HP不等于开场当前HP；Endless圆环工具当前仅DEBUG入口，AOD封路塔不可击杀，不能移植为普通可摧毁核心防区。

新静态问题：Grand Barrens脚本669行用AddDamageMod(Damage×倍率×成长)，本机mohodata Weapon是附加伤害，成长关闭普通100伤害选×2得到300；Horde使用Damage×(倍率−1)得到200。4组原片段/本机方法隔离通过；未覆盖自定义投射物及其它Mod，不改图。Run的save GROUP_6/UNIT_520.type='5'（479.5,30,259.5）本机无有效蓝图；原SpawnDefenses第3区难度>2请求该组，未取得此处游戏日志。5iver Land数量“70/60”实际key=50；反核使用GiveTacticalSiloAmmo，实际拦截待测。以上均未修复、未升版，不将分析替代实施授权。

92项本机Lua检查通过：42菜单、42save、4防御函数（24组合）、1蓝图（176个）、2分区函数（54组合）、1伤害对照（4组合）。安装960文件路径/SHA保持，未新增游戏/多人实测。Insane仍v4、炮台没有同类守备，约30～31宽防区/外刷兵为候选；详见[完整分析](SURVIVAL_DEFENSE_OPTIONS_COMPARISON_2026-10-20.md)和data摘要。

## F036：Insane紧凑布局已由分析落实v5（2026-10-20，已修改待实测）

用户确认希望落实炮塔布局，两处v4→v5：门跨度52→28、边缘8Scathis加守备；各23/27座共368/432，盾近核心原直径44，独立复制规格；活门外侧陆35/空15循环点逐点取高程。原v2初始化/统计、难度选项/单位池/公式/八门胜利与核心核爆保持。50+3本机Lua检查通过，两处七文件SHA一致、另957安装文件与其它61地图清单不变；未游戏/多人通过。旧v4报告是历史，不代表当前仍未应用。详见[当前v5](INSANE_COMPACT_FORTS_V5_2026-10-20.md)。

## F037：Insane主力T3点防及反核弹药通道核实（2026-10-20，v6已修改待实测）

用户要求点防用T3、两类反导齐备；两处5→6，16核心各8/12 XEB2306、1UEB4302预装7发且自动制造、原2TMD，24/28守备共384/448。反核4×4保守模型重新检查，旧外刷/盾44/八门胜利保留。50+3检查通过，另957安装文件与其它61地图清单保持，未实射/自动补弹/多人实测。

关键接口纠正：本机UEB4302武器拦STRATEGIC MISSILE但NukeWeapon缺省，CommandCaps SiloBuildTactical，Weapon.AmmoThread(false)使用GiveTacticalSiloAmmo；原platoon AntiNukeAI:SetAutoMode(true)。5iver此前同型号接口疑点现确认匹配，不得误修为GiveNukeSiloAmmo；其它型号/模组仍核蓝图。详见[当前v6](INSANE_T3_ANTINUKE_V6_2026-10-20.md)。

## F038：v6仍有T2防空，v7按用户要求取消科技门槛（2026-10-20，已修改待实测）

用户截图确认v6防区混T2防空，旧实现只升地防且继承难度≥4的4SAM门槛。本轮两处6→7，4阵营aa统一b2304，删aa/sam两档及难度分支，全部难度每处8T3 SAM、全图128T3/0T2防空；8/12T3地防保留，雷达3101→3104，战略反核/双TMD保留。50+3检查通过，实际安装初始化模型独立核对128/0/16；未v7游戏通过。原外刷、反核供给、选项、核爆/胜利保持；其它957文件/61清单不动。见[当前v7](INSANE_ALL_T3_V7_2026-10-20.md)。

## 2026-10-21：安装35图追加开局选项，原235项不变

[安装35图新增开局设置](INSTALLED_SURVIVAL_START_ADDITIONS_2026-10-21.md)：新增210项、原有235项完整保留；389个正式Lua检查入口通过，已修改待实测。Horde32上值限制已通过场景环境变量适配。XXX原BuildTime是首波准备而非结束时间，旧分析解释已纠正。Brainsucka仍依赖原专用模组。安装Insane升v8，维护包仍v7；勿相互覆盖。

## 2026-10-21：新增菜单依赖全局函数阻断多人入口（已修改待实测）

用户点击主菜单多人无反应；实际gameselect加载时预读地图，maputil的optionsEnv为空。此前新增菜单末尾ipairs/table.insert在空环境报错，35图全部复现。已改为静态索引赋值，原235项/全部445项不变，70文件更改，安装Insane v9。35空环境＋70语法＋35原版加载器实际文件对比通过，待用户UI复测。见[多人入口选项空环境修复](INSTALLED_OPTIONS_SANDBOX_FIX_2026-10-21.md)。

## 2026-10-21：按用户截图合并重复准备菜单（已修改待实测）

35图去掉开局单位菜单“新增”字样；31图直接扩展原准备values、移除第二个选择器，4图无原菜单保留单项。原235项保留，其中31项只扩展时间，其余204项完整不变；总445→414。31模块不再读取移除键，旧缓存不会覆盖原准备；Astro同时补原解码允许值。102语法＋35候选原加载器/计时＋35落盘通过，安装Insane10、维护包7。其它552自定义文件保持，程序/官方/其它7图未写入，未游戏实测。见[准备时间合并记录](INSTALLED_PREPARATION_MENU_MERGE_2026-10-21.md)。

## 2026-10-21：开局单位语义重复与旧生成链清理（已修改待实测）

Grand旧OnPopulate/SpawnACUs与新OnStart模块可同时生成；Key虽不同但用途重叠。扩查35安装图后，用户明确“直接去掉旧的，以新的为主”，共8图删20旧菜单与定义/读取/函数/线程，保留新5控制；区分主ACU、剧情增援、only强化等不同用途。Endless旧赠送零产出规则保留在本图新回调。35准备显示统一m:ss，键值/计时不变；45文件写、609自定义不变，35scenario名称/修订及SHA不变。106语法＋35候选菜单＋36候选行为＋35落盘菜单＋36落盘行为通过，未游戏实测。详见[开局单位去重与时间显示](INSTALLED_START_UNIT_DEDUP_2026-10-21.md)。

## 2026-10-21：主动炸毁目标后的判负与结算显示需分开

用户纠正为目标开局存在、自己用ACU爆炸/核弹摧毁；不是盟军AI攻击，也不是创建失败。Insane目标OnKilled写有OnDefeat但无EndGame，本机沙盘跳过普通CheckVictory；原UI失败只给“分数”入口，点击才开表。6实际源码隔离通过，四个目标/终局函数与开局扩展前v7一致，654自定义文件SHA保持。本局无日志，是否执行到判负仍待调查；未改地图，不宣布故障已修。见[沙盘与目标死亡只读核对](SANDBOX_OBJECTIVE_RESULT_AUDIT_2026-10-21.md)。

## 2026-10-21：Practice空槽ACU补发按明确选择删除

四个Commander_X_Faction只控制空槽主ACU补发，非玩家排名/SCU。先解释两种语义，用户选删除菜单和补发；仅options/script两文件改，正常InitializeArmies及新独立单位保留，菜单13→9、总390，安装修订12未改。2语法＋候选2/落盘2（各32完整脚本占槽/缩放组合）通过，未游戏实测。见[Practice空槽补发删除](PRACTICE_EMPTY_SLOT_ACU_REMOVAL_2026-10-21.md)。

## 2026-10-21：名称重复版本清理与大厅显示

用户明确只要名称不显版本、左侧可显示，并去手写标记。16自定义scenario仅改name；既有03_lobbyenhancement.scd内mapselect仅删列表追加Version的分支，左侧代码/所有map_version/路径玩法不改。17语法＋43候选/43落盘通过，UI未实测；此轮首次按该专项授权修改第三方UI包，不能沿用旧“SCD未动”状态。见[名称隐藏版本、左侧保留](MAP_NAME_VERSION_DISPLAY_2026-10-21.md)。

## 2026-10-21：5thdimension固定INITIAL八主ACU改为单台

用户要求默认只留所选阵营一台。查明四玩家INITIAL各8台（四族各2），原InitializeArmies有存档组时不再创建所选阵营单ACU；不是新高级数量失效。已仅删32固定单位、保留空INITIAL复用原版回退，更新描述，save/scenario两文件改，652自定义保持；脚本/options/实际修订9不变。8正式入口通过，候选/落盘各128占槽/阵营/预建组合及高级额外单位通过，未游戏实测。见[5thdimension单主指挥官](FIFTHDIMENSION_SINGLE_ACU_2026-10-21.md)。

## 2026-10-21 两张安装地图发布结构（已修改待实测）

Atoll安装目录含未引用的Old.scmap，严格单地形预检失败；已完整备份后移出旧地形，活动地图字节保持。Brainsucka原save.luac实际存在，截图客户端误报；以游戏原生LuaPlus导出真实等价save.lua并使用标准_script.lua入口，不改软件。存档1719表/6938标量精确相等，候选7＋落盘9项通过，其余996安装地图文件SHA保持；待内容中心重新扫描、云端及游戏验证。Brainsucka原必需MOD保留。仅安装两图，版本仍4，维护包不动。见[完整记录](TWO_INSTALLED_MAP_PUBLICATION_STRUCTURE_2026-10-21.md)。

## 2026-10-21 用户要求统一入口

后续本轮生存地图维护遵循[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)，其中明确后续取舍优先于历史相加方案。此次知识同步仅整理文档，未新增地图/软件改动或游戏测试结果。
