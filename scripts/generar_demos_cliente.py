#!/usr/bin/env python3
"""
FM105 ONE — demos PNG estilo referencia ChatGPT (SaaS empresarial).
Salida: cliente-demos/*.png
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "demo" / "assets"
OUT = ROOT / "cliente-demos"
ART = Path("/opt/cursor/artifacts/screenshots")

NAVY = (10, 26, 48)
NAVY2 = (20, 39, 78)
RED = (217, 32, 39)
YELLOW = (255, 205, 60)
BG = (241, 244, 248)
WHITE = (255, 255, 255)
INK = (33, 37, 41)
MUTED = (108, 117, 125)
OK = (40, 167, 69)
BLUE = (13, 110, 253)
LINE = (222, 226, 230)
SIDE = (10, 22, 40)

W, H = 1600, 1000
RNG = random.Random(105)


def F(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    )
    return ImageFont.truetype(path, size)


def rr(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def logo(h=48):
    im = Image.open(ASSETS / "logo-fm105.png").convert("RGBA")
    return im.resize((max(1, int(im.width * h / im.height)), h), Image.Resampling.LANCZOS)


def talent(name: str, size=(240, 280)):
    im = Image.open(ASSETS / "locutores" / name).convert("RGBA")
    tw, th = size
    w, h = im.size
    s = max(tw / w, th / h)
    im = im.resize((int(w * s), int(h * s)), Image.Resampling.LANCZOS)
    nw, nh = im.size
    left = (nw - tw) // 2
    top = max(0, int((nh - th) * 0.1))
    return im.crop((left, top, left + tw, top + th))


def paste_r(base, im, xy, r=14):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    base.paste(im, xy, m)


def card(base, box, r=14, fill=WHITE):
    x1, y1, x2, y2 = box
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x1 + 2, y1 + 4, x2 + 2, y2 + 4), r, fill=(0, 0, 0, 35))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(base).rounded_rectangle(box, r, fill=fill)


def save(im: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB")
    rgb.save(OUT / name, "PNG", optimize=True)
    rgb.save(ART / name, "PNG", optimize=True)
    print("OK", name)


def sidebar(im, active, items):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 248, H), fill=SIDE)
    lg = logo(38)
    im.paste(lg, (16, 20), lg)
    d.text((72, 24), "FM105 ONE", font=F(16, True), fill=WHITE)
    d.text((72, 46), "SaaS Radio", font=F(11), fill=(150, 160, 175))
    y = 105
    for it in items:
        if it == active:
            rr(d, (10, y - 6, 236, y + 34), 10, (30, 48, 78))
            d.rectangle((10, y - 6, 15, y + 34), fill=YELLOW)
            col = WHITE
            bold = True
        else:
            col = (165, 175, 190)
            bold = False
        d.text((34, y + 4), it, font=F(14, bold), fill=col)
        y += 46


def wave(d, x, y, w, h, color=RED, n=40):
    bw = w / n
    for i in range(n):
        bh = h * (0.2 + 0.8 * abs(math.sin(i / 2.8)) * (0.5 + 0.5 * RNG.random()))
        bx = x + i * bw
        by = y + (h - bh) / 2
        rr(d, (bx, by, bx + bw * 0.5, by + bh), 2, color)


def pill(d, x, y, text, bg, fg):
    f = F(11, True)
    tw = d.textlength(text, font=f)
    rr(d, (x, y, x + tw + 18, y + 24), 12, bg)
    d.text((x + 9, y + 5), text, font=f, fill=fg)


# ═══════════════════════════════════════════════════════════
# 01 PORTAL — como referencia ChatGPT (header blanco + hero + cards)
# ═══════════════════════════════════════════════════════════
def demo_portal():
    im = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(im)

    # header blanco
    d.rectangle((0, 0, W, 70), fill=WHITE)
    d.line((0, 70, W, 70), fill=LINE)
    lg = logo(42)
    im.paste(lg, (32, 14), lg)
    nav = ["Inicio", "En Vivo", "Noticias", "Programación", "Locutores", "Podcasts", "Contacto"]
    x = 260
    for n in nav:
        d.text((x, 26), n, font=F(13), fill=MUTED)
        x += 100
    for i, c in enumerate([RED, NAVY2, YELLOW, MUTED]):
        d.ellipse((1295 + i * 26, 26, 1311 + i * 26, 42), fill=c)
    rr(d, (1410, 16, 1568, 54), 20, RED)
    d.text((1430, 27), "Escuchar en Vivo", font=F(13, True), fill=WHITE)

    # HERO full-bleed con fotos
    d.rectangle((0, 70, W, 420), fill=NAVY)
    # foto collage fondo
    files = [
        "gerardo-castro.png",
        "ivan-vaca.png",
        "karla-montano.png",
        "ramon-barrera.png",
    ]
    for i, f in enumerate(files):
        t = talent(f, (400, 350))
        paste_r(im, t, (200 + i * 360, 70), 0)
    # overlay oscuro
    overlay = Image.new("RGBA", (W, 350), (10, 26, 48, 165))
    im.paste(overlay, (0, 70), overlay)
    d = ImageDraw.Draw(im)
    d.text((48, 130), "FM105  ·  Guaymas, Sonora", font=F(14, True), fill=YELLOW)
    d.text((48, 170), "La Madre de Todas", font=F(52, True), fill=WHITE)
    d.text((48, 240), "Noticias, música regional y la voz de casa.", font=F(18), fill=(220, 228, 238))
    rr(d, (48, 290, 290, 345), 24, RED)
    d.text((78, 307), "▶  Escuchar en Vivo", font=F(16, True), fill=WHITE)
    wave(d, 320, 300, 280, 40, YELLOW, 32)

    # mini fotos con nombre
    names = ["Gerardo", "Iván", "Karla", "Ramón"]
    for i, (f, name) in enumerate(zip(files, names)):
        t = talent(f, (150, 170))
        x0 = 920 + i * 165
        paste_r(im, t, (x0, 140), 12)
        rr(d, (x0, 285, x0 + 150, 318), 0, RED)
        d.text((x0 + 12, 292), name, font=F(14, True), fill=WHITE)

    # fila widgets
    card(im, (32, 450, 420, 700))
    d = ImageDraw.Draw(im)
    d.text((52, 470), "AHORA SUENA", font=F(11, True), fill=RED)
    d.text((52, 500), "Despierta Guaymas", font=F(24, True), fill=NAVY2)
    t = talent("gerardo-castro.png", (64, 72))
    paste_r(im, t, (52, 555), 10)
    d = ImageDraw.Draw(im)
    d.text((132, 568), "Gerardo Castro", font=F(15, True), fill=INK)
    d.text((132, 592), "06:00 – 10:00", font=F(13), fill=MUTED)
    d.ellipse((52, 655, 68, 671), fill=OK)
    d.text((80, 654), "EN VIVO · 1,284 oyentes", font=F(13, True), fill=OK)

    card(im, (440, 450, 820, 700))
    d = ImageDraw.Draw(im)
    d.text((460, 470), "PRÓXIMO PROGRAMA", font=F(11, True), fill=MUTED)
    d.text((460, 500), "Enlace 105", font=F(24, True), fill=NAVY2)
    t = talent("karla-montano.png", (64, 72))
    paste_r(im, t, (460, 555), 10)
    d = ImageDraw.Draw(im)
    d.text((540, 568), "Karla Montaño", font=F(15, True), fill=INK)
    d.text((540, 592), "10:00 – 14:00", font=F(13), fill=MUTED)
    pill(d, 460, 650, "En 45 min", (255, 243, 205), (154, 116, 0))

    card(im, (840, 450, 1180, 700))
    d = ImageDraw.Draw(im)
    d.text((860, 470), "CLIMA · GUAYMAS", font=F(11, True), fill=MUTED)
    d.text((860, 520), "34°", font=F(48, True), fill=NAVY2)
    d.text((980, 550), "Soleado", font=F(18), fill=MUTED)
    d.text((860, 620), "Viento SO 12 km/h", font=F(13), fill=MUTED)

    card(im, (1200, 450, 1568, 700))
    d = ImageDraw.Draw(im)
    d.text((1220, 470), "CONTACTO", font=F(11, True), fill=MUTED)
    d.text((1220, 510), "¿Quieres mandar\nun saludo?", font=F(20, True), fill=NAVY2)
    rr(d, (1220, 600, 1540, 660), 16, OK)
    d.text((1260, 618), "WhatsApp a cabina", font=F(15, True), fill=WHITE)

    # noticias
    d.text((32, 730), "Noticias destacadas", font=F(20, True), fill=NAVY2)
    news = [
        (NAVY2, "Obras en Unidad Deportiva", "Local · hace 2 h"),
        (RED, "Reapertura ganadera en Sonora", "Estatal · hace 4 h"),
        ((61, 90, 128), "Operativo en zona centro", "Policiaca · ayer"),
        (YELLOW, "Liga de tenis mejora instalaciones", "Deportes · ayer"),
    ]
    for i, (col, title, meta) in enumerate(news):
        x1 = 32 + i * 390
        card(im, (x1, 770, x1 + 375, 970))
        d = ImageDraw.Draw(im)
        rr(d, (x1 + 14, 788, x1 + 361, 880), 10, col)
        d.text((x1 + 14, 900), title, font=F(14, True), fill=INK)
        d.text((x1 + 14, 930), meta, font=F(12), fill=MUTED)

    save(im, "01-portal-publico.png")


# ═══════════════════════════════════════════════════════════
# 02 SISTEMA COMERCIAL
# ═══════════════════════════════════════════════════════════
def demo_comercial():
    im = Image.new("RGBA", (W, H), BG)
    sidebar(im, "Ventas", ["Dashboard", "Clientes", "Cotizaciones", "Órdenes", "Ventas", "Facturación", "Cobranza"])
    d = ImageDraw.Draw(im)
    d.text((275, 24), "Sistema Comercial — Ventas", font=F(26, True), fill=NAVY2)
    d.text((275, 60), "Julio 2026  ·  FM105 Guaymas", font=F(13), fill=MUTED)
    rr(d, (1385, 26, 1565, 62), 18, RED)
    d.text((1415, 36), "+ Nueva orden", font=F(13, True), fill=WHITE)

    kpis = [
        ("$215,450", "Ventas del mes", "+12.4%"),
        ("28", "Órdenes activas", "+3"),
        ("$185,300", "Ingresos del mes", "+8.1%"),
        ("78%", "Ocupación inventario", "+5%"),
    ]
    for i, (v, l, g) in enumerate(kpis):
        x = 275 + i * 325
        card(im, (x, 100, x + 310, 215))
        d = ImageDraw.Draw(im)
        d.text((x + 20, 118), l, font=F(12), fill=MUTED)
        d.text((x + 20, 145), v, font=F(28, True), fill=NAVY2)
        d.text((x + 20, 185), g + " vs mes ant.", font=F(12, True), fill=OK)

    card(im, (275, 235, 980, 580))
    d = ImageDraw.Draw(im)
    d.text((300, 255), "Ingresos por mes", font=F(16, True), fill=NAVY2)
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"]
    vals = [140, 155, 168, 175, 190, 182, 215]
    base = 520
    for i, (m, v) in enumerate(zip(months, vals)):
        x = 330 + i * 85
        hh = int(v * 1.15)
        rr(d, (x, base - hh, x + 40, base), 8, NAVY2)
        d.text((x + 5, 535), m, font=F(11, True), fill=MUTED)

    card(im, (1000, 235, 1565, 580))
    d = ImageDraw.Draw(im)
    d.text((1025, 255), "Órdenes por estatus", font=F(16, True), fill=NAVY2)
    cx, cy, r = 1220, 400, 95
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=NAVY2)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, 50, fill=OK)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 50, 140, fill=YELLOW)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 140, 210, fill=RED)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 210, 270, fill=MUTED)
    d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=WHITE)
    d.text((cx - 14, cy - 12), "28", font=F(20, True), fill=NAVY2)
    for i, (c, lab) in enumerate([(OK, "Activas 12"), (YELLOW, "Programadas 8"), (RED, "Pendientes 5"), (MUTED, "Canceladas 3")]):
        yy = 330 + i * 36
        d.ellipse((1400, yy, 1416, yy + 16), fill=c)
        d.text((1425, yy - 2), lab, font=F(13), fill=INK)

    card(im, (275, 600, 1565, 900))
    d = ImageDraw.Draw(im)
    d.text((300, 620), "Órdenes recientes", font=F(16, True), fill=NAVY2)
    heads = ["Cliente", "Campaña", "Fecha", "Spots", "Total", "Estatus"]
    xs = [300, 560, 820, 980, 1120, 1320]
    for h, x in zip(heads, xs):
        d.text((x, 655), h.upper(), font=F(11, True), fill=MUTED)
    rows = [
        ("Padilla Hermanos", "Verano 2026", "22 jul", "40", "$48,000", "Activa", (220, 245, 228), OK),
        ("Funeraria San Carlos", "Institucional", "20 jul", "30", "$32,500", "Programada", (220, 237, 255), (0, 86, 179)),
        ("Materiales Moreno", "Promo julio", "18 jul", "24", "$21,800", "Activa", (220, 245, 228), OK),
        ("Autos Guaymas", "Lanzamiento", "15 jul", "18", "$19,200", "Pendiente", (255, 243, 205), (154, 116, 0)),
    ]
    y = 690
    for cli, camp, fecha, spots, total, est, bg, fg in rows:
        d.text((300, y), cli, font=F(14, True), fill=INK)
        d.text((560, y), camp, font=F(13), fill=MUTED)
        d.text((820, y), fecha, font=F(13), fill=MUTED)
        d.text((980, y), spots, font=F(13), fill=MUTED)
        d.text((1120, y), total, font=F(14, True), fill=NAVY2)
        pill(d, 1320, y - 2, est, bg, fg)
        y += 45

    # FABs
    actions = [("+ Cotización", NAVY2), ("+ Orden", RED), ("+ Cliente", (52, 58, 64))]
    x = 275
    for lab, col in actions:
        rr(d, (x, 925, x + 180, 970), 18, col)
        d.text((x + 28, 937), lab, font=F(13, True), fill=WHITE)
        x += 200

    save(im, "02-sistema-comercial.png")


# ═══════════════════════════════════════════════════════════
# 03 CONTINUIDAD
# ═══════════════════════════════════════════════════════════
def demo_continuidad():
    im = Image.new("RGBA", (W, H), BG)
    sidebar(im, "Continuidad", ["Dashboard", "Producción", "Biblioteca", "Continuidad", "Alertas"])
    d = ImageDraw.Draw(im)
    d.text((275, 20), "Continuidad — Operación al aire", font=F(24, True), fill=NAVY2)

    rr(d, (275, 65, 430, 110), 18, RED)
    d.text((295, 77), "●  AL AIRE", font=F(16, True), fill=WHITE)
    d.text((460, 72), "10:15:30", font=F(28, True), fill=NAVY2)
    d.text((460, 108), "a.m.", font=F(12), fill=MUTED)

    # gauge ring
    card(im, (1280, 55, 1565, 200))
    d = ImageDraw.Draw(im)
    d.ellipse((1320, 75, 1420, 175), outline=LINE, width=10)
    d.arc((1320, 75, 1420, 175), start=-90, end=250, fill=OK, width=10)
    d.text((1345, 105), "96%", font=F(22, True), fill=NAVY2)
    d.text((1440, 100), "Cumplimiento", font=F(13, True), fill=NAVY2)
    d.text((1440, 125), "del día", font=F(13), fill=MUTED)

    # spot en aire
    card(im, (275, 220, 900, 480))
    d = ImageDraw.Draw(im)
    rr(d, (295, 240, 880, 460), 14, (230, 248, 237))
    d.text((325, 265), "SPOT EN AIRE", font=F(12, True), fill=OK)
    d.text((325, 300), "Súper del Norte", font=F(32, True), fill=NAVY2)
    d.text((325, 350), "Campaña verano  ·  30 segundos", font=F(15), fill=MUTED)
    d.text((325, 400), "00:04:15", font=F(40, True), fill=OK)
    d.text((560, 420), "restante", font=F(14), fill=MUTED)

    card(im, (920, 220, 1565, 480))
    t = talent("karla-montano.png", (140, 165))
    paste_r(im, t, (950, 260), 14)
    d = ImageDraw.Draw(im)
    d.text((1120, 250), "PROGRAMA ACTUAL", font=F(11, True), fill=RED)
    d.text((1120, 285), "Enlace 105", font=F(26, True), fill=NAVY2)
    d.text((1120, 330), "Karla Montaño", font=F(16), fill=INK)
    d.text((1120, 365), "10:00 – 14:00", font=F(14), fill=MUTED)
    d.text((1120, 415), "Siguiente: Tarde Poderosa · Iván", font=F(13), fill=MUTED)

    card(im, (275, 500, 1565, 880))
    d = ImageDraw.Draw(im)
    d.text((300, 520), "Agenda del día", font=F(16, True), fill=NAVY2)
    for h, x in zip(["HORA", "TIPO", "CONTENIDO", "DURACIÓN", "ESTATUS"], [300, 420, 580, 1180, 1360]):
        d.text((x, 555), h, font=F(11, True), fill=MUTED)
    rows = [
        ("10:12", "Música", "Regional hit — AutoDJ", "03:40", "Al aire", (220, 245, 228), OK),
        ("10:16", "Spot", "Súper del Norte · 30s", "00:30", "Al aire", (220, 245, 228), OK),
        ("10:17", "ID", "Identificador FM105", "00:10", "En espera", (255, 243, 205), (154, 116, 0)),
        ("10:18", "Spot", "Padilla Hermanos · 30s", "00:30", "En espera", (255, 243, 205), (154, 116, 0)),
        ("10:20", "Música", "Éxito grupero", "03:12", "Programado", BG, MUTED),
        ("10:24", "Spot", "Funeraria San Carlos · 20s", "00:20", "Programado", BG, MUTED),
    ]
    y = 590
    for hora, tipo, cont, dur, est, bg, fg in rows:
        d.text((300, y), hora, font=F(13, True), fill=NAVY2)
        pill(d, 420, y - 2, tipo, BG, NAVY2)
        d.text((580, y), cont, font=F(13), fill=INK)
        d.text((1180, y), dur, font=F(13), fill=MUTED)
        pill(d, 1360, y - 2, est, bg, fg)
        y += 42

    for i, (v, l) in enumerate([("152/240", "Spots hoy"), ("8", "Pendientes"), ("2", "Alertas activas")]):
        x = 275 + i * 430
        card(im, (x, 900, x + 415, 975))
        d = ImageDraw.Draw(im)
        d.text((x + 24, 920), v, font=F(22, True), fill=NAVY2)
        d.text((x + 150, 928), l, font=F(14), fill=MUTED)

    save(im, "03-continuidad.png")


# ═══════════════════════════════════════════════════════════
# 04 DASHBOARD CEO
# ═══════════════════════════════════════════════════════════
def demo_ceo():
    im = Image.new("RGBA", (W, H), BG)
    sidebar(im, "CEO", ["CEO", "Ventas", "Cobranza", "Audiencia", "Reportes"])
    d = ImageDraw.Draw(im)
    d.text((275, 20), "Dashboard Gerencial — CEO", font=F(26, True), fill=NAVY2)
    rr(d, (275, 58, 520, 92), 10, WHITE)
    d.text((290, 66), "01 jul – 25 jul 2026", font=F(13), fill=MUTED)
    rr(d, (1290, 28, 1405, 64), 14, WHITE)
    d.text((1330, 38), "PDF", font=F(13, True), fill=NAVY2)
    rr(d, (1425, 28, 1565, 64), 14, YELLOW)
    d.text((1460, 38), "Excel", font=F(13, True), fill=NAVY2)

    for i, (v, l) in enumerate([
        ("$842k", "Ventas"),
        ("$910k", "Facturación"),
        ("$724k", "Cobranza"),
        ("78%", "Inventario"),
        ("128", "Clientes activos"),
    ]):
        x = 275 + i * 258
        card(im, (x, 110, x + 245, 215))
        d = ImageDraw.Draw(im)
        d.text((x + 18, 128), l, font=F(12), fill=MUTED)
        d.text((x + 18, 158), v, font=F(28, True), fill=NAVY2)

    card(im, (275, 235, 1000, 600))
    d = ImageDraw.Draw(im)
    d.text((300, 255), "Ventas vs Meta", font=F(16, True), fill=NAVY2)
    pa, pb = [], []
    for i, (a, b) in enumerate(zip([55, 58, 62, 66, 70, 74, 84], [60, 60, 65, 70, 75, 80, 85])):
        x = 340 + i * 85
        pa.append((x, 540 - a * 3.0))
        pb.append((x, 540 - b * 3.0))
        d.text((x - 10, 555), ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"][i], font=F(11, True), fill=MUTED)
    d.line(pb, fill=YELLOW, width=4)
    d.line(pa, fill=RED, width=4)
    for p in pa:
        d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=RED)
    for p in pb:
        d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=YELLOW)
    d.text((300, 570), "● Ventas   ● Meta", font=F(12, True), fill=MUTED)

    card(im, (1020, 235, 1565, 600))
    d = ImageDraw.Draw(im)
    d.text((1045, 255), "Ingresos por tipo de cliente", font=F(15, True), fill=NAVY2)
    cx, cy, r = 1220, 410, 100
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, 50, fill=NAVY2)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 50, 140, fill=RED)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 140, 220, fill=YELLOW)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 220, 270, fill=MUTED)
    d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=WHITE)
    for i, (c, lab) in enumerate([(NAVY2, "Comercial 42%"), (RED, "Gobierno 28%"), (YELLOW, "Servicios 20%"), (MUTED, "Otros 10%")]):
        yy = 330 + i * 40
        d.ellipse((1395, yy, 1411, yy + 16), fill=c)
        d.text((1420, yy - 2), lab, font=F(13), fill=INK)

    card(im, (275, 620, 700, 960))
    d = ImageDraw.Draw(im)
    d.text((300, 640), "Top 5 anunciantes", font=F(15, True), fill=NAVY2)
    tops = [("Padilla Hermanos", "$128k"), ("Funeraria S. Carlos", "$96k"), ("Materiales Moreno", "$84k"), ("Autos Guaymas", "$71k"), ("Clínica del Puerto", "$58k")]
    y = 690
    for i, (n, v) in enumerate(tops, 1):
        d.text((300, y), f"{i}.  {n}", font=F(14), fill=INK)
        d.text((600, y), v, font=F(14, True), fill=NAVY2)
        y += 45

    card(im, (720, 620, 1120, 960))
    d = ImageDraw.Draw(im)
    d.text((745, 640), "Programas más rentables", font=F(15, True), fill=NAVY2)
    for i, (n, v) in enumerate([("Despierta Guaymas", "28%"), ("Enlace 105", "22%"), ("Tarde Poderosa", "20%"), ("Trayecto a Casa", "18%")]):
        y = 700 + i * 50
        d.text((745, y), n, font=F(14), fill=INK)
        d.text((1020, y), v, font=F(14, True), fill=RED)

    card(im, (1140, 620, 1565, 790))
    d = ImageDraw.Draw(im)
    d.text((1165, 640), "Audiencia estimada", font=F(14, True), fill=NAVY2)
    d.text((1165, 680), "85,400", font=F(36, True), fill=NAVY2)
    d.text((1165, 735), "oyentes / mes", font=F(14), fill=MUTED)

    card(im, (1140, 810, 1565, 960))
    d = ImageDraw.Draw(im)
    d.text((1165, 835), "Mensajes a cabina", font=F(13), fill=MUTED)
    d.text((1165, 865), "1,240", font=F(26, True), fill=NAVY2)
    d.text((1320, 875), "Tickets: 36", font=F(13), fill=MUTED)

    save(im, "04-dashboard-ceo.png")


# ═══════════════════════════════════════════════════════════
# 05 APP MÓVIL
# ═══════════════════════════════════════════════════════════
def phone(base, x, y, w=310, h=640, fill=NAVY):
    d = ImageDraw.Draw(base)
    rr(d, (x, y, x + w, y + h), 38, (25, 25, 30))
    rr(d, (x + 8, y + 8, x + w - 8, y + h - 8), 32, fill)
    rr(d, (x + w // 2 - 42, y + 18, x + w // 2 + 42, y + 34), 10, (12, 12, 14))
    return x + 8, y + 8, w - 16, h - 16


def demo_app():
    im = Image.new("RGBA", (W, H), (228, 232, 238))
    d = ImageDraw.Draw(im)
    d.text((50, 30), "App Móvil — Radioescucha", font=F(28, True), fill=NAVY2)
    d.text((50, 72), "iOS & Android  ·  Player · Noticias · Programación", font=F(15), fill=MUTED)

    # Player
    ix, iy, iw, ih = phone(im, 80, 140)
    d = ImageDraw.Draw(im)
    lg = logo(34)
    im.paste(lg, (ix + 18, iy + 40), lg)
    d = ImageDraw.Draw(im)
    d.text((ix + 18, iy + 100), "EN VIVO", font=F(12, True), fill=YELLOW)
    d.text((ix + 18, iy + 130), "Despierta\nGuaymas", font=F(28, True), fill=WHITE)
    d.text((ix + 18, iy + 220), "Gerardo Castro", font=F(14), fill=(200, 210, 220))
    wave(d, ix + 18, iy + 270, iw - 36, 42, RED, 26)
    d.ellipse((ix + iw // 2 - 38, iy + 345, ix + iw // 2 + 38, iy + 421), fill=RED)
    d.polygon([(ix + iw // 2 - 12, iy + 365), (ix + iw // 2 - 12, iy + 401), (ix + iw // 2 + 20, iy + 383)], fill=WHITE)
    rr(d, (ix + 12, iy + ih - 72, ix + iw - 12, iy + ih - 18), 18, (15, 28, 50))
    for i, lab in enumerate(["Inicio", "Vivo", "News", "Más"]):
        d.text((ix + 28 + i * 68, iy + ih - 52), lab, font=F(11, True), fill=YELLOW if lab == "Vivo" else (150, 160, 175))

    # News
    ix, iy, iw, ih = phone(im, 460, 140, fill=WHITE)
    d = ImageDraw.Draw(im)
    rr(d, (ix, iy, ix + iw, iy + 68), 32, NAVY)
    d.rectangle((ix, iy + 40, ix + iw, iy + 68), fill=NAVY)
    d.text((ix + 18, iy + 26), "Noticias", font=F(18, True), fill=WHITE)
    for i, (col, title) in enumerate([
        (NAVY2, "Obras en Unidad Deportiva"),
        (RED, "Reapertura ganadera"),
        ((61, 90, 128), "Operativo zona centro"),
        (YELLOW, "Liga de tenis Guaymas"),
    ]):
        y = iy + 90 + i * 105
        rr(d, (ix + 12, y, ix + iw - 12, y + 92), 12, BG)
        rr(d, (ix + 22, y + 12, ix + 88, y + 78), 8, col)
        d.text((ix + 100, y + 22), title, font=F(12, True), fill=INK)
        d.text((ix + 100, y + 50), "Hoy · FM105", font=F(11), fill=MUTED)
    rr(d, (ix + 12, iy + ih - 72, ix + iw - 12, iy + ih - 18), 18, NAVY)
    for i, lab in enumerate(["Inicio", "Vivo", "News", "Más"]):
        d.text((ix + 28 + i * 68, iy + ih - 52), lab, font=F(11, True), fill=YELLOW if lab == "News" else (150, 160, 175))

    # Programs
    ix, iy, iw, ih = phone(im, 840, 140, fill=WHITE)
    d = ImageDraw.Draw(im)
    rr(d, (ix, iy, ix + iw, iy + 68), 32, NAVY)
    d.rectangle((ix, iy + 40, ix + iw, iy + 68), fill=NAVY)
    d.text((ix + 18, iy + 26), "Programación", font=F(18, True), fill=WHITE)
    for i, (f, title, hour) in enumerate([
        ("gerardo-castro.png", "Despierta Guaymas", "06:00"),
        ("karla-montano.png", "Enlace 105", "10:00"),
        ("ivan-vaca.png", "Tarde Poderosa", "14:00"),
        ("ramon-barrera.png", "Trayecto a Casa", "18:00"),
    ]):
        y = iy + 95 + i * 95
        t = talent(f, (56, 64))
        paste_r(im, t, (ix + 18, y), 10)
        d = ImageDraw.Draw(im)
        d.text((ix + 90, y + 8), title, font=F(13, True), fill=INK)
        d.text((ix + 90, y + 34), hour + " hrs", font=F(12), fill=MUTED)
    d = ImageDraw.Draw(im)
    rr(d, (ix + 12, iy + ih - 72, ix + iw - 12, iy + ih - 18), 18, NAVY)
    for i, lab in enumerate(["Inicio", "Vivo", "News", "Más"]):
        d.text((ix + 28 + i * 68, iy + ih - 52), lab, font=F(11, True), fill=(150, 160, 175))

    card(im, (1220, 180, 1540, 700))
    d = ImageDraw.Draw(im)
    d.text((1245, 210), "Incluye", font=F(18, True), fill=NAVY2)
    for i, t in enumerate([
        "Splash + Login",
        "Player en vivo",
        "Noticias",
        "Programación",
        "Locutores",
        "Push notifications",
        "Mensaje a cabina",
    ]):
        yy = 270 + i * 50
        d.ellipse((1245, yy + 4, 1263, yy + 22), fill=RED)
        d.text((1280, yy), t, font=F(14), fill=INK)

    save(im, "05-app-movil.png")


# ═══════════════════════════════════════════════════════════
# 06 BROCHURE
# ═══════════════════════════════════════════════════════════
def demo_brochure():
    im = Image.new("RGBA", (W, H), (210, 216, 224))
    # shadow sheet behind
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((250, 110, 1390, 930), 18, fill=(0, 0, 0, 50))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))

    d = ImageDraw.Draw(im)
    rr(d, (220, 80, 1360, 900), 18, WHITE)
    rr(d, (220, 80, 1360, 340), 18, NAVY)
    d.rectangle((220, 280, 1360, 340), fill=NAVY)
    lg = logo(68)
    im.paste(lg, (280, 120), lg)
    d = ImageDraw.Draw(im)
    d.text((280, 210), "FM105 ONE", font=F(44, True), fill=WHITE)
    d.text((280, 275), "Sistema Integral para Radioemisoras", font=F(18), fill=YELLOW)

    d.text((280, 390), "Automatiza, administra y haz crecer\ntu estación de radio.", font=F(26, True), fill=NAVY2)
    d.text(
        (280, 490),
        "Plataforma SaaS multiempresa: portal público, streaming,\nprogramación, continuidad, ventas, CRM, facturación,\nKPIs gerenciales y app móvil.",
        font=F(15),
        fill=MUTED,
    )

    mods = [(RED, "Ventas"), (NAVY2, "Continuidad"), (YELLOW, "Producción"), (OK, "Finanzas"), (BLUE, "Reportes")]
    x = 280
    for c, n in mods:
        rr(d, (x, 640, x + 180, 790), 14, BG)
        d.ellipse((x + 60, 675, x + 120, 735), fill=c)
        d.text((x + 40, 750), n, font=F(14, True), fill=NAVY2)
        x += 200

    d.text((280, 840), "Demo comercial  ·  Tenant piloto: FM105 Guaymas, Sonora", font=F(13), fill=MUTED)
    save(im, "06-brochure-comercial.png")


# ═══════════════════════════════════════════════════════════
# 00 PORTADA + COMPOSITE (como la foto de ChatGPT)
# ═══════════════════════════════════════════════════════════
def demo_portada():
    im = Image.new("RGBA", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    for i in range(16):
        a = max(0, 18 - i)
        d.ellipse((1050 - i * 12, -120, 1900 + i * 12, 720), outline=(217, 32, 39, a * 8) if False else None)
        # solid red glow without alpha issues
    d.ellipse((1100, -80, 1850, 650), fill=(140, 20, 30))
    d.ellipse((1180, -20, 1780, 580), fill=RED)

    lg = logo(72)
    im.paste(lg, (70, 60), lg)
    d = ImageDraw.Draw(im)
    d.text((70, 170), "FM105 ONE", font=F(58, True), fill=WHITE)
    d.text((70, 245), "Paquete de demos visuales", font=F(26), fill=YELLOW)
    d.text((70, 295), "Estilo SaaS empresarial · listo para cliente", font=F(16), fill=(180, 190, 205))

    items = [
        "01  Portal público",
        "02  Sistema comercial",
        "03  Continuidad",
        "04  Dashboard CEO",
        "05  App móvil",
        "06  Brochure comercial",
    ]
    y = 370
    for t in items:
        # solid semi-light navy (NO rgba white — hides text)
        rr(d, (70, y, 720, y + 72), 12, (28, 48, 82))
        d.text((100, y + 22), t, font=F(20, True), fill=WHITE)
        y += 85

    t = talent("gerardo-castro.png", (400, 470))
    paste_r(im, t, (980, 260), 20)
    save(im, "00-portada-demos.png")


def demo_composite():
    """Una sola imagen tipo collage ChatGPT con miniaturas de las 6 demos."""
    files = [
        ("01-portal-publico.png", "Portal Público"),
        ("02-sistema-comercial.png", "Sistema Comercial"),
        ("03-continuidad.png", "Continuidad"),
        ("04-dashboard-ceo.png", "Dashboard CEO"),
        ("05-app-movil.png", "App Móvil"),
        ("06-brochure-comercial.png", "Brochure"),
    ]
    # layout 3x2
    cw, ch = 700, 440
    pad = 24
    out_w = pad * 4 + cw * 3
    out_h = 90 + pad * 3 + ch * 2
    im = Image.new("RGBA", (out_w, out_h), (230, 234, 240))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, out_w, 70), fill=NAVY)
    lg = logo(40)
    im.paste(lg, (20, 14), lg)
    d = ImageDraw.Draw(im)
    d.text((90, 20), "FM105 ONE — Demos visuales (estilo SaaS)", font=F(22, True), fill=WHITE)

    for i, (fn, title) in enumerate(files):
        col, row = i % 3, i // 3
        x = pad + col * (cw + pad)
        y = 90 + row * (ch + pad)
        src = Image.open(OUT / fn).convert("RGB")
        src = src.resize((cw, ch - 40), Image.Resampling.LANCZOS)
        card(im, (x, y, x + cw, y + ch), 12)
        im.paste(src, (x, y))
        d = ImageDraw.Draw(im)
        rr(d, (x, y + ch - 40, x + cw, y + ch), 0, WHITE)
        # fix bottom corners visually
        d.rectangle((x, y + ch - 40, x + cw, y + ch), fill=WHITE)
        d.text((x + 16, y + ch - 30), title, font=F(16, True), fill=NAVY2)

    save(im, "07-mosaico-demos.png")


def main():
    for old in OUT.glob("*.png"):
        old.unlink()
    for old in ART.glob("*.png"):
        if old.name.startswith(("0", "fm105", "01", "02", "03", "04", "05", "06", "07")):
            old.unlink(missing_ok=True)

    demo_portada()
    demo_portal()
    demo_comercial()
    demo_continuidad()
    demo_ceo()
    demo_app()
    demo_brochure()
    demo_composite()


if __name__ == "__main__":
    main()
