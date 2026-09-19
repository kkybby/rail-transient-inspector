# 双路执行器控制扩展 / LIMIT4 R0

**状态：可编辑硬件工程草案，尚未发布打样版；没有完成实物电机验证。**

本轮在 OpenDualMotorDriver 双 H 桥主板基础上，新增四路常闭触点限位输入扩展板，并独立实现双轴动作状态机。电机功率级保留上游设计，尚未重新设计或完成适用性验证。新增内容包括实际 KiCad 原理图、两层 PCB 布线、本地库、BOM、网表一致性校验和测试程序。

## 本轮完成的硬件

四路输入分别为 A_MIN、A_MAX、B_MIN、B_MAX。每一路采用输入串联电阻、外部上拉、RC 滤波、SN74LVC1G14DBVR 施密特反相器、输出串联电阻和下拉。在规定的共电源模型下，常闭触点闭合时 ALLOW 为高，回路断开时为低。只接受无源触点，不能接 12 V/24 V 传感器输出。

板子与主控共用 3.3 V 和 GND。两路 RESET 偏置预留需要按实际主板网络焊线并测试。接口为焊线孔，尚未选定连接器、线束及固定方式。板尺寸 68 × 66 mm，41 个位号。被动器件保留规格和待核实料号状态，当前 BOM 不作为采购放行表。

## 实际完成的检查

| 项目 | 结果 |
|---|---|
| KiCad 10.0.6 原理图 ERC | 0 错误、0 警告 |
| PCB DRC | 0 错误、0 警告、0 未连接项 |
| 原理图、PCB 与设计清单 | 84 个有效引脚网络对应项及 4 个 NC 焊盘一致 |
| 双轴状态机 | 47 项主机断言通过 |
| Pico 2 固件 | 固定版本 Pico SDK 2.2.0 交叉编译通过 |
| 实物电机、停机距离、抗干扰 | 尚未验证 |

真实运行记录：[CAD 检查与发布](https://github.com/kkybby/rail-transient-inspector/actions/runs/35427853316)、[Pico 2 编译](https://github.com/kkybby/rail-transient-inspector/actions/runs/35427472611)。不能将规则检查或代码编译通过描述为电机控制已经调通。

## 从这里检查

- [原理图 PDF](build/limit4-schematic.pdf) 与 [原理图源文件](hardware/limit4.kicad_sch)
- [PCB 源文件](hardware/limit4.kicad_pcb) 与 [实际 CAD 导出](build/pcb-top.png)
- [项目设置](hardware/limit4.kicad_pro)、[本地封装](hardware/LIMIT4.pretty)、[本地符号](hardware/RTI.kicad_sym)
- [BOM](hardware/BOM.csv)、[检查汇总](build/check-summary.json)、[原始 ERC](build/erc.json)、[原始 DRC](build/drc.json)
- [参数证据及计算](docs/EVIDENCE.md)、[计算适用边界](docs/QUALIFICATION.md)、[接口与上游问题](docs/INTEGRATION.md)
- [掉电及故障状态](docs/STATES.md)、[实物验收门槛](docs/VALIDATION.md)

## 控制逻辑和边界

独立状态机覆盖默认关闭、显式解锁、双向限位、禁止运动中直接换向、驱动故障输入、通信超时、动作超时和无自动重启。LIMIT_OPEN 只表示回路断开，无法区分到位与断线，也不能检测触点被短接。

Pico 2 程序是输出关闭的编译验证及输入观察版本，所有桥驱动 RESET、PWM 始终为低。本版没有可启用的实机功率驱动后端。实际电机、微动开关、Pico 硅版本、母板供电和被动器件完整料号需要在打样前锁定；不会把 A2 E9 的典型电流当作最大保证值。

暂不提供用于直接下单的 Gerber 包，不采购、不打板。这是工程复核材料，未获得安全或工业使用认证。

## 来源和贡献

上游为 Miloš Rašić 的 OpenDualMotorDriver，固定提交 `9a938240a8053269b1b8786dccdb6d541cb7396c`。主板、电流采样和上游照片不算本轮新增成果。本轮为 AI 辅助硬件扩展和独立代码。

上游 README 的软件许可描述与实际 LICENSE 不一致，已在 [来源记录](docs/PROVENANCE.md) 说明，本轮没有复制其固件。扩展硬件使用 [CERN-OHL-S-2.0 完整许可](LICENSES/CERN-OHL-S-2.0.txt)，独立软件使用 [MIT](firmware/LICENSE)。

文件目前放在现有仓库的独立硬件分支，软件 main 分支和私有工作资料库未修改。
