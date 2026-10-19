# Fort Ictus Survival两个同名条目的位置

2026-10-20，只读定位，未移动、删除、重命名或修改地图。

1. 解压地图目录：%USERPROFILE%/Documents/My Games/Gas Powered Games/Supreme Commander Forged Alliance/maps/fort_ictus_survival.v0008/
2. 同目录压缩包：%USERPROFILE%/Documents/My Games/Gas Powered Games/Supreme Commander Forged Alliance/maps/fort_ictus_survival.v0008.zip

E:/SCFA/maps/内没有找到对应场景；Steam安装maps目录也未找到。本机MyDocuments实际解析为%USERPROFILE%/Documents。E:/SCFA/bin/SupComDataPath.lua第20–23行会同时挂载用户mods、用户maps、gamedata和安装根目录；mount_contents遍历每个条目，并将zip/scd后缀移除后生成挂载点。因此地图不必位于E:/SCFA/maps才能出现在游戏列表。

两份scenario都声明name=Fort Ictus Survival、map_version=8，故显示名/版本相同。ZIP中另含顶层fort_ictus_survival.v0008/包装目录；规范化这层路径后，5个实际文件与解压目录逐文件SHA完全一致，ZIP完整性通过。压缩包SHA为cea02527a8cc7f73762e44031abb244ac46f6fa531a80a9c37c6257623831bf4。

原始ZIP成员路径并不等于解压目录的相对路径，不能遗漏包装目录而错误判断内容不同；挂载后的虚拟层级也须另查。本次没有运行时VFS转储，但已确认两份同名同版场景及加载配置，能够解释重复条目。

如果以后要去重，宜保留可直接工作的解压目录，把ZIP备份移到所有游戏挂载/扫描目录之外；不要直接把解压目录删掉并假定带包装层ZIP可独立替代。本次用户只要求定位，未执行此方案。

当前找到的是旧v8，不等于其他目录的维护v9或候选v10/v11。以后排查外交/结算，先按实际加载的scenario虚拟路径及文件哈希确定来源，不仅凭显示名认定版本或套用维护包修复结论。


原版地图列表枚举入口为lua.scd的lua/ui/maputil.lua第102行：DiskFindFiles('/maps', nameFilter .. '_scenario.lua')。本次定位不能反推10月18日某一局的实际加载来源，仍以该局日志/VFS信息为准。
