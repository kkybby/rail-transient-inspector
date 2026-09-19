# Provenance / changes / licensing

Upstream: Miloš Rašić, OpenDualMotorDriver, commit `9a938240a8053269b1b8786dccdb6d541cb7396c`.

Original files inspected: `Hardware/ProPrj_Dual_Motor_Driver_2026-05-02.epro`, three schematic PNGs, `Firmware/PicoDualMotorDriver/BoardConfig.h`, `DualMotorController.cpp`, README, LICENSE and LICENSE-HARDWARE. The epro is an EasyEDA Pro archive, editor metadata 2.2.45.4. Its source motherboard has LT8350-based12V gate-drive power, a5V converter and a3.3V regulator; the derivative has not requalified these sections. No upstream power ratings are adopted as our measured specifications.

**Licence discrepancy:** the pinned README/Hardware notice say firmware and host software are MIT; the actual root LICENSE is the GNU GPL version3 text. Our earlier claim that all software was MIT was overbroad. This release does not copy, modify or redistribute upstream firmware. The new small state machine and dry-run wrapper are independent code; pin/net assignments are documented interfaces. Any later reuse must first resolve the applicable terms.

The upstream `LICENSE-HARDWARE` explicitly assigns CERN-OHL-S-2.0 to the hardware. The new extension hardware, schematic, board, electrical manifest, design generator and technical hardware documents are offered under CERN-OHL-S-2.0. Preserve attribution and source location. No endorsement by the original author, TI, Raspberry Pi, CERN or Element14 is implied.

New contribution: four NC front ends, defined default-low outputs, two external driver-reset pulls, four-input harness map, independent state machine, tests, native CAD and source-to-board checks. Original main bridge PCB remains unmodified and linked, not claimed as a newly routed derivative. Original photographs are not used as photographs of our product.

Official licence: https://ohwr.org/licences/ . The authoritative licence, not this summary, governs. AI-assisted design; no physical board, motor measurement or customer result is claimed.
