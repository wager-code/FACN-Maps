# survival_5thdimension默认单主指挥官（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

用户截图指向安装目录E:/SCFA/maps/survival_5thdimension，实际地图修订9、显示名survival_5thdimension。此图不是Practice。用户明确要求删除默认大量指挥官，每名玩家只保留大厅所选阵营的一名主指挥官，额外SCU由高级设置控制。

## 原因与选择

不是高级菜单失效：survival_5thdimension_v6_save.lua中ARMY_1～ARMY_4的Units/INITIAL各预放8台ACU，四个原版种族各2台，共32台。原ScenarioUtils.InitializeArmies→CreateInitialArmyGroup先创建存档INITIAL，只有INITIAL为空时才按玩家GetFactionIndex和/lua/factions.lua的InitialUnit创建常规主ACU。因此原固定8台会绕过单台按大厅阵营生成的分支；原描述也明确每玩家8台。

已复用原版回退，不增加自建生成器：只删除上述32个INITIAL单位，保留INITIAL空组，让原版初始化创建一台所选阵营ACU。没有先生成再Kill/Destroy，没有杀ACU核爆风险，没有新增开关/线程/菜单。

## 实际修改

| 文件 | 修改 |
| --- | --- |
| E:/SCFA/maps/survival_5thdimension/survival_5thdimension_v6_save.lua | 删除32台固定ACU，4玩家各8台、四族各2；保留空INITIAL及其它全部存档字段 |
| E:/SCFA/maps/survival_5thdimension/survival_5thdimension_v6_scenario.lua | 描述更新为每玩家默认1名所选阵营主指挥官，额外SCU/工程师由高级设置选择；保留Amiga署名；移除旧LOC前缀避免回落到“8名”旧描述 |

名称、map_version=9、地图路径、玩家槽、脚本、options、FACN模块、SCMAP/预览保持。其余652个自定义文件SHA保持；官方地图文件、其它地图、此前大厅显示修改、维护地图包62图与游戏系统均未写入。高级单位默认数量仍0，种族和数量独立；选四族按每族计算，原菜单8项不变。

## 原版证据

本机mohodata.scd/lua/sim/ScenarioUtilities.lua:331～346的CreateInitialArmyGroup先CreateArmyGroup(strArmy,'INITIAL')，空组时GetFactionIndex→factions.Factions[factionIndex].InitialUnit→CreateInitialArmyUnit。436起InitializeArmies保留实际军队列表、Civilian和预建部队规则。当前地图OnPopulate继续调用原InitializeArmies，未改写这套初始化。

## 核验与边界

- 2份目标LuaPlus语法、3候选＋3落盘用例通过，共8个正式入口。
- 存档实际Lua求值，按删除清单从原数据去除32项后与新存档完整JSON相同，其余markers/资源/军队/组/单位/路径保持；非只按文本数量推断。
- 实际maputil/dataInit空环境加载，元数据除说明外完全一致，高级选项及实际修订保持。
- 完整实际主脚本搭配本机原版InitializeArmies、CreateInitialArmyGroup、FindUnitGroup/AssembleUnitGroup/AssembleArmyGroup、实际factions.lua，候选与落盘各跑128组合：16占槽子集×4种族×预建部队Off/On。原存档8台/玩家在模型中复现，新存档1台/玩家且与选择种族对应；空槽不发ACU，默认新单位数量0无额外安排。
- 既有高级设置再验证：四族SCU各2，共8，独立万古T2工程师1，额外共9台；不重新写一套赠送逻辑。

引擎原生CreateInitialArmyUnit/单位创建、platoon、地形、工厂与目标等使用受控替身；不把128组合称作128次真实游戏。**状态：已修改待实测。** 需要新开局分别选四种族、1人/4人/空槽和非零SCU数量验收，旧存档保留原已生成单位，不自动删除。预建部队引擎其它效果与多人/模组尚未实测。

完整9文件备份：5thdimension单主指挥官_20261021/修改前5thdimension完整备份.zip，SHA `5c21226b22293a1c77ad9c95fe6f169bd839d236dc4653eedea40423d9e82714`。删除清单（原行号/UNIT ID/军队/蓝图）、部署计划、语法与候选/落盘结果、最终核验位于同目录。
