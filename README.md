# FACN-Maps｜SCFA 地图修复知识库

本仓库用于沉淀 **Steam 原版《Supreme Commander: Forged Alliance》（SCFA）** 地图修复、FAF → Steam 兼容迁移、可选玩法扩展、重复地图去重与测试记录，供 FACN 地图中心及 Codex 长期维护。

> **当前状态：已建立维护文档，尚未上传或验收地图文件。** 文档中的“发现”来自对用户提供的 `04槽位.zip` 的静态检查；**不是游戏运行测试结论**。以前归档的 GPT 修复记录目前未取回完整源码，不能当作经过验证的事实。

## 给 Codex 的入口

**先阅读仓库根目录 [AGENTS.md](AGENTS.md)**，再按任务查阅：

| 文件 | 内容 |
| --- | --- |
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