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

def monitor(d, cx, cy, s, c, lw):
    w, h = s * 1.2, s * 0.68
    top = cy - h/2 - s*0.12
    d.rounded_rectangle([cx - w/2, top, cx + w/2, top + h], radius=s*0.05, outline=c, width=lw)
    d.rectangle([cx - s*0.05, top + h, cx + s*0.05, top + h + s*0.16], fill=c)
    d.rounded_rectangle([cx - s*0.28, top + h + s*0.14, cx + s*0.28, top + h + s*0.2], radius=s*0.03, fill=c)

IK = [(batarya, "Batarya"), (ekran, "Ekran"), (klavye, "Klavye"), (fan, "Fan"), (monitor, "Monitör")]

def simge_sira(d, y, s, renk, yazi_renk, xs, fs):
    f = F(SB, fs)
    for (fn, ad), x in zip(IK, xs):
        fn(d, x, y, s, renk, max(5, s // 16))
        ctext(d, y + s * 0.66, ad, f, yazi_renk, cx=x)

# Site adı üstte, simgeler hemen altında; hepsi yukarı-orta bantta (y≈280–600)
a = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(a)
f = F(SB, 80); t1, t2 = "www.nexusbilisim", ".net"
w1 = d.textlength(t1, font=f); w2 = d.textlength(t2, font=f); x = (W - w1 - w2) / 2
d.text((x, 245), t1, font=f, fill=WHITE); d.text((x + w1, 245), t2, font=f, fill=RED)
simge_sira(d, 385, 64, WHITE, (200, 202, 206), [640, 800, 960, 1120, 1280], 28)
a.save(D + "/kapak7-a.png")

prev = Image.new("RGB", (560 + 780 * 2 + 80, 420), WHITE); pd = ImageDraw.Draw(prev)
prev.paste(a.resize((540, 304), Image.LANCZOS), (20, 40)); pd.text((20, 5), "16:9 tam", font=F(SB, 24), fill=INK)
for i, r in enumerate([2.4, 3.0]):
    h = int(W / r); y0 = (H - h) // 2; th = round(780 / r)
    tel = a.crop((0, y0, W, y0 + h)).resize((780, th), Image.LANCZOS); px = 580 + i * 800
    prev.paste(tel, (px, 40)); pd.text((px, 5), f"telefon taklidi {r}:1", font=F(SB, 24), fill=INK)
    pd.ellipse([(px + 330, 40 + th - 60), (px + 450, 40 + th + 60)], fill=WHITE, outline=(200, 200, 200), width=3)
prev.save(D + "/onizleme7.png")
print("tamam")
