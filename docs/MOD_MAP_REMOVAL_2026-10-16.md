# 专用模组地图删除记录

2026-10-16。用户明确要求：“需要专用模组的 都删掉吧，模组我们也找不到的了”。

## 当前地图包

- 已删除确认需要专用模组才能完整运行的9张，地图包由71张减至 **62张**。
- 普通槽位52张，`待测试_依赖与资源核对`10张，专用模组图0张；`需专用模组`目录一并移除。
- 原83张先整合淘汰12张，再删除本次9张，累计移除21张。先前升版23张中有1张（3D v89）本次删除，当前保留22张修改图。
- 其余62张地图的全部文件、版本号保持不变；本次只删除地图并更新索引/说明，没有再修订地图，不额外升版。
- 62张仍包含依赖、资源和实际运行待核查项，不能当作全部通过纯原版游戏实测。疑似外置模式的线索未自动按确证删除。

## 本次删除的9张

| 地图 | 已记录依赖 | 删除前目录 |
| --- | --- | --- |
| Survival_5.thD_MayhemEdition | Total Mayhem v1.35 | `需专用模组/06槽位/survival_5.thd_mayhemedition` |
| survival_voodoo_double | Extreme Wars + Some Mods 2.1（作者原要求，历史版本未重新取得） | `需专用模组/08槽位/survival_voodoo_double` |
| eternals survival dimension | Mayhem Eternals Survival（模组提供生存玩法） | `需专用模组/09槽位/eternals_survival_dimension` |
| swarm survival mk4 | Swarm Survival（模组提供生存玩法） | `需专用模组/09槽位/swarm_survival_mk4` |
| swarm survival 10 players | Swarm Survival（模组提供生存玩法） | `需专用模组/11槽位/swarm_survival_10_players` |
| Survival Unit Mayhem | Total Mayhem v1.35 | `需专用模组/04槽位/survival_unit_mayhem` |
| Survival Beach Ramp Mayhem | Total Mayhem v1.35 | `需专用模组/06槽位/survival_beach_ramp_mayhem` |
| DDDX RPG survival | Survival Mayhem&BO Balance + Total Mayhem + BlackOps Unleashed；BlackOps ACUs 仅需安装 | `需专用模组/07槽位/dddx_rpg_survival` |
| Survival_Mayhem&BO_3D v89 | Total Mayhem v1.36 + BlackOps Unleashed v14；Balance 推荐且部分功能需要 | `需专用模组/07槽位/survival_mayhem&bo_3d` |

上述整张地图及其独立玩法从活动包删除，未移植其模组专属单位、技能、波次或模式。Eternals/Swarm即使地形可进入，缺少模组仍没有完整生存玩法；本次不以清空脚本冒充去模组修复。

## 备份与核验

- 删除前对照71张当前分类清单，逐文件核验SHA-256；先备份当前9张及模组区说明，共68文件（其中地图67文件），ZIP逐项解压读回核验通过。
- 当前版本备份：`<本地工作区>\专用模组地图删除_20261016\删除前9张专用模组地图备份.zip`。
- ZIP SHA-256：`91c6189bc5d8279a6c337d622714b1951aca708621c53cc36f958887e6bb34b8`。
- 以前的83张原始地图备份继续保留；本次额外备份包含整合后的3D v89，不能仅用最早原始ZIP代替。
- 删除前各索引保存在工作区`专用模组地图删除_20261016/删除前索引/`。
- 实际删除执行后需核验：目标目录不存在、62张场景配置与清单完全一致、保留图所有文件哈希未变；结果见`专用模组地图删除执行结果.json`。
- 本次未运行游戏、未多人测试、未安装或上传到内容中心。旧71/83张报告仅为历史来源；旧模组搬移/还原清单不能用于还原本次删除，应按本次备份与清单恢复，避免覆盖后续修改。

执行结果：9张67个地图文件删除完成，专用模组目录不存在；62张2228文件哈希保持，62份场景配置。仅静态/文件核验，未新增游戏测试。
