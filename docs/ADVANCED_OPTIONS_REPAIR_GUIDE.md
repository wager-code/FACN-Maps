# 地图高级设置修复与可选扩展：ACU、工程师、种族、数量

> 本文面向 **AI 阅读现有地图源码、修复和按需移植设置**；不是软件设计，也不是任意地图的即插即用补丁。
>
> 目标 Steam 原版自定义地图 `*_options.lua` 是否在原版大厅显示、读取和传入 sim **尚未由本仓库实机验证**。FAF 示例能工作≠Steam 原版能工作。无用户明确要求不得批量加入高级设置，默认行为不得变化。

## 1. 已核实的社区实现（原始代码定位）

1. [Genesis of the Order / 选项定义](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Genesis_of_the_Order_Survival_options.lua)：`Option_AllFactions` 包含关闭(0)、同族额外 3 名 T1 工程师(1)、同族额外 1 名 ACU(2)、其它三族工程师(3)、其它三族 ACU(4)。**数字是选项值的 key；`default` 的解释须按游戏大厅代码确认。**
2. [Genesis / Units AllFactions.lua](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Utilities/AllFactions.lua)：`SpawnAllFactions(PlayerArmies)` → `GetAllFactionOption()` → `GetUnitTable(Brain:GetFactionIndex())` → `Brain:CreateUnitNearSpot(Unit, PosX, PosY)`；使用 `GetArmyBrain`、`GetArmyStartPos` 取得玩家军队/初始位置。
3. [Genesis / GameSetup.lua](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Functionality/GameSetup.lua)：先枚举实际参与者，排除 `ARMY_ENEMY_AEON`、`ARMY_ENEMY_SERAPHIM` 等敌军，再在 `InitializeGame` 中调用额外单位生成模块。**不能把所有 `ListArmies()` 无差别视为玩家。**
4. [Survival 5th Dimension Center EE / options](https://github.com/SupremeCommanderMaps/Survival5thDimensionCenterEE/blob/master/survival_5th_dimension_center_ee_options.lua)：`opt_CenterAllFactions` 三档为 0 不生成、1 每玩家 3 工程师、2 每玩家 3 ACU，另有波次、时间、资源/目标设置。不要混淆此地图的“3 ACU”与 Genesis 的“1 ACU”。
5. 本仓库 [FEATURE_LIBRARY.md](FEATURE_LIBRARY.md) 列出用户历史地图 `Survival_BlackBox_10` 的 `opt_spawn_t1eng`、`opt_spawn_c`、`opt_spawn_sc`，以及 `survival_5thdimension_practice` 对各玩家种族的选项；这些是历史文件的静态证据，非本轮重新读取原图。

**迁移时只借鉴技术思路；保留作者信息和许可证，不未经许可拷贝完整第三方脚本。**

## 2. 先区分四个概念

| 概念 | 含义 | 不能混淆的点 |
|---|---|---|
| 玩家所属种族 | 玩家军队的默认阵营及其初始 ACU、建造菜单 | 不等于额外生成单位的种族 |
| 额外单位种族 | 选择给该玩家添加哪族蓝图 | UEF 玩家可以获得 Aeon 工程师，不自动变更玩家种族 |
| 额外 ACU | 真正指挥官，可能影响 defeat/victory 条件 | 不等于 SACU 支援指挥官，也不等于原始默认 ACU |
| 额外数量 | 在原地图默认开局**之外**追加 N 个 | 0 = 不追加，不能把“1 个”误认为总数只有 1 |

选项可能按**整局统一**或**每玩家槽位独立**配置。整局统一的方案更简单；每人独立需要目标大厅支持每槽选项，且必须识别真正已占用的玩家槽，而不是 `ARMY_X` 最大编号或 `ExtraArmies` 数量。

## 3. 四族基础蓝图参考（需按目标游戏核验）

以下 ID 能在上述 Genesis 社区示例中定位；属于**来源证据**，不是对每个 Steam/FAF 构建与 MOD 组合的认证：

| 阵营 / `GetFactionIndex()` 示例值 | ACU | T1 工程师 |
|---|---|---|
| UEF / 1 | `UEL0001` | `UEL0105` |
| Aeon / 2 | `UAL0001` | `UAL0105` |
| Cybran / 3 | `URL0001` | `URL0105` |
| Seraphim / 4 | `XSL0001` | `XSL0105` |

若要支持 T2/T3 工程师、SACU 或 MOD 新种族：**从目标 Steam `gamedata/*.scd` 或 FAF/MOD 的实际蓝图读出 ID 与类别**，不要仅凭命名规则拼接单位编号。每个 ID 必须检查实际装载、可生成、阵营、科技等级和单位类别。

示意数据映射（**不是可直接复制进地图的完整代码**）：

```lua
-- 概念片段：必须先确认引擎 API 与调用环境
local unitsByFaction = {
    [1] = { acu = 'UEL0001', t1 = 'UEL0105' },
    [2] = { acu = 'UAL0001', t1 = 'UAL0105' },
    [3] = { acu = 'URL0001', t1 = 'URL0105' },
    [4] = { acu = 'XSL0001', t1 = 'XSL0105' },
}
-- 真实值映射须检验：未知 faction 或无效蓝图不得强行创建。
```

## 4. 菜单、读取、生成的完整调用链

### 第一步：先检查大厅能否读取选项

先测试一张小范围实验副本：在 `*_options.lua` 写一个**无破坏性**选项，在目标 Steam 大厅检查是否可见，切换设置后检查 sim 是否得到不同值。需要同时满足：

- 菜单项显示：名称、各档选项与默认选项可见；
- 游戏脚本取值：`ScenarioInfo.Options.<key>` 与所选值相同；
- 实际效果：不同值产生不同单位数量/种族。

**任一步失败，都不能宣称在 Steam 新增了“大厅可选项”。** 若需额外 UI MOD、外部启动器或 FAF 才能做到，应如实标注依赖，而不是用固定补值冒充真实用户选择。

### 第二步：菜单定义（仅作结构讲解）

以下是 **示意结构**，key 前缀只是建议，不代表现成可用的 Steam 菜单方案：

```lua
options = {
    {
        key = 'opt_FACN_ExtraEngineerCount',
        pref = 'opt_FACN_ExtraEngineerCount',
        label = 'Extra engineers per player',
        help = 'Additional units; 0 keeps the original game start',
        default = 1, -- 是否代表第 1 个条目，先查目标大厅！
        values = {
            {text = 'Off (original start)', key = 0, help = ''},
            {text = 'One', key = 1, help = ''},
            {text = 'Three', key = 3, help = ''},
        },
    },
}
```

真实修图**不要覆盖已有 `options` 整表**：保留原地图全部选项，添加新的唯一键。先在目标大厅查 `default` 到底是条目索引还是键值，不可把 `default=1` 理解为“生成 1 个”而直接照抄。

### 第三步：消费设置（只在 nil 时回退）

```lua
-- 逻辑示意：值 0 表示“关闭”，不可写成 if not count then
local opts = (ScenarioInfo and ScenarioInfo.Options) or {}
local extraCount = opts.opt_FACN_ExtraEngineerCount
if extraCount == nil then extraCount = 0 end
-- 还须校验 extraCount 属于 UI 真正声明的档位，且蓝图/阵营可用
```

需检查包装选项库 `src/Options.lua`、`EntropyLib` 和各类默认值注入逻辑。有些地图在主脚本开头写缺省值，后续分支又写另一值。保证“菜单选择值 → 脚本取值 → 实际创建数量”完全一致。

### 第四步：锁定地图允许的玩家，按阵营/数量生成

1. 查 `*_scenario.lua` 的 `Configurations.teams.armies` 与 `ExtraArmies`，再看 `_save.lua` 初始单位，确定**哪些军队是当前有人参与的玩家**。
2. 参照 [Genesis GameSetup](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Functionality/GameSetup.lua) 区分玩家与敌方、观察者、NPC，空槽不生成单位。
3. 在 `ScenarioUtils.InitializeArmies()` 完成且 `Brain` 可用的适当 sim 初始化阶段运行**恰好一次**；确认默认 ACU 不会重复触发。
4. 根据选择“同族／指定族／混合族”取**目标游戏已装载**的单位 ID；固定数量应限定白名单，混合族还需定义多余数量如何分配，避免各客户端随机计算不同结果。
5. 生成位置以有效出生点为中心，但必须检查地形可走、海陆/水深、地图边界、碰撞、安全距离。不可无条件把所有单位生成在同一坐标。
6. 单位归属仍属于真正的玩家 `army`；额外单位的种族与归属军队是不同属性。
7. 单人/多人生成逻辑只在 sim 侧执行；不要让每个本地 UI 客户端各执行一次。日志要记录每个玩家预期及实际数量。

### 第五步：ACU、SACU 胜负语义单独审计

- 原地图可能按“默认 ACU 死亡即失败”、按“全 ACU 死亡才失败”或按“守护目标死亡失败”。
- 添加第二台 ACU 不应未经设计就变成多一条命；指挥官自爆、消失、赠送、被俘、玩家退出和队伍结束都需测试。
- SACU 是另一种单位类别；若特殊生存模式限制建造单位或统计 ACU，新增 SACU 与高级设置必须同步考虑限制逻辑。
- 不允许默默重写原地图的 `Victory` 设置来掩盖失败；要先理解目标胜负判定。

## 5. 推荐用户可选维度（按可验证程度分级）

| 维度 | 起步方案 | 注意 |
|---|---|---|
| 工程师数量 | 关闭 / 1 / 3（示例档位） | 默认关闭，未来扩档位需压力测试 |
| 工程师等级 | T1 为第一批，T2/T3 后续 | 蓝图核验、初始资源/游戏平衡 |
| 额外 ACU 数 | 关闭 / 1（建议第一批测试范围） | 胜负、多人同步风险高 |
| 额外 SACU | 关闭 / 1（独立选项） | 不得混为 ACU |
| 额外单位种族 | 跟随玩家 / 四族指定 / 三个其它种族 / 混合 | 玩家本身阵营不变；分配规则明确 |
| 影响玩家范围 | 所有已参加的玩家 | 单槽自选必须有真实大厅支持证据 |

这些是**推荐研究档位，不代表硬上限或已实测可用**。数量扩大以后考虑出生点容纳、游戏平衡、单位/线程性能以及玩家公平性。

## 6. 自动修复常见陷阱

- 选项 `pref` 误抄到别的选项；`default` 与 `values[].key` 解释错误；
- 在 `OnPopulate` / `OnStart` 两处都调用“额外单位生成”，重复刷出；
- 直接遍历 `ARMY_1..ARMY_16` 给无人槽生成幽灵单位；
- 把自定义 AI/NPC、`NEUTRAL_CIVILIAN` 等算作玩家；
- 生存地图通过 SpawnWithArmy/INITIAL 预置 ACU，却仍按默认再生成一台；
- 全部新增单位固定为 UEF 蓝图，忽略玩家选的 Aeon/Cybran/Seraphim；
- 选项关闭（0）与 nil 混为一谈；非法负数/字符串导致不受控刷怪；
- 多人仅验证“生成成功”，却忽视 ACU 失败逻辑、同步和退出。

## 7. 测试矩阵：新增高级设置至少覆盖

| 场景 | 预期 |
|---|---|
| 关闭全部新增选项 | 与原地图开局、人数、种族、胜负一致 |
| 工程师 1 / 3，分别四族 | 数量和蓝图准确，归属于正确玩家 |
| 指定别族工程师 | 玩家本身阵营不变，单位种族按选择生成 |
| 混合四族 | 所有单位来源准确，数量/分配策略确定 |
| 额外 1 ACU / 关闭 ACU | 创建恰好一次；死亡条件仍按预期 |
| 1人 / 2人 / 满员 / 空槽 / 跳号槽位 | 仅为参与者生成，NPC 不受影响 |
| 初始单位已预置 / 默认 ACU | 没有多余重复生成 |
| 目标 Steam 大厅 / FAF 大厅分别 | 菜单可见、读值、效果三个环节独立验证 |
| 玩家死亡/退出/赠送单位/多人 | 无错误胜负、无不同步 |
| 改回默认/回滚旧地图 | 原玩法不退化，SHA 及变更清单可追踪 |

## 8. 记录到 AI 可持续维护的功能案例

每次成功分析一个高级选项，填入 [FEATURE_LIBRARY.md](FEATURE_LIBRARY.md) 并记：地图名/仓库+commit+路径、选项 key/default/values、消耗位置、最终 Unit ID/Army/Position API、版本差异、所需素材/MOD、默认和最大设置、异常情况、玩家数测试、实机状态和补丁链接。

**可见菜单、成功编译、生成单位、胜负正确、多人同步**五项是不同证据，不得合并为一个“已修复”。
