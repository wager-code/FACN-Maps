# Brainsucka：上传误报与专用模组依赖（2026-10-20）

## 两个独立结论

1. 安装副本 `E:/SCFA/maps/5iver Survival Brainsucka/` 的 scenario 引用真实存在，8文件与2026-10-15专项逐一SHA-256相同。上传提示“引用文件不存在”是内容中心的后缀限制误报，不是地图丢失存档。
2. 同一份主字节码确实强制检测专用模组。修复上传预检不能令地图成为原版独立生存图。此前卡片“未发现强制专用模组证据”漏掉了OnStart分支，现予纠正；保留62张不等于62张全部无强制依赖。未新增删除、移动或地图修改。

## 文件、运行时与证据

scenario 的 `map/save/script` 三条路径均指向本目录真实文件；其中 save/script 为 `_save.luac` 和 `_script.luac`，另有 `Functions.luac`、`Hooks.luac`。不要改扩展名、造空白save或重新拼地形来绕过预检。

| 文件 | SHA-256 |
| --- | --- |
| 主脚本 | `5196bac19638740a1ec05bfba485e9e9eeb36056982ee170a88d88de79388146` |
| 存档字节码 | `45cdcaaf16fc02924fd50d6ed12177264cd3f2753ff88add483e0434e65cffc9` |
| scenario | `311a0b161b886d41a8068472f28b636bb80016f4a6f103ad4278f062ec4e0989` |
| SCMAP | `b7055fccdea0056b108d485bb3857f946213bd3711676acff331c4a72b37511f` |

使用本机32位 `LuaPlus_1081.dll`（SHA-256 `54167a0d72df75a06109879a9e3eb95bd5e83d1e07dd7c0d6156f05ca0835e28`）完成8项隔离检查：6文件加载、实际存档数据求值（540标记、9军队）及实际OnStart依赖分支夹具。不是普通Lua 5.4检查，也没有反编译出可维护源码。

专用模组UID：`d36d33e5-3927-499f-8990-55555b000001`。原始字节码内要求 `The 5iver Survival Brainsucka mod`。缺少UID时仅排队缺模组提示，不调用setupGame或SetupMission1；提示线程又在原源码163行调用缺失全局CreateDialogue。夹具提供该UID后才进入任务初始化分支。该UID仅是测试输入，不能冒充真实模组；setupGame/SetupMission1使用记录桩，未完成游戏模拟。

2026-10-15专项曾在安装/玩家模组目录和偏好中查找而未找到；2026-10-20没有重新证明所有模组目录仍缺少该包。脚本还有专用单位和音效引用，关闭检测不能补齐内容。没有足够源码和模组资产制作可靠的去模组版，不能报告“已兼容原版”。

## FACN源码的实际原因与修复

[客户端LocalContentService](https://github.com/wager-code/FACN/blob/main/src/SCFA.ContentCenter/Services/LocalContentService.cs)和[发布网关PackageValidator](https://github.com/wager-code/FACN/blob/main/server/SCFA.PublicationGateway/PackageValidator.cs)原先只接受 `_save.lua` / `_script.lua`；客户端还把后缀不符与真实缺失合并报错。PublicationPreparationService的文件枚举本身不排除luac。

修复两端为接受lua/luac，保留相同目录、引用归属、文件存在、ZIP、哈希、身份和版本保护；客户端分开提示文件缺失与现存但格式不支持。内容中心不执行地图Lua或字节码，也不保证任意luac的目标引擎兼容性。

FACN源码提交：[bd643ef](https://github.com/wager-code/FACN/commit/bd643efbb66cf369e0eea5eb1759ab4ef8cdd684)。

隔离的GitHub基线加本次修复：核心476项、网关65项通过；实际地图及混合/大写扩展名打包专项45项通过。实际地图ZIP全部8文件逐项SHA一致，四份字节码没有漏收，源目录内容指纹保持。异常跨图/越界/缺失引用及现存错误扩展名均拒绝。当前源码修复与正式EXE替换、真实网关部署、云端地图发布分别记录，未声称后者完成。

## 维修和发布边界

- 发布结构通过不代表可玩性、零模组依赖或多人同步通过。
- 未修改地图文件、map_version（仍1）、游戏设置或模组；未删除或归档本图。
- 若日后获得原模组或源码，先核对UID、单位/音效和初始化链，再验证首波、胜负、退出及多人；逐项报告去模组改编损失。
- 本地证据为工作区 `Brainsucka上传预检核对_20261020/` 和FACN项目 `artifacts/compiled-map-20261020/`；不上传原地图字节码、玩家配置或详细日志。

返回[地图卡片](maps/04.md) · [代码地图册](SURVIVAL_CODE_ATLAS_2026-10-16.md)。
