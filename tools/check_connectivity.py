from pathlib import Path
import json,xml.etree.ElementTree as ET
import pcbnew
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'hardware/design.json').read_text())
all_expected={(c['ref'],pin):(net or '') for c in manifest['components'] for pin,net in c['nets'].items()}
expected={k:v for k,v in all_expected.items() if v}
b=pcbnew.PCB_IO_KICAD_SEXPR().LoadBoard(str(root/'hardware/limit4.kicad_pcb'),None)
all_actual={(fp.GetReference(),pad.GetNumber()):pad.GetNetname() for fp in b.GetFootprints() for pad in fp.Pads()}
assert all_expected==all_actual,('PCB/manifest mismatch',all_expected.items()-all_actual.items(),all_actual.items()-all_expected.items())
x=ET.parse(root/'build/limit4.xml').getroot();sch={}
for net in x.findall('./nets/net'):
 for n in net.findall('node'):
  ref=n.get('ref');pin=n.get('pin')
  if not ref.startswith('#') and (ref,pin) in expected:sch[ref,pin]=net.get('name').lstrip('/')
assert sch==expected,('Schematic/manifest mismatch',expected.items()-sch.items(),sch.items()-expected.items())
print(f'{len(expected)} populated pin/net assignments and {len(all_expected)-len(expected)} NC pads match schematic, PCB and manifest.')
summary={'components':len(manifest['components']),'connected_pin_assignments':len(expected),'nc_pads':len(all_expected)-len(expected),'hardware_tested':False,'release':'ENGINEERING_DRAFT_NOT_FOR_FABRICATION'}
failed=False
for fn,key in [('drc.json','violations'),('erc.json','sheets')]:
 data=json.loads((root/'build'/fn).read_text())
 if key=='sheets':violations=[v for sheet in data.get(key,[]) for v in sheet.get('violations',[])]
 else:violations=data.get(key,[])+data.get('unconnected_items',[])
 errors=[v for v in violations if v.get('severity')=='error'];warnings=[v for v in violations if v.get('severity')=='warning']
 summary[fn]={'errors':len(errors),'warnings':len(warnings),'unconnected_items':len(data.get('unconnected_items',[])),'kicad_version':data.get('kicad_version')}
 print(fn,'errors=',len(errors),'warnings=',len(warnings),'unconnected=',len(data.get('unconnected_items',[])))
 for v in errors+warnings:print(v.get('type'),v.get('description'))
 failed=failed or bool(errors) or bool(data.get('unconnected_items',[]))
(root/'build/check-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if failed:raise SystemExit('CAD errors or unconnected items remain. Publication blocked.')
