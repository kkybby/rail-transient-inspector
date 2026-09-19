#!/usr/bin/env python3
"""Generate editable KiCad LIMIT4 R0 from one electrical manifest.
CERN-OHL-S-2.0. AI-assisted engineering prototype; NOT FOR FABRICATION.
Run with KiCad's system Python / pcbnew module.
"""
from pathlib import Path
import uuid, math, json, csv
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'hardware'; D.mkdir(exist_ok=True)
uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,'https://github.com/kkybby/dual-actuator-r0/'+s))
comps=[]
def comp(ref,kind,value,nets,sch,pcb,mpn='',rot=0):
    comps.append(dict(ref=ref,kind=kind,value=value,nets={str(k):v for k,v in nets.items()},sch=sch,pcb=pcb,mpn=mpn,rot=rot,uuid=uid(ref)))
for i,name in enumerate(['A_MIN','A_MAX','B_MIN','B_MAX']):
    k=i+1; y=42+36*i; by=116+12*i
    comp(f'J{k}','J2',name+' NC dry contact',{1:f'LOOP_{name}',2:'GND'},(25,y),(108,by-2))
    comp(f'R{k}1','R','330R 1%',{1:f'LOOP_{name}',2:f'FILT_{name}'},(50,y),(118,by),'SPEC_ONLY_MPN_PENDING')
    comp(f'R{k}2','R','4k7 1%',{1:f'FILT_{name}',2:'3V3'},(80,y-10.16),(124,by-5),'SPEC_ONLY_MPN_PENDING',90)
    comp(f'C{k}1','C','10nF C0G 5%',{1:'GND',2:f'FILT_{name}'},(80,y+10.16),(124,by+4),'SPEC_ONLY_MPN_PENDING',90)
    comp(f'U{k}','G14','SN74LVC1G14DBVR',{1:None,2:f'FILT_{name}',3:'GND',4:f'BUF_{name}',5:'3V3'},(105,y),(130,by),'SN74LVC1G14DBVR')
    comp(f'C{k}2','C','100nF X7R 10%',{1:'3V3',2:'GND'},(111,y-15.24),(134,by-3),'SPEC_ONLY_MPN_PENDING')
    comp(f'R{k}3','R','470R 1%',{1:f'BUF_{name}',2:f'ALLOW_{name}'},(128,y),(138,by+.95),'SPEC_ONLY_MPN_PENDING')
    comp(f'R{k}4','R','6k8 1%',{1:'GND',2:f'ALLOW_{name}'},(148,y+10.16),(145,by+4),'SPEC_ONLY_MPN_PENDING',90)
    comp(f'J{k+4}','J1','ALLOW_'+name,{1:f'ALLOW_{name}'},(179,y),(164,by+.95))
comp('J9','J2','HOST 3V3 / GND',{1:'3V3',2:'GND'},(235,38),(145,105))
comp('J10','J1','RESET_AB',{1:'RESET_AB'},(224,95),(140,160))
comp('R51','R','2k2 1%',{1:'RESET_AB',2:'GND'},(246,95),(147,160),'SPEC_ONLY_MPN_PENDING')
comp('J11','J1','RESET_CD',{1:'RESET_CD'},(224,123),(155,160))
comp('R52','R','2k2 1%',{1:'RESET_CD',2:'GND'},(246,123),(162,160),'SPEC_ONLY_MPN_PENDING')
netnames=sorted({n for c in comps for n in c['nets'].values() if n})
(D/'design.json').write_text(json.dumps({'revision':'R0','status':'ENGINEERING_DRAFT_NOT_FOR_FABRICATION','components':comps},indent=2)+'\n')
pins={
 'R':[('1',-5.08,0,0,'passive'),('2',5.08,0,180,'passive')],
 'C':[('1',-5.08,0,0,'passive'),('2',5.08,0,180,'passive')],
 'G14':[('1',-7.62,5.08,0,'passive'),('2',-7.62,0,0,'input'),('3',0,-7.62,90,'power_in'),('4',7.62,0,180,'output'),('5',0,7.62,270,'power_in')],
 'J1':[('1',0,0,0,'passive')],
 'J2':[('1',7.62,0,180,'passive'),('2',7.62,-5.08,180,'passive')],
 'FLAG':[('1',0,0,90,'power_out')]}
q=lambda s:json.dumps(str(s))
lib=[]
for kind,pp in pins.items():
    ref='U' if kind=='G14' else '#FLG' if kind=='FLAG' else kind[0]
    txt=f'(symbol "RTI:{kind}" (pin_names (offset 0.508)) (in_bom yes) (on_board yes) (property "Reference" "{ref}" (at 0 3.81 0) (effects (font (size 1.27 1.27)))) (property "Value" "{kind}" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))'
    shape=''
    if kind=='R': shape='(rectangle (start -2.54 1.016) (end 2.54 -1.016) (stroke (width 0.254) (type default)) (fill (type none)))'
    elif kind=='C':
        for x in [-.7,.7]:shape+=f'(polyline (pts (xy {x} -2.54) (xy {x} 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))'
    elif kind=='G14':shape='(rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type default)) (fill (type background))) (text "INV / ST" (at 0 1.27 0) (effects (font (size 1 1))))'
    elif kind=='J2':shape='(rectangle (start -2.54 2.54) (end 5.08 -7.62) (stroke (width 0.254) (type default)) (fill (type none)))'
    else:shape='(circle (center 0 1.27) (radius 1.27) (stroke (width 0.254) (type default)) (fill (type none)))'
    txt+=f'(symbol "{kind}_0_1" {shape}) (symbol "{kind}_1_1" '
    for no,x,y,a,typ in pp:
        ln=2.54 if kind not in ['J1','FLAG'] else 0
        nm={'1':'NC','2':'A','3':'GND','4':'Y','5':'VCC'}.get(no,no) if kind=='G14' else no
        txt+=f'(pin {typ} line (at {x} {y} {a}) (length {ln}) (name {q(nm)} (effects (font (size 1 1)))) (number "{no}" (effects (font (size 1 1)))))'
    lib.append(txt+'))')
root=uid('sheet')
out=[f'(kicad_sch (version 20231120) (generator eeschema) (uuid "{root}") (paper "A3") (title_block (title "LIMIT4 / dual-actuator extension") (date "2026-09-19") (rev "R0 DRAFT") (company "kkybby | AI-assisted hardware") (comment 1 "CERN-OHL-S-2.0 | no physical validation | not for fabrication")) (lib_symbols '+''.join(lib)+')']
def line(x1,y1,x2,y2):out.append(f'(wire (pts (xy {x1:.4f} {y1:.4f}) (xy {x2:.4f} {y2:.4f})) (stroke (width 0) (type default)) (uuid "{uid(str((x1,y1,x2,y2)))}"))')
def label(n,x,y,a=0):out.append(f'(label {q(n)} (at {x:.4f} {y:.4f} {a}) (effects (font (size 1.0 1.0)) (justify left bottom)) (uuid "{uid("L"+n+str(x)+str(y))}"))')
for c in comps+[dict(ref='#FLG01',kind='FLAG',value='POWER',nets={'1':'3V3'},sch=(218,45),pcb=None,rot=0,uuid=uid('flagv')),dict(ref='#FLG02',kind='FLAG',value='POWER',nets={'1':'GND'},sch=(218,53),pcb=None,rot=0,uuid=uid('flagg'))]:
    x,y=c['sch'];a=c['rot'];kind=c['kind'];ref=c['ref'];fp='LIMIT4:'+('DBV5' if kind=='G14' else '0805' if kind in ['R','C'] else kind)
    out.append(f'(symbol (lib_id "RTI:{kind}") (at {x} {y} {a}) (unit 1) (in_bom yes) (on_board {"no" if kind=="FLAG" else "yes"}) (dnp no) (uuid "{c["uuid"]}") (property "Reference" "{ref}" (at {x+2.5 if a else x} {y-4 if kind!="G14" else y-10.16} 0) (effects (font (size 1.1 1.1)))) (property "Value" {q(c["value"])} (at {x+3 if a else x} {y+4 if kind!="G14" else y+12} 0) (effects (font (size 1 1)))) (property "Footprint" {q(fp)} (at {x} {y} 0) (effects (font (size 1 1)) hide)) '+''.join(f'(pin "{no}" (uuid "{uid(ref+no)}"))' for no,*_ in pins[kind])+f'(instances (project "limit4" (path "/{root}" (reference "{ref}") (unit 1)))))')
    for no,px,py,pa,typ in pins[kind]:
        theta=math.radians(a);xx=x+px*math.cos(theta)-py*math.sin(theta);yy=y-px*math.sin(theta)-py*math.cos(theta);n=c['nets'].get(no)
        if not n:out.append(f'(no_connect (at {xx:.4f} {yy:.4f}) (uuid "{uid(ref+no+"NC")}"))');continue
        t=math.radians(pa+a);ex=xx-3.81*math.cos(t);ey=yy+3.81*math.sin(t)
        line(xx,yy,ex,ey);label(n,ex,ey)
for i,n in enumerate(['A_MIN','A_MAX','B_MIN','B_MAX']):out.append(f'(text "{n}: closed NC loop -> ALLOW high; open/broken -> low" (at 26 {24+36*i} 0) (effects (font (size 1.5 1.5)) (justify left)) (uuid "{uid(n+"note")}"))')
for y,tx in [(149,'RESET pulls require soldered rework wires to existing driver nets.'),(156,'3V3 and GND must share the host rail. No independent supply.'),(163,'No 12/24V sensor signals. Dry contacts only.'),(170,'Loop opening is not proof of physical arrival.'),(177,'Limit handling is firmware-supervised, not a safety interlock.'),(184,'Motor power motherboard stays upstream/unmodified.')]:out.append(f'(text {q(tx)} (at 211 {y} 0) (effects (font (size 1.1 1.1)) (justify left)) (uuid "{uid(tx)}"))')
out.append(')');(D/'limit4.kicad_sch').write_text('\n'.join(out))
b=p.BOARD();nets={}
for n in netnames:
    ni=p.NETINFO_ITEM(b,n);b.Add(ni);nets[n]=ni
mm=p.FromMM;v=lambda x,y:p.VECTOR2I(mm(x),mm(y));pads={}
libpath=D/'LIMIT4.pretty';libpath.mkdir(exist_ok=True)
def shape_line(fp,x1,y1,x2,y2,layer,width=.15):
    z=p.PCB_SHAPE(fp);z.SetShape(p.SHAPE_T_SEGMENT);z.SetStart(v(x1,y1));z.SetEnd(v(x2,y2));z.SetLayer(layer);z.SetWidth(mm(width));fp.Add(z)
for c in comps:
    fp=p.FOOTPRINT(b);kind=c['kind'];ref=c['ref'];x,y=c['pcb'];fname='DBV5' if kind=='G14' else '0805' if kind in ['R','C'] else kind
    fp.SetFPID(p.LIB_ID('LIMIT4',fname));fp.SetReference(ref);fp.SetValue(c['value']);fp.SetPath(p.KIID_PATH('/'+root+'/'+c['uuid']))
    fp.Reference().SetTextSize(v(.85,.85));fp.Reference().SetTextThickness(mm(.13));fp.Reference().SetPosition(v(0,-2.8));fp.Value().SetVisible(False)
    if kind=='G14':pos=[('1',-1.3,-.95),('2',-1.3,0),('3',-1.3,.95),('4',1.3,.95),('5',1.3,-.95)];sx,sy=1.1,.6;drill=0;cx,cy=2.1,1.6
    elif kind in ['R','C']:pos=[('1',-.95,0),('2',.95,0)];sx,sy=1.2,1.4;drill=0;cx,cy=1.9,1.1
    elif kind=='J2':pos=[('1',0,0),('2',0,5)];sx=sy=2;drill=1;cx,cy=1.3,6.3
    else:pos=[('1',0,0)];sx=sy=2;drill=1;cx=cy=1.3
    fp.SetAttributes(p.FP_THROUGH_HOLE if drill else p.FP_SMD)
    for no,xx,yy in pos:
        z=p.PAD(fp);z.SetNumber(no);z.SetShape(p.PAD_SHAPE_RECT if no=='1' else p.PAD_SHAPE_OVAL);z.SetSize(v(sx,sy));z.SetPosition(v(xx,yy));z.SetAttribute(p.PAD_ATTRIB_PTH if drill else p.PAD_ATTRIB_SMD)
        z.SetLayerSet(p.LSET.AllCuMask() if drill else p.LSET(p.F_Cu,p.F_Paste,p.F_Mask))
        if drill:z.SetDrillSize(v(drill,drill));z.SetLayerSet(p.LSET(p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask))
        if c['nets'][no]:z.SetNet(nets[c['nets'][no]])
        fp.Add(z);pads[(ref,no)]=(x+xx,y+yy)
    for x1,y1,x2,y2 in [(-cx,-1.6,cx,-1.6),(cx,-1.6,cx,cy),(cx,cy,-cx,cy),(-cx,cy,-cx,-1.6)]:shape_line(fp,x1,y1,x2,y2,p.F_CrtYd,.05)
    if kind=='G14':
        for x1,y1,x2,y2 in [(-.8,-1.45,.8,-1.45),(.8,-1.45,.8,1.45),(.8,1.45,-.8,1.45),(-.8,1.45,-.8,-1.45)]:shape_line(fp,x1,y1,x2,y2,p.F_Fab,.1)
    p.FootprintSave(str(libpath),fp);fp.SetPosition(v(x,y));b.Add(fp)
def track(n,points,layer=p.F_Cu,width=.25):
    for a,z in zip(points,points[1:]):
        if a==z:continue
        s=p.PCB_TRACK(b);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetLayer(layer);s.SetWidth(mm(width));s.SetNet(nets[n]);b.Add(s)
def via(n,x,y):
    z=p.PCB_VIA(b);z.SetPosition(v(x,y));z.SetWidth(mm(.65));z.SetDrill(mm(.3));z.SetViaType(p.VIATYPE_THROUGH);z.SetLayerPair(p.F_Cu,p.B_Cu);z.SetNet(nets[n]);b.Add(z)
def route_gnd(ref,no,dx=0,dy=1.5):
    x,y=pads[ref,str(no)];track('GND',[(x,y),(x+dx,y+dy)]);via('GND',x+dx,y+dy)
for i,n in enumerate(['A_MIN','A_MAX','B_MIN','B_MAX']):
    k=i+1;y=116+12*i
    track('LOOP_'+n,[(108,y-2),(114,y-2),(116,y),(117.05,y)])
    track('FILT_'+n,[(118.95,y),(128.7,y)])
    track('FILT_'+n,[(123.05,y-5),(122,y-5),(122,y)])
    track('FILT_'+n,[(124.95,y+4),(126,y+4),(126,y)])
    track('BUF_'+n,[(131.3,y+.95),(137.05,y+.95)])
    track('ALLOW_'+n,[(138.95,y+.95),(164,y+.95)])
    track('ALLOW_'+n,[(145.95,y+4),(145.95,y+.95)])
    track('3V3',[(131.3,y-.95),(133.05,y-2.7),(133.05,y-3)],width=.35)
    route_gnd('U'+str(k),3,0,1.5);route_gnd(f'C{k}1',1,0,1.5);route_gnd(f'C{k}2',2,1,0);route_gnd(f'R{k}4',1,0,1.5)
track('RESET_AB',[(140,160),(146.05,160)]);track('RESET_CD',[(155,160),(161.05,160)])
route_gnd('R51',2,0,1.5);route_gnd('R52',2,0,1.5)
for a,z in [((102,101),(170,101)),((170,101),(170,167)),((170,167),(102,167)),((102,167),(102,101))]:
    s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetWidth(mm(.05));s.SetLayer(p.Edge_Cuts);b.Add(s)
for layer,n in [(p.F_Cu,'3V3'),(p.B_Cu,'GND')]:
    z=p.ZONE(b);z.SetLayer(layer);z.SetNet(nets[n]);z.SetLocalClearance(mm(.3));z.SetThermalReliefGap(mm(.3));z.SetThermalReliefSpokeWidth(mm(.3));z.SetPadConnection(p.ZONE_CONNECTION_FULL)
    poly=z.Outline();poly.NewOutline()
    for x,y in [(102.5,101.5),(169.5,101.5),(169.5,166.5),(102.5,166.5)]:poly.Append(mm(x),mm(y))
    b.Add(z)
for x,y,t,size in [(121,105,'LIMIT4 R0',1.5),(126,164.5,'DRAFT - NO MOTOR POWER',1),(155,103,'3V3 ONLY',.9),(150,111,'GND',.85)]+[(162,113+12*i,n,.9) for i,n in enumerate(['A-MIN','A-MAX','B-MIN','B-MAX'])]:
    s=p.PCB_TEXT(b);s.SetText(t);s.SetPosition(v(x,y));s.SetTextSize(v(size,size));s.SetTextThickness(mm(.15));s.SetLayer(p.F_SilkS);b.Add(s)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'limit4.kicad_pcb'),b)
(D/'fp-lib-table').write_text('(fp_lib_table (lib (name "LIMIT4")(type "KiCad")(uri "${KIPRJMOD}/LIMIT4.pretty")(options "")(descr "Project-local prototype footprints")))\n')
(D/'limit4.kicad_pro').write_text(json.dumps({'meta':{'filename':'limit4.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.2,'min_track_width':.2,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_hole_clearance':.25,'min_copper_edge_clearance':.3}}}},indent=2))
with (D/'BOM.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['Reference','Value','Candidate_MPN','Footprint','Qualification'])
    for c in comps:w.writerow([c['ref'],c['value'],c['mpn'],'DBV-5' if c['kind']=='G14' else '0805' if c['kind'] in ['R','C'] else '1mm solder-wire holes','Exact TI IC checked; passive sourcing/assembly approval pending' if c['mpn'] else 'Wire termination only; no mating connector claimed'])
print('Generated',len(comps),'components',len(netnames),'nets. Prototype geometry68x66mm; no fabrication release.')
