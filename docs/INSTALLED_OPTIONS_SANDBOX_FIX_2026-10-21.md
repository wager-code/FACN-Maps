# 多人入口无响应：新增地图选项空环境修复（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

> 后续按用户截图已合并准备菜单：31图扩展原项并移除重复项，4图保留单项，所有开局单位菜单去掉“新增”；当前安装Insane v10，维护包仍v7。本页为历史阶段，最新见[准备时间合并记录](INSTALLED_PREPARATION_MENU_MERGE_2026-10-21.md)。

用户反馈主菜单点击“多人游戏”后无反应。此前新增开局功能写入了地图目录中的文件，没有写入game.exe、系统SCD、模组或Game.prefs；但地图元数据也会在多人入口阶段预读，因此不能因没有改游戏程序就排除本轮地图修改。

## 定位到本轮新增代码错误

实际本机源码调用链：

1. lua.scd及CSKMainMenu.scd的lua/ui/menus/main.lua，ButtonLAN调用gameselect.CreateUI；
2. lua.scd/lua/ui/lobby/gameselect.lua第33行，模块加载时即调用MapUtil.EnumerateSkirmishScenarios，发生在进入房间/选图之前；
3. lua.scd/lua/ui/maputil.lua第46～47行，创建空optionsEnv={}后doscript(optionsFileName,optionsEnv)，没有给选项环境设置_G回退；
4. 本轮此前追加菜单代码依赖ipairs和table.insert：`for _,entry in ipairs(__facn_additions) do table.insert(options,entry) end`。空环境没有这些全局函数，加载选项失败，足以阻断多人界面构建。

旧地图原options是静态表，能在该环境运行。此前389个正式Lua检查入口使用了带全局函数的测试环境，没有模拟这里的空环境，因此遗漏了错误，不能作为实际多人菜单通过的证据。这是助手本轮实现与验证范围的错误，不能归咎为原地图损坏或用户游戏环境。

## 已部署修正

35份选项文件的新增部分改为显式`options[N]={...}`赋值，不再调用任何全局库；原有235项字节前缀完整保留，新旧全部445项求值结果逐项一致。另修改35份scenario的map_version严格升一级，Insane安装v8→v9。没有改主脚本、新增运行时模块、原字节码、地形、存档、预览、原选项值、系统SCD、程序、模组、偏好或缓存，也没有结束用户游戏进程。

修复前35图当前版本完整备份597文件并逐文件核对，保留在本目录`修复前35张新增设置版完整备份.zip`。更早的558文件原图备份继续保留，不覆盖。

生成器同时改为输出静态赋值，并加原始文件基线保护；不能再次运行历史构建脚本给当前地图重复追加或恢复有问题的写法。

## 核验

- 修复前35份文件在空环境中均复现ipairs为nil；原始选项文件通过。
- 35组修复前/后空环境检查和70项候选语法通过。
- 使用本机SCD原版maputil.LoadScenario、dataInit和实际落盘文件，再做35组加载对比：修复前报错、修复后通过；选项环境无注入库、无_G元表回退。
- 与前次实际菜单求值结果对比，445项定义完全不变，其中原图235项完整保留。
- 本轮654个自定义文件中恰好70个预定文件变更、584个不变，无新增或删除；另外7张自定义地图不变，61官方目录排除写入。
- 所有修复前/候选/落盘SHA检查通过。未获取游戏错误日志；没有在实际运行的游戏界面重点击或重启，因此状态仍为“已修改待实测”，等待用户退出重开后复测多人入口。

## 后续状态边界

本轮是地图菜单加载修正，不是游戏程序修复；不把菜单复测结果自动扩展为35张游戏/多人战斗通过。维护地图包62张未同步，其中Insane仍v7；当前安装Insane已v9，不能再用先前v8或v7哈希覆盖。

## 当前安装修订

| 目录 | 修复前 | 当前 |
| --- | ---: | ---: |
| 5iver Survival Brainsucka | 2 | 3 |
| 5iver Survival Land | 3 | 4 |
| 5iver Survival Land Naval | 3 | 4 |
| 5iver_survival_land_oxtreme | 11 | 12 |
| 5iver_survival_landnaval-swarm | 13 | 14 |
| astro_surv_stm | 9 | 10 |
| BBF_BlackSunDefense | 3 | 4 |
| Desert_Swarm_v1c_Beta | 2 | 3 |
| dreamy_survival | 17 | 18 |
| endless_survival_defense | 18 | 19 |
| Fort Ictus Survival | 11 | 12 |
| grand_barrens_survival | 14 | 15 |
| sexy_survival | 14 | 15 |
| sh1r3_mycelium2_survival | 3 | 4 |
| Supreme_AOD | 6 | 7 |
| Supreme_survival | 2 | 3 |
| survival attack | 2 | 3 |
| Survival Omega | 2 | 3 |
| Survival Run | 9 | 10 |
| survival_5thdimension | 7 | 8 |
| survival_5thdimension_practice | 10 | 11 |
| Survival_BlackBox_10 | 2 | 3 |
| survival_defense_atoll | 2 | 3 |
| Survival_Escape | 6 | 7 |
| Survival_Extreme | 2 | 3 |
| Survival_ExtremeDesert | 4 | 5 |
| Survival_ExtremeNavy | 3 | 4 |
| survival_horde_ee | 23 | 24 |
| Survival_Insane_Beta1 | 8 | 9 |
| Survival_Insane_NvS_Beta1 | 2 | 3 |
| survival_NorthSouth_Barrens | 2 | 3 |
| survival_sea_fleet | 9 | 10 |
| survival_vs_4player | 3 | 4 |
| XXX_Survival | 1 | 2 |
| XXX_Survival_5P | 23 | 24 |
