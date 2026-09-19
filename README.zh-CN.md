# 硬件与工程作品

展示板级接口设计、动作控制逻辑及配套调试工具。

[English](README.md)

## 硬件作品：LIMIT4 四路限位接口板

[![LIMIT4 硬件作品封面，配图来自实际 PCB 导出](assets/limit4-cover.png)](https://github.com/kkybby/rail-transient-inspector/blob/hardware/dual-actuator-controller-r0/README.zh-CN.md)

面向双路小型执行器的限位输入扩展。包含可编辑两层 PCB、输入调理电路、独立动作状态机及可复查的设计检查记录。

**当前阶段：尚未制作实物的工程原型。** 软件测试和目标编译已完成，所提供的 Pico 2 程序保持电机输出关闭；尚无实机性能结论。

**[进入硬件作品页](https://github.com/kkybby/rail-transient-inspector/blob/hardware/dual-actuator-controller-r0/README.zh-CN.md)** | [查看原理图](https://github.com/kkybby/rail-transient-inspector/blob/hardware/dual-actuator-controller-r0/build/limit4-schematic.pdf) | [查看工程源文件](https://github.com/kkybby/rail-transient-inspector/tree/hardware/dual-actuator-controller-r0)

本项目扩展了 OpenDualMotorDriver 的公开接口，原电机功率主板保留原作者归属。扩展设计与软件使用 AI 辅助，作品页分别列明上游已有内容、新增贡献及待验证事项。

## 辅助工具：Rail Transient Inspector

将本地示波器 CSV 转换为电源压降事件和触发时间关联记录，支持单位确认、事件筛选及 HTML/JSON 报告。当前演示数据为合成数据，真实仪器验证待完成。

[中文工具说明](SOFTWARE.zh-CN.md) | [English documentation](SOFTWARE.md) | [离线程序文件](standalone.html)

仓库保留原名称，软件代码保留在 main，硬件文件位于上方链接的独立分支。这些入口是 GitHub 作品文档与源文件，尚未部署独立网站。
