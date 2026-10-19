# Survival Sea Fleet v8：同队AI、刷兵与空白结算（2026-10-20）

## 处理结果与实测来源

用户先反馈大厅同队AI入局后敌对、中途退出结算空白报错，后补充倒计时或刷兵没有正常出现，没有报错文字或日志。v7以最小补丁升至v8并写入本机安装副本和维护地图包后，用户明确回复“没问题了”。据此记录**用户实测确认本次问题已解决**，不是助手自行运行游戏。

此次反馈没有逐项截图/日志、精确构建、模组清单、非默认选项、多人或全波次验收细节；不扩写为纯原版无模组、Steam完整单人矩阵、Steam多人或FAF通过。修复前没有原生错误栈，不能进一步断言某一个类别引用是唯一根因。

## 关键源码事实

- 原v7主脚本462–465行将墙体蓝图类别写成`categories.UAB5101/UEB5101/URB5101/XSB5101`。v8统一使用蓝图小写键`uab5101/ueb5101/urb5101/xsb5101`。
- 原v7第480行禁造项`categories.xsb2406`不在本机全部SCD的573种单位蓝图中；原注释为“no supernuke”。实际`units.scd`中的`units/XSB2401/XSB2401_unit.bp`为Yolona Oss实验级核弹发射井，带STRATEGIC/EXPERIMENTAL/NUKE类别，因此修正为`categories.xsb2401`，保留禁造意图。
- `ArmyToPlayerID`在本图是脚本末尾定义的本地槽位转换函数，按ARMY_1～16返回数字，并不检查是否人类。旧代码的“human”注释不准确；不能凭函数名断定它排除AI，更不能据此重写全员联盟。
- 本机`mohodata.scd/lua/simInit.lua`的BeginSession先直接调用地图OnPopulate/OnStart，再按ArmySetup.Team>1恢复大厅队伍；`schook.scd/schook/lua/simInit.lua`包装函数在基础BeginSession返回后才启动CollectCurrentScores/SyncCurrentScores。初始化异常可以同时阻断大厅队伍恢复和分数采集。

## 实际补丁与保留内容

只修正上述5个类别键，在OnStart返回前增加完成日志；map_version 7→8，场景显示版本同步。没有改联盟、人数、出生路线、胜负逻辑、波次表或全局score/tabs/SimInit，也没有循环强制结盟。

两处各11文件相对路径及SHA相同。SCMAP/save/options/preview和4份自带纹理共8文件字节不变；script/scenario/changelog改变。旧v7两份完整ZIP及修改前管理清单归档放在游戏扫描根外，完整性及逐文件SHA通过。保留62图，累计修改29图不变；本轮未删除旧图或发布地图资产。

## 隔离验证与边界

目标运行时为本机32位LuaPlus_1081.dll。16项隔离检查及2项安装后检查均通过，安装scenario实际求值为map_version=8。

- 6个旧版严格类别模型对照在初始化阶段拒绝nil；1个允许大写墙体别名的模型仍在第5条xsb2406拒绝nil；1个容忍nil的对照则能完成原联盟和分数启动。
- 6种v8布局覆盖单人、本人加3名AI、4人、空槽和第4槽单人；实际完整地图脚本与本机BeginSession基础/hook、AddRestriction封装、分数采集/同步、score.UpdateData/UpdateDisplay函数组合执行。
- 得到1/2/4个可见结算行，姓名和6列数字非空；首波每槽6单位、前10波和防守目标死亡后的共同失败通过。
- 原生类别、外交、单位和UI控件采用模型。严格模型的断言栈不能冒称游戏当局日志；UI函数读值通过不等于实际界面渲染/网络同步通过。这里的用户反馈独立于隔离检查。

## 可复用的排查顺序

遇到“同队敌对＋不倒计时/不刷兵＋结算空白”，先检查OnPopulate/OnStart能否完整返回，以及结盟前是否有无效类别、空武器、marker异常；随后查大厅队伍恢复与统计线程。不先改全局结算UI，不默认增加外交循环。

区分三种症状：地图初始化中断造成无统计数据；Horde EE开启战役UI使中途退出直接跳过结算；原版结算可见行与军队索引错配。不要把本图的成功修复自动套到Fort Ictus特殊第4槽或其他地图。

核对类别时既检查蓝图存在，也检查大小写及实际传值。已知误写优先恢复原意的正确ID；未知可选类别需核实用途后决定guard，不能用忽略所有错误冒充修复。补丁成功也不能代替修复前的原生错误栈。

## 当前指纹与后续维护

- `survival_sea_fleet_script.lua` SHA-256 `eb99708524d6e5ea9c3955a5d459c0d059b09ad3656b12ec7bb751c5b8bf6484`。
- `survival_sea_fleet_scenario.lua` SHA-256 `54c9925b83ddd0d845e32673043b0b206bb74ef7e66aa7830c0d21de1322dbde`。
- `survival_sea_fleet_save.lua` SHA-256 `e1bfb40646ef308493d7fd0021c78385b6d0908f4c1d4fe7a9ee390b0b05719f`。
- `survival_sea_fleet_options.lua` SHA-256 `536df56ab788fe20713271e483afd21cce94fc607dc5dcdea55a7bdb04f3a539`。
- `survival_sea_fleet.scmap` SHA-256 `82cacdafec7988cc22e0bb810c4390b1ec6c58f701755c7951cfe93d21b2d77e`。

完整回归仍覆盖不同选项、后期/无尽波次、自然胜利、实际多人和退出；未来修改后需重新验证。来源/行号/哈希和用户反馈摘要见[机器可读记录](data/sea_fleet_fix_2026-10-20.json)。商业游戏源码、原始地图和本地私人路径不上传。
