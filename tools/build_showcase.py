#!/usr/bin/env python3
"""Build a portfolio cover from the actual committed CAD export, not an invented board."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json

root = Path(__file__).resolve().parents[1]
out = root/'showcase'
out.mkdir(exist_ok=True)
font_root = Path('/usr/share/fonts/truetype/dejavu')
def font(size, bold=False):
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype(str(font_root/name), size)

img = Image.new('RGB', (1440, 790), '#f5f4ef')
d = ImageDraw.Draw(img)
ink, sub, accent = '#162c3c', '#4f5b62', '#176765'
d.rectangle((52,54,94,59), fill=accent)
d.text((112,41), 'HARDWARE DESIGN PORTFOLIO', font=font(22,True), fill=ink)
d.text((52,117), 'LIMIT4', font=font(110,True), fill=ink)
d.text((56,269), 'Limit feedback for', font=font(42,True), fill=ink)
d.text((56,325), 'dual-actuator projects.', font=font(42,True), fill=ink)
d.text((56,413), 'A four-channel input board,', font=font(29), fill=sub)
d.text((56,456), 'with an explicit motion-state model.', font=font(29), fill=sub)
for x, value, title in [(56,'04','LIMIT INPUTS'),(282,'02','TARGET AXES'),(510,'02','PCB LAYERS')]:
    d.text((x,548), value, font=font(43,True), fill=accent)
    d.text((x,606), title, font=font(16,True), fill=sub)
d.rounded_rectangle((823,88,1392,682),radius=18,fill='#ffffff',outline='#d9dedc',width=2)
source = root/'build/pcb-top.png'
board = Image.open(source).convert('RGB')
board.thumbnail((505,490),Image.Resampling.LANCZOS)
img.paste(board,(1107-board.width//2,119))
d.text((851,631), 'Actual CAD export. No assembled board.',font=font(20),fill=sub)
d.line((54,714,1390,714),fill='#d4dad7',width=2)
d.text((56,741), 'R0 engineering prototype',font=font(22,True),fill=ink)
d.text((823,741), 'Physical validation pending',font=font(22),fill=sub)
img.save(out/'cover.png',optimize=True)
(out/'asset-provenance.json').write_text(json.dumps({'source':'build/pcb-top.png','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'operation':'Resize and place the unchanged CAD export in a typographic layout','photo_or_render_claim':'CAD copper-layer export only; no assembled hardware depicted','content_status':'Unbuilt engineering prototype'},indent=2)+'\n')
print('Portfolio cover generated from the actual board export.')
