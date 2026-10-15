# 62张地图研究期间的代码维护

2026-10-16。当前62张，专用模组9张已在上一阶段删除。本轮对全部地图建立源码/函数/选项/资源索引，以下9张有明确最小修正。

| 地图 | 修复前map_version | 作者历史保守下限 | 修复后map_version | 修正 |
| --- | ---: | ---: | ---: | --- |
| Survival Escape v4 | 4 | 4 | 5 | 选项偏好键 |
| Survival Sea Fleet | 6 | 6 | 7 | 选项偏好键 |
| Genesis of the Order Survival | 12 | 12 | 13 | 区域边界接口 |
| desert front survival | 9 | 24 | 25 | 选项偏好键 |
| Survival Genesis | 16 | 16 | 17 | 选项偏好键 |
| voodoo battle survival new v4 | 4 | 24 | 25 | 选项偏好键 |
| Survival Terror Lands | 1 | 1 | 2 | 选项偏好键 |
| Survival Stranded v22 | 22 | 22 | 23 | 区域边界接口 |
| onixs voodoo survival | 16 | 16 | 17 | 选项偏好键 |

## 改动及保持范围

- Escape：StartTime的pref原误用Difficulty，改为StartTime。Sea Fleet、Desert Front、Genesis、Voodoo New、Terror Lands、Onix Voodoo：Wreckage的pref原多了s，改为与key一致。
- 上述只修正偏好键；default、选项值、刷兵和胜负不变。是否由大厅持久保存pref取决于加载器；不能宣传成修复了Steam所有自定义菜单显示问题。
- Genesis of the Order、Stranded：ScenarioFramework模块没有SetIgnorePlayableRect；原写法在执行到时会调用nil。改用Steam已有的全局SetIgnorePlayableRect，以GetArmyBrain(name):GetArmyIndex()传入数值军队编号，保留区域和AI边界豁免意图。
- 本机Steam官方战役X1CA_001_script.lua:209使用该全局函数；ScenarioFramework.SetPlayableArea位于lua.scd内lua/ScenarioFramework.lua:1056，不包含该模块方法。Steam SupremeCommander.exe存在对应全局符号。没有照抄FAF新增API。
- 各改图严格升版且显示名同步。Desert Front与Voodoo New脚本历史含v24，保守升至25，避免小于作者脚本历史；这不证明当前地图与作者全部v24版本相同。
- 9张共27文件改写/新增（含各图FACN_CHANGELOG.md）；其余地图文件保持。当前累计28张有此前整合或本轮维护修改。
- 地形、资源点、出生点、模组可选分支未作修改。本轮没有为了通过检查删除玩法。

## 核验与恢复

37项目标Lua检查全部通过：18个变更Lua文件编译、7组选项键一致性、3组实际区域模块路由（含调试分支）、9组版本/显示名实际求值。引擎接口用桩记录调用，未运行游戏；状态均为“已修改待实测”。

完整修复前9张备份：`<本地工作区>\62张地图代码与制作研究_20261016\本轮9张修复前备份.zip`；SHA-256：`d5840cc8030fb9fca7d65b568bf5e000e0f173fac3389699a7bc1ffb962c93fb`。旧83张原始备份及被删除模组图当前版备份继续保留。执行后文件验证见`代码维护执行结果.json`。

其余静态疑点和可复用玩法详见`62张地图代码研究与维护报告.md`及知识库。备用EventDispatcher库、编辑器主题文件、缺失贴图和外置模式线索单独标注，不冒充已经游戏修复。
