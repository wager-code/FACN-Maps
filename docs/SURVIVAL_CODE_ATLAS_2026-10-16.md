# 62张生存地图代码地图册（历史快照，2026-10-16起）

本文件记录维护包的代码研究和历史快照。全局当前数量及累计维护修改数以 [CURRENT_STATE.md](CURRENT_STATE.md) 为准。先前9张专用模组地图的删除与当时的修正范围见对应历史报告。逐图卡片记录玩法、函数位置、选项、来源哈希和回归边界；使用前必须确认卡片证据仍匹配目标文件。

> 2026-10-20纠正：保留数量仍62，但Brainsucka实际OnStart字节码存在强制专用模组检测。此前卡片遗漏已更正，不能把保留分类当作全部无模组证明；本轮没有删除或改写地图。见[依赖与上传专项](BRAINSUCKA_LUAC_AND_REQUIRED_MOD_2026-10-20.md)。

> 2026-10-20维护：ID30 Insane Beta1已修为v2，包与安装均更新；原默认目标无武器错误会阻断刷兵和原版统计初始化。36项隔离及3项部署后Lua核验通过，仍待游戏测试；当前累计29张有维护修改。下方28张及689项是10月16日快照。见[专项](INSANE_BETA1_STARTUP_SCORE_FIX_2026-10-20.md)。

> 2026-10-20用户实测更新：ID33 Sea Fleet已修为v8，用户确认本次同队AI、开局与结算问题“没问题了”。16项隔离＋2项落盘Lua核验通过；用户反馈不扩展为其他地图、全波次/多人/FAF通过，累计修改仍29。见[专项](SEA_FLEET_ALLIANCE_STARTUP_SCORE_2026-10-20.md)。

> 2026-10-20后续增强：ID30当前v3，加入传送门堡垒96/112单位，保留v2修复。50＋3项隔离/落盘检查通过，未游戏实测；累计修改数仍29。上方v2段为历史修复阶段。见[当前v3](INSANE_GATE_FORTRESS_V3_2026-10-20.md)。

> 2026-10-20最新迭代：ID30已由v3升v4，按截图反馈收拢并加密为184/216建筑；50＋3项检查通过，仍待游戏实测，62/累计29保持。上方v2/v3是历史阶段。见[当前v4](INSANE_GATE_FORTRESS_V4_2026-10-20.md)。

## 覆盖和结论边界

- 扫描627个Lua/字节码文件，识别2833个函数定义（按函数体哈希1674种），361个选项；总文本行含大型存档、辅助文件和重复库，不冒称每行均人工执行或语义证明。
- 全量目标Lua检查689项：62份场景/存档/选项数据求值全部通过；627份编译中622通过、5份备用/编辑辅助文件失败，详见下方。
- 25张经典字面量波表地图做缺省/最小/最大选择的75个首波隔离用例，全部通过；9张实际修正另有37项目标Lua/路由/偏好键/版本验证通过。
- 当前扫描669处常量import/doscript可在Steam及地图包定位。动态拼接、条件分支、回调、字节码和引擎行为不由此证明。
- 本机Steam资源索引573种蓝图。25张提取出的字面量波表没有缺失蓝图；可选MOD/独立模块/运行时生成单位另查，不宣称所有选项组合都无模组依赖。
- 在2026-10-16扫描快照中，保留62张，其中28张有此前整合或当时维护修改；这是历史阶段的统计，不是当前累计修改数。后续累计数见 [CURRENT_STATE.md](CURRENT_STATE.md)。本地图册未证明62张全部通过Steam/FAF实机、后期完整流程或多人测试。

## 需要保留的疑点

1. Zhuna只有初始化和空OnStart，没有地图内置生存链；外置模式来源待调查。普通槽位目录不等于有完整生存实现。
2. AIX TeamPlayAI和Pass AIX依靠大厅AI对战，没有固定生存波表；不能因为名字含survival便补写新的波次。
3. Onix海军的ARMY_SUPERWEAPON同时在大厅与ExtraArmies，特殊槽意图待实测，保持原配置。
4. DDay的Floe prop和Temple的Floe材质路径在目标资源中未找到；先调查完整资源和画面，不随意替换地形。
5. Rainmakers的info-theme.lua为辅助数据格式，旧Lua不能编译但无活动引用证据；Endless/Horde/Center EE/Aeon的EventDispatcher.lua使用旧Lua不支持的可变参转发表达式，仅找到vendor测试引用，不据此宣布整图不可玩。未来启用该模块须先作语法兼容、参数含nil及监听器增删测试。
6. 部分图带.git、测试、编辑器辅助文件和额外SCMAP。内容中心发布包宜基于实际运行资源清单排除开发缓存，但本轮未删除这些来源材料或擅改地图身份。

## 逐图入口

| 原ID | 地图 | 当前修订 | 玩法与研究方向 | 选项 |
| ---: | --- | ---: | --- | ---: |
| 1 | [Rainmakers Survival](maps/01.md) | 65 | 火炮阵地防守与战役事件 | 9 |
| 2 | [SH1R3_Mycelium2_Survival](maps/02.md) | 1 | 三槽Mycelium经典生存 | 3 |
| 3 | [Survival Omega v3](maps/03.md) | 3 | Omega经典守点 | 3 |
| 4 | [5iver Survival Brainsucka](maps/04.md) | 1 | Brainsucka编译脚本生存 | 2 |
| 5 | [Black Sun Defense v2](maps/05.md) | 2 | Black Sun阶段/传送门防守 | 3 |
| 7 | [Desert Swarm v1c Beta](maps/07.md) | 1 | Desert Swarm经典波次 | 3 |
| 8 | [Dreamy Survival v16](maps/08.md) | 16 | Dreamy经典波次改版 | 3 |
| 9 | [Endless Survival Defense](maps/09.md) | 17 | 经济驱动、随机AI性格与竞争生存 | 24 |
| 10 | [Fort Ictus Survival v9](maps/10.md) | 9 | Fort Ictus经典守点 | 3 |
| 11 | [Sexy Survival v13](maps/11.md) | 13 | Sexy经典波次改版 | 3 |
| 12 | [SH1R3_Mycelium2_Survival](maps/12.md) | 2 | 四槽Mycelium经典生存 | 3 |
| 13 | [Survival of the Fittest](maps/13.md) | 1 | Survival of the Fittest竞争生存 | 0 |
| 14 | [Survival Attack](maps/14.md) | 1 | 移动战列舰目标与进攻任务 | 4 |
| 15 | [Survival Run v8](maps/15.md) | 1 | Survival Run撤离护送 | 3 |
| 16 | [survival_5thdimension v6](maps/16.md) | 1 | 四槽沙漠5th经典防守 | 3 |
| 17 | [survival_5thdimension_practice v9](maps/17.md) | 9 | practice阵营选择与可选人数缩放 | 8 |
| 18 | [Survival Blackbox 10](maps/18.md) | 1 | Blackbox多阶段守宫殿 | 12 |
| 19 | [Survival Defense Atoll](maps/19.md) | 1 | Atoll环礁守点 | 3 |
| 20 | [Survival Escape v5](maps/20.md) | 5 | Escape护送与扩区 | 2 |
| 22 | [Survival EXtreme](maps/22.md) | 1 | Extreme传送门/超级武器防守 | 4 |
| 23 | [Survival EXtreme Desert v3](maps/23.md) | 3 | Extreme Desert常规版 | 4 |
| 25 | [Survival EXtreme NavyV2](maps/25.md) | 1 | 四槽Extreme Navy | 4 |
| 29 | [Survival Horde EE v22](maps/29.md) | 22 | Horde EE分路线防守 | 7 |
| 30 | [Survival Insane (Beta1)](maps/30.md) | 4 | Insane挑战版 | 4 |
| 31 | [Survival Insane NvS (Beta1)](maps/31.md) | 1 | Insane North vs South挑战 | 4 |
| 32 | [Survival North and South Barrens](maps/32.md) | 1 | North and South Barrens | 4 |
| 33 | [Survival Sea Fleet v8](maps/33.md) | 8 | Sea Fleet海军与空军 | 5 |
| 34 | [Genesis of the Order Survival v13](maps/34.md) | 13 | Genesis of the Order剧情事件生存 | 6 |
| 35 | [Broad Front Survival v8](maps/35.md) | 8 | Broad Front预建基地生存 | 3 |
| 36 | [desert front survival v25](maps/36.md) | 25 | Desert Front多模式守点 | 18 |
| 38 | [survival_5thdimension v8](maps/38.md) | 1 | 六槽沙漠5th | 3 |
| 39 | [Survival Genesis v17](maps/39.md) | 17 | Genesis多模式与无尽 | 16 |
| 41 | [Zhunas Crater Swarm Survival](maps/41.md) | 3 | 仅初始化地形，外置模式待调查 | 0 |
| 42 | [5iver Survival LandNaval v2](maps/42.md) | 2 | LandNaval八槽海陆对半 | 25 |
| 43 | [AIX survival TeamPlayAI](maps/43.md) | 1 | 大厅AI对战布局 | 0 |
| 44 | [Battle of Thermopylae Survival](maps/44.md) | 1 | Thermopylae八人经典防守 | 3 |
| 45 | [beach survival](maps/45.md) | 6 | Beach经典防守 | 3 |
| 46 | [Center Arena Survival v18](maps/46.md) | 18 | Center Arena经典防守 | 3 |
| 47 | [Final Rush Survival](maps/47.md) | 6 | Final Rush科技解锁与随机事件 | 7 |
| 48 | [Forges Survival](maps/48.md) | 5 | Forges经典防守 | 3 |
| 49 | [Not Agincourt Survival](maps/49.md) | 4 | Not Agincourt合作守点 | 3 |
| 50 | [Survival Light 2a](maps/50.md) | 2 | Light 2a工厂/指挥官防守 | 12 |
| 51 | [Survival 5th Dimension Center EE v7](maps/51.md) | 7 | Center EE扩展经典守点 | 9 |
| 54 | [survival_5thdimension 8 player](maps/54.md) | 4 | 真正八人5th | 3 |
| 55 | [Survival EXtreme NavyV28](maps/55.md) | 1 | 八槽Extreme Navy | 4 |
| 57 | [voodoo battle survival new v25](maps/57.md) | 25 | Voodoo New多模式 | 18 |
| 60 | [naval survival onix v70](maps/60.md) | 70 | Naval Onix海战变体 | 4 |
| 61 | [pass survival aix v2](maps/61.md) | 15 | AIX布局与军队初始化 | 0 |
| 63 | [Survival Terror Lands v2](maps/63.md) | 2 | Terror Lands多模式守点 | 18 |
| 65 | [66安尔乐v05C](maps/65.md) | 5 | Anerle分队与竞争波次 | 0 |
| 66 | [Survival EpischeLAN v6](maps/66.md) | 6 | EpischeLAN多门攻防 | 6 |
| 68 | [survival_5thdimension 16 player](maps/68.md) | 8 | 十六人5th | 3 |
| 69 | [Survival DDay Horde](maps/69.md) | 2 | DDay Horde海滩路线防守 | 3 |
| 71 | [Aeon Illuminate Survival v12](maps/71.md) | 12 | Aeon Illuminate黑日守护 | 8 |
| 72 | [deadzone survival v9](maps/72.md) | 9 | Deadzone经典守点 | 3 |
| 74 | [Survival Experimental Factory](maps/74.md) | 3 | Experimental Factory实验级突击 | 3 |
| 75 | [Survival Stranded v23](maps/75.md) | 23 | Stranded多模块海陆空防守 | 10 |
| 78 | [Dune Survival v2](maps/78.md) | 2 | Dune城市守点 | 3 |
| 79 | [onixs voodoo survival v17](maps/79.md) | 17 | Onix Voodoo扩展多模式 | 22 |
| 80 | [Survival Temple v5](maps/80.md) | 5 | Temple山顶守护 | 3 |
| 81 | [survival_生存AN_voodoo_no_mods v4](maps/81.md) | 4 | AN Voodoo无模组改版 | 3 |
| 83 | [Tomb Guard Survival v4](maps/83.md) | 4 | Tomb Guard多阵营职责守点 | 3 |

## 可复用与外部资料

- [AI制作地图/玩法的方法与Steam、FAF配置](AI_MAP_AUTHORING.md)
- [其他作者报告的问题、来源、已关闭/待调查状态](EXTERNAL_MAPPING_RESEARCH_2026-10-16.md)
- [本轮实际9张修正、损失和验证](CODE_MAINTENANCE_2026-10-16.md)
- [机器可读摘要与函数位置/哈希](data/survival_code_atlas_2026-10-16.json)
- 只读扫描器：`tools/scan_scfa_maps.py`。已在当前62张实际运行；不会修改游戏或地图。

本地图册以当前文件哈希为准。地图更新后先重扫，再更新卡片；不能用历史行号和过去版本的补丁覆盖未知新版本。

## ID30最新状态覆盖：v5紧凑防区已落实（2026-10-20）

上方v2/v3/v4为历史；当前包/安装v5，16防区368/432守备，活门外侧出生点，50+3隔离/落盘通过、未游戏实测。62/累计29保持。详见[当前v5](INSANE_COMPACT_FORTS_V5_2026-10-20.md)与30卡片，勿用旧v4只读候选覆盖。

## ID30最新v6（2026-10-20）

当前包/安装v6，16核心各8/12座T3点防＋1满仓战略反核＋原2TMD，总384/448守备，50+3项通过，未游戏实测。仍62/累计29；v5及以前为历史，见[当前报告](INSANE_T3_ANTINUKE_V6_2026-10-20.md)与30卡片。

## ID30最新v7（2026-10-20）

当前包/安装v7：所有难度下128座守备防空全T3、T2防空0，地防8/12T3与反核/双TMD保持，16雷达升T3。50+3项通过，未v7游戏实测，仍62/29。[当前v7](INSANE_ALL_T3_V7_2026-10-20.md)覆盖上方v6及更早状态。
