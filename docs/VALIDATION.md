# Validation / release gates

Engineering draft; no physical assembly, powered motor or measurements.

Executable host tests: `g++ -std=c++17 -Wall -Wextra -Werror tests/motion_test.cpp -o /tmp/test && /tmp/test`. Actual assertion count is printed and stored in build/host-tests.txt. KiCad version, ERC/DRC and schematic/PCB/manifest comparison are in build/. A green workflow only proves the steps ran; inspect the rule findings separately. Pico dry-run compilation is tracked independently; no flash or hardware run is claimed.

R0 deliberately supplies no fabrication Gerber package. Editable CAD is for independent review and iteration; a generated file is not an assembly release. Remaining gates:

1. Confirm physical Pico2 stepping, host PCB/epro/schematic correspondence and host supply/USB connections.
2. Select and verify exact passive MPNs, footprint/body/voltage/tolerance/temperature/leakage and capacitor effective value. Qualify actual micro-switch at sub-mA wetting current.
3. Without motors, verify all loop states, unplugged wires and host harness, GPIO input modes and output voltages across intended supply range. Inspect raw signal and ALLOW waveforms.
4. Characterize response, startup pulse, bounce and noise; stop latency must be based on mechanics, not just an RC calculation.
5. Test MCU reset, watchdog, incorrect command direction, limit-at-start, both loopsopen, fault, communication expiry and no-restart behavior. LIMIT_OPEN must never masquerade as physical arrival.
6. Measure external reset-pull behavior with host reset/off and driveron. Driver powered-input leakage does not guarantee every independent power state.
7. Audit upstream power/current-sense mapping, choose motor/currentlimit/fuse/braking/guards, then implement a real-drive backend only after review.
8. Controlled low-energy bench work with independent power cutoff and recorded stop distance. No personnel protection, human-trapping locks, lifting, vehicles or unguarded use.

Command acceptance, GPIO state and physical arrival remain separate. Software tests prove none of the physical performance claims.
