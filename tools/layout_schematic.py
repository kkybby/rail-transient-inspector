"""Deterministic schematic presentation pass; electrical net manifest is unchanged."""
from pathlib import Path
import json,math,uuid
r=Path(__file__).resolve().parents[1];f=r/'hardware/limit4.kicad_sch'
s=f.read_text();cs=json.loads((r/'hardware/design.json').read_text())['components'];by={c['ref']:c for c in cs}
def nodes(text):
 out=[];depth=0;quoted=False;escaped=False;start=None
 for i,ch in enumerate(text):
  if quoted:
   if escaped:escaped=False
   elif ch=='\\':escaped=True
   elif ch=='"':quoted=False
   continue
  if ch=='"':quoted=True
  elif ch=='(':
   depth+=1
   if depth==2:start=i
  elif ch==')':
   if depth==2:out.append(text[start:i+1])
   depth-=1
 return out
parts=[]
for node in nodes(s):
 tag=node[1:].split()[0]
 if tag in ['wire','label','junction','no_connect']:continue
 if tag=='symbol':
  ref=next((n.split('"')[3] for n in nodes(node) if n.startswith('(property "Reference"')),None)
  for prop in nodes(node):
   if not prop.startswith('(property "Value"'):continue
   if ref in by and by[ref]['kind']=='J2':
    c=by[ref];x,y=c['sch'];new=f'(property "Value" {json.dumps(c["value"])} (at {x} {y+10.16} 0) (effects (font (size 1 1))))';node=node.replace(prop,new)
   elif ref and ref.startswith('#FLG'):
    node=node.replace(prop,prop[:-2]+' hide))')
 parts.append(node)
def uid(t):return str(uuid.uuid5(uuid.NAMESPACE_URL,'limit4/presentation/'+t))
def wire(a,b):
 if a==b:return
 parts.append(f'(wire (pts (xy {a[0]:.4f} {a[1]:.4f}) (xy {b[0]:.4f} {b[1]:.4f})) (stroke (width 0) (type default)) (uuid "{uid(str((a,b)))}"))')
def label(n,at):parts.append(f'(label {json.dumps(n)} (at {at[0]:.4f} {at[1]:.4f} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid(n+str(at))}"))')
def dot(at):parts.append(f'(junction (at {at[0]:.4f} {at[1]:.4f}) (diameter 0) (color 0 0 0 0) (uuid "{uid("dot"+str(at))}"))')
pins={'R':[('1',-5.08,0,0),('2',5.08,0,180)],'C':[('1',-5.08,0,0),('2',5.08,0,180)],'G14':[('1',-7.62,5.08,0),('2',-7.62,0,0),('3',0,-7.62,90),('4',7.62,0,180),('5',0,7.62,270)],'J1':[('1',0,0,0)],'J2':[('1',7.62,0,180),('2',7.62,-5.08,180)]}
def pt(ref,pin):
 c=by[ref];x,y=c['sch'];a=math.radians(c['rot']);_,px,py,pa=next(z for z in pins[c['kind']] if z[0]==str(pin))
 return (round(x+px*math.cos(a)-py*math.sin(a),4),round(y-px*math.sin(a)-py*math.cos(a),4)),pa+c['rot']
for c in cs:
 for pin,n in c['nets'].items():
  a,angle=pt(c['ref'],pin)
  if n is None:parts.append(f'(no_connect (at {a[0]} {a[1]}) (uuid "{uid(c["ref"]+pin+"NC")}"))')
  if n not in ['3V3','GND']:continue
  t=math.radians(angle);b=(round(a[0]-3.81*math.cos(t),4),round(a[1]+3.81*math.sin(t),4));wire(a,b);label(n,b)
for k in range(1,5):
 n=['A_MIN','A_MAX','B_MIN','B_MAX'][k-1]
 a=pt(f'J{k}',1)[0];b=pt(f'R{k}1',1)[0];wire(a,b);label('LOOP_'+n,(a[0]+1.27,a[1]))
 a=pt(f'R{k}1',2)[0];b=pt(f'U{k}',2)[0];wire(a,b);label('FILT_'+n,(a[0]+5.08,a[1]))
 for ref,pin in [(f'R{k}2',1),(f'C{k}1',2)]:
  t=pt(ref,pin)[0];wire(t,(t[0],a[1]))
 dot((by[f'R{k}2']['sch'][0],a[1]))
 a=pt(f'U{k}',4)[0];b=pt(f'R{k}3',1)[0];wire(a,b);label('BUF_'+n,(a[0]+.0,a[1]))
 a=pt(f'R{k}3',2)[0];b=pt(f'J{k+4}',1)[0];wire(a,b);label('ALLOW_'+n,(a[0]+5.08,a[1]))
 t=pt(f'R{k}4',2)[0];wire(t,(t[0],a[1]));dot((t[0],a[1]))
for j,rr,n in [('J10','R51','RESET_AB'),('J11','R52','RESET_CD')]:
 a=pt(j,1)[0];b=pt(rr,1)[0];wire(a,b);label(n,(a[0]+3.81,a[1]))
for y,n in [(45.72,'3V3'),(58.42,'GND')]:wire((218.44,y),(218.44,y+3.81));label(n,(218.44,y+3.81))
f.write_text('(kicad_sch\n'+'\n'.join(parts)+'\n)\n')
print('Schematic presentation rebuilt from exact pin/net manifest; no electrical changes intended.')
