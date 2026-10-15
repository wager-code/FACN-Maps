# SCFA Steam / FAF 地图接口证据表（供 Codex 修复时查阅）

> 不是“所有 API 已跨版本验证”的白名单。来源分为：①社区源码实际调用、②FAF 游戏源码可定位、③目标 Steam 版本实机/本机 `gamedata/*.scd` 验证。**目前本表主要达到①②，③待提供与测试；不能据此宣布 Steam 兼容**。
>
> 有新接口时追加：API 签名/参数、定义位置、调用位置、sim/UI 运行环境、适用游戏构建、Steam 证据、FAF 证据、替代路径和最小用例。

## A. 地图装载与生命周期

| 名称/文件 | 用途与上下文 | 源证据 | Steam 校验与关键风险 |
|---|---|---|---|
| `ScenarioInfo` | 场景表、`map_version`、地图与脚本路径、`Configurations` | [FAF 地图版本指南](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md) | 版本、目录、`map/save/script` 一致；`version=3` 不等于 `map_version` |
| `ScenarioInfo.Options` | 在 sim 中读取玩家选项（在支持的大厅/脚本条件下） | [Genesis options](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Genesis_of_the_Order_Survival_options.lua) + [Genesis AllFactions](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Utilities/AllFactions.lua) | Steam 原版能否显示自定义 `*_options.lua` **未验证**；需大厅截图、取值日志、效果对照 |
| `OnPopulate()` | 场景填充生命周期入口 | [FAF 指南脚本示例](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md) | 与 `OnStart` 先后顺序、重复初始化与默认 ACU |
| `OnStart(...)` | 开始游戏后的逻辑入口 | 同上 | 线程/刷怪启动时机、某些地图自定义签名 |
| `import('/lua/sim/ScenarioUtilities.lua')` | 加载场景/军队辅助 | [FAForever/fa 的 ScenarioUtilities.lua](https://github.com/FAForever/fa/blob/develop/lua/sim/ScenarioUtilities.lua) | Steam 是否同文件、同导出；虚拟路径与大小写 |
| `ScenarioUtils.InitializeArmies()` | 初始化地图各 Army | [FAF 官方脚本示例](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md) | 根据当前地图既有处理确认何时、是否已调用，不要插两次 |

## B. 玩家 Army、阵营与单位

| 接口 | 参考用途（不擅自扩展未核实语义） | 有效来源 | 必须验证 |
|---|---|---|---|
| `ListArmies()` | 枚举参与场景的 Army | [Genesis GameSetup.lua](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Functionality/GameSetup.lua) | 不意味着枚举结果全部是人类玩家，需排除 NPC / 敌军和无效槽 |
| `GetArmyBrain(armyName)` | 按 Army 名称取得 Brain 对象 | [Genesis AllFactions.lua](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Utilities/AllFactions.lua) | 空槽/未初始化可能为 nil；不要先用后判 |
| `Brain:GetFactionIndex()` | 得到军队阵营索引，Genesis 映射 1–4 | [Genesis AllFactions.lua](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Utilities/AllFactions.lua) | 阵营索引/其他模组阵营需目标游戏核验 |
| `Brain:GetArmyStartPos()` | 取得玩家起始位置（Genesis 以 PosX/PosY 使用） | 同上 | 生成地点不是必然安全地点；地图边界/碰撞/陆海适性 |
| `Brain:CreateUnitNearSpot(unitId, x, y)` | 参照 Genesis，在出生点附近附加生成单位 | 同上 | 单位蓝图需存在；目标 Steam API/生成表现待测；返回与失败情形 |
| `CreateUnitHPR(id, army, x,y,z,h,p,r)` | 通过指定 Army、坐标和朝向创建单位 | [5th Dimension Center EE 脚本](https://github.com/SupremeCommanderMaps/Survival5thDimensionCenterEE/blob/master/survival_5th_dimension_center_ee_script.lua) | 所有数值、army、位置及源目标构建实际签名 |
| `ScenarioUtils.MarkerToPosition(name)` | 以地图标记取得坐标 | [5th Dimension Center EE 脚本](https://github.com/SupremeCommanderMaps/Survival5thDimensionCenterEE/blob/master/survival_5th_dimension_center_ee_script.lua) | 对照 `_save.lua` 实际标记；nil 时不能继续索引 |
| `GetListOfUnits(...)` | 查询某军队单位集合 | [FAForever ScenarioUtilities.lua](https://github.com/FAForever/fa/blob/develop/lua/sim/ScenarioUtilities.lua) 及 [Genesis](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival) | 避免每帧全图扫描；类别过滤与军队空值问题 |

注意：例子里 `GetArmyStartPos()` 接收的是地图开始位置，与 `CreateUnitHPR` 所需的三维坐标、朝向不同；**不能不经转换就传入另一接口**。建立一个经过当前引擎证明的生成位置适配逻辑。

## C. AI、线程、胜负、菜单

| 接口/概念 | 修图意义 | 风险 |
|---|---|---|
| `ForkThread(...)` / `WaitSeconds(...)` | 生存波次、计时与事件线程 | 重复启动、无间隔循环、后期性能；确认目标 Lua 方言 |
| `ScenarioFramework`、`SimObjectives` | 任务目标、完成/失败及部分地图事件 | 不同游戏构建行为可能不同；不可全局直接照搬 |
| `ScenarioInfo.Options.Victory` | 地图可能覆盖默认胜负模式 | 原 ACU 死亡/全 ACU 死亡/目标死亡必须明确测试 |
| `GetFactionIndex` + Blueprint ID | 选定额外单位种族 | **单位种族≠玩家 Army 所属种族** |
| `*_options.lua` 的 `key/pref/default/values` | 菜单定义与偏好、默认项 | `default` 可能是条目序号而非 `values[].key`，必须看当前大厅加载逻辑 |
| `import('/lua/ui/...')` | UI 环境模块 | 地图主模拟脚本不可把 UI API 当成 sim API 直接调用 |
| `src/vendor` 或 `.luac` | 外置库/编译 Lua | 递归检查全部依赖；字节码不保证跨版本兼容 |

上述第三段为审查对象，不是全部接口都已查明具体 Steam/FAF 签名。需继续从目标 Steam 安装脚本及 FAF 当前源码建立逐条定义定位证据。

## D. 参考工程中的完整调用路径（AI 必须追踪）

**Genesis of the Order：** `*_options.lua:Option_AllFactions` → `Functionality/GameSetup.lua:InitializeGame()` → `Utilities/AllFactions.lua:SpawnAllFactions(PlayerArmies)` → `GetAllFactionOption()`（选 ID）→ `GetUnitTable(Brain:GetFactionIndex())` → `Brain:CreateUnitNearSpot(...)`。

工程名和所需文件：
- [游戏选项声明](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Genesis_of_the_Order_Survival_options.lua)
- [初始化时机和实际玩家 Army 集合](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Functionality/GameSetup.lua)
- [种族及生成逻辑](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival/blob/main/Utilities/AllFactions.lua)

**Horde EE：** `*_scenario.lua` 声明 `/maps/survival_horde_ee.v0021/`，`*_script.lua` 有指向固定地图目录的 `src/`、`vendor/EntropyLib/src/` 导入路径；更名时必须处理整条 VFS 依赖链，不能只改 scenario。

- [Horde EE 场景](https://github.com/SupremeCommanderMaps/survival_horde_ee/blob/master/survival_horde_ee_scenario.lua)
- [Horde EE 主脚本](https://github.com/SupremeCommanderMaps/survival_horde_ee/blob/master/survival_horde_ee_script.lua)

## E. Codex 每遇新接口的增量记录模板

```text
接口 / 所属环境（sim/UI）：
定义源码仓库、commit、文件+行号：
样例地图仓库、commit、文件+行号：
参数与返回值（未核实处注明）：
Steam 安装版本/安装资源定义证据：
FAF 构建/定义证据：
对应单位蓝图与额外依赖：
默认、异常、空槽、多人用例：
状态（源码可见 / 静态确认 / 已修改待实测 / 实机结果）：
风险 / 兼容替代 / PR：
```

**仅凭链接到 FAF 源码，绝不在“Steam 已验证”一栏填写是。** 保持适用版本和运行环境可追溯。
