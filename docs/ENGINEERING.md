# LIMIT4 engineering reference

[Project overview](../README.md) | [中文作品介绍](../README.zh-CN.md)

This page contains detailed review and reproduction material. R0 is an unbuilt engineering prototype, not a manufacturing or motor-operation release.

## Design files

| Material | Source |
|---|---|
| Schematic | [PDF](../build/limit4-schematic.pdf), [editable KiCad file](../hardware/limit4.kicad_sch) |
| PCB | [Layout image](../build/pcb-top.png), [editable PCB](../hardware/limit4.kicad_pcb), [project settings](../hardware/limit4.kicad_pro) |
| Libraries | [Footprints](../hardware/LIMIT4.pretty), [symbols](../hardware/RTI.kicad_sym) |
| Parts and nets | [BOM qualification](../hardware/BOM.csv), [electrical manifest](../hardware/design.json) |
| Design reasoning | [Evidence](EVIDENCE.md), [qualification limits](QUALIFICATION.md), [power/reset states](STATES.md) |
| Integration | [Interface map and upstream issues](INTEGRATION.md) |
| Firmware | [Independent state model](../firmware/motion.hpp), [output-disabled Pico 2 program](../firmware/pico_dryrun.cpp) |
| Validation | [Scope and release gates](VALIDATION.md), [ERC](../build/erc.json), [DRC](../build/drc.json), [connectivity](../build/connectivity.txt), [host tests](../build/host-tests.txt) |
| Attribution | [Provenance](PROVENANCE.md), [hardware notice](../LICENSE-HARDWARE), [complete hardware licence](../LICENSES/CERN-OHL-S-2.0.txt), [software licence](../firmware/LICENSE) |

## Reproduction

Use KiCad 10.0.6 and the system Python installation that provides its matching `pcbnew` module. Native CAD and local libraries can also be opened directly without regeneration.

```sh
mkdir -p build
python3 tools/build_hardware.py
python3 tools/layout_schematic.py
python3 tools/polish_symbols.py
kicad-cli sch export pdf -o build/limit4-schematic.pdf hardware/limit4.kicad_sch
kicad-cli sch export netlist --format kicadxml -o build/limit4.xml hardware/limit4.kicad_sch
kicad-cli sch erc --format json -o build/erc.json hardware/limit4.kicad_sch
kicad-cli pcb drc --format json -o build/drc.json hardware/limit4.kicad_pcb
python3 tools/check_connectivity.py
c++ -std=c++17 -Wall -Wextra -Werror tests/motion_test.cpp -o /tmp/limit4-test
/tmp/limit4-test
python3 tools/build_showcase.py
```

The generator overwrites generated CAD. Incorporate any manual edits deliberately. Symbol polishing changes label visibility and the power-flag graphic only. Pin definitions, wires, net labels, PCB geometry and firmware are compared before and after that step; its record is in `build/symbol-display-audit.json`.

## Reading the checks

ERC, DRC and matching net names validate configured file rules and source consistency. They do not prove electrical margins, correct physical assembly, appropriate contact wetting, stop distance or safety. The 47 host assertions exercise software requests. The Pico 2 compile uses a dry-run program with physical PWM and RESET outputs held low.

Full passive part qualification, host silicon revision, power sequencing, motor/contact selection and physical tests remain open. Do not order parts or fabrication from the draft BOM without resolving the release gates.

## Presentation assets

The cover is built from `build/pcb-top.png`, an actual CAD copper-layer export. It is resized and placed in a typographic layout; it is not a product photograph or a claim that a board has been assembled. The source fingerprint is recorded in `showcase/asset-provenance.json`.

The repository overview is a GitHub README, not a deployed application website. The hardware project currently lives on `hardware/dual-actuator-controller-r0`; the software application remains on `main`.
