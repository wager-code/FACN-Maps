# Steam 原版 / FAF 地图 Lua 兼容与修复手册

> 目标：Steam 版《Supreme Commander: Forged Alliance》。本文件是 **问题定位方法与审查规范**，不是“接口全部已验证”的承诺。凡涉及目标游戏引擎实现的结论，都应在当前 Steam 安装的 `gamedata/*.scd`、游戏日志或实机测试中证实。

## 1. 先核对游戏环境，不直接照抄 FAF 源码

1. 确认正在运行的 Steam 游戏版本、exe 路径、安装位置、地图搜索目录与加载方式；同时记录是否安装了其他 MOD、UI MOD、地图加载器。
2. 以 Steam 实际加载的游戏脚本和内容为基准：检查 `gamedata/*.scd` 里的 `/lua/`、`/units/`、`/projectiles/` 等资源。必要时仅在临时目录解包检查，不修改原始 .scd。
3. FAF GitHub 开源代码适合了解玩法与扩展实现，**不能单凭 FAF 存在某函数就假定 Steam 一定支持**。不同版本可能函数名相同而参数、线程环境或行为不同。
4. 建议制作表格：调用位置 | API/路径 | Steam 中存在？ | 参数/返回行为 | FAF 差异 | 替代方案 | 实测日志。
5. 检查虚拟文件系统挂载顺序与冲突地图。文件被另一个地图/MOD 覆盖时，日志与表面文件不一定相符。

参考：[FAF 地图版本指南](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md)、[FAF 源码（仅参考）](https://github.com/FAForever/fa)、[FAF 文件加载方式参考](https://github.com/HUSSAR-fa/faf)。

## 2. 典型地图文件的职责

| 文件 | 重点字段/逻辑 | 常见故障 |
| --- | --- | --- |
| `<map>_scenario.lua` | `ScenarioInfo`，`map`、`save`、`script`，`size`、`map_version`，`Armies`/`ExtraArmies` | 地图找不到、路径错、槽位与额外军队不匹配 |
| `<map>_save.lua` | `MASTERCHAIN`、`Markers`、`Units`、`INITIAL`/`WRECKAGE` | 出生点缺失、标记不存在、AI/防守物件未生成 |
| `<map>_script.lua` | `OnPopulate`、`OnStart`、刷怪、胜负判定、阵营与 AI | 开局失败、波次停止、队伍错乱、胜负无法结束 |
| `<map>_options.lua` | `options`、`key`、`pref`、`default`、`values` | 选项不显示、复用错键、默认难度变更 |
| `.scmap` | 地形、地图对象与图像内容 | 格式不兼容、资源缺失、地形损坏 |
| `.luac` | 编译后的 Lua 字节码 | 不同引擎/编译格式不兼容、源代码不可直接改 |

**所有相对文件引用、地图目录名、虚拟路径 `/maps/<folder>/...` 必须一致（包括大小写）。** 变更名称时核对每处 `import()` 与保存数据引用；不要简单全局替换字符串造成脚本逻辑改变。地图的 `size` 和地形尺寸不能随意篡改。

## 3. 重点接口（逐个定位调用源和引擎定义）

| 接口或模块 | 可能用途 | 检查重点 |
| --- | --- | --- |
| `import('/lua/sim/ScenarioUtilities.lua')` | 地图初始化、标记/单位组工具 | 目标环境具体导出函数及返回结果 |
| `ScenarioUtils.InitializeArmies()` | 初始化军队 | 是否调用一次；初始单位对默认指挥官生成的影响 |
| `OnPopulate()`, `OnStart(...)` | 脚本入口 | 运行先后顺序、重复调用、线程开始时机 |
| `GetArmyBrain(name)` | 取得军队 Brain | 名称是否存在、空槽是否导致 nil、敌方/友方判断 |
| `ScenarioUtils.MarkerToPosition(...)` | 标记坐标 | `_save.lua` 的标记是否存在、坐标合法 |
| `CreateUnitHPR(...)` | 创建单位 | 蓝图是否内置，所属军队、朝向、海陆空有效位置 |
| `ForkThread(...)`, `WaitSeconds(...)` | 后台游戏模拟任务 | 生命周期、退出条件、重复启动、模拟负载 |
| `ScenarioInfo.Options` | 游戏设置值 | 键、类型、默认、是否来自真实大厅 |
| `ScenarioFramework`, `SimObjectives` | 目标、胜负、可玩区域 | Steam 中可用范围与返回行为 |
| `GetListOfUnits(...)` / 类别表达式 | 侦测/统计单位 | nil brain、单位过滤、遍历频率 |
| `ScenarioInfo.Options.Victory = 'sandbox'` | 地图覆盖默认胜负规则 | 是否需要完整自定义胜负判定，避免永远不结束 |

特别关注：

- **UI / sim 分离**：模拟脚本直接 `import('/lua/ui/...')` 可能有环境问题；核对 API 是否属于 UI 线程、是否可在游戏 sim 中调用，必须查真实游戏日志。
- **编译字节码**：`.luac` 不保证跨游戏版本可执行；无来源时不要编造“解码成功”。检查它的来源、授权、字节码格式和日志，尽量找可维护的合法源码。
- **单位蓝图**：只要地图引用一个 FAF 或第三方 MOD 专用单位，Steam 无对应蓝图就可能在特定波次才报错。检查 **所有分支/所有波次** 而非仅首波。
- **引擎特定 Lua 方言**：游戏脚本可能有 `#` 注释、不同的循环语法或引擎扩展；普通 Lua 5.x 检查器报告的语法错误未必是游戏错误。不要未经验证就机械转换。
- **模块自带库**：如果 `vendor/` 已经随地图一起打包，优先确认在 Steam 中的具体支持程度，再决定需不需要移植、替换或裁剪。

## 4. 自定义大厅选项：最大兼容陷阱

FAF 地图能展示自定义 `_options.lua`，**不等于 Steam 原版游戏大厅能加载相同格式**。最小验证必须分三项：

1. Steam 游戏大厅是否显示选项（截图/日志）。
2. 游戏启动后是否能在模拟代码中读到所选值（受控日志）。
3. 切换两个不同选项后行为是否真的不同（如准备时间/工程师数量）。

若第 1 步不通过，不能靠在 `_script.lua` 里补默认值来宣称“新增了大厅选项”。需评估目标 Steam 版的可行入口，若必须改游戏本体、装 MOD 或替换 UI，则告知用户并标注依赖；优先保留默认玩法兼容性。

### 选项审计顺序

- `options` 里每项 `key` 与 `pref` 是否一致且不冲突；特殊设计例外需注释。
- `default` 究竟表示 **列表位置**、**选项键值** 还是特定加载器语义？**必须从目标游戏/FAF 对应的选项解析代码及实测确认**，不能全地图套用统一解释。
- `values[].key` 的类型（数字/字符串/布尔）是否与脚本比较、数学运算一致。
- 缺失字段是否只在 `nil` 时回退，不要用 `if not value` 覆盖合法的 0/false。
- `pref` 不要误复制别的选项名称，避免游戏大厅偏好互相污染。
- 所谓“默认”提示文字需与选项实际落地一致；不要凭界面标注就修改原作者选择。

**安全的值读取示意（仅逻辑概念；真实语法/执行阶段以游戏引擎为准）：**

```lua
local opts = (ScenarioInfo and ScenarioInfo.Options) or {}
local startSeconds = opts.StartTime
if startSeconds == nil then
    startSeconds = 0  -- 仅当已核实原设计默认是 0
end
startSeconds = tonumber(startSeconds) or 0
```

启动参数和选项的兼容性应先通过小范围地图实验确认，再批量迁移。

## 5. 工程师、指挥官及阵营扩展

- **先找玩家对应 army**，不要假设所有玩家总在 ARMY_1…ARMY_4，亦不要把特殊 NPC 当成玩家；从军队对象与实际占用槽位判断。
- `InitializeArmies` 后再选合适的初始化时机生成额外单位，防止与引擎默认指挥官重复、预置 INITIAL 单位互相干扰。
- `CreateUnitHPR` 之前检查单位 ID、军队 Brain、位置、地形/水深、地图边界和生成安全间距。
- 工程师等级按阵营使用真实 Steam 蓝图，不可将 FAF 自定义单位 ID 当作内置；选项关闭时 **零额外单位**。
- 指挥官/支援指挥官模式需核对 **自爆、死亡、复活/替代目标、队伍胜利**，不能只保证生成成功。
- 阵营选择与图形/初始单位一致；空玩家槽位不能生成幽灵指挥官。
- 刷怪阵营及波次切换必须同时更新独立的波次表与判断逻辑，避免只有 UI 标签改变。

## 6. AI、刷怪、胜负与联机同步

- 先把“加载成功”和“功能正常”区分开；首波成功也可能在 T2/T3/实验级时遇到不存在的蓝图。
- 关注 `Random()`、循环波次状态、游戏计时器、不同机器触发次数是否一致；不要在仅 UI 客户端上决定 sim 结果。
- 防止重复 `ForkThread`、永远无法退出的 while、无间隔循环、大量 `GetListOfUnits` 全图扫描、单位数量无上限；需要可配置的生成上限与性能观测。
- 占用槽位少于配置槽位时，应有明确 AI/玩家处理，不能盲目对 nil 军队执行 `OnDefeat` / `OnVictory`。
- 启用自定义 `Victory='sandbox'` 时，**成功、失败、玩家退出、目标毁灭** 都要有相应状态终止与多人一致性验证。
- 对条件型地图要测试有 MOD / 无 MOD、1/2/4 人、不同出生槽位、默认/自定义难度，以及至少多个代表性后期波次。

## 7. 地形相同 ≠ 玩法冗余

去重分层：
1. 文件夹全文件 SHA-256 一致 → 全量副本候选。
2. `.scmap` 相同但脚本不同 → **同地形不同玩法**，需对比脚本、选项、波次表、单位及胜利规则。
3. 地形近似 → 需要二进制结构、地形预览、资源/标记以及脚本证据，不能凭名字删除。
4. 合并需保留基准版本，并验证新增模式覆盖原差异。不能验证的版本留存并标记。

## 8. 排错方法

建议先记录 `game.exe` 实际参数与启动方式，在测试环境启用游戏支持的 `/showlog`、`/log`（以当前版本实测为准），使用 **已存在、可写的日志目录**；避免让测试日志覆写正式日志。

每个故障保存：地图文件夹、文件/行号、游戏构建、启动选项、玩家槽位、错误堆栈、第一次故障时间、预期与实际行为、变更前后结果。

**没有跑 Steam 原版，不得写“Steam 已兼容”。**

## 参考文档与证据级别

- [FAF 地图版本指南](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md)
- [FAF Lua 源码（参考）](https://github.com/FAForever/fa)
- [FAF 社区关于地图初始单位与默认指挥官生成的讨论](https://forums.faforever.com/viewtopic.php?f=53&t=19289)
- 地图包事实与待调查项：见 [KNOWN_MAP_FINDINGS.md](KNOWN_MAP_FINDINGS.md)。

本文中列出的引擎 API 仅为**待核验审计清单**，不是对 Steam 兼容性的证明。

## 2026-10-16 现场补充：依赖与预览分层

- 单位ID不是固定“字母+四位数字”；Total Mayhem长编号、FAF的DRLK001等必须从实际使用点提取。大小写先规范化，注释与字符串要用支持FA方言的词法处理，不能直接在所有文本上套正则。
- 静态线索分为：强制导入/直接单位/活动波次，按检测启用的可选支持，FAF原生资源差异，贴图/道具缺失，地图不带波次但为外置模式制作。每类证据不同，不统一塞入“需MOD”。
- 外置图像像素相同、内嵌预览相同、高度数据相同、完整scmap相同，是四个不同结论。地图高度全平时碰撞哈希不能证明地形相同。
- 主脚本相同仍须递归比较导入的独立波表/命令表；Horde Aeon Fixed与EE提供了实际反例。
- Scenario teams.armies可能含特殊军队；与ExtraArmies重复时先查作者设计、初始化和胜负，不直接宣布玩家人数。
- 未启动游戏只能记录静态确认或候选已修改待实测；成功求值波表不等于单位创建、模型、武器或网络同步通过。

具体证据见 [已知发现](KNOWN_MAP_FINDINGS.md)，去模组的逐图方案与不可避免损失见 [迁移指南](VANILLA_MIGRATION.md)。

## 整合版本与标记检测补充（2026-10-16）

- 本轮使用目标Lua的string.find捕获编号，避免假定现代Lua的string.match可用。连续编号要验证起点/最大值/数量一致；缺号回退原设计，不将未知标记简单计数。
- 玩家缩放只统计明确防守army，排除ExtraArmies和补发的额外ACU；原脚本将同一人数用于目标属性时，菜单和报告需同步说明副作用。
- 波表与命令表要共同切换：Horde万古模式的单位替换不只影响刷兵，还影响协助命令的单位过滤。
- 升版检查ScenarioInfo.map_version，不改Lua格式version=3；完整数值字面量替换后必须实际求值核验。显示名、元数据清单与场景值一致。
- 保留内部旧文件名/作者版本历史作为来源，不据文件名中的v1断言当前上传版本低。真正的地图内容身份与安装目录冲突须另行确认。

精确来源、保留与舍弃见 [整合记录](CONSOLIDATION_2026-10-16.md)。


## 2026-10-16：实际Steam接口、旧Lua和双端资源

- `SetIgnorePlayableRect`是原生全局接口，不是当前Steam `ScenarioFramework`模块方法。对照Steam官方X1CA_001:209；以`GetArmyBrain(name):GetArmyIndex()`将命名army变成数值索引。Order/Stranded误用已修，区域与军队不删。
- 基础ScenarioUtilities源码在本机`mohodata.scd`内，而非必须在`lua.scd`；定位API应遍历实际所有挂载SCD，不因一个压缩包没有便宣布缺失。
- Lua5.0式vararg函数定义可接受`...`参数列表，但不能直接作为表达式转发。现有备用EventDispatcher四份因此编译失败。未来若改造应保留参数个数及中间/末尾nil，测试监听器增删和一次性监听，不只让编译通过。
- 不能用“所有扩展名.lua都编译成功”代替加载链分析：info-theme辅助数据不是运行入口；反之也不能忽略运行时真正会导入的失败模块。
- Steam与FAF共享基础资源且加载不同扩展；SCMAP v56/v60不是Steam/FAF的对应编号。详见[双构建配置](AI_MAP_AUTHORING.md)与[原始来源](EXTERNAL_MAPPING_RESEARCH_2026-10-16.md)。未验证FAF，不报告双端通过。

## 2026-10-19：初始化测试不能将缺失类别兜底为任意值

Fort Ictus调查的旧队伍用例把AddRestriction作无操作桩，并给任意类别键返回占位值，因此绕开了结盟前的uaa0314风险。573蓝图类别夹具加实际Lua封装只能证明该夹具里的参数流；原生AddBuildRestriction未执行，不能据此声称游戏崩溃。先取得当前构建的日志和首个错误栈，分开记录静态缺失、Lua参数转交与原生行为。
## 2026-10-19：Fort Ictus v8 — FAF 单位依赖与具名 MOD 依赖分开判定

`fort_ictus_survival.v0008` 只有三个常规游戏模块导入，没有 `/mods/`、`src/`、`vendor/` 或外置 MOD 包引用。不要把“没有具名 MOD 导入”写成“完全原版兼容”。

- 活动波次 `DRLK001` 在仓库目标 Steam 蓝图清单中不存在，但存在于 FAF 源码。它属于直接单位蓝图依赖，不要求地图脚本一定显式 import MOD 才会依赖该蓝图。
- 注释掉的备用波次示例里的单位 ID 不等于活动依赖；要剥离注释后核对真正的活动表、存档单位和条件分支。
- `categories.uaa0314` 是另一种问题：它出现在 `ScenarioFramework.AddRestriction` 中，而不是创建/刷出单位的位置。缺失类别可能向原生限制 API 传入 nil；应区分静态缺失、Lua 参数流与原生运行结果，未取得日志不能宣称已崩溃。
- v8 的存档文件与当前 v9 相同，但 scenario/options/script 指纹不同。只把 v8 用作来源审计；实际修复应基于最新 v9，避免丢失已做的单位替换和路径修订。

详见 [Fort Ictus FAF v8 静态审计](FORT_ICTUS_FAF_V8_STEAM_AUDIT_2026-10-19.md)。
## Fort Ictus 候选补丁：缺失单位与缺失类别分开处理（2026-10-19）

v8 派生测试候选中采用两个不同策略：

- 活动波次蓝图 `DRLK001` 确认不在目标 Steam 蓝图索引中，按仓库已有候选映射替换为 `URL0205`。此类替换会改变原单位属性与波次平衡，必须记录损失并测试。
- `categories.uaa0314` 是传入限制 API 的类别值，不是直接刷出的单位 ID。仅当该字段存在时才调用 `AddRestriction`，避免将 nil 传入原生接口；不能把这个 guard 写成已证实的崩溃修复，仍需游戏日志/实机验证。
- 这个补丁仅作用于 v8 派生候选，不自动证明当前 v9 已修复。v9 与 v8 的 script/options/scenario 指纹不同，移植前必须比较文件并将改动以最小差异应用。

## 官方教程跨地图引用与发布闭包（2026-10-19）

X1CA_TUT原版scenario复用SCMP_019.scmap，独立save/script/strings仍属于教程。共享地形是官方正常设计，不能直接判坏或删除重复；发布时则必须明确内置依赖或带齐依赖并保持路径。不能只把campaign改skirmish绕过打包器。其version=3是Lua格式，map_version未声明，内容中心须与发布修订分开。见[X1CA_TUT案例](X1CA_TUT_PUBLICATION_2026-10-19.md)。
## Fort Ictus v9：marker 拼写不一致与空列表防护（2026-10-19）

本机 v9 包中，Fort_Ictus_Survival_save.lua 的炮兵标记名为 SURVIVAL_ATY_1..4，而脚本使用 GetMarker("SURVIVAL_ARTY_" .. i)。少一个字母 R 会让脚本读不到原本存在的标记。审计时不能只搜索脚本期待的名字，然后断言地图缺少该标记；必须比对 save 中实际键名。

原脚本的 Survival_GetPOS 对空表执行 math.random(1, table.getn(...))，空表会产生非法随机范围。v10 候选同时修正四个存档标记名，并为炮兵 marker 列表缺失/耗尽增加安全回退。修正拼写是主修复，回退只是防御性保护。

候选另修复内层联盟判断的变量错误，并统一显示名/目录名与版本字段。人数计算、选项默认值和缺失类别 guard 仍需 Steam 实机确认。详见 [Fort Ictus v10 修复报告](FORT_ICTUS_V10_STEAM_REPAIR_2026-10-19.md)。

## Omega预览选择与资源同步（2026-10-20）

本机原版mapselect.lua:364–365和lobby.lua:1016–1017先尝试scenario.preview，失败后SetTextureFromMap读取活动地形。preview为空时，文件夹旁边的外置PNG/DDS不一定就是游戏显示来源。旧安装Omega原外置红图与内嵌灰色星空图不同；只提取已有内嵌DDS并生成同源PNG即可同步外置预览，不能重绘或更改地形。详见[专项记录](OMEGA_PREVIEW_MISMATCH_2026-10-20.md)。

## 安装maps不是唯一地图来源（2026-10-20）

本机SupComDataPath.lua还会挂载SHGetFolderPath(PERSONAL)下的My Games/Gas Powered Games/Supreme Commander Forged Alliance/maps，mount_contents可同时挂载目录与ZIP，并移除zip/scd后缀生成挂载点。原版maputil从虚拟/maps递归枚举scenario。Fort Ictus v8的解压目录与同名ZIP同时存在，可产生同名同版场景来源；ZIP有顶层包装目录，不能不核对成员层级就当作等价可用的单独挂载包。定位地图先查scenario显示名、实际路径和哈希，不仅搜索安装文件夹名称。只读定位不构成删除授权。见[案例](FORT_ICTUS_DUPLICATE_SOURCES_2026-10-20.md)。


## 中途退出没有结算：先区分界面模式（2026-10-20）

地图scenario的type='skirmish'不保证普通UI。检查主脚本Sync.CampaignMode，再追实际schook.scd中的UserSync同步块、campaignmanager.campaignMode和tabs.EndGame。在本机Steam代码，战役中途退出传score.CreateDialog(nil,nil,nil,true)，其midGame分支直接ExitGame并return，普通结算界面不会创建。基础UserSync位于mohodata.scd，战役扩展在schook.scd，不能只查lua.scd。

“没有打开结算”与“打开但数据空白”分别调查；手动退出、自然胜负、退出程序也不是同一入口。不要在地图模拟环境直接import UI模块并声称修改了UI，也不要直接关闭战役UI或修改全局退出代码；保留目标面板/计时/存取档和多人语义，限定地图适配后再实测。实际Horde EE v22证据见[专项](HORDE_EE_MANUAL_EXIT_2026-10-20.md)。


## 初始化报错可能同时阻断刷兵与分数（2026-10-20）

本机schook/lua/simInit.lua的BeginSession先调用baseBeginSession，后启动aibrain分数采集与同步；基础BeginSession直接执行地图OnPopulate/OnStart。检查空白结算时，应先核对地图开局是否返回，不要直接修改全局score界面。Insane Beta1默认黑日控制中心UEC1902无Weapon，目标存在不代表GetWeapon(1)可用；检查实际蓝图武器条目及对象后才调射程。万古资源发生器有DeathWeapon，不能凭“经济建筑”名称断言无武器。详见[最小修复及隔离测试](INSANE_BETA1_STARTUP_SCORE_FIX_2026-10-20.md)。

## 同队AI异常伴随不刷兵与空白结算：先查初始化（2026-10-20）

本机基础BeginSession的大厅队伍恢复在地图OnPopulate/OnStart之后，schook的分数采集/同步又在基础函数返回后启动。三种症状并存时，先找结盟前的初始化断点，不直接改全局结算UI或循环外交。Sea Fleet v8修正小写墙体类别和xsb2406→xsb2401后用户反馈正常；这是本次问题的用户实测结果，无修复前日志，不能把原生nil行为或唯一根因写成已由日志证实。

本图ArmyToPlayerID在文件末尾自行定义，按军队名转槽号、包括AI；检查完整定义，不能仅凭“human”注释决定重写盟友和人数。类别参数要对照实际蓝图及大小写；模型应保留拒绝nil和容忍nil两种对照，以免把测试替身的异常冒称游戏异常。详见[Sea Fleet案例](SEA_FLEET_ALLIANCE_STARTUP_SCORE_2026-10-20.md)。

## 伤害倍率与基地布置不能只看函数/菜单名称（2026-10-20）

本机mohodata.scd/lua/sim/weapon.lua:421的AddDamageMod累加到DamageMod；284起GetDamageTable的DamageAmount=蓝图Damage+DamageMod。希望总伤害为D×M时，无其它修改应添加D×(M−1)，不是D×M；Horde UnitBuff为前者，Grand Barrens当前脚本669为后者。4组本机Lua隔离确认100基础选2分别200/300，仅覆盖普通武器、无其它加成模型；核爆、自定义投射物和Mod另查，不凭此一次改全图。

GetSkirtRect需完整Footprint/Skirt/Offset，建筑Skirt、物理Footprint、模型大小、盾面尺寸不是一回事。5iver原模板确实可执行生成，但有8对已知完整Skirt相交；隔离CreateUnitHPR记录成功不证明实际碰撞/寻路正确。源码文件存在或DEBUG测试可调用也不代表正常玩法已启用。详见本次对比报告。
