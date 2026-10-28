import cv2, subprocess, json, hashlib, os, math
from PIL import Image, ImageDraw, ImageFont
base='/mnt/data/playlist_20261024'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(font,17); items=[]
for stem in ['496150','496165','496174','496183','496192','496201','496210']:
 path=f'/mnt/data/{stem}.mp4'; info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',path])); dur=float(info['format']['duration']);
 cap=cv2.VideoCapture(path)
 ts=[(i+0.5)*dur/28 for i in range(28)]
 sheets=[]
 for group in range(2):
  canvas=Image.new('RGB',(4*270,4*490),(19,24,33)); d=ImageDraw.Draw(canvas)
  for n in range(14):
   ix=group*14+n
   t=ts[ix]
   cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
   ok,bgr=cap.read()
   if not ok:continue
   rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
   im=Image.fromarray(rgb);im.thumbnail((262,464))
   x=(n%4)*270 +(270-im.width)//2;y=(n//4)*490+25
   canvas.paste(im,(x,y));d.text(((n%4)*270+7,(n//4)*490+3),f'{stem} {t//60:.0f}:{int(t%60):02d}',fill='white',font=f)
  p=f'{base}/contact/{stem}_{group+1}.jpg';canvas.save(p,quality=85)
 cap.release();items.append(dict(stem=stem,duration=dur,sha256=hashlib.sha256(open(path,'rb').read()).hexdigest(),bytes=os.stat(path).st_size,subtitle_streams=sum(s.get('codec_type')=='subtitle' for s in info['streams']),contact=sheets))
 print(stem,round(dur,1),flush=True)
with open(base+'/media_manifest.json','w') as out:json.dump(items,out,ensure_ascii=False,indent=2)
