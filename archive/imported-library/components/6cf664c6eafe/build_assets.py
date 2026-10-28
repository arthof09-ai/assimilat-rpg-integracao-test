#!/usr/bin/env python3
"""Small CC0-independent, original synthetic sprite/tiles export smoke test.
NOT a gameplay engine, NOT final art, NOT VLAB mechanics.
"""
from PIL import Image, ImageDraw
from pathlib import Path
import json,hashlib
P=Path(__file__).parent
cell=24
D=['sul','norte','oeste','leste']
colors={'mestre_test':('#568cda','#c5e8f5'),'inimigo_test':('#ad465f','#ffe3ae')}
for name,(clothes,accent) in colors.items():
    img=Image.new('RGBA',(cell*2,cell*4))
    for row,direction in enumerate(D):
        for frame in range(2):
            r=Image.new('RGBA',(cell,cell)); dr=ImageDraw.Draw(r)
            step=frame
            # Original 24px prototype: feet shadow + cloak + hair + face / back by direction
            dr.ellipse((6,21,20,23), fill=(0,0,0,75))
            dr.rectangle((7,13,17,21),fill=clothes)
            dr.polygon([(8,15),(5,21),(20,21),(17,15)], fill=clothes)
            dr.rectangle((9,20-step,11,22-step),fill='#423729')
            dr.rectangle((14,20+step,16,22+step),fill='#423729')
            if direction=='norte':
                dr.ellipse((7,4,18,15),fill='#382e2b')
                dr.rectangle((9,10,16,13),fill='#6e4d42')
            else:
                dr.ellipse((7,4,18,15),fill='#d9a17b')
                dr.pieslice((7,3,19,14),180,360,fill='#382e2b')
                if direction=='sul':dr.point((10,12),fill='#302324');dr.point((15,12),fill='#302324')
                elif direction=='oeste':dr.point((9,12),fill='#302324')
                else:dr.point((16,12),fill='#302324')
            dr.rectangle((7,16,17,17),fill=accent)
            img.paste(r,(frame*cell,row*cell),r)
    img.save(P/f'{name}_sprite_atlas.png')
# Separate neutral tiles, procedural and fully original
palettes={
 'grama':('#3b7250','#559061','#6ba56c'),
 'pedra':('#484e63','#626a79','#868c93'),
 'agua':('#23637f','#2f8db3','#92d2d6')
}
for name,cols in palettes.items():
    tile=Image.new('RGBA',(cell,cell),cols[0]);dr=ImageDraw.Draw(tile)
    for i in range(7):
        x=(i*13+3)%cell;y=(i*11+7)%cell
        dr.line((x,y,min(x+4,cell-1),y),fill=cols[1],width=1)
        if name=='agua': dr.point(((x+1)%cell,(y+1)%cell),fill=cols[2])
        else: dr.point((x,y-1),fill=cols[2])
    tile.save(P/f'base_{name}.png')
manifest={"schema":"assimilat.visual.asset-proof.v1","status":"SINTETICO_TEST_NAO_CANONICO","frame_size":24,"fps_preview":6,
          "directions":D,"frames_per_direction":2,"resources":{}}
for f in sorted(P.glob('*.png')):
    if f.name.startswith('contact_') or f.name.startswith('hi_'): continue
    im=Image.open(f)
    manifest['resources'][f.name]={"bytes":f.stat().st_size,"dimensions":list(im.size),"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
(P/'MANIFESTO_ASSETS_TEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v['dimensions'] for k,v in manifest['resources'].items()}))
