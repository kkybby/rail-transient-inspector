# Electrical evidence and calculations / R0

## Exact devices / documents

Extension IC: TI **SN74LVC1G14DBVR**, DBV 5-pin SOT-23. Product https://www.ti.com/product/SN74LVC1G14 ; data sheet **SCES218AA, October2025**, https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf . No externally selectable silicon stepping was established; physical lot remains unknown. Input is high-impedance Schmitt CMOS; output is push-pull with Ioff support, not open drain. No internal resistor to VCC is assumed.

Host: upstream **Pico2/RP2350A module**. Pico2 datasheet Release5, build03/07/2026 d4e0f1799616: https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf . RP2350 datasheet build2025-07-29 d126e9e-clean: https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf . Actual module stepping must be identified; A2 erratum E9 is considered and B2 is not assumed.

Existing driver: **DRV8412DDWR**, DDW44 HTSSOP+PowerPAD. **SLES242H, July2024**: https://www.ti.com/lit/ds/symlink/drv8412.pdf . Product/EVM pages inspected: https://www.ti.com/product/DRV8412 and https://www.ti.com/tool/DRV8412DDWEVM . EVM user-guide download did not open in this session. No separate applicable errata was established from the inspected pages; this is not proof none exists. Full power-stage qualification remains open.

## Cell-by-cell evidence log

TI printed page equals PDF ordinal except unnumbered mechanical addendum. RP2350 viewer index is explicitly zero-based below.

| Document/table | Page | Row / column | Minimal relevant cell / condition | Supported conclusion |
|---|---|---|---|---|
| SCES218AA Table4-1 | print4/PDF4 | A,GND,Y,VCC / DBV | 2,3,4,5 | Exact DBV pin map |
| Same footnote1 | print4/PDF4 | NC | no internal connection, soldered | NC1 left electrically unconnected, pad retained |
| SCES218AA5.5 | print7/PDF7 | VT+ /3V min,max | 1.5,1.87V | Tested rising threshold |
| Same | print7/PDF7 | VT- /DBV /3V /-40..85C | 0.84,1.14V | Tested falling threshold; not DPW row |
| Same | print7/PDF7 | VT+4.5Vmax;VT-4.5Vmin | 2.74V;1.41V | Adjacent points for engineering interpolation |
| Same | print7/PDF7 | VOH /3V /-16mA /min | 2.4V | Loaded high output at tested condition |
| Same | print7/PDF7 | VOL /3V /16mA /max | 0.4V | Loaded low output at tested condition |
| Same | print7/PDF7 | II /VI5.5V or GND,VCC0..5.5 | +/-5uA | Input leakage, no assumed internal pull |
| Same | print7/PDF7 | Ioff /VCC0,VI or VO5.5V | +/-10uA | Qualified poweroff leakage |
| Same | print7/PDF7 | ICC /IO0,VI5.5V or GND | 10uAmax | Static rail-level current, not transient current |
| SCES218AA5.1/5.3 | print5/6/PDF5/6 | recommended input/output | 0..5.5V /0..VCC | No external12/24V inputs; abs-max not normal operation |
| SCES218AA7.2.3 Fig7-2 | print13/PDF13 | explanation | interpolation between table points | An engineering estimate, not a new independently tested limit |
| SCES218AA7.3 | print13/PDF13 | bypass | 0.1uF near VCC | Local Cx2 purpose |
| DBV0005A4214839/K08/2024 | PDF39, unnumbered | land pad/column/row pitch | 1.1x0.6mm /2.6mm /0.95mm | Custom DBV copper geometry |
| RP2350 Table1436,14.9.4 | print1339..1340,viewer1339..1340 | VIH/VIL at IOVDD3.3 | 2.0Vmin /0.8Vmax | GPIO compatibility comparison |
| Same | print1340,viewer1340 | VOH2mAmin /inputpullup | 2.62V /32..86kOhm | Reset drive and unexpected pull-up calculation |
| RP2350-E9 | print1366..1367,viewer1366..1367 | A2 mitigation | external pull-down8.2kOhm or less | 6k8+1% is within explicit workaround |
| SLES242H Table4-1 | print3/PDF3 | DDW RESET_AB/CD | pins16/6 | Not adjacent DRV8432 column |
| SLES242H5.7 | print7/PDF7 | RESETVIH/VIL,leak | 2Vmin /0.8Vmax /+/-100uA | Powered reset bias calculation |
| SLES242H6.3.3 | print13/PDF13 | reset mode | bridge high impedance | Coast/Hi-Z, not guaranteed mechanical braking |

E9's approximately120uA is typical, never treated as a guaranteed maximum. The explicit8.2k workaround is used instead. Active buffer drive helps when powered;6k8 also biases a disconnected/unpowered output. The standard GPIO1uA leakage applies only where the erratum does not invalidate it.

## Circuit / explicit assumptions

Engineering target: shared nominal3.3V, assumed3.135..3.465V; initial bench0..50C; NC contact+cable resistance<=10Ohm; cable capacitance<=1nF. These are qualification targets, not user equipment facts. Long-wire, industrial ESD/surge and independently powered hosts are excluded.

LOOP--330R--FILT; FILT--4k7--3V3; FILT--10nF--GND; U.A=FILT; U.Y--470R--ALLOW; ALLOW--6k8--GND. Four100nF bypasses. Resistors1%, filterC5% C0G targets. Exact passive MPNs are not yet qualified and are labelled SPEC_ONLY_MPN_PENDING in the BOM, preventing an unverified purchase recommendation.

Closed FILT worst at3.465V, series+contact343.3Ohm and pull4653Ohm:
`Vclosed <= 3.465*343.3/(4653+343.3) + 5uA*(4653||343.3) = 0.240V`.
Open FILT at minimum supply:
`Vopen >= 3.135-5uA*4747 = 3.111V`.
Contamination leakage must be added after qualification. The3V and4.5V threshold rows bracket an engineering interpolation as illustrated by Fig7-2; supply/temperature sweeps are still required. Wetting current is approximately0.62..0.70mA: do not assume an arbitrary micro-switch supports that low-current operation.

Using tested VOH2.4V, output resistor474.7Ohm and pull6732Ohm:
`VALLOW >= 2.4*6732/(6732+474.7)-1uA*6732 = 2.235V`, margin0.235V over GPIO VIH2.0V at3.3V. Tested VOL0.4V is below0.8V. The loaded specification is evaluated at its actual test point; extending to the full assumed common-rail range remains prototype qualification. Actual static load<0.52mA per output, below the16mA test condition. Intended resistor loss is only a few mW.

Buffer poweroff: `10uA*6868Ohm =0.069V`. Unexpected host internal pull-up32kOhm at3.465V gives `3.465*6868/(32000+6868)=0.612V`; adding0.069V yields0.681V<0.8V under this defined model. This does not cover ground loss or an actively driven host output. GPIO inputs have internal pulls disabled in the intended firmware.

Accidental opposing push-pull outputs are current-limited nominally by470R: `3.465/465.3=7.45mA`. This is mitigation of accidental DC contention, not a valid operating mode or a verified transient-clamp budget. Positive/negative transients and separate supply behavior are not certified.

Filter open tau maximum=`4747*(10.5nF+1nF)=54.59us`. The table-based interpolated rising threshold at3.465V is about2.14V. Crossing is on the order of50..65us for these assumptions. This is not a motor-stop guarantee: polling, scheduling, bounce, driver behavior and inertia add delay. Startup capacitor charging can temporarily make ALLOWhigh, so the controller requires stable inputs and explicit arm. No automatic restart is implemented.

Optional RESET2k2 pulls: powered-driver leakage100uA times Rmax2222Ohm is0.2222V<0.8V. At GPIO VOHmin2.62V the load including100uA is about1.30mA, below the2mA output test; high-level margin is0.62V. Driver leakage was specified under powered conditions; fully independent poweroff still needs investigation. The driver's ~1kOhm internal pull-down row applies to each OUTPUT half-bridge, not RESET. No invented RESET internal pull is used.

## Classification

Cx2: data-sheet recommended bypass. R x1/x2/x3/x4, Cx1,R51/R52: computed engineering selections under stated assumptions, require physical validation. Host mapping: source-verified but assembled continuity pending. No unverified motor-current, clamp/ESD or connector behavior enters a production connection table. R0 is not a production release.
