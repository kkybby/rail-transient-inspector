# Dual Actuator Controller / LIMIT4 R0

[中文说明](README.zh-CN.md)

**Editable hardware engineering draft. NOT FOR FABRICATION. No motor operation has been validated.**

![Actual KiCad PCB export](build/pcb-top.png)

Two small brushed actuators, four normally-closed dry-contact limit loops, and an explicit stopped/fault state. R0 adds a **68 × 66 mm two-layer LIMIT4 input-conditioning PCB** to the existing OpenDualMotorDriver power motherboard. It does not claim to redesign or qualify that entire power stage.

## Open the engineering files

- [Editable schematic](hardware/limit4.kicad_sch) and [schematic PDF](build/limit4-schematic.pdf)
- [Editable routed PCB](hardware/limit4.kicad_pcb), [project](hardware/limit4.kicad_pro), [local footprints](hardware/LIMIT4.pretty)
- [BOM qualification](hardware/BOM.csv) and [electrical manifest](hardware/design.json)
- [Evidence and calculations](docs/EVIDENCE.md), [qualification limits](docs/QUALIFICATION.md), [power/reset states](docs/STATES.md)
- [Integration map](docs/INTEGRATION.md), [validation record](docs/VALIDATION.md), [provenance and licensing](docs/PROVENANCE.md)
- [Independent state machine](firmware/motion.hpp), [output-disabled Pico 2 program](firmware/pico_dryrun.cpp)

## Actual results, 2026-09-19

| Check | Observed result |
|---|---|
| Native CAD | Generated and exported with KiCad 10.0.6 |
| Schematic ERC | 0 errors, 0 warnings |
| PCB DRC | 0 errors, 0 warnings, 0 unconnected items |
| Cross-file connectivity | 41 components; 84 connected pin assignments and 4 NC pads checked |
| Independent host state machine | 47 assertions passed |
| Pico 2 target | Cross-compiled with pinned Pico SDK 2.2.0; physical drive disabled |
| Hardware measurements | None; physical qualification pending |

[Actual CAD CI and publication](https://github.com/kkybby/rail-transient-inspector/actions/runs/35427853316) · [Actual firmware compile](https://github.com/kkybby/rail-transient-inspector/actions/runs/35427472611)

Rule checks establish consistency with the configured rules. They do not establish correct component selection, electrical margins at untested corners, mechanical safety or motor performance.

## Actual increment

Each NC loop has an RC front end and a TI SN74LVC1G14DBVR Schmitt inverter. In the intended shared-rail model, a closed contact yields ALLOW high; an open contact or disconnected loop yields low. A local pull-down biases an unpowered/disconnected output. Two reset-bias provisions require explicit motherboard rework wires and qualification.

A loop opening is reported as LIMIT_OPEN, not automatically as physical arrival. The circuit cannot distinguish an endpoint from a broken wire and cannot detect a short across the switch. Corresponding limit, driver fault, expired communication or motion timeout clears the software motion request. Reclosing a switch cannot restart motion automatically; a new command is required to retreat.

Based on the interfaces of [Miloš Rašić's OpenDualMotorDriver](https://github.com/MilosRasic98/OpenDualMotorDriver), pinned at `9a938240a8053269b1b8786dccdb6d541cb7396c`. The original motor bridge, current sensors and original photographs remain the upstream author's work. The new contribution is the extension PCB, independent controller code and review documents.

AI-assisted engineering. This is not an emergency stop, safety-rated interlock, industrial 24 V input or certified assembly. Below-supply-threshold behavior, independent power states, RP2350 A2 erratum E9, contact wetting, reset wiring and the original power stage remain qualification gates. Read [QUALIFICATION.md](docs/QUALIFICATION.md) alongside the numerical estimates.

Dry-run firmware continuously keeps PWM and RESET low. Real-drive compilation is blocked; no tested power-stage backend is supplied. No physical derivative has been assembled, flashed or measured. No manufacturing, motor operation or purchasing is part of R0.

## Reproduce

Use KiCad 10.0.6 with its matching system Python `pcbnew` module. Other versions have not been qualified.

```sh
mkdir -p build
python3 tools/build_hardware.py
python3 tools/layout_schematic.py
kicad-cli sch export pdf -o build/limit4-schematic.pdf hardware/limit4.kicad_sch
kicad-cli sch export netlist --format kicadxml -o build/limit4.xml hardware/limit4.kicad_sch
kicad-cli sch erc --format json -o build/erc.json hardware/limit4.kicad_sch
kicad-cli pcb drc --format json -o build/drc.json hardware/limit4.kicad_pcb
python3 tools/check_connectivity.py
c++ -std=c++17 -Wall -Wextra -Werror tests/motion_test.cpp -o /tmp/limit4-test
/tmp/limit4-test
```

Use the system Python installation that provides KiCad's module. The generator and presentation pass overwrite generated CAD; incorporate manual edits deliberately. Native CAD and local libraries are included, so review does not require regeneration.

Hardware and associated hardware source: [CERN-OHL-S-2.0](LICENSES/CERN-OHL-S-2.0.txt), with [source and modification notice](LICENSE-HARDWARE). Independent new firmware/tests: [MIT](firmware/LICENSE). The upstream software licence conflict is documented; no upstream firmware is copied.

This project lives on the isolated `hardware/dual-actuator-controller-r0` branch. The existing software `main` branch and private archive remain unchanged. A separate hardware repository has not been created.
