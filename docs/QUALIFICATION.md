# Qualification boundaries / engineering review, 2026-09-19

Read this with EVIDENCE.md and STATES.md. These restrictions take precedence over any simplified interpretation of the numerical examples.

1. **RP2350 A2 erratum E9:** the normal input-leakage specification is not a worst-case substitute for the erratum. The 6k8 resistor is chosen within the documented external pull-down workaround; this does not establish all combinations of supply, ramp, internal pulls and disconnects. The 0.681 V unexpected-pull-up estimate in EVIDENCE.md excludes additional erratum-related current and therefore is NOT a guarantee for an A2 input with its internal pull-up enabled. Intended firmware disables internal pulls. Powered active-buffer high-drive margin also remains subject to the actual silicon and load. Do not use the approximately 120 uA typical erratum figure as a maximum.

2. **Supply-dependent specifications:** a VOH/VOL limit tested at 3.0 V and a receiver threshold specified at 3.3 V do not automatically prove every corner of an assumed 3.135–3.465 V shared rail. Interpolated Schmitt thresholds and RC crossing times are design estimates. The full range requires independent analysis and physical supply/temperature sweeps. Absolute maximum ratings are never an operating recommendation.

3. **Power sequencing:** separate buffer/host supplies are excluded. Below the logic devices' operating range, output behavior is unspecified. A common ground break is not covered by Ioff or the external pull-down. Partial-power and ramp calculations support a prototype concept only; no fail-safe guarantee is made.

4. **Reset provisions:** R51/R52 have an intended powered-driver bias calculation. They provide no protection if omitted or not connected to the verified motherboard nets. Unpowered driver input behavior, source-board stuffing, watchdog behavior and back-power paths still require qualification. RESET low means the specified electrical high-impedance/coast state, not instantaneous mechanical stopping.

5. **Contact and passive selection:** the NC contact must be qualified at the proposed sub-mA wetting current. Cable resistance/capacitance are engineering assumptions. Full passive MPNs, tolerances, voltage ratings, leakage, dimensions and footprints remain unresolved; the BOM is not a manufacturing authorization. Long-cable ESD, industrial inputs and surge protection are outside R0.

6. **Evidence interpretation:** ERC, DRC and netlist checks validate configured file rules and consistency, not these electrical assumptions. The host tests validate software requests only. The cross-compiled Pico program continuously holds real motor outputs off. There is no motor drive release, guaranteed stop latency or safety certification.

R0 remains NOT FOR FABRICATION and NOT FOR MOTOR OPERATION until these gates and the physical validation plan are resolved.
