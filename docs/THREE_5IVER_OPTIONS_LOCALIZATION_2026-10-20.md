# 三张安装地图高级设置汉化与升版（2026-10-20）

用户在前次核对后明确要求“这三个地图先汉化一下，版本号记得升一级”。本次只处理E:/SCFA/maps下指定三份安装副本的高级设置，并各将ScenarioInfo.map_version加1。没有替换为维护包的近似同名图，没有改官方地图、游戏SCD、其他自定义地图、玩法脚本或维护包62张清单。

| 安装目录 | 大厅显示名 | 修订变化 | 选项数 |
| --- | --- | --- | ---: |
| 5iver Survival Land | 5iver Survival Land | 1→2 | 23 |
| 5iver Survival Land Naval | 5iver Survival LandNaval | 1→2 | 25 |
| 5iver_survival_landnaval-swarm | 5iver_survival_landnaval-swarm | 11→12 | 7 |

共55项高级设置，296个原显示字段汉化，并为6个最高守备组合补充完整中文说明。覆盖选项标题、帮助、下拉条目；数字、时间、星号标记保留。后台key/pref/default、数值表达式、重复key、条目顺序完整保留。原有“70/60显示但key同为50”等独立问题未在语言任务中改数值，汉化不等于修复全部玩法选项。

## 文字处理

- 开局暂停、胜利条件、防守目标、总部通讯、预设、难度、毁门生成实验级单位、单位上限、目标启动/生命恢复等均改为中文。
- 科技巅峰时间、单位/人/分钟、生命加成、老练度区分；Land Naval增加的海军项目分别翻译，未漏项。
- 地面炮、防空导弹、护盾、反核、反战术导弹、二级火炮分别解释；保留两图守备组合的真实文字差别，没有把Land的8座二级炮套到Naval。原长组合用短中文保留数量，并在帮助中展开。
- 全敌军胜利条目缩为“清除传送门及全部敌军”，仅拆门条目仍为“摧毁全部传送门”。本机原版下拉框宽240，参考14px字体测量原长译文约286宽，故收短；没有声称实际UI显示已验证。
- `*`保留作者原标记，不新增“默认”断言；原菜单default及重复首项保留。顶层version字段、地图显示名、目录和内部资源路径保持，仅修改map_version。

## 实际修改6文件

每个目录只改对应的`*_options.lua`和`*_scenario.lua`：

- `E:/SCFA/maps/5iver Survival Land/5iver Survival Land_options.lua`
- `E:/SCFA/maps/5iver Survival Land/5iver Survival Land_scenario.lua`
- `E:/SCFA/maps/5iver Survival Land Naval/5iver Survival Land Naval_options.lua`
- `E:/SCFA/maps/5iver Survival Land Naval/5iver Survival Land Naval_scenario.lua`
- `E:/SCFA/maps/5iver_survival_landnaval-swarm/5iver_survival_landnaval-swarm_options.lua`
- `E:/SCFA/maps/5iver_survival_landnaval-swarm/5iver_survival_landnaval-swarm_scenario.lua`

`*_script.lua`、save、SCMAP、预览、作者玩法说明文档均未改；没有往地图目录放备份或新增文件。

## 备份与验证

部署前完整备份三图26个文件及原SHA清单，在工作区`三张5iver高级设置汉化_20261020/汉化前3张完整地图备份.zip`；ZIP完整性和26个原文件SHA逐个通过。后续字体长度收短继续使用该不可变原始备份。

本机LuaPlus_1081.dll完成9项候选检查：6文件语法加载、3图原/新选项去除显示字段后深度相等；实际求值比较包括60/60、5/60等数值表达式、默认值、重复项与顺序。所有label/help/text字段不残留英文字母；三图场景深度比较仅map_version变化，顶层version、名称、路径和军队配置不变。

部署后重新读取实际落盘字节，3项场景/选项求值通过，实际修订为2/2/12，选项仍23/25/7。整个E:/SCFA/maps与前次960文件基线对比：路径集合一致，只有上述6文件SHA改变，其余954保持，包括61张官方地图文件和目标图全部玩法/地形资产。没有新增/删除地图文件。

上述为源文件、目标Lua与数据一致性验证；未游戏实测、未实际点击菜单或多人测试。需要关闭旧地图选择界面后重新选择对应新版；旧运行局不会热更新。汉化成功不代表已确认三图全部模组依赖、平衡或脚本功能。

## 与维护包及审计的关系

前次[中文核对](INSTALLED_ADVANCED_OPTIONS_CHINESE_AUDIT_2026-10-20.md)的“3张英文”是汉化前快照，本次这三份已处理。当前42自定义中34份有自带高级设置的地图均为主体中文，8份无自带；Grand Barrens的Boss等少量术语和共享模组界面不在本次范围。

维护包ID42的`08槽位/5iver_survival_landnaval`也是修订2，但不是本次`5iver Survival Land Naval`目录，不因版本数字相等就当作文件相同。本次没有改62张维护包清单、累计维护图数或上传云端。

工作区保存原/新296字段映射、部署计划/原SHA/新SHA、9+3检查结果和960文件变化核对。知识库只收文档和本次摘要，不上传游戏地图资产。
