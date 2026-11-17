from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
D = os.path.dirname(os.path.abspath(__file__))
S = "C:/Users/smart/nexus-site-deneme/static/"
W, H = 1920, 1080
RED = (211, 15, 68); INK = (27, 28, 31); BG = (247, 247, 248)
F = lambda n, s: ImageFont.truetype("C:/Windows/Fonts/" + n, s)

def logo(name, w):
    im = Image.open(S + name).convert("RGBA")
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

def ctext(d, y, t, font, fill, sp=0):
    if sp:
        ws = [d.textlength(c, font=font) for c in t]
        tw = sum(ws) + sp * (len(t) - 1); x = (W - tw) / 2
        for c, w in zip(t, ws):
            d.text((x, y), c, font=font, fill=fill); x += w + sp
    else:
        tw = d.textlength(t, font=font); d.text(((W - tw) / 2, y), t, font=font, fill=fill)

# A — koyu zemin, büyük logo, tek satır
a = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(a)
for i in range(0, W + H, 90):  # çok silik çapraz çizgiler (logodaki X'ten)
    d.line([(i, 0), (i - H, H)], fill=(34, 35, 39), width=3)
lg = logo("logo-light.png", 1100); a.paste(lg, ((W - lg.width) // 2, 230), lg)
ctext(d, 620, "LAPTOP YEDEK PARÇA", F("segoeuib.ttf", 64), (235, 236, 238), sp=10)
d.rectangle([(W // 2 - 70, 730), (W // 2 + 70, 738)], fill=RED)
a.save(D + "/kapak-a.png")

# B — açık zemin, kırmızı çapraz şerit
b = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(b)
d.polygon([(1700, 0), (1870, 0), (1350, H), (1180, H)], fill=(252, 231, 238))
d.polygon([(1920, 0), (1960, 0), (1440, H), (1400, H)], fill=RED)
lg = logo("logo.png", 1100); b.paste(lg, ((W - lg.width) // 2, 250), lg)
ctext(d, 640, "Batarya · Ekran · Klavye · Fan", F("segoeuib.ttf", 62), INK)
b.save(D + "/kapak-b.png")

# C — kırmızı zemin, beyaz logo, tek kelime
c = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(c)
g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
gd.ellipse([(W // 2 - 900, -700), (W // 2 + 900, 900)], fill=60)
g = g.filter(ImageFilter.GaussianBlur(160))
c.paste(Image.new("RGB", (W, H), (240, 60, 100)), (0, 0), g)
lg = Image.open(S + "logo-light.png").convert("RGBA")
r, gg, bb, al = lg.split(); white = Image.new("RGBA", lg.size, (255, 255, 255, 255)); white.putalpha(al)
white = white.resize((1100, round(lg.height * 1100 / lg.width)), Image.LANCZOS)
c.paste(white, ((W - 1100) // 2, 240), white)
d = ImageDraw.Draw(c)
ctext(d, 630, "LAPTOP YEDEK PARÇA", F("segoeuib.ttf", 64), (255, 255, 255), sp=10)
c.save(D + "/kapak-c.png")

# Önizleme: telefon boyutunda, profil dairesi alt-ortada
prev = Image.new("RGB", (3 * 520 + 80, 420), (255, 255, 255)); pd = ImageDraw.Draw(prev)
for i, (im, t) in enumerate([(a, "A"), (b, "B"), (c, "C")]):
    x = 20 + i * 540; th = im.resize((520, 293), Image.LANCZOS); prev.paste(th, (x, 40))
    pd.ellipse([(x + 260 - 55, 40 + 293 - 50), (x + 260 + 55, 40 + 293 + 60)], fill=(255, 255, 255), outline=(200, 200, 200), width=3)
    pd.text((x, 5), t, font=F("segoeuib.ttf", 26), fill=INK)
prev.save(D + "/onizleme.png")
print("tamam")
