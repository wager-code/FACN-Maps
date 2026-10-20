# Insane v6：全部主力T3点防、战略反核和战术反导（2026-10-20）

**当前已部署v6，已修改待游戏实测。** 游戏E:/SCFA/maps/Survival_Insane_Beta1与维护包同名副本5→6；用户要求把主力点防换成T3并配齐两种导弹防御。本轮没有停留在建议。

## 实际配置

8门与8台Scathis均配置：8座本机自带XEB2306 T3点防（高难≥7共12座）、8防空（≥4其中4座SAM）、4重盾、1座UEB4302战略反核、2座各阵营战术反导、雷达。每处24/28座，全图384/448守备；反核16座、战术反导32座。上轮8主力沿用各阵营T2、仅高难追加4T3；本轮4套阵营的point条目统一为原生XEB2306，没有引入FAF/专用模组炮塔。战术反导本身为对应T2单位，它与战略反核拦截目标不同，不能互相替代。

反核门处坐标side/forward=(0,-7.5)、雷达移(0,-11.5)；边缘火炮反核放(13.5,0)、原雷达保留。反核原始Skirt3×3但Footprint未完整列出，因此以明确的4×4保守包围模型重新检查，不冒称引擎已补全Footprint。16防区无模型相交/越界，400外侧出生格保持通畅模型。真实碰撞/寻路待实测。

## 本机反核弹药接口：不能按名字猜

- `units.scd/units/UEB4302/UEB4302_unit.bp`：武器AntiNuke，TargetRestrictOnlyAllow='STRATEGIC MISSILE'、CountedProjectile=true、MaxProjectileStorage=7、InitialProjectileStorage=0；未设置NukeWeapon，单位CommandCaps是RULEUCC_SiloBuildTactical。
- `mohodata.scd/lua/sim/weapon.lua:31～49`：初装弹仓通过NukeWeapon标志分发，false时调用GiveTacticalSiloAmmo。因此本图显式调用**GiveTacticalSiloAmmo(7)**正确，不因“战略反核”四字改用GiveNukeSiloAmmo。已在本机Lua隔离执行原AmmoThread分支验证通道，模拟单位对象，不是实射验证。
- `lua.scd/lua/platoon.lua:425～440`：原AntiNukeAI用SetAutoMode(true)开启自动制造。本图开局给足7发，再显式开自动制造。
- 四阵营TMD蓝图武器仅针对'TACTICAL MISSILE'；保留原两座，不用它们冒充战略反核，也不套用反核的储弹逻辑。

此前跨图分析把5iver同型号GiveTacticalSiloAmmo列作待核实；本次已从实际UEB4302蓝图/Weapon分支确认这个接口匹配。5iver整套行为、其它型号和实际拦截仍未因此自动验收，不把历史疑点写成已证实错误。

## 自动补弹与经济边界

反核每台仅对敌方产出20质量/秒、2000能量/秒，支持原生制造；不可俘获/回收，不向玩家提供经济。当前本机拦截弹projectiles.scd/TIMMissileIntercerptor01的质量3600、能量360000、BuildTime259200；UEB4302 BuildRate1080。理论单发240秒，平均15质量/秒、1500能量/秒。20/2000留余量，避免场上全靠免费刷兵、敌军没质量导致自动制造饿死。

这不是脚本无限补弹：满仓7发，射出后仍需原生制造时间；实际经济、建造加成、损毁和模组影响另测。没有增加补弹循环/复活炮塔。核心死亡仍按原核爆，附近反核也可能被摧毁。

## 验证、备份与保留行为

50项本机LuaPlus编译/隔离通过：4阵营×9难度、1～4玩家/各目标；T3类别、每核心8/12座T3、1反核满7发且自动模式和20/2000供给、2战术反导；原始AmmoThread通道；全部防区/护盾模型和400出生格；首波计时、统计启动、八门胜利和胜利停刷。部署后3项通过：实际script编译、实际scenario v6与save86标记、实际script初始化导出高难464单位（16核心＋448守备）。本轮仍没有游戏实射/补弹、盾、路径、性能或多人通过记录。

v5紧凑布局和独立陆空出生格、盾44、波次/准备/目标选项与各类HP/数量公式、八门胜利、核心核爆均保留；兵种更换和新增反核是本次明确增强，不暗改其它难度曲线。

完整v5七文件及部署前两清单备份：本地`Insane_Beta1_T3与反核v6_20261020/修改前v5与清单备份.zip`，逐项SHA核验。两处七文件一致；仅script/scenario/changelog各3文件改变，SCMAP/save/options/preview不变；其它957安装文件及清单其它61张保持，仍62张/累计29张维护修改。

script SHA-256 `1cc8cd53a0b96d9e43f34c234d545f89ff51a22ca35f6cfb3852991b5fb56d73`；scenario SHA-256 `1ba622caac0fff193258fdcc339441b986728b6df94a3397eb758b39ebdecfb2`。完整source SHA、53检查和布局坐标在本地本轮目录及data摘要。

完全退出游戏再打开，确认Version 6新开局；旧局/旧存档不自动重载。后续重点测试实际反核拦截、打空7发后自动制造、TMD拦战术导弹、密集T3炮射界、核心爆炸、多人和高难性能。

> 后续v7已部署：用户要求防空也全部T3，已取消防空科技难度门槛，128座守备防空全部T3、雷达升T3。本文为v6历史，当前见[当前v7](INSANE_ALL_T3_V7_2026-10-20.md)。
