"""Junta fotos lado a lado, com um título em cima de cada uma (antes e depois).

Uso: python3 juntar.py saida.jpg "ANTES · Loja" antes.jpg "DEPOIS · Loja" depois.jpg [...]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) < 4 or len(sys.argv) % 2:
    sys.exit(__doc__)
saida, pares = sys.argv[1], list(zip(sys.argv[2::2], sys.argv[3::2]))
imgs = [Image.open(f).convert('RGB') for _, f in pares]
alt = max(i.height for i in imgs)
imgs = [i.resize((round(i.width * alt / i.height), alt)) if i.height != alt else i for i in imgs]
try:
    fonte = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
except OSError:
    fonte = ImageFont.load_default()
folha = Image.new('RGB', (sum(i.width for i in imgs) + 12 * (len(imgs) - 1), alt + 50), 'white')
d = ImageDraw.Draw(folha)
x = 0
for (titulo, _), im in zip(pares, imgs):
    folha.paste(im, (x, 50))
    d.text((x + 8, 14), titulo, fill='black', font=fonte)
    x += im.width + 12
folha.save(saida, quality=82)
print(saida, folha.size)
