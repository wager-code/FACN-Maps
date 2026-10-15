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