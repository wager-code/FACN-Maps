# 外部地图问题与版本差异研究

查询日期2026-10-16。只以开发者仓库、作者项目和官方维护文档作为技术依据。Issues状态是查询时快照，不能代替本机复现。部分历史问题已修复；没有向其他作者发消息、提Issue或安装下载模组。

| 原始来源 | 作者/项目记录 | 对本包的用途和边界 |
| --- | --- | --- |
| [FAF #6841](https://github.com/FAForever/fa/issues/6841) | Garanas于2025-06-01用Rainmakers Survival的计时目标复现提示控件生命周期错误；2025-06-09关闭，completed | 本包有同名地图，但未复现该FAF版本问题；检查FAF任务UI回归，不将该补丁照抄Steam。 |
| [FAF #2619](https://github.com/FAForever/fa/issues/2619) | JeroenDeDauw报告运输机内载员击杀未计入质量击杀统计；2024-04-22关闭，completed | Endless等击杀质量计分/自动回收需要验证运输机及载员；不能把关闭记录称当前仍必现，也不能认为Steam已有同一修复。 |
| [FAF #7133](https://github.com/FAForever/fa/issues/7133) | 查询时open；报告地面与水面高度相同时轰炸机地面攻击指令被清除，标记engine | 用于海岸/浅水地图测试矩阵；未证明本包某图触发，不能据此重绘海岸。 |
| [编辑器 #74](https://github.com/ozonexo3/FAForeverMapEditor/issues/74) | ozonexo3报告对称纹理绘制可能偏移1像素，查询时open | AI/编辑器输出需核对真实像素和高度/资源，不因勾选对称就视为对称完成。 |
| [编辑器 #136](https://github.com/ozonexo3/FAForeverMapEditor/issues/136) | badbwoi请求编辑SCMAP中的灯光/波浪资源路径，查询时open | 说明资源路径检查不能只看Lua或可见的地表层，须查二进制内引用。该条是功能请求，不是所有地图贴图故障证明。 |
| [FAF加载器](https://github.com/FAForever/fa/blob/develop/init_shared.lua) | 同时挂载原版安装资源与FAF `.nx2` 扩展包 | 证明两套环境共享基础且挂载不同；支持“逐项判定兼容”，不支持“所有地图绝不互通”。 |
| [FAF引擎注解](https://github.com/FAForever/fa/blob/develop/engine/Sim.lua) | SetIgnorePlayableRect是全局引擎接口 | 本轮修正还额外对照本机Steam二进制及官方战役调用；FAF注解本身不作为Steam可用性的唯一依据。 |
| [FAF地图版本指南](https://github.com/FAForever/wiki-pages/blob/main/faf-version-guidelines.md) | 解释scenario/save/script、SCMAP地形/资源路径及v56/v60 | AI制图应分离二进制格式版本与平台版本；转换格式可能丢失内容，不只改文件名。 |
| [SurvivalVersus](https://github.com/SupremeCommanderMaps/SurvivalVersus) | 作者说明同一显示版本可有不同开发文件，文件不同会desync；玩法代码有Busted/Docker测试及vendor库 | 借鉴数据/逻辑测试与多人文件一致性；代码/库须核对授权与FAF依赖，不直接复制成Steam模板。 |
| [程序化素材工作流](https://github.com/FAForever/fa-automation-procedural-content) | 项目已于2024-06-15归档；组织高度图/蒙版/层纹理/贴花转换 | 作为AI生成地形与素材的流程参考，不能宣称现成全自动制图已经在本项目落地。 |
| [Neroxis生成器](https://github.com/FAForever/Neroxis-Map-Generator) | 用种子生成Supreme Commander地图 | 为以后AI驱动程序化地形提供工程依据；未安装运行该工具，不保证默认资源适配Steam。 |
| [FAF开发环境](https://faforever.github.io/fa/development/development-environment) | 仓库不包含所有原版蓝图/脚本，需实际游戏资源 | GitHub代码搜索不到不能直接判资源不存在；本轮以本机`.scd`索引核实Steam。 |

## 本地能够确认、网上资料不能代替的内容

- Steam本机索引573种单位蓝图；没有提供FAF本机资源清单，因此没有计算两边贴图数量差。
- 62张的常量import/doscript引用在当前包或Steam索引可定位，不包括动态拼接、运行时条件导入及任意字节码行为。
- 对`.scmap`内ASCII资源路径的扫描，发现DDay的`/env/Seraphim II/Props/Floe_prop.bp`和Temple的`/env/Seraphim II/Props/Floe_Floe_specteam.dds`在目标Steam及当前包未找到。未擅自从FAF安装素材、没有用不明替代物重绘地形；仍需完整格式解析和实机画面确认。
- 本轮修正两图错误的模块接口调用、七图偏好键；其他外部问题仅列回归测试，不冒称全部复现或修复。
- 本机未启动FAF，所有“FAF通过”状态保持未验证。两版应分别记录API、单位、贴图、加载器和游戏测试结果。

查询所得文件blob SHA与Issue状态记录在[外部来源元数据](data/external_mapping_sources_2026-10-16.json)。长期复用时应重新查询已变化的源码和Issue状态。
