# Validation record and remaining release gates

## Actually executed, 2026-09-19

| Check | Actual result |
|---|---|
| KiCad version | 10.0.6 |
| Native schematic/PCB | Generated and opened by KiCad CLI; PDF/SVG exports produced |
| ERC | 0 errors, 0 warnings |
| DRC | 0 errors, 0 warnings, 0 unconnected items |
| Manifest/schematic/PCB mapping | 41 components, 84 connected pin assignments, 4 NC pads checked |
| Independent host controller | 47 assertions passed using g++ C++17, -Wall -Wextra -Werror |
| Pico 2 cross-compilation | Success, pinned official Pico SDK 2.2.0 |
| Resulting ELF size | text 35168 bytes, data 0 bytes, BSS 3792 bytes |
| Assembly, flashing, motor tests | Not performed |

CAD source commit: `394ce1f6ac9a20584c89738f3ebd1a408357ee30`.
[CAD CI and generated-file publication](https://github.com/kkybby/rail-transient-inspector/actions/runs/35427853316).
Actual reports: [check summary](../build/check-summary.json), [connectivity](../build/connectivity.txt), [ERC](../build/erc.json), [DRC](../build/drc.json), [host assertions](../build/host-tests.txt).

Firmware source commit: `59efa8e02bd895e27b4777502ecefca23f3a303f`.
[Actual Pico 2 compile run](https://github.com/kkybby/rail-transient-inspector/actions/runs/35427472611).
Pico SDK commit: `a1438dff1d38bd9c65dbd693f0e5db4b9ae91779`.
Board target: `pico2`, `PICO_NO_PICOTOOL=1`; ELF/bin/hex compiled, no UF2 creation claimed. Firmware source has not changed after this successful run. The separate compile artifact contains logs and binaries; no flashing or hardware result follows from compilation.

Read [QUALIFICATION.md](QUALIFICATION.md) with the circuit estimates. No rule errors have been waived to manufacture a passing status. However, a passing automated check cannot establish physical correctness, appropriate component choice or safety.

## Physical release gates, still open

1. Confirm actual Pico 2 stepping and host PCB/epro/schematic correspondence, supply and USB connections.
2. Qualify full passive MPNs, footprint/body dimensions, voltage/tolerance/temperature/leakage and effective capacitance. Select the actual micro-switch for sub-mA wetting current.
3. With no motors connected, verify all loop states, unplugged wires, host harness, input modes and levels over the intended supply range. Record raw-input and ALLOW waveforms.
4. Characterize startup pulses, switch bounce and interference. Stop latency and stop distance must include mechanics and scheduling, not only an RC calculation.
5. Check reset, watchdog, invalid/reversed commands, limit-at-start, both loops open, driver fault, communication expiry and no automatic restart. A loop opening must not be labelled physical arrival without independent evidence.
6. Verify actual external reset-pull wiring and bias with each power state. Powered-input leakage does not cover all independent-off states.
7. Audit the upstream supply and current-channel mapping. Lock motor voltage/stall current/inertia, current limit, fuse, braking and guarding before implementing a real-drive backend.
8. Only then perform controlled low-energy motor testing with an independent cutoff and recorded results.

No fabrication Gerber package is issued in R0. Editable CAD is for review and iteration. No personnel-protection, human-trapping lock, lifting, vehicle or unguarded application is qualified. Firmware deliberately keeps physical outputs disabled.
