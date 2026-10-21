# 地图名称隐藏版本、左侧保留版本（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

用户连续明确：“我只要地图名称不显示版本号就行了，左侧信息里面可以显示”“手写的版本号也要去掉”。本轮据此允许名称字段调整及选图列表的UI显示调整，覆盖此前本轮不改名称的限制；**不修改任何实际map_version**。

## 实现

安装42张自定义地图名称逐个检查，清理16个name中的手写版本/发布标签，包括14生存图及6 Fields of Isis、6Castles两张普通自定义图。明确版本尾缀v2/v9/v16、NavyV2、v1c Beta、(Beta1)清掉；保留4v4、5P、5thdimension、Blackbox 10等用途/身份数字。没有新引入同名冲突。只改ScenarioInfo.name字段，不改目录、路径、描述、修订、槽位和玩法。61官方地图文件未写入。

本机选图界面来自既有第三方大厅增强包E:/SCFA/gamedata/03_lobbyenhancement.scd，文件schook/lua/ui/dialogs/mapselect.lua。列表行原逻辑为name再追加“(Version:map_version)”。只删除该列表追加分支，保留LOC(name)；左侧scen.map_version→VersionLoc→description:AddItem块逐字节保持。

此次用户明确授权这项大厅显示调整，因此改了既有第三方UI包；没有改基础lua.scd/mohodata.scd/schook.scd、bin、模组启用状态、用户偏好或官方地图。zip内仅mapselect一项内容变化，其余成员、元数据和归档注释保留，未引入新hook/重复加载入口。

## 核验

17份本机Lua语法通过（16场景＋1UI）；候选43及落盘43用例通过（42实际原版LoadScenario完整元数据比对，除name以外完全相同；1个实际列表/左侧代码片段行为检查）。42个名称列表输出无自动Version串，左侧Version:12仍生成；4v4等身份保留断言通过。UI包所有成员逐个解压SHA核验，只有mapselect改变。638个其它自定义文件SHA保持，35生存菜单总390不因改名变化。

备份位于地图名称版本显示清理_20261021/修改前名称与大厅增强包备份.zip，SHA `b9d98ad9b827e53c5a5b503a9a56cfa71283bb556f1769bac9fdae0f98524199`。备份含全部本轮目标原文件，并额外保留1份只读审阅过的4v4场景原文件；该图未写入。此前Practice补发删除有独立完整备份，两阶段不要互相覆盖。

状态：已修改待实测，未实际打开游戏选图界面。需完全重启游戏刷新UI模块/场景缓存，确认列表纯名称、左侧Version仍在、筛选/随机选图/创建房间正常；没有清用户缓存、没强退进程，也没有做真实多人或FAF验证。

## 名称对照

| 目录 | 原名称 | 当前名称 |
| --- | --- | --- |
| `6 fields of isis` | 6 Fields of Isis v13 | 6 Fields of Isis |
| `6castles` | 6Castlesv2 | 6Castles |
| `BBF_BlackSunDefense` | Black Sun Defense v2 | Black Sun Defense |
| `Desert_Swarm_v1c_Beta` | Desert Swarm v1c Beta | Desert Swarm |
| `dreamy_survival` | Dreamy Survival v16 | Dreamy Survival |
| `sexy_survival` | Sexy Survival v13 | Sexy Survival |
| `Survival Run` | Survival Run v8 | Survival Run |
| `survival_5thdimension` | survival_5thdimension v6 | survival_5thdimension |
| `survival_5thdimension_practice` | survival_5thdimension_practice v9 | survival_5thdimension_practice |
| `Survival_Escape` | Survival Escape v5 | Survival Escape |
| `Survival_ExtremeDesert` | Survival EXtreme Desert v3 | Survival EXtreme Desert |
| `Survival_ExtremeNavy` | Survival EXtreme NavyV2 | Survival EXtreme Navy |
| `survival_horde_ee` | Survival Horde EE v22 | Survival Horde EE |
| `Survival_Insane_Beta1` | Survival Insane (Beta1) | Survival Insane |
| `Survival_Insane_NvS_Beta1` | Survival Insane NvS (Beta1) | Survival Insane NvS |
| `survival_sea_fleet` | Survival Sea Fleet v8 | Survival Sea Fleet |

版本由map_version保留，左侧自动显示；不要删除map_version来隐藏名称版本，也不要把目录名中的旧版本数字改掉而破坏虚拟路径。当前已部署的菜单和版本以实际安装文件为准。
