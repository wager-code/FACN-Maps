# 安装生存地图开局单位去重与时间显示（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

## 用户授权和当前范围

用户要求先检查定义/Key/默认/读取/实际调用/生成时机，删除确认冗余的选项与引用，保留作用不同的功能，并将检查扩展到其它生存图。最初要求复用原实现；对发现的旧固定赠送与新独立设置差异提出选择后，用户明确回答“直接去掉旧的，以新的为主啊”。本轮以该最新指示执行：**普通开局工程师/副指挥官保留新一套，删除重复旧一套**。用户另外要求准备时间数字统一，例如12:00。明确禁止改地图名称、版本号和无关玩法；此项优先于旧通用升版约定。

范围为E:/SCFA/maps当前35张生存/AOD；61官方、7其它自定义、维护地图包62张、程序/SCD、模组和用户偏好不写入。35张均检查菜单及地图局部开局模块，目标8张额外追踪旧生成链。字节码图保留原入口和模组检测，不声称证明所有动态/字节码功能无重叠。

## Grand Barrens完整判定

修改前26项菜单，各Key本来就不相同；问题是两套相同用途的设置和生成链，不是重复Key。

旧链：主脚本OnPopulate→EnsureSteamDefaults→lib/SpawnACUs.lua.SpawnACUs→SpawnConfiguredUnits→GetSelectedFactions/SpawnStartUnit→CreateUnitHPR。每名实际玩家在OnPopulate时生成，四族模式按每族数量；工程师必须Tier为1～3且数量>0；副指挥官只需数量>0。旧Tier=0关闭、数量0～10、阵营0本阵营/1～4指定/5四族。

新链：主脚本末尾FACNStart.Attach→包装OnStart→原OnStart先执行→额外一次ForkThread→WaitSeconds(0.1)→FACN_StartOptions.Spawn→按实际玩家/阵营/等级生成。新数量0～20、独立阵营/四族、工程师T1/T2/T3。两套同时非零会相加；没有证据表明这两套是作者设计的不同剧情援军。按最新授权保留新链，删除旧链。

| 选项名称 | 原有情况 | 处理方式 | 最终结果 |
| --- | --- | --- | --- |
| 生存：工程师阵营 | opt_Survival_EngineerFaction；default字段1，首项0本阵营；OnPopulate读取 | 删除旧定义、默认回退与生成读取 | 由新工程师种族统一控制 |
| 生存：工程师数量 | opt_Survival_EngineerCount；default字段1，首项0；0～10，四族按每族计数 | 删除旧定义、默认回退与生成读取 | 新数量0～20，0不生成 |
| 生存：副指挥官阵营 | opt_Survival_SCUFaction；default字段1，首项0；本族/指定/四族 | 删除旧定义、默认回退与生成读取 | 由新副指挥官种族统一控制 |
| 生存：副指挥官数量 | opt_Survival_SCUCount；default字段1，首项0；0～10 | 删除旧定义、默认回退与生成读取 | 新数量0～20，0不生成 |
| 生存：额外工程师等级 | opt_Survival_EngineerTier；default字段1，首项0关闭；0/T1/T2/T3 | 删除旧定义及Tier门控 | 新等级T3默认，可选T1/T2；数量0负责关闭 |
| 额外副指挥官数量（每阵营） | 新Key opt_FACN_StartV1_SACUCount，编码200000+n，default=1指向0 | 保留原新实现 | 每玩家每族0～20；四族20为80名 |
| 额外副指挥官种族 | 新Key opt_FACN_StartV1_SACUFaction，编码300000+n，default=1指向跟随玩家 | 保留 | 本族/UEF/万古/塞布兰/瑟拉芬/四族 |
| 额外工程师数量（每阵营） | 新Key opt_FACN_StartV1_EngineerCount，编码400000+n，default=1指向0 | 保留 | 每玩家每族0～20；与副指挥官独立 |
| 额外工程师等级 | 新Key opt_FACN_StartV1_EngineerTech；值500003/500001/500002 | 保留 | T3默认，T1/T2可选；数量0不生成 |
| 额外工程师种族 | 新Key opt_FACN_StartV1_EngineerFaction，编码600000+n | 保留 | 与副指挥官独立；四族按每族计数 |

旧菜单原始定义、每项default/values、定义和读取行号、上下文，完整保存在工作区逐项检查清单_修改前.json；行号仅对应该次原SHA。Grand当前地图修订仍16，名称不变。

从Grand的SpawnACUs.lua移除V13额外单位表、GetSelectedFactions、SpawnStartUnit、SpawnConfiguredUnits及其调用；同时删已被EnsureSteamDefaults强制归零、菜单不再提供的spawnID=1～4旧固定工程师/SCU分支。保留旧缓存1～4归零保护，保留AllFactions=0普通ACU、5各族ACU、6各族双ACU、7实验单位开局。后者是主指挥官/特殊开局，不能与SUBCOMMANDER普通赠送混删。

## 其它地图判定和清理

| 地图 | 已核实旧链/差异 | 清理结果 |
| --- | --- | --- |
| Astro | 原SACU数量/阵营、工程师数量/等级；InitGame编码解码，OnStart ForkThread(Survival_SpawnStartBonusUnits)；原工程师只跟随本族 | 删除4旧项、4解码及日志字段、3生成辅助函数与线程调用，保留新5项补足独立工程师族及四族 |
| XXX Survival 5P | 原5项Reinforcement设置；OnStart启动独立线程，WaitSeconds(1)；SCU0～10、工程师0～20、仅单族 | 删除5旧项、7辅助函数/表和旧ForkThread，保留新5项及四族 |
| 5iver Survival Land | opt_General_PrebuiltEngineers按等级或SCU选择四族各1，原setupGame调用spawnPrebuiltEngineers | 删除1旧项、旧函数和调用；新数量/种族/等级控制 |
| 5iver oxtreme | 同类固定四族赠送，先读局部同名配置再生成 | 删除1旧项、该配置读取、旧函数和调用 |
| 5iver landnaval-swarm | 原关闭/T1/SCU四族固定赠送，setupGame调用 | 删除1旧项、旧函数和调用 |
| Endless | 四族固定赠送且这些单位质量/能量自产归零 | 删除1旧项、默认配置、旧函数和调用；将原零产出规则保留在本图新生成回调，不改共享蓝图 |
| BlackBox | opt_spawn_sc及opt_spawn_t1eng在原OnStart各送四族1个 | 删除2旧项、默认回退、两个if块与SpawnSupcoms/SpawnIngis函数；保留SpawnCommis、GimmeGods、only模式/限制/强化 |

共8张删除20旧菜单。未删除作用不同的设置：Grand特殊主ACU/实验开局、Practice四个主ACU阵营选项、Run/Attack剧情战斗增援、BlackBox主ACU开局及only强化模式。另24张没有发现与本次5个可配置开局单位菜单等效的旧菜单链，保留新入口和已有正常固定/剧情单位；此结论基于当前活动Lua/菜单，不夸大为所有动态加载和字节码已完全证明。

默认按新一套：工程师/副指挥官数量0，种族跟随玩家，工程师T3。旧固定赠送不再叠加，也不再根据旧偏好自动赠送；这是用户选择“去掉旧的，以新的为主”的结果。旧缓存键不会触发旧链，因为定义、读取和函数引用均已移除。没有清用户偏好。两类均选四族20时，每玩家各80、合计160；实际放置空间不足会WARN跳过。

## 准备时间

35张全部固定时长显示统一为m:ss，例如0:30、1:00、12:00、20:00。分钟键、秒键、Astro10000+秒编码、扩展100000+秒编码分别转换显示；没有改变key、pref、default、时长、顺序、帮助或消费公式。四张“沿用原图（默认）”保留语义文字。其它波次间隔菜单不在此格式修改范围。

## 检查、边界和备份

- 35张本机实际maputil/dataInit严格空optionsEnv菜单加载，候选35及落盘35均通过；总菜单414→394，Key全部唯一，每图保留5项有效独立开局单位控制，且一个准备时间。
- 106份实际目标LuaPlus语法检查通过：35主脚本/字节码、35菜单、35局部模块、Grand原ACU模块。没有用普通Lua版本冒充。
- 候选36＋落盘36行为用例通过。各35模块覆盖72个阵营/等级组合，独立种族、数量0与0～20解码、旧缓存键、重复Attach/回调不重复安排新单位、空槽/额外军队/已失败军队、160上限；Grand另执行真实保留ACU模块验证普通ACU及5/6/7特殊开局不回归。Endless实际模块验证新赠送单位质量/能量产出为0。
- 八图整个Lua树的20旧Key和被删生成符号均无残留；所有保留菜单逐字段比对，仅允许删确认的20旧项和准备值text改m:ss，其它定义不变。35场景完整元数据一致且文件SHA不变，地图名/版本/槽位/路径不改。
- 只写45文件：35 options、8 script、Grand的1个lib/SpawnACUs、Endless的1个FACN_StartOptions。无增删文件，609个其它自定义文件SHA保持；地形/save/预览/字节码不写入。官方61与其它7图不在写入范围，维护地图包62张及游戏系统不动。

状态：**已修改待实测**。本轮总248个候选/落盘Lua检查入口通过，是本机Lua隔离检查，不是游戏运行验收。未运行真实游戏首波、碰撞/寻路、单位限制、完整模式联动、多人同步或FAF。需重启游戏新开局检查新菜单、实际单位数量/族/等级、0关闭、两类四族、原主指挥官/剧情/特殊模式、Endless经济及多人；同版本保存/缓存不能作为本轮文件验收，版本按用户明确要求未升。

备份：工作区生存地图开局单位去重_20261021/去重前35张完整地图备份.zip，597文件逐个SHA核验，归档SHA：`991fec4055b1563726581d0f4a765bcc190097e0df01dce13d6b66cd44bb552d`。保留本次原文件，不删除地图。证据包括逐项检查清单_修改前.json、全部差异.diff、部署计划/部署结果、Lua语法结果、候选/实际落盘菜单与行为结果、最终核验.json。

## 实际修改文件清单

- `E:/SCFA/maps/5iver Survival Brainsucka/5iver Survival Brainsucka_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/5iver Survival Land/5iver Survival Land_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/5iver Survival Land/5iver Survival Land_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/5iver Survival Land Naval/5iver Survival Land Naval_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/5iver_survival_land_oxtreme/5iver_survival_land_oxtreme_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/5iver_survival_land_oxtreme/5iver_survival_land_oxtreme_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/5iver_survival_landnaval-swarm/5iver_survival_landnaval-swarm_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/5iver_survival_landnaval-swarm/5iver_survival_landnaval-swarm_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/astro_surv_stm/astro_surv_stm_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/astro_surv_stm/astro_surv_stm_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/BBF_BlackSunDefense/BBF_BlackSunDefense_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Desert_Swarm_v1c_Beta/Desert_Swarm_v1c_Beta_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/dreamy_survival/dreamy_survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/endless_survival_defense/endless_survival_defense_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/endless_survival_defense/endless_survival_defense_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/endless_survival_defense/FACN_StartOptions.lua` — preserve-endless-start-unit-zero-production
- `E:/SCFA/maps/Fort Ictus Survival/Fort_Ictus_Survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/grand_barrens_survival/grand_barrens_survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/grand_barrens_survival/grand_barrens_survival_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/grand_barrens_survival/lib/SpawnACUs.lua` — remove-old-grand-configured-generator
- `E:/SCFA/maps/sexy_survival/sexy_survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/sh1r3_mycelium2_survival/SH1R3_Mycelium2_Survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Supreme_AOD/Supreme_AOD_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Supreme_survival/Supreme_survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival attack/Survival Attack_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival Omega/Survival Omega_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival Run/Survival Run v8_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival_5thdimension/survival_5thdimension_v6_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival_5thdimension_practice/survival_5thdimension_practice_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_BlackBox_10/Survival_BlackBox_10_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_BlackBox_10/Survival_BlackBox_10_script.lua` — remove-old-start-unit-entry
- `E:/SCFA/maps/survival_defense_atoll/Survival_Defense_Atoll_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_Escape/Survival_Escape_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_Extreme/Survival_Extreme_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_ExtremeDesert/Survival_ExtremeDesert_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_ExtremeNavy/Survival_ExtremeNavyV2_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival_horde_ee/survival_horde_ee_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_Insane_Beta1/Survival_Insane_Beta1_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/Survival_Insane_NvS_Beta1/Survival_Insane_NvS_Beta1_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival_NorthSouth_Barrens/Survival_NorthSouth_Barrens_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival_sea_fleet/survival_sea_fleet_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/survival_vs_4player/survival_vs_4player_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/XXX_Survival/XXX_Survival_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/XXX_Survival_5P/XXX_Survival_5P_options.lua` — menu-dedup-and-clock-labels
- `E:/SCFA/maps/XXX_Survival_5P/XXX_Survival_5P_script.lua` — remove-old-start-unit-entry

## Grand修改前逐项定位

| 显示名 / Key | 原定义位置 | 原读取与执行线索 | 处理 |
| --- | --- | --- | --- |
| 生存：额外工程师等级 / `opt_Survival_EngineerTier` | `grand_barrens_survival/grand_barrens_survival_options.lua:201` | `grand_barrens_survival/grand_barrens_survival_script.lua:59`; `grand_barrens_survival/grand_barrens_survival_script.lua:60`; `grand_barrens_survival/grand_barrens_survival_script.lua:952`; `grand_barrens_survival/grand_barrens_survival_script.lua:953`; `grand_barrens_survival/lib/SpawnACUs.lua:37` | 删除旧菜单及旧读取/生成入口 |
| 生存：工程师阵营 / `opt_Survival_EngineerFaction` | `grand_barrens_survival/grand_barrens_survival_options.lua:214` | `grand_barrens_survival/grand_barrens_survival_script.lua:62`; `grand_barrens_survival/grand_barrens_survival_script.lua:63`; `grand_barrens_survival/grand_barrens_survival_script.lua:955`; `grand_barrens_survival/grand_barrens_survival_script.lua:956`; `grand_barrens_survival/lib/SpawnACUs.lua:38` | 删除旧菜单及旧读取/生成入口 |
| 生存：工程师数量 / `opt_Survival_EngineerCount` | `grand_barrens_survival/grand_barrens_survival_options.lua:229` | `grand_barrens_survival/grand_barrens_survival_script.lua:65`; `grand_barrens_survival/grand_barrens_survival_script.lua:66`; `grand_barrens_survival/grand_barrens_survival_script.lua:958`; `grand_barrens_survival/grand_barrens_survival_script.lua:959`; `grand_barrens_survival/lib/SpawnACUs.lua:39` | 删除旧菜单及旧读取/生成入口 |
| 生存：副指挥官阵营 / `opt_Survival_SCUFaction` | `grand_barrens_survival/grand_barrens_survival_options.lua:249` | `grand_barrens_survival/grand_barrens_survival_script.lua:68`; `grand_barrens_survival/grand_barrens_survival_script.lua:69`; `grand_barrens_survival/grand_barrens_survival_script.lua:961`; `grand_barrens_survival/grand_barrens_survival_script.lua:962`; `grand_barrens_survival/lib/SpawnACUs.lua:40` | 删除旧菜单及旧读取/生成入口 |
| 生存：副指挥官数量 / `opt_Survival_SCUCount` | `grand_barrens_survival/grand_barrens_survival_options.lua:264` | `grand_barrens_survival/grand_barrens_survival_script.lua:71`; `grand_barrens_survival/grand_barrens_survival_script.lua:72`; `grand_barrens_survival/grand_barrens_survival_script.lua:964`; `grand_barrens_survival/grand_barrens_survival_script.lua:965`; `grand_barrens_survival/lib/SpawnACUs.lua:41` | 删除旧菜单及旧读取/生成入口 |
| 额外副指挥官数量（每阵营） / `opt_FACN_StartV1_SACUCount` | `grand_barrens_survival/grand_barrens_survival_options.lua:348` | `grand_barrens_survival/FACN_StartOptions.lua:5` | 保留 |
| 额外副指挥官种族 / `opt_FACN_StartV1_SACUFaction` | `grand_barrens_survival/grand_barrens_survival_options.lua:371` | `grand_barrens_survival/FACN_StartOptions.lua:6` | 保留 |
| 额外工程师数量（每阵营） / `opt_FACN_StartV1_EngineerCount` | `grand_barrens_survival/grand_barrens_survival_options.lua:379` | `grand_barrens_survival/FACN_StartOptions.lua:7` | 保留 |
| 额外工程师等级 / `opt_FACN_StartV1_EngineerTech` | `grand_barrens_survival/grand_barrens_survival_options.lua:402` | `grand_barrens_survival/FACN_StartOptions.lua:8` | 保留 |
| 额外工程师种族 / `opt_FACN_StartV1_EngineerFaction` | `grand_barrens_survival/grand_barrens_survival_options.lua:407` | `grand_barrens_survival/FACN_StartOptions.lua:9` | 保留 |

新模块使用Keys表间接读取：Read→Spawn/Attach；其读取映射和生成位于FACN_StartOptions.lua的Keys、Read、selectedFactions、Spawn与Attach。源码明细在同目录SHA审计JSON；上述修改前行号不能直接当修改后行号使用。
