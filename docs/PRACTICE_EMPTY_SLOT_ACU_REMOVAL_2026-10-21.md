# Practice空槽主指挥官补发删除（2026-10-21）

> 当前统一要求见[用户要求与执行约定](USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)。本页按其标题记录当时的检查/部署阶段；后续明确取舍优先，不使用历史菜单总数、版本或“原赠送相加”方案覆盖当前安装状态。

用户截图要求删除“生存：第一/二/三/四名指挥官阵营”。已追踪证明：这些不是玩家排名，也不是SCU，而是在Survival_InitGame中把空槽的主ACU补发给实际玩家，4人齐全不补、少人时补足4台。正常玩家主ACU由OnPopulate的ScenarioUtils.InitializeArmies生成，与这段补发不同。

已向用户列出两种处理方式。用户明确选择1：“删除四项及空槽补发，只保留正常玩家主指挥官和现有额外单位设置”。因此不是按名称相似误删，也不是沿用上一轮“功能不同保留”默认结论。

## 已落实

- options中删opt_Survival_Commander_One/Two/Three/Four_Faction四定义。
- script中删四个firstChoices、四个nil默认块、缺槽发现/轮流分配/固定补位坐标/factionsList/factionSelections及CreateUnitHPR补发代码。
- 删除人数缩放帮助中“额外补发的指挥官不计为新增玩家”失效句子，保留固定4人/已占槽缩放逻辑、默认值、目标生命/回血/能量公式。
- 正常InitializeArmies、准备时间、波次、目标和工厂创建、胜负、现有FACN额外SCU/工程师五项保留。原补发不是新数量的一部分；用户选择后少人不再自动获赠其它空槽的主ACU。

仅安装Practice的options/script两文件写入，菜单13→9，总生存菜单394→390；652其它自定义文件SHA保持，本阶段scenario/name/map_version不改，实际修订仍12。随后用户另行授权名称清理，Practice.name去掉v9，是下一阶段独立变更，不能因此说本阶段改了版本号。维护包62图及其中Practice仍原版本，未同步。

## 检查与备份

备份Practice完整10文件：Practice空槽指挥官删除_20261021/修改前Practice完整备份.zip，SHA `78e7fec39e4876b6a8eb63df1c37cb3616e123be40182e48195861f5c3877d68`。2份旧Lua语法、候选和落盘各2用例通过：真实maputil/dataInit无库空环境菜单；完整实际主脚本执行32组合（16占槽子集×2缩放模式），旧缓存四键存在仍无补发，0人分支不报错，人数缩放和720秒准备保持，原目标/工厂/波次初始化调用保留，现有独立SCU/工程师调用保留。InitializeArmies/地图引擎/地形为测试替身，不能说实机ACU放置通过。

状态：已修改待实测；尚未真实少人开局、多人、碰撞/寻路、完整胜负与后期测试。证据含部署计划、全部差异、语法结果、候选/落盘检查结果及最终核验.json。
