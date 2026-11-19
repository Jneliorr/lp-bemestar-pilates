"""Monta uma apresentação em MP4 a partir de capturas reais do site.

Requer Pillow e um executável FFmpeg com libx264. As capturas são feitas
pelo navegador e fornecidas em --captures; este script não controla a UI.
"""

import argparse
import array
import math
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SIZE = (1920, 1080)
FPS = 30
INK = '#173e4d'
ICE = '#edf6f9'
PINK = '#c65da2'
MUTED = '#546d77'


def font(size, italic=False, sans=False):
    name = 'space-grotesk.woff2' if sans else 'cormorant-garamond-italic.woff2' if italic else 'cormorant-garamond.woff2'
    return ImageFont.truetype(str(ROOT / 'assets/fonts' / name), size)


def text(draw, position, value, size, color=INK, italic=False, sans=False, anchor=None, spacing=4):
    draw.multiline_text(position, value, font=font(size, italic, sans), fill=color,
                        anchor=anchor, spacing=spacing, align='center' if anchor else 'left')


def background(dark=False):
    image = Image.new('RGB', SIZE, INK if dark else ICE)
    draw = ImageDraw.Draw(image)
    color = '#355564' if dark else '#d5e8ee'
    for inset in range(0, 160, 44):
        draw.ellipse((1510 + inset, -240 + inset, 2240 - inset, 490 - inset), outline=color, width=2)
    draw.line((100, 1000, 1820, 1000), fill='#3b5d6d' if dark else '#c9dfe7', width=1)
    return image


def logo(image, box):
    mark = Image.open(ROOT / 'assets/logo-bem-estar-transparente.png').convert('RGBA')
    mark.thumbnail(box[2:], Image.Resampling.LANCZOS)
    image.paste(mark, (box[0] + (box[2] - mark.width)//2, box[1] + (box[3] - mark.height)//2), mark)


def browser(image, source):
    x, y, w, h = 560, 155, 1260, 752
    shadow = Image.new('RGBA', SIZE)
    ImageDraw.Draw(shadow).rounded_rectangle((x-2, y+16, x+w+2, y+h+18), radius=18, fill=(23,62,77,36))
    image.paste(Image.alpha_composite(image.convert('RGBA'), shadow.filter(ImageFilter.GaussianBlur(22))).convert('RGB'))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((x, y, x+w, y+h), radius=14, fill='#ffffff', outline='#cadfe7', width=1)
    for i, color in enumerate(('#c65da2', '#8dc8dc', '#bfd3db')):
        draw.ellipse((x+22+i*22, y+19, x+31+i*22, y+28), fill=color)
    shot = Image.open(source).convert('RGB')
    # Remove only browser scrollbar pixels from the recorded image edge.
    shot = shot.crop((0,0,shot.width-16,shot.height))
    shot = shot.resize((w-2, h-48), Image.Resampling.LANCZOS)
    image.paste(shot, (x+1, y+47))


def caption(draw, title, subtitle, kicker='CONHEÇA A BEM ESTAR'):
    draw.line((100,242,155,242), fill=PINK, width=3)
    text(draw, (100,190), kicker, 19, MUTED, sans=True)
    text(draw, (100,300), title, 84, spacing=-3)
    text(draw, (100,650), subtitle, 27, MUTED, sans=True, spacing=13)


def foot(draw, label, index, total=8):
    text(draw,(100,1020),'BEM ESTAR FISIO PILATES',18,MUTED,sans=True)
    text(draw,(1818,1020),label,18,MUTED,sans=True,anchor='ra')
    for j in range(total):
        x=850+j*30
        draw.rounded_rectangle((x,1028,x+18,1031),radius=2,fill=PINK if j==index else '#b8d1dc')


def make_slides(captures, work):
    slides=[]
    image=background()
    logo(image,(720,180,480,290))
    draw=ImageDraw.Draw(image)
    text(draw,(960,535),'Conheça o novo site.',110,anchor='ma')
    text(draw,(960,690),'Mente e corpo em completa sintonia.',35,MUTED,sans=True,anchor='ma')
    draw.line((885,812,1035,812),fill=PINK,width=3)
    text(draw,(960,875),'BEM ESTAR FISIO PILATES',20,MUTED,sans=True,anchor='ma')
    slides.append((image,3,'Abertura'))

    scenes=[
        ('01-inicio.jpg','Um primeiro\nolhar para\no bem-estar.','Identidade, acolhimento\ne movimento em uma\nexperiência digital.',7,'VISUAL & IDENTIDADE'),
        ('02-essencia.jpg','Essência em\ncada detalhe.','Uma apresentação próxima\nda marca e do cuidado\nque inspira o studio.',5,'NOSSA ESSÊNCIA'),
        ('03-pilates.jpg','Movimento\ncom cuidado.','Conteúdo para conhecer\no Pilates e encontrar\num ponto de partida.',5,'O PILATES'),
        ('04-debora.jpg','Conheça\na Débora.','Fisioterapeuta e proprietária.\nUma apresentação com\nrosto, história e proximidade.',7,'QUEM CUIDA DE VOCÊ'),
    ]
    for filename,title,subtitle,duration,label in scenes:
        image=background()
        browser(image,captures/filename)
        draw=ImageDraw.Draw(image)
        caption(draw,title,subtitle,label)
        foot(draw,'APRESENTAÇÃO DO SITE',len(slides))
        if filename=='01-inicio.jpg':
            text(draw,(1818,944),'Cenas de Pilates ilustrativas.',17,MUTED,sans=True,anchor='ra')
        slides.append((image,duration,label))

    image=background()
    draw=ImageDraw.Draw(image)
    caption(draw,'No seu ritmo.\nEm qualquer\ntela.','Uma experiência responsiva\npara navegar também\npelo celular.','VERSÃO PARA CELULAR')
    draw.ellipse((980,115,1770,905),fill='#dceef3')
    px,py,pw,ph=1170,105,390,870
    draw.rounded_rectangle((px-12,py-12,px+pw+12,py+ph+12),radius=48,fill=INK)
    shot=Image.open(captures/'05-celular.jpg').convert('RGB')
    shot=shot.crop((0,0,shot.width-12,shot.height)).resize((pw,ph),Image.Resampling.LANCZOS)
    mask=Image.new('L',(pw,ph))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,pw,ph),radius=38,fill=255)
    image.paste(shot,(px,py),mask)
    draw=ImageDraw.Draw(image)
    draw.rounded_rectangle((px+135,py+ph-17,px+255,py+ph-11),radius=3,fill=INK)
    foot(draw,'DESKTOP & CELULAR',len(slides))
    slides.append((image,5,'CELULAR'))

    image=background()
    browser(image,captures/'06-contato.jpg')
    draw=ImageDraw.Draw(image)
    caption(draw,'Comece com\numa conversa.','WhatsApp, telefone\ne localização em um\nsó lugar.','CONTATO DIRETO')
    foot(draw,'PRÓXIMO PASSO: CONVERSAR',len(slides))
    slides.append((image,7,'CONTATO'))

    image=background(dark=True)
    draw=ImageDraw.Draw(image)
    draw.rounded_rectangle((700,125,1220,430),radius=16,fill='#fafcfc')
    logo(image,(720,140,480,275))
    draw=ImageDraw.Draw(image)
    text(draw,(960,490),'Seu próximo passo pode ser leve.',87,'#fafcfc',anchor='ma')
    draw.rounded_rectangle((710,650,1210,730),radius=4,fill='#fafcfc')
    text(draw,(960,671),'(21) 99832-8486',36,INK,sans=True,anchor='ma')
    text(draw,(960,790),'Av. 22 de Maio · Prédio Helix · Torre 1 · Sala 206',28,'#d7e8ef',sans=True,anchor='ma')
    text(draw,(960,845),'Itaboraí · Rio de Janeiro',28,'#d7e8ef',sans=True,anchor='ma')
    text(draw,(960,1020),'BEM ESTAR FISIO PILATES',20,'#bdd4df',sans=True,anchor='ma')
    slides.append((image,6,'Encerramento'))

    for index,(frame,duration,label) in enumerate(slides):
        frame.save(work/f'cena-{index:02d}.png')
    return [(duration,label) for _,duration,label in slides]


def make_music(path, seconds):
    rate=48000
    chords=[(146.832,184.997,220.0,329.628),(123.471,146.832,184.997,220.0),(97.999,123.471,146.832,220.0),(146.832,220.0,293.665,369.994)]
    samples=array.array('h')
    # Original synthesized ambient bed: no downloaded or copyrighted recording.
    for i in range(int(seconds*rate)):
        t=i/rate
        cycle=t/10
        idx=min(int(cycle),len(chords)-1)
        prev=max(0,idx-1)
        blend=min(1.0,max(0.0,(t-idx*10)/2.5)) if idx else 1.0
        blend=blend*blend*(3-2*blend)
        def chord(notes):
            return sum((math.sin(2*math.pi*f*t)+.15*math.sin(2*math.pi*2*f*t)) for f in notes)/4.6
        v=chord(chords[prev])*(1-blend)+chord(chords[idx])*blend
        envelope=min(1,t/3,max(0,(seconds-t)/4))
        v*=.11*envelope*(.93+.07*math.sin(t*.7))
        samples.append(round(max(-1,min(1,v))*32767))
    with wave.open(str(path),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(samples.tobytes())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--ffmpeg',type=Path,required=True)
    parser.add_argument('--captures',type=Path,required=True)
    parser.add_argument('--work',type=Path,default=ROOT/'outputs/video-site')
    parser.add_argument('--output',type=Path,default=ROOT/'media/apresentacao-bem-estar-pilates-sem-link.mp4')
    args=parser.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    scenes=make_slides(args.captures,args.work)
    total=sum(duration for duration,_ in scenes)
    assert total==45
    music=args.work/'trilha-original.wav'
    if not music.exists():make_music(music,total)
    listing=[]
    for index,(duration,label) in enumerate(scenes):
        output=args.work/f'cena-{index:02d}.mp4'
        print(f'Renderizando {index+1}/{len(scenes)}: {label}',flush=True)
        video_filter=(f"scale=2880:1620,zoompan=z='min(zoom+0.00007,1.016)':"
                      f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={duration*FPS}:s=1920x1080:fps={FPS},"
                      f'fade=t=in:st=0:d=0.28:color=0xedf6f9,fade=t=out:st={duration-.28}:d=0.28:color=0xedf6f9,format=yuv420p')
        subprocess.run([str(args.ffmpeg),'-hide_banner','-loglevel','error','-y','-loop','1','-i',str(args.work/f'cena-{index:02d}.png'),
                        '-vf',video_filter,'-t',str(duration),'-an','-c:v','libx264','-preset','fast','-crf','20','-threads','4',str(output)],check=True)
        listing.append("file '"+output.name+"'")
    manifest=args.work/'sequencia.txt'
    manifest.write_text('\n'.join(listing),encoding='utf-8')
    subprocess.run([str(args.ffmpeg.resolve()),'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',manifest.name,'-i',music.name,
                    '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-af','volume=1.8','-movflags','+faststart','-shortest',str(args.output.resolve())],
                   cwd=args.work.resolve(),check=True)
    print(f'Vídeo pronto: {args.output.resolve()} ({total}s, 1920x1080, 30fps)',flush=True)


if __name__=='__main__':main()
