"""Idempotent source migration; fixes are committed as actual generator source."""
from pathlib import Path
f=Path(__file__).with_name('build_hardware.py')
s=f.read_text()
if 'def layer_set(' not in s:
 s=s.replace('import pcbnew as p','import pcbnew as p\ndef layer_set(*layers):\n    result=p.LSET()\n    for layer in layers: result.AddLayer(layer)\n    return result\n')
s=s.replace('p.LSET(p.F_Cu,p.F_Paste,p.F_Mask)','layer_set(p.F_Cu,p.F_Paste,p.F_Mask)')
s=s.replace('p.LSET(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask)','layer_set(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask)')
s=s.replace('p.FootprintSave(str(libpath),fp)','p.PCB_IO_KICAD_SEXPR().FootprintSave(str(libpath),fp)')
s=s.replace("p.SaveBoard(str(D/'limit4.kicad_pcb'),b)","p.PCB_IO_KICAD_SEXPR().SaveBoard(str(D/'limit4.kicad_pcb'),b)")
needle="    elif kind=='G14':shape="
if '# Complete capacitor leads' not in s:
 s=s.replace(needle,"        # Complete capacitor leads\n        for a,b in [(-2.54,-.7),(.7,2.54)]:shape+=f'(polyline (pts (xy {a} 0) (xy {b} 0)) (stroke (width 0.254) (type default)) (fill (type none)))'\n"+needle)
f.write_text(s)
c=Path(__file__).with_name('check_connectivity.py')
z=c.read_text().replace("pcbnew.LoadBoard(str(root/'hardware/limit4.kicad_pcb'))","pcbnew.PCB_IO_KICAD_SEXPR().LoadBoard(str(root/'hardware/limit4.kicad_pcb'),None)")
c.write_text(z)
print('Source migration: explicit layer sets, native IO plugin and complete capacitor graphics.')
