# Fort Ictus Survival v10：Steam 原版修复候选（2026-10-19）

## 结论与边界

本报告基于用户上传的本机地图 RAR（v9），不是此前的 v8 派生候选。已制作独立 ZIP 候选，地图目录名与游戏基础显示名称统一为 `Fort Ictus Survival`，版本通过 `map_version = 10` 单独显示。

- 输入 RAR SHA-256：`e615d864586d2e391a2cfad6421fc52a92be6188348d8bdca20d45a793d7ad87`
- 输出 ZIP：`Fort_Ictus_Survival_v10_Steam_Candidate.zip`
- 输出 ZIP SHA-256：`1fdfc61347b65705ff558e56c7170abda341938877f09b4a4a4b95940362076b`
- 候选包不上传至仓库，也不覆盖用户电脑中的 v9。
- 状态：静态修复候选，尚未在 Steam 游戏内启动或进行单人/多人对局。

## v9 中确认的问题

### 1. 炮兵标记是拼写错误，不是地图完全没有炮兵标记

`Fort_Ictus_Survival_script.lua` 按 `SURVIVAL_ARTY_1` 至 `SURVIVAL_ARTY_N` 读取标记，但 save 文件里实际写成 `SURVIVAL_ATY_1` 至 `SURVIVAL_ATY_4`，漏了字母 `R`。因此脚本读不到存档中已有的 4 个炮兵标记，炮兵位置表为空。原有 `Survival_GetPOS` 仍直接执行 `math.random(1, table.getn(...))`，空表时可能调用 `math.random(1, 0)`。

修复：
- 将存档中的四个标记改为 `SURVIVAL_ARTY_1..4`，位置、朝向和其他 marker 属性不变。
- 在 `Survival_GetPOS` 中增加空表保护；如果炮兵标记缺失或耗尽，回退到普通敌军出生点，并记录一次警告；其他缺失的标记类型则记录并返回 nil。
- 该回退是防御措施；正常情况下应使用修正后的四个炮兵标记。

### 2. 玩家联盟判断变量写错

原代码的内层循环在判断 `ArmyX` 时，最后一项却检查外层变量 `Army == "ARMY_4"`。已改为检查 `ArmyX == "ARMY_4"`，并将限制/联盟处理范围对齐到场景配置的四个玩家槽 `ARMY_1..ARMY_4`。

### 3. 玩家数量不应固定减去两个 AI

原代码以 `table.getn(ListArmies()) - 2` 推算人数，隐含假设总有且只有两个非玩家军队。候选改为统计 `ListArmies()` 中的 `ARMY_1..ARMY_4`。这消除了“固定减 2”的假设，但仍须在 Steam 中验证 ListArmies 对空槽和电脑队友的实际行为，不能仅凭静态代码宣布人数缩放正确。

### 4. 缺失类别保护

对 `categories.uaa0314` 增加存在性判断，避免缺失类别直接传给 `ScenarioFramework.AddRestriction`。如果目标 Steam 构建没有此类别，该条限制将跳过；必须确认这不会开放本来应禁用的单位。未将其描述为已证实的崩溃根因。

### 5. 大厅默认值与脚本 fallback 对齐

三个选项的 `default` 统一改为第一项；脚本的 fallback 同步为：
- 建造准备时间：0 秒
- 普通敌军数量：16 / 分钟 / 玩家槽
- 普通波次间隔：10 秒

该设置旨在匹配选项文件第一项的“默认”标签。实际 Steam 大厅的默认选中项及 `ScenarioInfo.Options` 传值仍需实测。

### 6. 地图名称与文件夹统一

- ZIP 根目录：`Fort Ictus Survival/`
- 场景基础名称：`Fort Ictus Survival`
- `map_version = 10`
- `map`、`save`、`script`、`preview` 四条虚拟路径均改为 `/maps/Fort Ictus Survival/...`
- 内部文件名保留原样；地图显示名不再拼接 `v10`。

## 文件与静态验证

| 文件 | SHA-256 |
| --- | --- |
| `Fort_Ictus_Survival.scmap` | `a7ca26164efb4cbe9be78558ab1b3221a2724885a1471fb26e990b1c51a6dfd0` |
| `Fort_Ictus_Survival_script.lua` | `290b2c58f037c210dd0f1af1593fce2434195badc43f31331f86a3293b161aa9` |
| `Fort_Ictus_Survival_save.lua` | `7d2b18fecbb8020c66a956f085d543c40062cd074b462efe48fde85c059d4d3f` |
| `Fort_Ictus_Survival_scenario.lua` | `d6a89e04dd1c88e924008724e746190851a3f8f6cf1257f95f33f3e383bd97ce` |
| `Fort_Ictus_Survival_options.lua` | `2bbf4f6bdbee3ec1bfb520298bd8b274e4dcb6c1167c1d20cd77c71e83694215` |

Static checks passed:
- ZIP integrity; seven expected files.
- Four scenario paths use the same directory name as the game display name.
- Four artillery marker spellings now match the script.
- Empty artillery marker list is guarded.
- `uaa0314` is guarded.
- Inner alliance loop checks `ArmyX`.
- Player-count calculation no longer subtracts a fixed two armies.
- All three option defaults are set to the first visible choice.
- Terrain `.scmap` SHA-256 is unchanged.

## Required in-game regression

1. Install the candidate beside, not over, the existing v9; ensure the folder is exactly `Fort Ictus Survival` and no duplicate-name conflict exists.
2. Confirm the map list shows `Fort Ictus Survival` and Version 10, and the preview loads.
3. Launch with no extra MODs; capture the first simulation error if any.
4. Test 1, 2 and 4 occupied player slots, including computer teammates and empty slots; confirm player count, defense-object scaling and wave quantity.
5. Reach the first artillery special wave (about 37 minutes in the current schedule) and confirm the four artillery markers resolve.
6. Test first wave, later waves, nuke spawns, restrictions, allied relationships, objective defeat, timed victory, and end-of-game cleanup.
7. Verify the three lobby options select the intended defaults and that changing each option changes `ScenarioInfo.Options` as expected.
8. Record Steam build, ZIP hash, logs, single-player and multiplayer results separately.

Do not label the candidate Steam-compatible until these tests are performed.
