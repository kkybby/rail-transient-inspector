# State / failure review

| Condition | Expected in stated model | Residual risk |
|---|---|---|
| Powered/NCclosed | FILTlow/ALLOWhigh | Contact wetting must be qualified |
| NCopens/either loopwire breaks | FILThigh/ALLOWlow; directional request stopped | Cannot distinguish endpoint/wirebreak; short defeats detection |
| MCU reset/high-Z | External2k2 aim to hold RESETlow | Physical rework and driver-powered leakage must be tested |
| RESET high/low | Enable /Hi-Z according to TI | Dry-run never drives high |
| GPIO mistakenly output |470R mitigates contention | Invalid operating state, no correctness claim |
| Buffer off/hoston |Ioff and6k8 model yields low | Shared supplies are intended; verify GPIO/ground |
| Bufferon/hostoff |Buffer can drive hostpad |Independent supplies prohibited; abs-max not permission |
| Ramp/brownout |Logic below supplymin unspecified |Explicit arm; measure reset sequence |
| Sleep/wake |Require reset and newarm |Sleep routine not implemented |
| Driverfault/both limitsopen |All requests disabled |OCP may not protect gearbox |
| Communication expires |Requests cleared at500ms policy |Host test only; no measured latency |
| Firmware lockup |Watchdog100ms request/reset pulls |Actual watchdog behavior untested |
| Reverse request while moving |Rejected |Qualified PWM/deadtime backend not implemented |
| Contact recloses after stop |No automatic restart |Bounce/EMI still require testing |
| Common groundbreak |Undefined references |Not fail-safe; independent cutoff needed |

No optocoupler, MOSFET, level translator or TVS is installed on this controlled shared-rail dry-contact interface. Their absence restricts use; it is not a robustness claim. Long cables/industrial24V sensors need a separate protection design. Local100nF capacitors bypass each gate;10nF filters and external pulls have explicit calculations, not generic boilerplate.
