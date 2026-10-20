# E:/SCFA/maps 地图高级设置中文核对（2026-10-20）

> 后续更新：本次3张英文菜单已按用户授权汉化并各升一级，当前为v2/v2/v12；下方是汉化前审计快照。详见[完成记录](THREE_5IVER_OPTIONS_LOCALIZATION_2026-10-20.md)。

本轮只检查，不修改、删除、升版或复制任何地图。排除用户确认的61张官方配置；官方/系统/模组文件均未改。检查103个地图目录中的42张自定义地图，34张有地图自身高级设置，共243项、2974个非空显示字段；42张场景/活动菜单在本机LuaPlus隔离求值全部通过，未实际点击游戏菜单。

## 确认3张高级设置仍为英文

| 安装目录 | 当前显示名 | 修订 | 英文选项标题数 |
| --- | --- | ---: | ---: |
| `5iver Survival Land` | 5iver Survival Land | 1 | 23 |
| `5iver Survival Land Naval` | 5iver Survival LandNaval | 1 | 25 |
| `5iver_survival_landnaval-swarm` | 5iver_survival_landnaval-swarm | 11 | 7 |

这3份活动options.lua的全部55个选项标题仍是英文，帮助和文字型下拉值也大量英文。它们是作者直接写入的字符串，未引用LOC语言键；只把游戏切成中文不会自动翻译。可代表用户所见的两个主要候选是5iver Survival Land与5iver Survival Land Naval，但没有用户截图/具体图名，不声称已证明过去那两次加载的地图。

| 地图 | 英文例子 | 中文含义参考 |
| --- | --- | --- |
| Land / Land Naval | Pause at game start | 开局暂停 |
| Land / Land Naval | End game scenario | 胜利条件 |
| Land / Land Naval | Defense Objects | 防守目标 |
| Land / Land Naval | Defenses: Gate | 传送门守备 |
| Swarm | Difficulty (Gate hp boost) | 难度（传送门生命加成） |
| Swarm | Timing: Startup delay | 开局准备时间 |
| Swarm | Timing: Peak Tech Time | 最高科技阶段时间 |

准确路径：

- `E:/SCFA/maps/5iver Survival Land/5iver Survival Land_options.lua`
- `E:/SCFA/maps/5iver Survival Land Naval/5iver Survival Land Naval_options.lua`
- `E:/SCFA/maps/5iver_survival_landnaval-swarm/5iver_survival_landnaval-swarm_options.lua`

本轮针对安装目录，不用维护包“已汉化”状态替代安装副本证据。维护包的ID42活动路径为`08槽位/5iver_survival_landnaval`、显示名5iver Survival LandNaval v2；不能因名字相似直接覆盖上述安装副本。本轮没有做同图版本取舍或同步。

## 其余地图

其余31张有自定义高级设置的地图主体中文；其中grand_barrens_survival有5处Boss词语（例如“生存：Boss波次”），可统一成“首领”。survival_5thdimension_practice有一处中文帮助使用ARMY_1至ARMY_4内部标识，建议以后改成“玩家槽位1至4”；它不是整张菜单未翻译。

AI、T1/T2/T3、UEF、SCU、阵营英文括注、Horde EE/Aeon Fixed等模式专名、x倍数和时间数字不算整张高级设置英文。保留这些文字的地图仍按主体中文记录，不能宣称每个字符都已中文化。

8张没有地图自带高级设置：
- 6 fields of isis
- 6castles
- astro_crater_battles_4x4_teamplay_ai
- dunes_of_arracis
- quad_pass_teamplay_ai_4v4
- Supreme_AOD
- Supreme_survival
- survival_vs_4player

“没有自带高级设置”不代表没有通用队伍/游戏选项，也不代表地图没有玩法。官方61配置仅排除，不重新判断是否损坏。

## 避免误报的方法

依据本机lua/ui/maputil.lua:44–50，由scenario文件名前缀拼出对应options.lua，执行后读取options表。仅检查这张活动表中的label、help、values.text、values.help，不按文件里所有英文粗略统计。此次活动显示文本没有LOC标签，不需要猜测英文fallback是否会被中文语言库覆盖；以后出现LOC时应核对实际语言键。

例如Adaptive Black Mesa与Signalpoint的文件中保留很多注释掉的英文选项，实际求值的活动选项已中文；Endless文件也有未启用英文条目，不能算当前菜单英文。34张活动选项文件均为文本，本轮没有跳过任何活动字节码菜单。

另只读发现已安装gamedata中的cityscapes.scd提供Cityscapes:*选项，CSKMainMenu.scd的通用菜单含Unit Cap、User Spawn/Cheat Menu等直接英文标题。前者带LOC需核对当前语言解析，后者是否出现在界面取决于实际挂载覆盖。本轮没有验证全局VFS/模组启用状态，也不把这些来源算到某张地图；若同一英文项跨多张图出现，优先查共享模组界面，不逐图改玩法。本轮不动任何官方或系统SCD。

## 验证与交付

保存检查前960文件SHA清单，结束后逐个重算并比较路径集合；完整地图根没有修改、新增或删除。42项隔离检查通过只证明场景/选项求值与当前活动文本，不代表游戏启动、玩法、多人或真实UI全部通过。

工作区有逐图CSV、全部活动菜单数据、英文/术语明细及行号、实际maputil来源和检查前后哈希。后续若实施汉化，只改显示文字，保留key/pref/default和值列表顺序；先备份、核对脚本消费者，按用户此前要求严格升版，并只在确认同一维护副本后同步。当前仅检查，无地图修订变化。
