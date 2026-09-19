"""Idempotent source migration; patched source is included in build artifacts."""
from pathlib import Path
f=Path(__file__).with_name('build_hardware.py');s=f.read_text()
if 'def layer_set(' not in s:
 s=s.replace('import pcbnew as p','import pcbnew as p\ndef layer_set(*layers):\n    result=p.LSET()\n    for layer in layers: result.AddLayer(layer)\n    return result\n')
s=s.replace('p.LSET(p.F_Cu,p.F_Paste,p.F_Mask)','layer_set(p.F_Cu,p.F_Paste,p.F_Mask)').replace('p.LSET(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask)','layer_set(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask)')
s=s.replace('p.FootprintSave(str(libpath),fp)','p.PCB_IO_KICAD_SEXPR().FootprintSave(str(libpath),fp)').replace("p.SaveBoard(str(D/'limit4.kicad_pcb'),b)","p.PCB_IO_KICAD_SEXPR().SaveBoard(str(D/'limit4.kicad_pcb'),b)")
needle="    elif kind=='G14':shape="
if '# Complete capacitor leads' not in s:
 s=s.replace(needle,"        # Complete capacitor leads\n        for a,b in [(-2.54,-.7),(.7,2.54)]:shape+=f'(polyline (pts (xy {a} 0) (xy {b} 0)) (stroke (width 0.254) (type default)) (fill (type none)))'\n"+needle)
s=s.replace('sch=sch,pcb=pcb','sch=tuple(round(t/1.27)*1.27 for t in sch),pcb=pcb')
s=s.replace("value='POWER',nets={'1':'3V3'},sch=(218,45)","value='3V3',nets={'1':'3V3'},sch=(218.44,45.72)")
s=s.replace("value='POWER',nets={'1':'GND'},sch=(218,53)","value='GND',nets={'1':'GND'},sch=(218.44,58.42)")
s=s.replace("y=42+36*i", "y=50.8+45.72*i").replace("(111,y-15.24)","(111,y-20.32)").replace("{24+36*i}","{25.4+45.72*i}")
s=s.replace("else y+12}","else y+16.51}")
s=s.replace("fp='LIMIT4:'+('DBV5'", "fp='LIMIT4:'+('DBV5'")
# Hide board footprint link for the two non-board external power symbols.
s=s.replace("(D/'fp-lib-table').write_text", "(D/'fp-lib-table').write_text")
if '# Local symbol library' not in s:
 s=s.replace("out.append(')');(D/'limit4.kicad_sch').write_text('\\n'.join(out))", "out.append(')');(D/'limit4.kicad_sch').write_text('\\n'.join(out).replace('\\\"LIMIT4:FLAG\\\"','\\\"\\\"'))\n# Local symbol library\n(D/'RTI.kicad_sym').write_text('(kicad_symbol_lib (version 20231120) (generator kicad_symbol_editor) '+''.join(lib).replace('symbol \\\"RTI:','symbol \\\"')+')')\n(D/'sym-lib-table').write_text('(sym_lib_table (lib (name \\\"RTI\\\")(type \\\"KiCad\\\")(uri \\\"${KIPRJMOD}/RTI.kicad_sym\\\")(options \\\"\\\")(descr \\\"Local LIMIT4 symbols\\\")))')")
if '# Keep silk clear' not in s:
 s=s.replace("    if kind=='G14':pos=", "    # Keep silk clear of the preceding channel's capacitors.\n    if ref in ['R12','R22','R32','R42']:fp.Reference().SetPosition(v(-3.5,0))\n    if ref in ['R51','R52']:fp.Reference().SetPosition(v(0,2.0))\n    if kind=='G14':pos=")
# Add real wires between the components; preserve net labels for cross-checks.
if '# Channel trunk wiring' not in s:
 block="""# Channel trunk wiring
lookup={c['ref']:c for c in comps}
for k in range(1,5):
    def pt(ref,pin):
        c=lookup[ref]; x,y=c['sch']; a=math.radians(c['rot'])
        _,px,py,_,_=next(z for z in pins[c['kind']] if z[0]==str(pin))
        return (x+px*math.cos(a)-py*math.sin(a),y-px*math.sin(a)-py*math.cos(a))
    a=pt(f'J{k}',1);z=pt(f'R{k}1',1);line(*a,*z)
    a=pt(f'R{k}1',2);z=pt(f'U{k}',2);line(*a,*z)
    for ref,pin in [(f'R{k}2',1),(f'C{k}1',2)]:
        t=pt(ref,pin);line(*t,t[0],a[1])
    a=pt(f'U{k}',4);z=pt(f'R{k}3',1);line(*a,*z)
    a=pt(f'R{k}3',2);z=pt(f'J{k+4}',1);line(*a,*z)
    t=pt(f'R{k}4',2);line(*t,t[0],a[1])
"""
 s=s.replace("for i,n in enumerate(['A_MIN'",block+"for i,n in enumerate(['A_MIN'",1)
f.write_text(s)
compile(s,str(f),'exec')
c=Path(__file__).with_name('check_connectivity.py');z=c.read_text().replace("pcbnew.LoadBoard(str(root/'hardware/limit4.kicad_pcb'))","pcbnew.PCB_IO_KICAD_SEXPR().LoadBoard(str(root/'hardware/limit4.kicad_pcb'),None)");c.write_text(z)
print('CAD corrections applied: layer sets, native IO, distinct power nets, grid, local symbols, actual interconnect wires, silk clearances.')
