# GitHub / 社区地图修复问题案例索引

> 范围：从社区作者实际公开的 issue、源码和修订说明中提取**可复用故障排查方法**，不等于本仓库地图出现同样故障，更不等于已修复。Issue 开/关状态会变化，以链接打开时为准。调查记录整理于 2026-10-15。

## 1. 已公开的编辑器/地图故障及排查顺序

| 案例（链接） | 作者报告的确切现象 | 修复技术 / 回归要点 |
|---|---|---|
| [FAForeverMapEditor #114：原版地图重存加载失败](https://github.com/FAForever/FAForeverMapEditor/issues/114) | 打开 Steam+FAF 的原版 `SCMP_021` 时贴花显示异常；另存后编辑器崩溃、重命名版在游戏找不到（报告未关闭） | 先保留原始 `.scmap`，比对新旧 binary、scenario 路径、资源引用、编辑器日志；不能把“保存完成”当成地图可玩 |
| [#112：Effect marker 保存错误](https://github.com/FAForever/FAForeverMapEditor/issues/112) | 编辑器存档把 `EffectTemplate` 写为空字符串，游戏 `BeginSessionEffects` 报未定义全局名（报告未关闭） | 检查 `_save.lua` 的 effect 标记模板字段；对照有效 `EffectTemplates.lua` 名称；只修字段，在重新用编辑器保存后再复核 |
| [#79：水面坡道/波浪贴图路径](https://github.com/FAForever/FAForeverMapEditor/issues/79) | 另存新地图版本/目录后，water ramp 和 wave 纹理仍指向旧位置（报告已关闭） | 更新实际内嵌水纹引用，和其它自定义层纹理区别核查；比较两个版本的水面效果 |
| [#101：地形类型存储不稳定](https://github.com/FAForever/FAForeverMapEditor/issues/101) | 地形类型图层绘制并保存后，重新打开有随机区域缺失（报告未关闭） | 比较保存前后的 terrain-type 数据，保存后再打开校验；不要无意重存既有地形 |
| [#69：无 Alpha DDS 贴图](https://github.com/FAForever/FAForeverMapEditor/issues/69) | 编辑器无法正确处理某些不含 Alpha 通道的 DDS，包括未压缩或 BC1（报告未关闭） | 先识别 DDS 格式和可用解码器，再确认具体失败条件；优先恢复未修改素材，不机械转码全部图片 |
| [#102：贴图路径格式不一致](https://github.com/FAForever/FAForeverMapEditor/issues/102) | layer texture 和 water ramp 路径的开头斜杠约定不同（报告未关闭） | 对每种资源引用按其读取器规则验证；不要把所有路径统一改成相同斜杠形式 |
| [#109：贴花镜像错误](https://github.com/FAForever/FAForeverMapEditor/issues/109) | X 对称处理后部分 decals 朝向/镜像不正确 | 不要在无地形改造需求时运行镜像/旋转；必须做就逐区域对照 |
| [Neroxis #368：宏观纹理缺失](https://github.com/FAForever/Neroxis-Map-Generator/issues/368) | 部分 biome 丢失 macrotexture，雪地外观明显变化 | 只作为贴图层结构与视觉比对研究；用户目前不需要地图生成器 |
| [Neroxis #376：80km 内存问题](https://github.com/FAForever/Neroxis-Map-Generator/issues/376) | 社区报告较大地图处理时内存不足 | 大地图格式/编辑场景谨慎处理；不是建议现在开发生成器 |

处理上述问题的一般原则：找到**第一条错误日志 → 对应文件/行号 → 读取目标版本资源定义 → 在副本修最小变化 → 前后对比 → 实机验证**。编辑器“已修复”与地图兼容成功是不同事情。

## 2. 社区地图作者的实用经验

### Survival Versus

[项目源码/README](https://github.com/SupremeCommanderMaps/SurvivalVersus)

- README 明确提醒：**两位玩家哪怕地图显示版本一致，只要实际源码不同，也可能不同步**。联机应比较完整地图文件，而非只看地图版本显示。
- 项目依赖 `vendor` 外置/引入内容（文档有将 `lib` 放入 `vendor` 的步骤），因此检查脚本主文件还不够。
- 历史更新包括仅单队游戏结束检测、不同阵营/队伍胜负规则、自动回收、生存波次难度等；说明“地图可进入”与“胜负正确”要分开测试。
- **修复方法**：完整依赖图 + 测试 1 队/2 队、ACU 全灭、主动离开、最后一波、游戏结束事件。

### Genesis of the Order Survival

[源码及版本变更记录](https://github.com/SupremeCommanderMaps/Genesis_of_the_Order_Survival)

- 作者更新日志记录：曾修复后期 `ForkThread` 故障引发的延迟、单位不前进、Boss 与胜利/目标联动、仅给活跃玩家发放增援等问题。
- `GameSetup.lua` 把玩家军队和敌方军队分开，并在初始化中调用额外单位功能；
- `Utilities/AllFactions.lua` 用四族蓝图映射、Army Brain、出生点在 sim 中生成额外单位。
- **修复方法**：线程入口唯一、周期有等待和退出条件；确认活跃玩家，区别目标死亡与 ACU 死亡；检查全部阵营与波次后期性能。
- **高级设置教程**：见 [ADVANCED_OPTIONS_REPAIR_GUIDE.md](ADVANCED_OPTIONS_REPAIR_GUIDE.md)。

### Survival 5th Dimension Center EE

[实际菜单选项](https://github.com/SupremeCommanderMaps/Survival5thDimensionCenterEE/blob/master/survival_5th_dimension_center_ee_options.lua)

- `opt_CenterAllFactions` 明确区分关、给工程师、给 ACU；和 Genesis 中 ACU 数量不同，不能复制“启用”标签就假设单位数量相同。
- 中央目标生命、回复、资源和波次都与具体选项键相连；修改菜单不能忽略波次/胜负关联代码。

### Survival Horde EE

[主脚本](https://github.com/SupremeCommanderMaps/survival_horde_ee/blob/master/survival_horde_ee_script.lua) · [scenario](https://github.com/SupremeCommanderMaps/survival_horde_ee/blob/master/survival_horde_ee_scenario.lua)

- 固定虚拟路径 `/maps/survival_horde_ee.v0021/src/` 与 `vendor/EntropyLib`，重命名/版本迁移是常见问题。
- 本仓库历史审计证实 Horde EE 与 Aeon Fixed 不仅要看 `_script.lua`，还要配对核对不同 `WaveTable` 和 `WaveOrders`。不要凭相同 `.scmap` 或主脚本删另一个版本。

## 3. 地图格式与教程

- [FAF Mapping Guidelines / 文件结构与版本迁移](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md)：`.scmap` 包含纹理、贴花、物件、skybox 等；`_scenario.lua` 包含路径与玩家；`_save.lua` 包含 markers/军队；`_script.lua` 包含启动逻辑。
- 官方指南指出 FAF Editor 可读存 `v56/v60`；GPG Editor 仅 `v56`，重存降格式可能丢 skybox 等内容。**这不是 Steam 与 FAF 的一一对应编码**。
- [Adaptive Maps 开源教程（仅供 FAF 参考）](https://github.com/CookieNoob/Adaptive-Maps-forged-alliance)：自定义选项与 `_tables.lua` 绑定、`AdaptiveMap` 标志及地图更名路径处理。其成功经验不能自动推出 Steam 大厅原生支持。
- [FAForever/fa](https://github.com/FAForever/fa) 是 FAF 的游戏 Lua 参考；Steam 是否存在对应定义，仍以目标 Steam 安装和实机为准。

## 4. 未来由 AI 增加案例的标准

1. 引用原 issue/commit/PR、作者/仓库、源码路径；备注检索日期与报告状态。
2. 写明触发版本、准确现象和可复现步骤，不只写“贴图问题/地图坏了”。
3. 区分**外部报告**、**本地图静态确认**、**候选已改待实测**与**实机成功**；不能将外部 bug 自动套到不同文件。
4. 将根因与候选修法挂钩，并记录可能造成的资源/玩法损失。
5. 若是可复用 API，更新 [API_EVIDENCE_MATRIX.md](API_EVIDENCE_MATRIX.md)；若是可复用选项，更新 [FEATURE_LIBRARY.md](FEATURE_LIBRARY.md) 与 [ADVANCED_OPTIONS_REPAIR_GUIDE.md](ADVANCED_OPTIONS_REPAIR_GUIDE.md)；若有新测试陷阱，更新 [TEST_AND_RELEASE.md](TEST_AND_RELEASE.md)。
6. 保存原始地图/代码快照及哈希，不未经许可复制、二次发布第三方资源。

**故障研究和教程优先服务已有地图修复；本仓库不把 AI 自动生成地图作为当前任务。**
