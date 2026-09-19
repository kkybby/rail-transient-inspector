# Hardware and engineering projects

Board-level interface design, motion-state logic and supporting bench-analysis tools.

[中文介绍](README.zh-CN.md)

## Featured hardware: LIMIT4

[![LIMIT4 four-channel interface design, showing the actual PCB export](assets/limit4-cover.png)](https://github.com/kkybby/rail-transient-inspector/tree/hardware/dual-actuator-controller-r0)

A four-channel limit-switch interface for small dual-actuator projects. The work includes an editable two-layer PCB, input-conditioning circuits, independent motion-state code and reproducible design checks.

**Stage:** unbuilt engineering prototype. The software has been tested and cross-compiled; the supplied Pico 2 program keeps motor outputs disabled. No physical motor performance is claimed.

**[Explore the hardware project](https://github.com/kkybby/rail-transient-inspector/tree/hardware/dual-actuator-controller-r0)** | [View the schematic](https://github.com/kkybby/rail-transient-inspector/blob/hardware/dual-actuator-controller-r0/build/limit4-schematic.pdf) | [中文作品页](https://github.com/kkybby/rail-transient-inspector/blob/hardware/dual-actuator-controller-r0/README.zh-CN.md)

The new interface extends the published OpenDualMotorDriver platform. The original motor-power motherboard is attributed to its author and is not represented as a new design. AI assistance was used for the extension and software; the project page separates reused work, new contributions and pending validation.

## Supporting tool: Rail Transient Inspector

Local oscilloscope CSV analysis for voltage dips and trigger timing. This software prototype includes explicit units, event filtering and HTML/JSON reports. Demonstration data is synthetic; real-instrument validation is pending.

[Software documentation](SOFTWARE.md) | [中文工具说明](SOFTWARE.zh-CN.md) | [Offline application file](standalone.html)

The repository retains its original name and software code on `main`. The hardware project is on the linked hardware branch. These links lead to project documentation and source, not a separately deployed website.
