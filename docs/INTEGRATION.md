# Integration / engineering suggestion only

This is a wired expansion, not a mechanically interchangeable motherboard. There are no motor-current paths on LIMIT4. Verify actual board revision and continuity before soldering.

| LIMIT4 | Purpose | Intended upstream net |
|---|---|---|
| J9.1 | Shared3V3 | CN7.1 /host3V3 |
| J9.2 | Ground | CN7.5/GND |
| J5.1 | A_MIN ALLOW | GPIO16/CN7.2/SPI_MISO |
| J6.1 | A_MAX ALLOW | GPIO17/CN7.4/SPI_CS |
| J7.1 | B_MIN ALLOW | GPIO18/CN7.6/SPI_SCK |
| J8.1 | B_MAX ALLOW | GPIO19/CN7.3/SPI_MOSI |
| J10.1 | Optional reset pull | RESET_AB/GPIO12/DRV8412DDW16 |
| J11.1 | Optional reset pull | RESET_CD/GPIO9/DRV8412DDW6 |
| J1..J4.1 | Contact signal | NC switch to corresponding pin2 |
| J1..J4.2 | Contact return | GND |

Mapping evidence: upstream schematic pages2/3 and BoardConfig.h at pinned commit; TI SLES242H Table4-1 DDW column. Classification: engineering connection suggestions after source review, pending physical continuity and power-state checks. The4k7/6k8/470/330 and2k2 parts' calculations are in EVIDENCE.md.

All J footprints are plated solder-wire pads with1mm holes; pin1 is rectangular. No mating connector/strain relief/wire model is qualified. Upstream CN7 drawing has a part-name suggesting a different contact count; do not assume an off-the-shelf cable maps correctly.

Axis A is bridgeAB, PWM_A GPIO11/PWM_B GPIO13. B is bridgeCD, PWM_C GPIO8/PWM_D GPIO10. Direction versus actual travel must be checked. Four limit signals consume the original SPI GPIOs; SPI peripherals cannot run concurrently.

Review finding: firmware axis0 samples GPIO26/ACS722_OUT1, while schematic links OUT1 to CD and OUT2/GPIO27 to AB. This is a source inconsistency to investigate, not a measured hardware failure. R0 uses no current measurement for protection. Confirm physical netlist/mapping before current-based stopping. Existing driver OCP is not automatically appropriate for a small motor/gearbox.

Original power schematic shows external5V attached to Pico VBUS and external3V3 arrangements. USB plus external power, regulator reverse current and actual stuffing need a separate audit. Avoid simultaneous unverified power sources. Native source/README voltage claims are not adopted as our ratings.

Real drive is compile-blocked. Required before enabling: motor full model/voltage/stall current/inertia, micro-switch model/wetting requirements, guard/stop strategy, actual part revisions, power-sequence tests. Driver RESETlow gives Hi-Z/coast with the specified weak output pull-down; it does not guarantee instantaneous braking or zero travel.
