from pathlib import Path
import json,xml.etree.ElementTree as ET
import pcbnew
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'hardware/design.json').read_text())
expected={(c['ref'],pin):net for c in manifest['components'] for pin,net in c['nets'].items() if net}
b=pcbnew.LoadBoard(str(root/'hardware/limit4.kicad_pcb'))
actual={(fp.GetReference(),pad.GetNumber()):pad.GetNetname() for fp in b.GetFootprints() for pad in fp.Pads() if pad.GetNetname()}
assert expected==actual,('PCB/manifest mismatch',expected.items()-actual.items(),actual.items()-expected.items())
x=ET.parse(root/'build/limit4.xml').getroot();sch={}
for net in x.findall('./nets/net'):
 for n in net.findall('node'):
  ref=n.get('ref');pin=n.get('pin')
  if not ref.startswith('#') and (ref,pin) in expected:sch[ref,pin]=net.get('name').lstrip('/')
assert sch==expected,('Schematic/manifest mismatch',expected.items()-sch.items(),sch.items()-expected.items())
print(f'{len(expected)} populated pin/net assignments match schematic, PCB and manifest; no hidden connectivity substitutions.')
for fn,key in [('drc.json','violations'),('erc.json','sheets')]:
 data=json.loads((root/'build'/fn).read_text())
 if key=='sheets':violations=[v for sheet in data.get(key,[]) for v in sheet.get('violations',[])]
 else:violations=data.get(key,[])+data.get('unconnected_items',[])
 errors=[v for v in violations if v.get('severity')=='error'];warnings=[v for v in violations if v.get('severity')=='warning']
 print(fn,'errors=',len(errors),'warnings=',len(warnings))
