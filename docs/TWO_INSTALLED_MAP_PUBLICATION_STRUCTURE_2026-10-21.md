# 两张安装地图发布结构修复（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

状态：已修改待实测。范围仅 E:/SCFA/maps/5iver Survival Brainsucka 与 E:/SCFA/maps/survival_defense_atoll。没有修改内容中心源码、可执行程序或游戏系统文件；没有同步维护地图包。地图名称、map_version=4、高级菜单和玩法脚本保持。

| 地图 | 原有情况 | 处理方式 | 最终结果 |
| --- | --- | --- | --- |
| Survival Defense Atoll | 根目录包含活动地形及 Survival_Defense_Atoll_Old.scmap，共2个；scenario仅引用活动地形，Lua无旧地形引用 | 完整备份后从安装目录移出未使用的旧地形 | 只剩1个scmap；活动地形、save、script、options字节完全不变 |
| 5iver Survival Brainsucka | 实际存在_save.luac；用户截图客户端误报缺失；当前FACN_Start_Entry.lua入口也不满足严格_script.lua后缀 | 用安装游戏实际LuaPlus求值原存档，导出完整真实_save.lua；更新scenario两处引用；将原入口内容原样移至标准_script.lua并归档旧入口 | 标准Lua引用均存在；新存档与旧存档逐值、逐键类型相同；原编译主脚本仍仅加载一次 |

## 修改文件

- 修改 `E:/SCFA/maps/5iver Survival Brainsucka/5iver Survival Brainsucka_scenario.lua`：只改save和script引用。
- 新建 `E:/SCFA/maps/5iver Survival Brainsucka/5iver Survival Brainsucka_save.lua`：真实存档数据；不是将字节码改扩展名，也不是空白占位文件。
- 新建 `E:/SCFA/maps/5iver Survival Brainsucka/5iver Survival Brainsucka_script.lua`：与此前FACN_Start_Entry.lua逐字节相同；仍doscript原主字节码并Attach原高级开局模块。
- 从地图安装目录移出 `5iver Survival Brainsucka/FACN_Start_Entry.lua`、`survival_defense_atoll/Survival_Defense_Atoll_Old.scmap`；均在完整备份内。
- Brainsucka四份原始luac（含原save）全部保留且SHA不变；FACN_StartOptions、options、地形及预览保持。
- Atoll旧script没有被场景调用，也不影响发布预检；本次未为整理目录顺手删除它。

## 原因证据与验证

只读核对内容中心 LocalContentService.AnalyzeMap/ValidateReference 以及网关PackageValidator规则，没有编辑或构建软件。当前磁盘源码已经支持luac，不能据此断言截图运行的客户端具有相同规则；截图现象与旧版lua-only预检一致。本次地图适配同时满足更严格的lua后缀要求，不依赖客户端升级。

- 修改前两图21文件完整ZIP逐文件SHA核对；ZIP在工作区`两张地图发布结构修复_20261021/修改前两张完整地图备份.zip`。
- 原生LuaPlus存档导出1项通过。诊断另确认SCFA LuaPlus普通table具有相同默认空元表；导出只接受该默认元表，拒绝自定义元表和共享/循环表。
- 候选7项通过；部署后9项通过。含实际编译脚本入口求值、真实场景/空环境菜单求值及存档精确比较；入口测试的外部引擎接口及Attach为记录桩，不冒称完整OnStart战斗测试。
- 新旧存档：1,719个表、6,938个标量值精确相等（包括数值键与字符串键、类型字段）；540标记、9军队保持。
- 两图目录各恰有1个scmap、1个scenario；map/save/script文件存在、目录归属正确、符合标准后缀；保留菜单Key无重复，各8项。
- 全安装地图哈希对比：1个旧文件修改、2个新增、2个已备份文件移出，其余996文件不变，包含全部61张官方图。没有修改地图名称或修订号。

## 尚待验证

1. 用户在运行中的内容中心点击“重新扫描”，确认版本/大小恢复及两条红框不再出现；本轮没有实际执行内容中心扫描或云端上传，不能声称已发布。
2. 游戏重新开局、默认及非默认高级选项、完整刷兵/胜负和多人。存档等价不替代游戏测试。
3. Brainsucka原主脚本仍要求模组UID `d36d33e5-3927-499f-8990-55555b000001`；没有移除原依赖检查，上传结构修复不代表去模组兼容。

完整证据：工作区`两张地图发布结构修复_20261021/部署核验.json`、`部署计划.json`、`候选Lua核验结果.json`、`部署后Lua核验结果.json`。修复脚本和部署脚本位于工作区，不进入地图发布目录。
