# 安装35张生存地图准备时间合并（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

> 后续用户明确改为“去掉旧的，以新的为主”：8图删20重复旧开局设置及对应生成链，35图准备显示统一m:ss，当前总394项；地图名/版本本轮不动。旧235项全部保留、445/414项及相加方案均为历史。最新见[开局单位去重与时间显示](INSTALLED_START_UNIT_DEDUP_2026-10-21.md)。

用户在高级设置截图中明确要求：“不用带新增两个字啊，而且地图原来有开局准备时间的，在原来的基础上改不就行了。”本轮授权允许扩展原准备时间的档位；其它原设置和玩法继续保留。此记录覆盖前一轮追加独立准备选项的方案，仅针对E:/SCFA/maps安装副本。

## 当前结果

- 31张已有准备时间：保留原菜单的key、pref、default、标题、帮助、旧values及顺序；只在末尾补充缺少的1～10、12/14/16/18/20分钟档，删除此前追加的第二个准备时间。原图已有的半分钟、15/25/30/60分钟等档位均保留。
- 4张无原准备菜单：Brainsucka、Supreme_AOD、Supreme_survival、survival_vs_4player，保留一个“开局准备时间”，默认沿用原图。
- 35张的开局单位菜单去掉“新增”字样，保留“额外”以说明数量与原图赠送相加。副指挥官/工程师各自的数量、种族、四种族模式，及工程师等级均保留。
- 原235项菜单仍在，只有31个准备选项的可选时间按授权扩展；其它204项完整相同。总菜单445→414，每图只有一个准备选项。

## 计时接入

31份地图局部模块的Preparation直接返回原值，Read.preparation固定-1，不再读取被删除菜单的键。即使大厅缓存里残留opt_FACN_StartV1_Preparation，也不会覆盖原菜单选择；无需清除用户偏好。

原消费者继续使用原键和单位：5iver四张为分钟、普通图为秒，Horde使用原getSpawnDelay；未改变预设的优先级、禁止快攻、固定初始化延迟、科技时钟、波次间隔、计分、胜负或核爆。原预设可能覆盖手动时间，继续遵守原图规则。

Astro的原菜单键编码为10000+秒，脚本还存在允许值列表；本轮同步在该列表末尾追加720/840/960/1080/1200，保留所有旧索引，避免菜单有20分钟而实际回退300秒。其余33张文本主脚本不变，Brainsucka四份原字节码不变；4张无原菜单仍使用上一轮准备适配。

## 文件、备份和检查

已改102文件：35 options、35 scenario修订、31地图局部模块、1 Astro脚本。没有增删文件，另552个自定义文件SHA保持；61官方及7其它自定义地图不在写入范围。游戏程序、SCD、模组、用户偏好/缓存与维护包62张均未写入。安装Insane9→10，维护包Insane仍7；不能互相覆盖。

先备份35图完整597文件到工作区“35张生存地图准备时间合并_20261021/合并前35张完整地图备份.zip”，逐文件与归档SHA核对。当前备份SHA：`06b432ffacb6a17fae67c08fba188a3b468d1f203a4d997bd9103bb103b6732c`。

本机LuaPlus_1081.dll：102份候选正式Lua语法、35组实际游戏maputil/dataInit空环境加载与模块计时检查、35组落盘检查均通过。原菜单逐字段比对只允许准备values末尾扩展；单位菜单仅显示文本调整，键/偏好/数量/种族/等级不变。包含残留旧准备键不会覆盖原值、四张无原菜单主动/沿用分支、独立单位设置与Astro旧/新编码及索引断言。

**状态：已修改待实测。** 用户截图证明前一阶段可见高级菜单，不代表本轮实机、首波、单/多人、后期或FAF验收。重新启动游戏并新开局，在原准备菜单选20分钟观察准备/首波，同时单独测试两类单位及多人同步。没有淘汰或删除地图；完整旧文件留在备份。

## 当前逐图修订

| 安装目录 | 修订前→后 | 准备菜单原键 | 补充档位（分钟） |
| --- | --- | --- | --- |
| `5iver Survival Brainsucka` | 3→4 | `无原菜单，保留单项` | 无需补充/单项沿用 |
| `5iver Survival Land` | 4→5 | `opt_General_StartupDelay` | 12, 14, 16, 18, 20 |
| `5iver Survival Land Naval` | 4→5 | `opt_General_StartupDelay` | 12, 14, 16, 18, 20 |
| `5iver_survival_land_oxtreme` | 12→13 | `opt_General_StartupDelay` | 16, 18, 20 |
| `5iver_survival_landnaval-swarm` | 14→15 | `opt_General_StartupDelay` | 8, 9, 12, 14, 16, 18 |
| `astro_surv_stm` | 10→11 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `BBF_BlackSunDefense` | 4→5 | `startupDelay` | 4, 6, 7, 8, 9, 12, 14, 16, 18, 20 |
| `Desert_Swarm_v1c_Beta` | 3→4 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `dreamy_survival` | 18→19 | `opt_Survival_BuildTime` | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 |
| `endless_survival_defense` | 19→20 | `opt_Survival_BuildTime` | 无需补充/单项沿用 |
| `Fort Ictus Survival` | 12→13 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `grand_barrens_survival` | 15→16 | `opt_Survival_BuildTime` | 1, 2, 5, 7, 9, 12, 14, 16, 18, 20 |
| `sexy_survival` | 15→16 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `sh1r3_mycelium2_survival` | 4→5 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `Supreme_AOD` | 7→8 | `无原菜单，保留单项` | 无需补充/单项沿用 |
| `Supreme_survival` | 3→4 | `无原菜单，保留单项` | 无需补充/单项沿用 |
| `survival attack` | 3→4 | `StartTime` | 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 |
| `Survival Omega` | 3→4 | `opt_Survival_BuildTime` | 1, 2, 3, 4, 6, 7, 8, 9, 12, 14, 16, 18 |
| `Survival Run` | 10→11 | `StartTime` | 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 |
| `survival_5thdimension` | 8→9 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `survival_5thdimension_practice` | 11→12 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `Survival_BlackBox_10` | 3→4 | `opt_startupTime` | 1, 2, 18 |
| `survival_defense_atoll` | 3→4 | `opt_Survival_BuildTime` | 12, 14, 16, 18 |
| `Survival_Escape` | 7→8 | `StartTime` | 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 |
| `Survival_Extreme` | 3→4 | `opt_startupTime` | 4, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 |
| `Survival_ExtremeDesert` | 5→6 | `opt_startupTime` | 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 |
| `Survival_ExtremeNavy` | 4→5 | `opt_startupTime` | 1, 2, 4, 6, 7, 8, 9, 12, 14, 16, 18, 20 |
| `survival_horde_ee` | 24→25 | `opt_HordeSpawnDelay` | 12, 14, 16, 18, 20 |
| `Survival_Insane_Beta1` | 9→10 | `opt_startupTime` | 12, 14, 16, 18, 20 |
| `Survival_Insane_NvS_Beta1` | 3→4 | `opt_startupTime` | 12, 14, 16, 18, 20 |
| `survival_NorthSouth_Barrens` | 3→4 | `opt_startupTime` | 4, 6, 7, 8, 9, 12, 14, 16, 18, 20 |
| `survival_sea_fleet` | 10→11 | `opt_Survival_BuildTime` | 1, 2, 4, 5, 6, 7, 8, 9, 12, 14, 16, 18, 20 |
| `survival_vs_4player` | 4→5 | `无原菜单，保留单项` | 无需补充/单项沿用 |
| `XXX_Survival` | 2→3 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |
| `XXX_Survival_5P` | 24→25 | `opt_Survival_BuildTime` | 12, 14, 16, 18, 20 |

本地证据：本轮目录内备份核验、部署计划、候选Lua语法结果、候选加载与计时结果、实际落盘检查结果和最终核验JSON。历史v8/v9报告保持为阶段记录，当前版本以本页和本轮实际文件为准。
