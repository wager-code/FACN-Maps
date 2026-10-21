# FACN-Maps｜SCFA 地图修复知识库

本仓库用于沉淀 **Steam 原版《Supreme Commander: Forged Alliance》（SCFA）** 地图修复、FAF → Steam 兼容迁移、可选玩法扩展、重复地图去重与测试记录，供 FACN 地图中心及 Codex 长期维护。

> **当前状态见 [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md)。** 当前维护包保留62张，按2026-10-20记录累计29张地图有维护修改；另有35张用户本机安装地图，当前菜单条目统计390项。两套对象彼此独立。地图源码/资源未全部上传本仓库，不能把静态或隔离测试说成Steam游戏、多人或发布通过。

## 最新用户要求与安装地图记录（2026-10-21）

后续维护先读[生存地图用户要求与执行约定](docs/USER_REQUIREMENTS_SURVIVAL_MAPS_2026-10-21.md)：原设置保护、按生成链去重、复用准备时间并统一m:ss、独立SCU/工程师、指定地图单主ACU、名称隐藏版本，以及仅改地图文件解决发布预检。

该页区分早期方案和后续明确取舍，并索引本轮专项。安装地图与仓库维护包的数量、菜单统计和总体验收状态统一查看 [CURRENT_STATE.md](docs/CURRENT_STATE.md)；具体单图状态以对应最新专项为准。下方历史记录不能覆盖当前状态页。

## 给 Codex 的入口

**先阅读仓库根目录 [AGENTS.md](AGENTS.md)**，再按任务查阅：

| 文件 | 内容 |
| --- | --- |
| [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) | **全局当前状态唯一入口**：维护包/安装地图数量、统计口径、验证状态与已知限制 |
| [docs/STEAM_FA_COMPATIBILITY.md](docs/STEAM_FA_COMPATIBILITY.md) | Steam/FAF 兼容差异、Lua 接口核对顺序、已知风险与修复方案 |
| [docs/FEATURE_LIBRARY.md](docs/FEATURE_LIBRARY.md) | 工程师、额外指挥官、阵营、难度、刷怪等选项的真实参考位置 |
| [docs/KNOWN_MAP_FINDINGS.md](docs/KNOWN_MAP_FINDINGS.md) | 当前压缩包已发现的问题、重复地形分组与优先级 |
| [docs/TEST_AND_RELEASE.md](docs/TEST_AND_RELEASE.md) | Steam 实机验收、多人同步、日志、发布和回滚检查 |
| [docs/MAINTENANCE_LOG.md](docs/MAINTENANCE_LOG.md) | Codex 以后发现问题、修复问题时持续更新的记录 |

## 固定原则

1. Steam 原版正常运行优先；不能用 FAF 能运行冒充 Steam 兼容。
2. **不删除原玩法、不凭同一张 `.scmap` 就删除地图。** 相同地形可能搭配不同脚本、阵营、波次、胜利条件。
3. 游戏是否启动、选项是否显示、选项是否真正生效、单人/多人是否稳定，分别验证。
4. **保留原始素材，先在单独分支修复，再测试、审阅与发布。**
5. 每次修复必须同步更新已知问题和维护日志，记录“证据位置 → 改动 → 验证 → 剩余风险”。

## 建议的未来布局

```text
AGENTS.md
README.md
docs/
  CURRENT_STATE.md
  STEAM_FA_COMPATIBILITY.md
  FEATURE_LIBRARY.md
  KNOWN_MAP_FINDINGS.md
  TEST_AND_RELEASE.md
  MAINTENANCE_LOG.md
maps/                # 未来可选：经审核的地图资源（须检查授权与体积）
```

### 参考资料

- [FAForever 地图版本处理指南](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md)：Scenario/Save/Script、地图路径、玩家与额外军队。
- [FAF Lua 源码](https://github.com/FAForever/fa)：**仅用于差异参考，不能当作 Steam 原版 API 的直接证明。**
- Steam 本机安装目录下的 `gamedata/*.scd` 及实际游戏日志才是目标环境最终依据。

文档内容是维护规范而非自动修复程序。Codex 在有本仓库写权限的工作区中应按 `AGENTS.md` 更新并提交记录。

## 2026-10-16 本地复核增量

本次读取了用户本地当前83张生存地图，源码与资源未上传本仓库；静态审计不代表Steam实机通过。已记录11张完整玩法需模组、14张FAF单位差异、15组预览/地形/玩法比较。11张仅移动分类，2522个文件哈希保持。

- [逐图依赖发现与证据](docs/KNOWN_MAP_FINDINGS.md)
- [无模组迁移方法与明确损失](docs/VANILLA_MIGRATION.md)
- [相同图片和不同版本保留建议](docs/SURVIVAL_AUDIT_2026-10-16.md)
- [可复现摘要、源文件哈希和路径](docs/data/survival_audit_2026-10-16.json)
- [测试与发布](docs/TEST_AND_RELEASE.md) · [维护日志](docs/MAINTENANCE_LOG.md)

15张局部候选通过编译和数据核验但未写回原图，仍需单人、后期波次、模型/武器和多人实测。Swarm/Eternals及DDDX RPG不能靠替换几个单位保留完整原模式。

## 历史阶段：71张整合与内容中心版本（2026-10-16）

按用户明确取舍完成83→71张，12张旧版已归档后从活动包删除，23张修订号与显示名同步提高。Horde保留万古可选波次，黑日保留固定生命选项，practice保留人数缩放，Escape保留稳健路点识别。

- [实际保留、舍弃、升版与验证报告](docs/CONSOLIDATION_2026-10-16.md)
- [71张当前元数据、23张版本对照、73文件变化与哈希](docs/data/survival_consolidation_2026-10-16.json)

未进行Steam实机或多人测试，也未上传发布地图；上面的83张记录保留为整合前来源。

## 历史操作：删除9张确认依赖专用模组的地图，维护包保留62张（2026-10-16）

用户明确表示模组无法取得，要求删除确认依赖专用模组的地图。已先备份当前版本，再删除9张；当前普通槽位52张、依赖与资源待测试10张，专用模组0张。保留图2228文件与版本未改，仍未游戏实测；不能据此宣称62张全部通过纯原版。历史23张修改图中3D v89已删除，当前保留22张修改图。

- [删除清单、依据与恢复记录](docs/MOD_MAP_REMOVAL_2026-10-16.md)
- [9张原文件哈希与删除后验证数据](docs/data/mod_map_removal_2026-10-16.json)


## 当前代码研究与AI制图参考（62张）

- [62张玩法和代码地图册，逐图维护卡片](docs/SURVIVAL_CODE_ATLAS_2026-10-16.md)
- [9张明确代码修正、版本和验证](docs/CODE_MAINTENANCE_2026-10-16.md)
- [AI能制作什么、如何分别面向Steam/FAF](docs/AI_MAP_AUTHORING.md)
- [网上和GitHub作者记录的问题与状态](docs/EXTERNAL_MAPPING_RESEARCH_2026-10-16.md)
- [只读依赖/资源/哈希扫描工具](tools/scan_scfa_maps.py)

627份Lua/字节码中622编译通过、5份辅助/备用异常明示；62份地图数据通过，25张75个首波隔离用例通过。截至2026-10-20，累计29张地图有维护修改；全局统计口径见 [CURRENT_STATE](docs/CURRENT_STATE.md)。无Steam/FAF实机或多人结果，不将地图全部称作兼容通过；仓库没有上传原图源码和素材。

## Fort Ictus最新调查（2026-10-18）

[特殊第4槽与玩法冲突](docs/FORT_ICTUS_GAMEPLAY_2026-10-18.md) · [中途结束空白结算](docs/FORT_ICTUS_SCORE_INVESTIGATION_2026-10-18.md)。第4槽带396条预置记录，不能按普通4人合作直接修复；活动图仍v9，候选未部署，游戏根因及结算仍待日志。

## Fort Ictus恢复续办（2026-10-19）

[最新核验、测试及缺失条件](docs/FORT_ICTUS_RECOVERY_2026-10-19.md)：活动包v9未改；原安装图和原启动入口缺失、没有本局日志，不安装候选或猜测根因。新增只读日志工具：`python tools/inspect_scfa_log.py <游戏.log> --out <新的诊断.json>`；拒绝覆盖源文件，输出错误上下文仍须人工判断。

## 地图目录名与版本号分开管理（2026-10-19）

为了让用户能根据游戏地图列表直接找到数百张地图的本地文件夹，统一采用以下规则：

- 文件夹名与场景配置中的基础显示名 `name` 保持一致。
- 如果名称末尾的 `v6` 等只是版本标记，从文件夹名和基础显示名中移除；版本由场景配置的 `map_version` 字段记录，游戏会单独显示 `Version: N`。
- 重命名前先备份，检查重名，并审计 `map`、`save`、`script`、`import()` 和硬编码目录路径；不要无必要地改内部地图文件名。
- 如果版本尾缀的含义不确定，或重命名会造成目录冲突，先停下来核对，不要猜测或覆盖。
- 重命名后必须做路径静态检查，并实际加载一次。原始地图已能运行，不代表重命名后的路径也一定正确。

示例：`survival_5thdimension` 是文件夹名和基础显示名；若原名称中的 `v6` 确认表示第 6 版，则用 `map_version` 表达版本，不再把 `v6` 拼进地图名。实际版本值仍须核对来源历史，并遵守本仓库的升版规则。
### Fort Ictus Survival：FAF v8 → Steam 迁移审计

新收到的 v8 源包与仓库当前维护版 v9 并不相同。已记录 FAF 单位依赖、无效类别风险、版本/目录差异和后续回归范围；详见 [Fort Ictus v8 静态审计](docs/FORT_ICTUS_FAF_V8_STEAM_AUDIT_2026-10-19.md)。修复必须基于最新 v9，不从旧 v8 覆盖已有修改；目前没有新的 Steam 实机通过记录。
### Fort Ictus Steam 测试候选（非正式发布）

基于当前上传的 v8 单独生成了 `Fort_Ictus_Survival_Steam_Candidate_v11.zip`，并未覆盖当前维护版 v9。候选修复了 13 个活动 FAF 单位引用，并为缺失类别调用增加 guard；地形未改，Steam 实机仍待测。详细证据、SHA-256 和限制见 [专项审计报告](docs/FORT_ICTUS_FAF_V8_STEAM_AUDIT_2026-10-19.md)。

## 官方教程共享地形发布分析（2026-10-19）

[X1CA_TUT与内容中心上传限制](docs/X1CA_TUT_PUBLICATION_2026-10-19.md)：官方教程4文件与Steam一致，复用SCMP_019地形，不能把跨目录依赖当作地图损坏。说明内置依赖/完整合包/独立副本三种路线，区分格式version=3和未声明map_version；原图未改、内容中心未改。
## Fort Ictus v10 Steam 修复候选（2026-10-19）

已基于用户本机 v9 包发现并记录炮兵 marker 拼写问题：save 使用 SURVIVAL_ATY_1..4，script 读取 SURVIVAL_ARTY_。v10 候选还统一地图文件夹/基础显示名、版本字段、场景路径、选项默认值，并修复联盟判断变量与空列表保护。静态检查通过，Steam 实机尚未验证。详见 [修复报告](docs/FORT_ICTUS_V10_STEAM_REPAIR_2026-10-19.md)。
