from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math
D = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
RED = (211, 15, 68); INK = (27, 28, 31); BG = (247, 247, 248); WHITE = (255, 255, 255)
F = lambda n, s: ImageFont.truetype("C:/Windows/Fonts/" + n, s)
SB = "segoeuib.ttf"

def ctext(d, y, t, font, fill, sp=0, cx=W / 2):
    ws = [d.textlength(c, font=font) for c in t]
    tw = sum(ws) + sp * (len(t) - 1); x = cx - tw / 2
    for c, w in zip(t, ws):
        d.text((x, y), c, font=font, fill=fill); x += w + sp

# --- simgeler (merkez cx,cy; boy s) ---
def batarya(d, cx, cy, s, c, lw):
    w, h = s * 1.1, s * 0.6
    d.rounded_rectangle([cx - w/2, cy - h/2, cx + w/2, cy + h/2], radius=s*0.08, outline=c, width=lw)
    d.rounded_rectangle([cx + w/2, cy - h*0.2, cx + w/2 + s*0.09, cy + h*0.2], radius=s*0.03, fill=c)
    for i in range(3):
        x0 = cx - w/2 + s*0.12 + i * s*0.3
        d.rounded_rectangle([x0, cy - h/2 + s*0.12, x0 + s*0.22, cy + h/2 - s*0.12], radius=s*0.03, fill=c)

def ekran(d, cx, cy, s, c, lw):
    w, h = s * 1.1, s * 0.72
    d.rounded_rectangle([cx - w/2, cy - h/2 - s*0.08, cx + w/2, cy + h/2 - s*0.08], radius=s*0.06, outline=c, width=lw)
    d.line([cx - w*0.62, cy + h/2 + s*0.08, cx + w*0.62, cy + h/2 + s*0.08], fill=c, width=lw)

def klavye(d, cx, cy, s, c, lw):
    w, h = s * 1.2, s * 0.66
    d.rounded_rectangle([cx - w/2, cy - h/2, cx + w/2, cy + h/2], radius=s*0.08, outline=c, width=lw)
    k = s * 0.13; g = s * 0.06
    for r in range(2):
        for i in range(6):
            x0 = cx - w/2 + s*0.11 + i * (k + g*0.55); y0 = cy - h/2 + s*0.12 + r * (k + g)
            d.rounded_rectangle([x0, y0, x0 + k, y0 + k], radius=s*0.02, fill=c)
    d.rounded_rectangle([cx - s*0.3, cy + h/2 - s*0.22, cx + s*0.3, cy + h/2 - s*0.1], radius=s*0.02, fill=c)

def fan(d, cx, cy, s, c, lw):
    r = s * 0.5
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=lw)
    for i in range(5):
        a = math.radians(i * 72)
        pts = []
        for t in range(0, 11):
            aa = a + t * 0.06; rr = s*0.1 + (s*0.3) * t / 10
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        for t in range(10, -1, -1):
            aa = a + 0.55 + t * 0.03; rr = s*0.1 + (s*0.3) * t / 10
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        d.polygon(pts, fill=c)
    d.ellipse([cx - s*0.1, cy - s*0.1, cx + s*0.1, cy + s*0.1], fill=c)

IK = [(batarya, "Batarya"), (ekran, "Ekran"), (klavye, "Klavye"), (fan, "Fan")]

def simge_sira(d, y, s, renk, yazi_renk, xs):
    f = F(SB, 46)
    for (fn, ad), x in zip(IK, xs):
        fn(d, x, y, s, renk, max(6, s // 18))
        ctext(d, y + s * 0.62, ad, f, yazi_renk, cx=x)

# A — koyu, büyük iki satır yazı + 4 simge (simgeler ikişer yanlara, alt-orta boş)
a = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(a)
ctext(d, 150, "LAPTOP", F(SB, 190), WHITE, sp=18)
ctext(d, 360, "YEDEK PARÇA", F(SB, 120), RED, sp=14)
simge_sira(d, 740, 150, WHITE, (200, 202, 206), [260, 560, 1360, 1660])
a.save(D + "/kapak2-a.png")

# B — açık zemin, simgeler üst sırada, yazı altta-üstte
b = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(b)
simge_sira(d, 250, 170, INK, (98, 102, 110), [390, 770, 1150, 1530])
d.rectangle([(W//2 - 80, 500), (W//2 + 80, 510)], fill=RED)
ctext(d, 560, "Laptop Yedek Parça", F(SB, 120), INK)
b.save(D + "/kapak2-b.png")

# C — kırmızı zemin, büyük beyaz yazı + silik dev simgeler
c = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(c)
ghost = (225, 45, 92)
fan(d, 1700, 260, 520, ghost, 30); batarya(d, 230, 860, 420, ghost, 26)
ctext(d, 230, "LAPTOP YEDEK PARÇA", F(SB, 130), WHITE, sp=10)
ctext(d, 430, "Batarya · Ekran · Klavye · Fan", F(SB, 66), (255, 225, 233))
c.save(D + "/kapak2-c.png")

prev = Image.new("RGB", (3 * 520 + 80, 420), WHITE); pd = ImageDraw.Draw(prev)
for i, (im, t) in enumerate([(a, "A"), (b, "B"), (c, "C")]):
    x = 20 + i * 540; prev.paste(im.resize((520, 293), Image.LANCZOS), (x, 40))
    pd.ellipse([(x + 205, 283), (x + 315, 393)], fill=WHITE, outline=(200, 200, 200), width=3)
    pd.text((x + 238, 322), "PP", font=F(SB, 30), fill=(170, 170, 170))
    pd.text((x, 5), t, font=F(SB, 26), fill=INK)
prev.save(D + "/onizleme2.png")
print("tamam")
