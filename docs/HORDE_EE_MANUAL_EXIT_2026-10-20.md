# Survival Horde EE v22：中途退出不显示结算（2026-10-20）

## 结论

用户确认操作是“中途退出后直接回大厅”。当前地图在遭遇战配置中开启了战役UI；原版退出菜单因此走战役中途退出分支，结算函数收到midGame=true后直接ExitGame并返回，普通结算界面不会创建。

这是实际源码可以完整解释、且已隔离执行复现的分支行为，不是“结算表出现但数据空白”。没有取得当局日志，也没有助手实机点击退出；不据此排除其他运行时MOD覆盖。

## 地图身份与范围

- 地图包：`E:/地图包/02_生存与波次防守/04槽位/survival_horde_ee/`。
- 安装副本：`E:/SCFA/maps/survival_horde_ee/`。
- 两处各44个地图/辅助文件（排除.git元数据）相对路径及SHA-256完全一致，版本均22，显示名Survival Horde EE v22。
- 主脚本SHA-256：`62bed7fb343b1059062440e02e66deca9241642c423c9d1257af05d43e71f38c`；与地图卡片一致。
- scenario为type='skirmish'不代表UI一定处于普通遭遇战模式，运行中的Sync标志要单独检查。

## 已核对的实际调用链

| 环节 | 位置 | 行为 |
| --- | --- | --- |
| 地图开启战役UI | survival_horde_ee_script.lua:848，OnPopulate | Sync.CampaignMode = true；原作者注释说明用于启用战役界面 |
| 模拟同步到UI | schook.scd内schook/lua/UserSync.lua:12–14 | 将Sync.CampaignMode写入campaignmanager.campaignMode |
| 用户点中途结束 | lua.scd内lua/ui/game/tabs.lua:258–265 | campaignMode为真时调用score.CreateDialog(nil,nil,nil,true) |
| 跳过结算 | lua.scd内lua/ui/dialogs/score.lua:213–218 | midGame为真：ExitGame()后return；后面的scoreScreenActive、SessionEndGame、UpdateData等不会执行 |

检查了E:/SCFA与Steam安装目录全部gamedata/*.scd中这些确切路径；提取的campaignmanager、tabs、score、基础UserSync和战役UserSync hook共5种源文件在两个安装中逐一SHA相同。战役同步赋值实际在schook.scd，不能只读mohodata里的基础UserSync便断言不存在。

## 验证与局限

目标运行时是本机32位LuaPlus_1081.dll。5项检查全部通过：当前地图script/scenario及原始tabs/score模块加载；另把实际地图标志赋值、实际UserSync条件块、实际tabs.EndGame函数和实际score.CreateDialog函数组合隔离执行。

- 战役模式：调用一次ExitGame，未调用SessionEndGame，未置scoreScreenActive。
- 普通模式对照：没有额外调用ExitGame，进入SessionEndGame；使用记录桩在此停止，没有伪造完整UI渲染或分数表。
- 此验证证明条件路由，不等于游戏通关、结算数值完整、多人同步或FAF当前客户端实测。

## 修复边界

当前地图用Objectives.Protect创建“坚守阵地”任务，并有任务面板、对白和胜负演出。不能为了显示普通结算，直接把CampaignMode关掉便声称完整修复；这会改变战役UI相关路径，至少需要验证任务面板、计时、存取档、观察者和退出行为。

如果以后要求中途退出也显示普通结算，应设计限定本地图的UI退出适配，保留任务显示，并验证退出前统计快照及额外军队显示。模拟脚本中的import不能直接当成修改UI虚拟机的入口；暂没有已验证可部署的地图内补丁。不修改全局tabs.lua/score.lua来影响所有官方战役。

自然胜利/失败在主脚本982–1084行，调用各军队OnVictory/OnDefeat后EndGame；本次用户没有走这个入口，不能把中途退出复现当成自然结算已验证。另发现1077行的条件最后一项写成or "ARMY_5"，Lua非空字符串为真，会把额外军队也纳入失败通知，属于独立静态问题；不是本次中途退出跳过结算的原因，未修改。

## 当前处理状态

状态：静态确认＋目标LuaPlus隔离分支复现。地图包、安装副本和游戏SCD均未改；版本仍22，没有新游戏实测。本轮产物为只读提取源码、哈希记录、最小隔离夹具与文档，不把分析称作已修复。

本地证据：工作区`Horde_EE退出结算检查_20261020/`的来源与哈希.json、Lua检查清单.json、Lua检查结果.json和实际退出调用链隔离检查.lua；提取的商业游戏源码仅留本地，不上传知识库。
