# 防守目标摧毁与沙盘结算只读核对（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

用户最初描述“目标没了”，后明确目标开局存在，并纠正为自己主动用指挥官爆炸和核弹摧毁目标，不是盟军AI主动攻击。不可把该现象登记为建筑未创建或联盟故障。用户当前询问沙盘是否必须手动退出，本轮仅调查，未修改地图、游戏模式、系统或用户偏好。

## 本机源码已确认

1. E:/SCFA/gamedata/lua.scd的lua/victory.lua:2～17，只有demoralization/domination/eradication建立普通胜负检查；sandbox等其它值直接return。因此沙盘不会依靠普通指挥官/单位清零流程自动结束。但沙盘并不禁止地图自己调用OnVictory/OnDefeat或安排主动结束。
2. 当前安装Insane脚本691行主动设置Victory='sandbox'，785～800行目标OnKilled先核爆、消息、原OnKilled，再设置loopEnd/gameEnd并对玩家killAllCommanders/OnDefeat。不存在按攻击者阵营限制判负的条件。因此主动自爆、核弹或敌人攻击，只要正常触发目标OnKilled，走相同判负链。它没有CallEndGame/EndGame调用。
3. 本机lua/aibrain.lua:782～799的OnDefeat将军队标出局并向Sync.GameResult追加defeat；OnVictory追加victory。判负/判胜、终止整局模拟、打开完整分数表是三个不同动作。
4. 本机schook/lua/UserSync.lua:94～98把Sync.GameResult交给gameresult.DoGameResult；lua/ui/game/gameresult.lua:38起对本地军队执行UI OnGameOver、失败公告及AddModeText“分数”回调，CreateDialog放在点击回调内，并不自动打开完整结算表。允许观察时还会切观察视角。

结论：沙盘与“战场继续运行/不自动弹完整结算表”有关，但不能据此断言地图完全没有判负，更不能说生存模式一律只能手动退出。应保留自定义生存所需沙盘，再按用户想要的结束方式处理地图自身终局流程；不要切普通歼灭导致辅助军队/无ACU模式提前结束。此处没有部署这样的改动。

## 对近期改动的核对

Insane当前目标OnKilled、killAllCommanders、setupGame、gameLogic四个完整函数，与“35张生存地图新增开局设置_20261021/修改前35张完整地图备份.zip”的修订7函数逐字相同。最近开局菜单/数量/去重没有改变这四段胜负代码。当前654个自定义文件SHA全部匹配上一轮去重完成状态，未新增地图改动；不把静态一致扩大为所有模组/实际游戏行为已排除。

## 检查与限制

6项实际源码隔离检查通过：普通victory.CheckVictory沙盘提前返回；1人与4人分别用主动测试核弹/敌人作为instigator执行实际Insane目标回调和实际AIBrain.OnDefeat；原版DoGameResult验证失败后仅登记分数入口、点击时才调CreateDialog。核爆物理、单位原生OnKilled、UI渲染为测试替身，不冒称游戏实测。

在默认位置未找到本局游戏日志；读取到的上次回放头为Insane、sandbox，但回放头不是错误日志，也不能单独证明截图当局的完整执行链。本局到底已判负但未弹表，还是在核爆/原OnKilled等步骤中断，仍需要实际日志或失败通知观察。不能凭源码调用存在宣称用户当局已成功判负，也不能将所有35张的不同胜负设计归为同一故障。

状态：本机行为静态确认，用户当局判负执行待调查；无地图修改，未新增Steam单人/多人或FAF通过。证据位于同目录原版源码副本、只读证据摘要.json、沙盘与判负隔离清单/结果.json。
