# FACN-Maps｜SCFA 地图修复知识库

本仓库用于沉淀 **Steam 原版《Supreme Commander: Forged Alliance》（SCFA）** 地图修复、FAF → Steam 兼容迁移、可选玩法扩展、重复地图去重与测试记录，供 FACN 地图中心及 Codex 长期维护。

> **当前状态：知识库包含历史ZIP审计、本机83张复核及71张整合记录；地图源码/资源未上传本仓库。** 本轮23张修改图均为“已修改待实测”，不是Steam游戏运行通过。以前未取回完整源码的GPT记录仍不能当作已验证事实。

## 当前研究范围

**只研究 AI 如何检查、修复已有地图及按需增加地图内高级设置（工程师/ACU/SACU、种族、数量等）**。当前不开发地图修复软件，也不实施 AI 生成地图。Steam 原版为主要验收目标；FAF 作为独立兼容环境和公开源码参考。研究教程不代表任何地图已经实机验证。

## 给 Codex 的入口

**先阅读仓库根目录 [AGENTS.md](AGENTS.md)**，再按任务查阅：

| 文件 | 内容 |
| --- | --- |
| [docs/AI_REPAIR_PLAYBOOK.md](docs/AI_REPAIR_PLAYBOOK.md) | **AI 修图任务入口**：地图诊断、最小补丁、验证与回滚步骤 |
| [docs/ADVANCED_OPTIONS_REPAIR_GUIDE.md](docs/ADVANCED_OPTIONS_REPAIR_GUIDE.md) | **高级设置实操教程**：额外工程师/指挥官、种族/数量、默认及胜负问题 |
| [docs/API_EVIDENCE_MATRIX.md](docs/API_EVIDENCE_MATRIX.md) | Lua/API 调用证据、Steam/FAF 适用范围及核对清单 |
| [docs/COMMUNITY_REPAIR_CASES.md](docs/COMMUNITY_REPAIR_CASES.md) | Github 编辑器 Issues 与作者故障案例、候选修复方法 |
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

## 最新：71张整合与内容中心版本（2026-10-16）

按用户明确取舍完成83→71张，12张旧版已归档后从活动包删除，23张修订号与显示名同步提高。Horde保留万古可选波次，黑日保留固定生命选项，practice保留人数缩放，Escape保留稳健路点识别。

- [实际保留、舍弃、升版与验证报告](docs/CONSOLIDATION_2026-10-16.md)
- [71张当前元数据、23张版本对照、73文件变化与哈希](docs/data/survival_consolidation_2026-10-16.json)

未进行Steam实机或多人测试，也未上传发布地图；上面的83张记录保留为整合前来源。
