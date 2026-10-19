# Fort Ictus Survival：FAF v8 到 Steam 原版的静态兼容审计（2026-10-19）

## 结论

**可以尝试改编为 Steam 原版地图；本次上传包没有发现必须导入某个具名第三方 MOD 的直接证据，但它不是零依赖的 Steam 原版包。** 已确认一个活动波次中的 FAF 单位引用，以及一个缺失/未知的单位类别限制引用。当前结论是静态审计，不是 Steam 实机通过。

## 输入与完整性

- 上传文件：`fort_ictus_survival.v0008.zip`
- ZIP SHA-256：`cea02527a8cc7f73762e44031abb244ac46f6fa531a80a9c37c6257623831bf4`
- ZIP 完整性：`testzip()` 未发现损坏。
- 共 5 个实际文件：`.scmap`、`_options.lua`、`_save.lua`、`_scenario.lua`、`_script.lua`；未包含 `src/`、`vendor/`、MOD 文件夹或单独的依赖包。

文件 SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| `Fort_Ictus_Survival.scmap` | `a7ca26164efb4cbe9be78558ab1b3221a2724885a1471fb26e990b1c51a6dfd0` |
| `Fort_Ictus_Survival_options.lua` | `bf5f31dc0110cd6a971c9c376ecf96ec127cceb0eb8d15961aba8525ffd625ac` |
| `Fort_Ictus_Survival_save.lua` | `5e2616a723af1c86a3167075032169634190e622f6cef1254d40c7bb8d367572` |
| `Fort_Ictus_Survival_scenario.lua` | `baea1e323618eeaa1ad00d3be40c0f37d9a5aa621e3b4e2b06f6dbf849ce3d52` |
| `Fort_Ictus_Survival_script.lua` | `80254eccf978a7da2b2c4e1a3faa83b426b1cab86c5f30bc9a85444fe35a998b` |

## 目录与版本

- 场景基础显示名：`Fort Ictus Survival`。
- 场景版本：`map_version = 8`。
- 文件夹和三个虚拟路径使用 `fort_ictus_survival.v0008`。
- 这与仓库已经追踪的 v9 不同：当前维护卡使用目录 `fort_ictus_survival` 和 `map_version = 9`。依照仓库命名规范，正式目录不应再把版本号拼进文件夹名；改名时必须同步 `map/save/script` 路径。

## 选项默认值语义待核对

v8 的三个选项在 `_options.lua` 中分别使用 `default = 10`、`default = 3`、`default = 3`，而对应 `values[].key` 列表里没有相同的数值。它们可能按选项列表位置解释，但不能直接假定 Steam 目标大厅采用同一语义。

- 保留原始值，不能仅因它们不等于某个 `values[].key` 就擅自改动。
- 在目标 Steam 大厅确认默认选中项；启动后记录 `ScenarioInfo.Options` 实际值，并切换准备时间、每分钟敌人数、波次间隔做对照。
- 当前 v9 维护卡同样把 default 解释标为待验证；本次 v8 静态审计没有证明其菜单行为正常。

## 依赖审计

### 1. 没有发现具名第三方 MOD 的直接导入

`Fort_Ictus_Survival_script.lua` 仅有三个常量导入：

- `/lua/sim/ScenarioUtilities.lua`
- `/lua/ScenarioFramework.lua`
- `/lua/utilities.lua`

没有发现 `/mods/...` 导入、外置 `src/` / `vendor/` 模块或依赖包。仅凭这一点不能证明所有地形资源都存在于 Steam：SCMAP 可打印路径扫描得到的路径位于 `/env/` 与 `/textures/` 下，但这不是对目标 Steam 资源索引的完整核验。

### 2. 活动波次依赖 FAF 单位 DRLK001

- v8 脚本在活动波次表中引用 `DRLK001` 共 13 次；第 118 行还有一处同样的注释引用，不属于活动波次。
- 仓库已有的目标 Steam 蓝图清单未包含 `DRLK001`；FAF 源码中存在该蓝图定义：[FAF DRLK001 blueprint](https://github.com/FAForever/fa/blob/4ef41e436a67f5936bae65c7de0677b639435a93/units/DRLK001/DRLK001_unit.bp)。
- 这属于**FAF 单位资源依赖**，但不是“地图明确要求安装某个独立专用 MOD”的证据。
- 仓库的原版迁移指南已有候选映射 `DRLK001 → URL0205`。这会改变原单位的科技等级与强度，不能宣称无损；必须检查所有相关波次、生成数量和后期难度。

### 3. 第 1063 行存在缺失/未知类别引用

`Fort_Ictus_Survival_script.lua:1063`：

`ScenarioFramework.AddRestriction(Army, categories.uaa0314)`

- 仓库已有的 Steam 蓝图清单未找到 `uaa0314`；本次可检索的 FAForever/fa 源码也未找到同名蓝图。
- 这不是活动波次单位生成，而是玩家单位限制。
- 缺失的类别字段可能得到 `nil` 并被传入限制 API。仓库此前对 v9 的参数追踪确认了 Lua 层的 nil 转交路径，但原生接口行为和实际崩溃尚未被游戏日志证明。
- 不要把此项直接判为“必须装专用 MOD”。应确认原意后，删除这条无效限制或改用目标 Steam 中确实存在、语义正确的限制类别；不能随意扩大限制范围。

### 4. 其他可疑编号

- `QEL01112`（第 116 行）和 `LDUC260`（第 120 行）只出现在注释掉的备用波次示例中，不构成当前活动依赖。
- 活动波次中的其余字面量单位已与仓库既有 Steam 蓝图审计结果对照；本报告未重新读取一套完整的本机 Steam 安装资源，因此仍需在最终目标构建上复核。

## 与仓库当前 v9 的关系

- v8 的 `Fort_Ictus_Survival_save.lua` SHA-256 与仓库 v9 维护卡记录完全一致：`5e2616a723af1c86a3167075032169634190e622f6cef1254d40c7bb8d367572`。
- v8 的 `_scenario.lua`、`_options.lua`、`_script.lua` 指纹均不同于维护卡记录的 v9 文件。不能把 v8 ZIP 当成 v9 的完整替代品。
- 当前 v9 维护卡记录活动波次单位已替换为 Steam 蓝图中存在的单位（字面量清单缺失数为 0），但 v9 的 `uaa0314` 限制风险仍在调查中。
- 因此本次**不从旧 v8 重新生成一个冒充更新版本的发布包**。下一步应在最新 v9 原包上做最小修改，避免丢失已有的波次/选项/目录修订。

## 建议修复顺序

1. 以最新 v9 完整包为基底，先备份并核对 SHA-256。
2. 只处理仍存在的 `categories.uaa0314` 无效限制；确认语义后采用最小变更。
3. 核对场景目录为 `fort_ictus_survival`，`map/save/script` 路径大小写完全一致。
4. 使用目标 Steam 构建的蓝图索引重新扫描存档、全部活动波次和所有条件分支；不能只检查首波。
5. 检查三个大厅选项的实际可见性和值传递：准备时间、每分钟敌人数、波次间隔。
6. 在无额外 MOD 的 Steam 环境测试：大厅加载、默认开局、非默认选项、首波、后期波次、保护目标毁灭、计时胜利、少人/空槽、特殊第 4 槽、多人同步和退出结算。
7. 记录真实日志与逐项结果；在上述测试前，状态保持“静态确认 / 已修改待实测”，不得标为 Steam 单人或多人通过。

## 本次测试边界

- 已执行：ZIP 完整性检查、文件清单与 SHA-256、ScenarioInfo 路径/版本审查、常量 import 检查、Lua 字符串/注释扫描、活动波次单位引用审查、SCMAP 可打印资源路径抽查。
- 未执行：Steam 游戏启动、目标 Steam Lua 引擎编译、实机刷波、完整资源加载、单人/多人对局。
- 当前结论：**可行的原版改编候选；未完成 Steam 实机验证。**
## 后续动作：独立 Steam 候选包（2026-10-19）

由于当前可用文件只有上传的 v8 ZIP，而仓库没有 v9 完整地图包，已另行生成**不覆盖 v9 的 v8 派生测试候选**：

- ZIP：`Fort_Ictus_Survival_Steam_Candidate_v11.zip`
- SHA-256：`4ac2f416230ab6439bcfbaea8b85303fe748eecb98b9b2cdfa9adf6d4fe175c3`
- 场景名：`Fort Ictus Survival Steam Candidate`
- `map_version = 11`；虚拟目录 `fort_ictus_survival_steam_candidate`。这是隔离测试候选，不是已发布的 v11，也不是当前 v9 的替代品。
- 13 处活动波次 `DRLK001` 改为仓库已有候选映射 `URL0205`（Cybran T2 防空单位）；明确损失为 T3/FAF 单位强度与原平衡下降，须实测波次难度。
- 对 `categories.uaa0314` 增加存在性判断，避免 Steam 环境将缺失类别 nil 传入 `AddRestriction`；若该类别存在仍保留限制。
- 更新场景名、描述、版本和 map/save/script 三个虚拟路径，使用独立文件夹，避免与现有地图冲突。
- `.scmap`、`_save.lua`、`_options.lua` 内容保持原始哈希；没有改变第4槽联盟/胜负逻辑，也没有猜测修改菜单默认值。

静态验证：ZIP 完整性通过；恰有 5 个文件；13 处活动 `DRLK001` 全部替换，活动引用剩余 0；`uaa0314` guard 存在；三个虚拟路径一致；地形哈希不变。

**尚未验证**：目标 Steam Lua 引擎编译、Steam 大厅、开局初始化、首波/后期、特殊第4槽、多人与结算。由于源基底是 v8，不能证明其包含 v9 所有修订；当前状态为“已修改待实测”。若要修复并发布当前 v9，仍须取得 v9 完整包后将最小补丁移植过去。
## 后续更正：炮兵标记是拼写不一致（2026-10-19）

此前静态扫描将未找到 SURVIVAL_ARTY_ 记为炮兵标记数量为 0；进一步检查用户本机 v9 的 save 后确认，四个 marker 实际存在，但被拼为 SURVIVAL_ATY_1..4，脚本却读取 SURVIVAL_ARTY_。因此不能把“期望前缀搜索结果为 0”误判为“地图中没有炮兵 marker”。此发现已由 v10 修复候选修正，详见 [Fort Ictus v10 修复报告](FORT_ICTUS_V10_STEAM_REPAIR_2026-10-19.md)。
