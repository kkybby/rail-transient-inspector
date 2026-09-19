"""Idempotent source migration; fixes are committed as actual generator source."""
from pathlib import Path
f=Path(__file__).with_name('build_hardware.py')
s=f.read_text()
if 'def layer_set(' not in s:
 s=s.replace('import pcbnew as p','import pcbnew as p\ndef layer_set(*layers):\n    result=p.LSET()\n    for layer in layers: result.AddLayer(layer)\n    return result\n')
s=s.replace('p.LSET(p.F_Cu,p.F_Paste,p.F_Mask)','layer_set(p.F_Cu,p.F_Paste,p.F_Mask)')
s=s.replace('p.LSET(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask)','layer_set(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask)')
needle="    elif kind=='G14':shape="
if '# Complete capacitor leads' not in s:
 s=s.replace(needle,"        # Complete capacitor leads\n        for a,b in [(-2.54,-.7),(.7,2.54)]:shape+=f'(polyline (pts (xy {a} 0) (xy {b} 0)) (stroke (width 0.254) (type default)) (fill (type none)))'\n"+needle)
f.write_text(s)
print('Source migration complete; explicit layer sets and complete capacitor graphics.')
