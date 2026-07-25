#!/usr/bin/env python3
"""
FM105 ONE — demos PNG fieles a la referencia ChatGPT (foto enviada).
Página web pública oscura · Módulo ventas · KPI gerenciales · collage.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "demo" / "assets"
OUT = ROOT / "cliente-demos"
ART = Path("/opt/cursor/artifacts/screenshots")

# Paleta referencia ChatGPT
DARK = (22, 28, 36)
DARK2 = (32, 40, 52)
SIDE = (28, 34, 44)
NAVY = (20, 39, 78)
RED = (220, 38, 38)
YELLOW = (255, 204, 0)
BLUE = (37, 99, 235)
CYAN = (14, 165, 233)
GREEN = (34, 197, 94)
ORANGE = (249, 115, 22)
PURPLE = (139, 92, 246)
BG = (243, 244, 246)
WHITE = (255, 255, 255)
INK = (17, 24, 39)
MUTED = (107, 114, 128)
LINE = (229, 231, 235)

W, H = 1600, 1000
RNG = random.Random(1053)


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
    # convert palette cleanly
    return im.resize((max(1, int(im.width * h / im.height)), h), Image.Resampling.LANCZOS)


def talent(name: str, size=(220, 260)):
    im = Image.open(ASSETS / "locutores" / name).convert("RGBA")
    tw, th = size
    w, h = im.size
    s = max(tw / w, th / h)
    im = im.resize((int(w * s), int(h * s)), Image.Resampling.LANCZOS)
    nw, nh = im.size
    left = (nw - tw) // 2
    top = max(0, int((nh - th) * 0.08))
    return im.crop((left, top, left + tw, top + th))


def paste_r(base, im, xy, r=12):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    base.paste(im, xy, m)


def card(base, box, r=12, fill=WHITE):
    x1, y1, x2, y2 = box
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x1 + 2, y1 + 3, x2 + 2, y2 + 3), r, fill=(0, 0, 0, 40))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(base).rounded_rectangle(box, r, fill=fill)


def save(im: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB")
    rgb.save(OUT / name, "PNG", optimize=True)
    rgb.save(ART / name, "PNG", optimize=True)
    print("OK", name)


def wave(d, x, y, w, h, color=YELLOW, n=36):
    bw = w / n
    for i in range(n):
        bh = h * (0.18 + 0.82 * abs(math.sin(i / 2.6)) * (0.45 + 0.55 * RNG.random()))
        bx = x + i * bw
        by = y + (h - bh) / 2
        rr(d, (bx, by, bx + bw * 0.45, by + bh), 2, color)


def pill(d, x, y, text, bg, fg):
    f = F(11, True)
    tw = d.textlength(text, font=f)
    rr(d, (x, y, x + tw + 16, y + 22), 11, bg)
    d.text((x + 8, y + 4), text, font=f, fill=fg)


def icon_circle(d, cx, cy, r, fill, glyph="●"):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    d.text((cx - 6, cy - 10), glyph, font=F(14, True), fill=WHITE)


def sidebar_admin(im, active, items):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 250, H), fill=SIDE)
    lg = logo(36)
    im.paste(lg, (14, 16), lg)
    d.text((68, 20), "FM105 ONE", font=F(15, True), fill=WHITE)
    d.text((68, 42), "Admin", font=F(11), fill=(156, 163, 175))
    y = 90
    for it in items:
        if it == active:
            rr(d, (10, y - 5, 238, y + 32), 8, (45, 55, 72))
            d.rectangle((10, y - 5, 14, y + 32), fill=RED)
            col, bold = WHITE, True
        else:
            col, bold = (156, 163, 175), False
        d.text((32, y + 4), it, font=F(13, bold), fill=col)
        y += 40


# ═══════════════════════════════════════════════
# 01 PÁGINA WEB PÚBLICA (tema oscuro ChatGPT)
# ═══════════════════════════════════════════════
def demo_portal():
    im = Image.new("RGBA", (W, H), DARK)
    d = ImageDraw.Draw(im)

    # top nav
    d.rectangle((0, 0, W, 64), fill=(15, 20, 28))
    lg = logo(40)
    im.paste(lg, (28, 12), lg)
    nav = ["Inicio", "En Vivo", "Noticias", "Programación", "Podcast", "Galería", "Contacto"]
    x = 300
    for n in nav:
        d.text((x, 24), n, font=F(13), fill=(209, 213, 219))
        x += 110
    rr(d, (1455, 14, 1570, 50), 18, RED)
    d.text((1478, 24), "EN VIVO", font=F(13, True), fill=WHITE)

    # HERO con micrófono (crop de locutor con mic)
    hero = talent("ramon-barrera.png", (900, 420))
    # darken and focus
    hero = ImageEnhance.Brightness(hero).enhance(0.55)
    paste_r(im, hero, (0, 64), 0)
    # left gradient panel
    for i in range(700):
        a = int(230 * (1 - i / 700))
        if a > 0:
            overlay = Image.new("RGBA", (1, 420), (*DARK, a))
            im.paste(overlay, (i, 64), overlay)

    d = ImageDraw.Draw(im)
    d.text((40, 110), "FM 105", font=F(42, True), fill=WHITE)
    d.text((40, 165), "El poder de la información", font=F(18), fill=YELLOW)
    d.text((40, 210), "Guaymas · Empalme · San Carlos", font=F(14), fill=(180, 190, 200))

    # play + waveform
    d.ellipse((40, 270, 100, 330), fill=YELLOW)
    d.polygon([(62, 285), (62, 315), (88, 300)], fill=DARK)
    d.text((120, 280), "Escuchar en Vivo", font=F(18, True), fill=WHITE)
    wave(d, 120, 310, 260, 28, YELLOW, 30)

    # Al Aire card (derecha)
    card(im, (1080, 100, 1560, 430), 14, DARK2)
    d = ImageDraw.Draw(im)
    pill(d, 1110, 120, "AL AIRE", (127, 29, 29), (254, 202, 202))
    d.text((1110, 160), "Noticiero 105", font=F(26, True), fill=WHITE)
    t = talent("gerardo-castro.png", (90, 100))
    paste_r(im, t, (1110, 220), 10)
    d = ImageDraw.Draw(im)
    d.text((1220, 235), "Gerardo Castro", font=F(16, True), fill=WHITE)
    d.text((1220, 265), "06:00 – 10:00", font=F(13), fill=(156, 163, 175))
    d.line((1110, 340, 1530, 340), fill=(55, 65, 80))
    d.text((1110, 360), "Siguiente", font=F(11, True), fill=MUTED)
    d.text((1110, 385), "Enlace 105 · Karla Montaño", font=F(14, True), fill=WHITE)

    # Ahora Suena
    card(im, (40, 470, 520, 780), 12, DARK2)
    d = ImageDraw.Draw(im)
    d.text((60, 490), "Ahora Suena", font=F(16, True), fill=WHITE)
    songs = [
        ("09:42", "Grupo Firme", "Ya Supérame"),
        ("09:38", "Christian Nodal", "Botella Tras Botella"),
        ("09:34", "Peso Pluma", "Ella Baila Sola"),
        ("09:30", "Carín León", "La Boda del Huitlacoche"),
        ("09:26", "Banda MS", "Háblame de Ti"),
    ]
    y = 530
    for tm, art, title in songs:
        d.text((60, y), tm, font=F(12, True), fill=YELLOW)
        d.text((120, y), art, font=F(12, True), fill=WHITE)
        d.text((120, y + 18), title, font=F(12), fill=(156, 163, 175))
        y += 45

    # Programación
    card(im, (540, 470, 1020, 780), 12, DARK2)
    d = ImageDraw.Draw(im)
    d.text((560, 490), "Programación", font=F(16, True), fill=WHITE)
    progs = [
        ("gerardo-castro.png", "Noticiero 105", "06:00"),
        ("karla-montano.png", "Enlace 105", "10:00"),
        ("ivan-vaca.png", "Tarde Poderosa", "14:00"),
        ("ramon-barrera.png", "Trayecto a Casa", "18:00"),
    ]
    y = 535
    for f, title, hour in progs:
        t = talent(f, (48, 54))
        paste_r(im, t, (560, y), 24)
        d = ImageDraw.Draw(im)
        d.text((625, y + 4), title, font=F(14, True), fill=WHITE)
        d.text((625, y + 26), hour + " hrs", font=F(12), fill=(156, 163, 175))
        y += 58

    # Noticias
    card(im, (1040, 470, 1560, 780), 12, DARK2)
    d = ImageDraw.Draw(im)
    d.text((1060, 490), "Noticias Destacadas", font=F(16, True), fill=WHITE)
    news = [
        (BLUE, "Reunión de gabinete en Sonora"),
        (RED, "Alerta climática en Guaymas"),
        (GREEN, "Triunfo local en deportes"),
        (ORANGE, "Avance de obras públicas"),
    ]
    for i, (col, title) in enumerate(news):
        col_i, row = i % 2, i // 2
        x1 = 1060 + col_i * 240
        y1 = 535 + row * 105
        rr(d, (x1, y1, x1 + 220, y1 + 90), 10, (40, 48, 60))
        rr(d, (x1, y1, x1 + 220, y1 + 40), 10, col)
        d.rectangle((x1, y1 + 20, x1 + 220, y1 + 40), fill=col)
        d.text((x1 + 10, y1 + 52), title, font=F(11, True), fill=WHITE)

    # Social + apps
    d.text((40, 810), "Síguenos", font=F(14, True), fill=WHITE)
    for i, (name, col) in enumerate([("Facebook", BLUE), ("Instagram", RED), ("X", MUTED), ("YouTube", RED)]):
        x = 40 + i * 130
        rr(d, (x, 845, x + 115, 885), 10, DARK2)
        d.text((x + 18, 855), name, font=F(12, True), fill=col)

    rr(d, (700, 845, 900, 885), 10, (15, 23, 42))
    d.text((725, 855), "Google Play", font=F(12, True), fill=WHITE)
    rr(d, (920, 845, 1100, 885), 10, (15, 23, 42))
    d.text((950, 855), "App Store", font=F(12, True), fill=WHITE)

    # footer devices
    d.rectangle((0, 920, W, H), fill=(15, 20, 28))
    d.text((40, 948), "Compatible con  Web  ·  Móvil  ·  Tablet  ·  Smart TV", font=F(14, True), fill=(180, 190, 200))
    d.text((1200, 948), "FM105 ONE  ·  Demo cliente", font=F(13, True), fill=YELLOW)

    save(im, "01-portal-publico.png")


# ═══════════════════════════════════════════════
# 02 MÓDULO DE VENTAS — Órdenes de Transmisión
# ═══════════════════════════════════════════════
def demo_ventas():
    im = Image.new("RGBA", (W, H), BG)
    items = [
        "Inicio",
        "Clientes",
        "Cotizaciones",
        "Órdenes",
        "Campañas",
        "Comerciales",
        "Contratos",
        "Facturación",
        "Cobranza",
        "Reportes",
        "Calendario",
        "Configuración",
    ]
    sidebar_admin(im, "Órdenes", items)
    d = ImageDraw.Draw(im)

    # topbar
    d.rectangle((250, 0, W, 64), fill=WHITE)
    d.line((250, 64, W, 64), fill=LINE)
    d.text((280, 14), "Órdenes de Transmisión", font=F(22, True), fill=INK)
    d.text((280, 42), "Módulo de Ventas  ·  FM105 Guaymas", font=F(12), fill=MUTED)
    # icons
    d.ellipse((1320, 18, 1355, 53), outline=LINE, width=2)
    d.ellipse((1375, 18, 1410, 53), outline=LINE, width=2)
    d.ellipse((1430, 18, 1465, 53), fill=NAVY)
    d.text((1440, 26), "AL", font=F(11, True), fill=WHITE)
    rr(d, (1490, 18, 1575, 50), 8, BLUE)
    d.text((1505, 26), "+ Nueva", font=F(12, True), fill=WHITE)

    kpis = [
        ("24", "Órdenes activas", GREEN),
        ("152", "Spots hoy", BLUE),
        ("18", "Campañas activas", ORANGE),
        ("$125,680", "Ingresos del mes", PURPLE),
    ]
    for i, (v, l, c) in enumerate(kpis):
        x = 275 + i * 325
        card(im, (x, 90, x + 310, 200), 12)
        d = ImageDraw.Draw(im)
        d.ellipse((x + 22, 112, x + 42, 132), fill=c)
        d.text((x + 55, 112), l, font=F(12), fill=MUTED)
        d.text((x + 22, 145), v, font=F(28, True), fill=INK)

    card(im, (275, 220, 1575, 920), 12)
    d = ImageDraw.Draw(im)
    heads = ["No. Orden", "Cliente", "Campaña", "Inicio", "Fin", "Spots", "Total", "Estatus"]
    xs = [295, 430, 680, 900, 1020, 1140, 1260, 1420]
    for h, x in zip(heads, xs):
        d.text((x, 245), h.upper(), font=F(10, True), fill=MUTED)
    d.line((295, 275, 1555, 275), fill=LINE)

    rows = [
        ("OT-2401", "Padilla Hermanos", "Verano 2026", "01 jul", "31 jul", "40", "$48,000", "Activa", (220, 252, 231), (21, 128, 61)),
        ("OT-2402", "Funeraria San Carlos", "Institucional", "05 jul", "05 ago", "30", "$32,500", "Programada", (255, 237, 213), (194, 65, 12)),
        ("OT-2403", "Materiales Moreno", "Promo julio", "08 jul", "22 jul", "24", "$21,800", "Activa", (220, 252, 231), (21, 128, 61)),
        ("OT-2404", "Autos Guaymas", "Lanzamiento", "10 jul", "10 ago", "18", "$19,200", "Programada", (255, 237, 213), (194, 65, 12)),
        ("OT-2405", "Clínica del Puerto", "Salud 105", "12 jul", "12 ago", "36", "$28,400", "Activa", (220, 252, 231), (21, 128, 61)),
        ("OT-2406", "Gobierno Municipal", "Campaña civica", "15 jul", "30 jul", "50", "$55,000", "Activa", (220, 252, 231), (21, 128, 61)),
        ("OT-2407", "Tienda El Faro", "Back to school", "18 jul", "18 ago", "22", "$16,900", "Programada", (255, 237, 213), (194, 65, 12)),
        ("OT-2408", "Restaurante Bahía", "Happy hour", "20 jul", "20 ago", "16", "$12,400", "Activa", (220, 252, 231), (21, 128, 61)),
    ]
    y = 300
    for no, cli, camp, ini, fin, spots, total, est, bg, fg in rows:
        d.text((295, y), no, font=F(13, True), fill=BLUE)
        d.text((430, y), cli, font=F(13, True), fill=INK)
        d.text((680, y), camp, font=F(13), fill=MUTED)
        d.text((900, y), ini, font=F(12), fill=MUTED)
        d.text((1020, y), fin, font=F(12), fill=MUTED)
        d.text((1140, y), spots, font=F(13), fill=INK)
        d.text((1260, y), total, font=F(13, True), fill=INK)
        pill(d, 1420, y - 2, est, bg, fg)
        d.line((295, y + 38, 1555, y + 38), fill=(243, 244, 246))
        y += 70

    # pagination hint
    d.text((295, 870), "Mostrando 8 de 24 órdenes", font=F(12), fill=MUTED)
    rr(d, (1450, 860, 1555, 900), 8, BLUE)
    d.text((1470, 870), "Exportar", font=F(12, True), fill=WHITE)

    save(im, "02-sistema-comercial.png")


# ═══════════════════════════════════════════════
# 03 KPI GERENCIALES
# ═══════════════════════════════════════════════
def demo_kpi():
    im = Image.new("RGBA", (W, H), BG)
    sidebar_admin(im, "Reportes", ["Inicio", "Ventas", "Clientes", "Facturación", "Reportes", "Configuración"])
    d = ImageDraw.Draw(im)
    d.rectangle((250, 0, W, 64), fill=WHITE)
    d.line((250, 64, W, 64), fill=LINE)
    d.text((280, 18), "KPI Gerenciales — Dashboard", font=F(22, True), fill=INK)
    d.text((280, 46), "Julio 2026  ·  Vista ejecutiva", font=F(12), fill=MUTED)

    kpis = [
        ("$125,680", "Ingresos", "+12.4%"),
        ("24", "Órdenes activas", "+8.0%"),
        ("78%", "Ocupación pub.", "+5.2%"),
        ("128", "Clientes activos", "+3.1%"),
    ]
    for i, (v, l, g) in enumerate(kpis):
        x = 275 + i * 325
        card(im, (x, 90, x + 310, 200), 12)
        d = ImageDraw.Draw(im)
        d.text((x + 22, 110), l, font=F(12), fill=MUTED)
        d.text((x + 22, 140), v, font=F(28, True), fill=INK)
        d.text((x + 22, 175), g, font=F(13, True), fill=GREEN)

    # bar chart
    card(im, (275, 220, 980, 620), 12)
    d = ImageDraw.Draw(im)
    d.text((300, 240), "Ingresos por mes", font=F(16, True), fill=INK)
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"]
    vals = [82, 90, 95, 102, 110, 118, 126]
    base = 560
    for i, (m, v) in enumerate(zip(months, vals)):
        x = 340 + i * 85
        hh = int(v * 2.4)
        rr(d, (x, base - hh, x + 44, base), 8, BLUE)
        d.text((x + 8, 575), m, font=F(11, True), fill=MUTED)

    # doughnut
    card(im, (1000, 220, 1575, 620), 12)
    d = ImageDraw.Draw(im)
    d.text((1025, 240), "Ingresos por tipo", font=F(16, True), fill=INK)
    cx, cy, r = 1220, 420, 105
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, 40, fill=BLUE)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 40, 120, fill=RED)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 120, 200, fill=YELLOW)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 200, 270, fill=GREEN)
    d.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=WHITE)
    d.text((cx - 22, cy - 12), "100%", font=F(16, True), fill=INK)
    for i, (c, lab) in enumerate([
        (BLUE, "Comerciales 38%"),
        (RED, "Menciones 25%"),
        (YELLOW, "Patrocinios 22%"),
        (GREEN, "Otros 15%"),
    ]):
        yy = 320 + i * 40
        d.ellipse((1400, yy, 1418, yy + 18), fill=c)
        d.text((1430, yy), lab, font=F(13), fill=INK)

    # Top 5
    card(im, (275, 640, 900, 820), 12)
    d = ImageDraw.Draw(im)
    d.text((300, 655), "Top 5 clientes", font=F(15, True), fill=INK)
    tops = [("Padilla Hermanos", "$48,000"), ("Gob. Municipal", "$55,000"), ("Funeraria S.C.", "$32,500"), ("Clínica Puerto", "$28,400"), ("Mat. Moreno", "$21,800")]
    y = 690
    for i, (n, v) in enumerate(tops, 1):
        d.text((300, y), f"{i}. {n}", font=F(13), fill=INK)
        d.text((750, y), v, font=F(13, True), fill=NAVY)
        y += 24

    # bottom status circles
    stats = [
        (BLUE, "152", "Spots TX hoy"),
        (PURPLE, "85.4k", "Audiencia est."),
        (ORANGE, "12", "Programas vivos"),
        (GREEN, "96%", "Cumplimiento"),
    ]
    for i, (c, v, l) in enumerate(stats):
        x = 930 + i * 160
        card(im, (x, 640, x + 150, 820), 12)
        d = ImageDraw.Draw(im)
        d.ellipse((x + 40, 665, x + 110, 735), fill=c)
        d.text((x + 55 if len(v) < 4 else x + 48, 685), v if len(v) <= 3 else v[:4], font=F(14, True), fill=WHITE)
        # rewrite value centered better
        d.ellipse((x + 40, 665, x + 110, 735), fill=c)
        bbox = d.textbbox((0, 0), v, font=F(13, True))
        tw = bbox[2] - bbox[0]
        d.text((x + 75 - tw // 2, 688), v, font=F(13, True), fill=WHITE)
        d.text((x + 18, 760), l, font=F(11, True), fill=MUTED)

    # footer strip
    d.rectangle((250, 860, W, H), fill=SIDE)
    d.text((280, 910), "FM105 ONE  ·  Decisiones inteligentes con KPIs en tiempo real", font=F(14, True), fill=WHITE)
    rr(d, (1380, 895, 1555, 940), 10, YELLOW)
    d.text((1405, 907), "Exportar PDF", font=F(13, True), fill=DARK)

    save(im, "04-dashboard-ceo.png")


# ═══════════════════════════════════════════════
# Continuidad (mantener módulo ops)
# ═══════════════════════════════════════════════
def demo_continuidad():
    im = Image.new("RGBA", (W, H), BG)
    sidebar_admin(im, "Inicio", ["Inicio", "Producción", "Biblioteca", "Continuidad", "Alertas"])
    # force Continuidad active look by redrawing - simpler: call with Continuidad
    im = Image.new("RGBA", (W, H), BG)
    sidebar_admin(im, "Continuidad", ["Inicio", "Producción", "Biblioteca", "Continuidad", "Alertas"])
    d = ImageDraw.Draw(im)
    d.rectangle((250, 0, W, 64), fill=WHITE)
    d.line((250, 64, W, 64), fill=LINE)
    d.text((280, 12), "Continuidad — Operación al aire", font=F(22, True), fill=INK)
    rr(d, (280, 70, 430, 108), 16, RED)
    d.text((300, 80), "●  AL AIRE", font=F(14, True), fill=WHITE)
    d.text((460, 75), "10:15:30 a.m.", font=F(22, True), fill=INK)

    card(im, (1280, 70, 1570, 200), 12)
    d = ImageDraw.Draw(im)
    d.ellipse((1310, 90, 1400, 180), outline=LINE, width=8)
    d.arc((1310, 90, 1400, 180), start=-90, end=255, fill=GREEN, width=8)
    d.text((1330, 118), "96%", font=F(18, True), fill=INK)
    d.text((1420, 110), "Cumplimiento", font=F(13, True), fill=INK)
    d.text((1420, 135), "del día", font=F(12), fill=MUTED)

    card(im, (275, 220, 920, 480), 12)
    d = ImageDraw.Draw(im)
    rr(d, (295, 240, 900, 460), 12, (220, 252, 231))
    d.text((320, 265), "SPOT EN AIRE", font=F(12, True), fill=GREEN)
    d.text((320, 300), "Súper del Norte", font=F(30, True), fill=INK)
    d.text((320, 350), "Campaña verano · 30s", font=F(14), fill=MUTED)
    d.text((320, 400), "00:04:15", font=F(36, True), fill=GREEN)

    card(im, (940, 220, 1570, 480), 12)
    t = talent("karla-montano.png", (130, 150))
    paste_r(im, t, (970, 260), 12)
    d = ImageDraw.Draw(im)
    d.text((1130, 250), "PROGRAMA ACTUAL", font=F(11, True), fill=RED)
    d.text((1130, 285), "Enlace 105", font=F(24, True), fill=INK)
    d.text((1130, 330), "Karla Montaño", font=F(15), fill=MUTED)
    d.text((1130, 370), "10:00 – 14:00", font=F(14), fill=MUTED)
    d.text((1130, 415), "Siguiente: Tarde Poderosa · Iván", font=F(13), fill=INK)

    card(im, (275, 500, 1570, 920), 12)
    d = ImageDraw.Draw(im)
    d.text((300, 520), "Agenda del día", font=F(16, True), fill=INK)
    for h, x in zip(["HORA", "TIPO", "CONTENIDO", "DURACIÓN", "ESTATUS"], [300, 420, 600, 1200, 1380]):
        d.text((x, 555), h, font=F(10, True), fill=MUTED)
    rows = [
        ("10:12", "Música", "Regional hit — AutoDJ", "03:40", "Al aire", (220, 252, 231), (21, 128, 61)),
        ("10:16", "Spot", "Súper del Norte · 30s", "00:30", "Al aire", (220, 252, 231), (21, 128, 61)),
        ("10:17", "ID", "Identificador FM105", "00:10", "En espera", (255, 237, 213), (194, 65, 12)),
        ("10:18", "Spot", "Padilla Hermanos · 30s", "00:30", "En espera", (255, 237, 213), (194, 65, 12)),
        ("10:20", "Música", "Éxito grupero", "03:12", "Programado", BG, MUTED),
        ("10:24", "Spot", "Funeraria San Carlos · 20s", "00:20", "Programado", BG, MUTED),
    ]
    y = 590
    for hora, tipo, cont, dur, est, bgc, fg in rows:
        d.text((300, y), hora, font=F(13, True), fill=INK)
        pill(d, 420, y - 2, tipo, BG, NAVY)
        d.text((600, y), cont, font=F(13), fill=INK)
        d.text((1200, y), dur, font=F(13), fill=MUTED)
        pill(d, 1380, y - 2, est, bgc, fg)
        y += 45

    save(im, "03-continuidad.png")


def demo_app():
    im = Image.new("RGBA", (W, H), (226, 232, 240))
    d = ImageDraw.Draw(im)
    d.text((50, 30), "App Móvil — Radioescucha", font=F(26, True), fill=INK)
    d.text((50, 70), "iOS & Android", font=F(14), fill=MUTED)

    def phone(x, y, fill=DARK):
        rr(d, (x, y, x + 300, y + 620), 36, (20, 20, 24))
        rr(d, (x + 8, y + 8, x + 292, y + 612), 30, fill)
        rr(d, (x + 110, y + 18, x + 190, y + 32), 8, (10, 10, 12))
        return x + 8, y + 8, 284, 604

    ix, iy, iw, ih = phone(100, 140)
    d = ImageDraw.Draw(im)
    lg = logo(32)
    im.paste(lg, (ix + 16, iy + 40), lg)
    d = ImageDraw.Draw(im)
    d.text((ix + 16, iy + 100), "EN VIVO", font=F(12, True), fill=YELLOW)
    d.text((ix + 16, iy + 130), "Noticiero 105", font=F(24, True), fill=WHITE)
    d.text((ix + 16, iy + 175), "Gerardo Castro", font=F(13), fill=(180, 190, 200))
    wave(d, ix + 16, iy + 230, iw - 32, 36, RED, 24)
    d.ellipse((ix + iw // 2 - 34, iy + 310, ix + iw // 2 + 34, iy + 378), fill=RED)
    d.polygon([(ix + iw // 2 - 10, iy + 328), (ix + iw // 2 - 10, iy + 360), (ix + iw // 2 + 18, iy + 344)], fill=WHITE)
    rr(d, (ix + 10, iy + ih - 70, ix + iw - 10, iy + ih - 16), 16, (15, 20, 28))
    for i, lab in enumerate(["Home", "Live", "News", "More"]):
        d.text((ix + 28 + i * 65, iy + ih - 48), lab, font=F(11, True), fill=YELLOW if lab == "Live" else (140, 150, 160))

    ix, iy, iw, ih = phone(480, 140, fill=WHITE)
    d = ImageDraw.Draw(im)
    rr(d, (ix, iy, ix + iw, iy + 64), 30, DARK)
    d.rectangle((ix, iy + 36, ix + iw, iy + 64), fill=DARK)
    d.text((ix + 16, iy + 24), "Noticias", font=F(16, True), fill=WHITE)
    for i, (c, t) in enumerate([(BLUE, "Gabinete Sonora"), (RED, "Clima Guaymas"), (GREEN, "Deportes local"), (ORANGE, "Obras públicas")]):
        y = iy + 85 + i * 100
        rr(d, (ix + 12, y, ix + iw - 12, y + 88), 10, BG)
        rr(d, (ix + 22, y + 12, ix + 86, y + 72), 8, c)
        d.text((ix + 100, y + 22), t, font=F(12, True), fill=INK)
        d.text((ix + 100, y + 48), "Hoy · FM105", font=F(11), fill=MUTED)

    ix, iy, iw, ih = phone(860, 140, fill=WHITE)
    d = ImageDraw.Draw(im)
    rr(d, (ix, iy, ix + iw, iy + 64), 30, DARK)
    d.rectangle((ix, iy + 36, ix + iw, iy + 64), fill=DARK)
    d.text((ix + 16, iy + 24), "Programación", font=F(16, True), fill=WHITE)
    for i, (f, title, hour) in enumerate([
        ("gerardo-castro.png", "Noticiero 105", "06:00"),
        ("karla-montano.png", "Enlace 105", "10:00"),
        ("ivan-vaca.png", "Tarde Poderosa", "14:00"),
        ("ramon-barrera.png", "Trayecto a Casa", "18:00"),
    ]):
        y = iy + 90 + i * 95
        t = talent(f, (54, 60))
        paste_r(im, t, (ix + 16, y), 10)
        d = ImageDraw.Draw(im)
        d.text((ix + 85, y + 8), title, font=F(13, True), fill=INK)
        d.text((ix + 85, y + 32), hour, font=F(12), fill=MUTED)

    card(im, (1220, 180, 1540, 680), 12)
    d = ImageDraw.Draw(im)
    d.text((1245, 210), "Incluye", font=F(18, True), fill=INK)
    for i, t in enumerate(["Splash + Login", "Player en vivo", "Noticias", "Programación", "Push", "Mensaje cabina"]):
        y = 270 + i * 55
        d.ellipse((1245, y, 1265, y + 20), fill=RED)
        d.text((1280, y), t, font=F(14), fill=INK)

    save(im, "05-app-movil.png")


def demo_brochure():
    im = Image.new("RGBA", (W, H), (203, 213, 225))
    card(im, (260, 80, 1340, 900), 16)
    d = ImageDraw.Draw(im)
    rr(d, (260, 80, 1340, 320), 16, DARK)
    d.rectangle((260, 260, 1340, 320), fill=DARK)
    lg = logo(64)
    im.paste(lg, (320, 120), lg)
    d = ImageDraw.Draw(im)
    d.text((320, 210), "FM105 ONE", font=F(40, True), fill=WHITE)
    d.text((320, 270), "Sistema Integral para Radioemisoras", font=F(16), fill=YELLOW)

    d.text((320, 370), "Automatiza · Administra · Vende\nFactura · Analiza · Crece", font=F(26, True), fill=INK)
    d.text((320, 480), "Brochure Comercial PDF — tenant piloto FM105 Guaymas", font=F(14), fill=MUTED)

    caps = ["Automatiza", "Administra", "Vende", "Factura", "Analiza", "Crece"]
    cols = [RED, BLUE, ORANGE, GREEN, PURPLE, YELLOW]
    for i, (c, n) in enumerate(zip(cols, caps)):
        x = 320 + (i % 3) * 300
        y = 560 + (i // 3) * 120
        rr(d, (x, y, x + 270, y + 100), 12, BG)
        d.ellipse((x + 20, y + 30, x + 60, y + 70), fill=c)
        d.text((x + 80, y + 40), n, font=F(18, True), fill=INK)

    save(im, "06-brochure-comercial.png")


def demo_portada():
    im = Image.new("RGBA", (W, H), DARK)
    d = ImageDraw.Draw(im)
    d.ellipse((1050, -100, 1900, 700), fill=(120, 20, 30))
    d.ellipse((1150, -40, 1800, 620), fill=RED)
    lg = logo(70)
    im.paste(lg, (70, 50), lg)
    d = ImageDraw.Draw(im)
    d.text((70, 160), "FM105 ONE", font=F(56, True), fill=WHITE)
    d.text((70, 235), "El poder de la información…\ny de tu gestión.", font=F(22), fill=YELLOW)
    items = [
        "01  Página web pública",
        "02  Módulo de ventas",
        "03  Continuidad al aire",
        "04  KPI gerenciales",
        "05  App móvil",
        "06  Brochure comercial",
    ]
    y = 360
    for t in items:
        rr(d, (70, y, 720, y + 70), 10, (40, 48, 62))
        d.text((100, y + 22), t, font=F(18, True), fill=WHITE)
        y += 80
    t = talent("gerardo-castro.png", (400, 470))
    paste_r(im, t, (980, 280), 16)
    save(im, "00-portada-demos.png")


def demo_mosaico_chatgpt():
    """Collage tipo la foto ChatGPT: web + ventas + KPI + panel marketing + banner."""
    # Load panels
    web = Image.open(OUT / "01-portal-publico.png").convert("RGB").resize((780, 520), Image.Resampling.LANCZOS)
    ventas = Image.open(OUT / "02-sistema-comercial.png").convert("RGB").resize((780, 420), Image.Resampling.LANCZOS)
    kpi = Image.open(OUT / "04-dashboard-ceo.png").convert("RGB").resize((780, 420), Image.Resampling.LANCZOS)

    out_w, out_h = 1800, 1400
    im = Image.new("RGBA", (out_w, out_h), (229, 231, 235))
    d = ImageDraw.Draw(im)

    # left column screens
    card(im, (30, 30, 830, 570), 14)
    im.paste(web, (40, 40))
    d = ImageDraw.Draw(im)
    d.text((40, 530), "Página Web Pública", font=F(14, True), fill=INK)

    card(im, (30, 590, 830, 1030), 14)
    im.paste(ventas, (40, 600))
    d = ImageDraw.Draw(im)
    d.text((40, 1005), "Módulo de Ventas — Órdenes de Transmisión", font=F(13, True), fill=INK)

    card(im, (860, 30, 1660, 470), 14)
    im.paste(kpi, (870, 40))
    d = ImageDraw.Draw(im)
    d.text((870, 445), "KPI Gerenciales — Dashboard", font=F(13, True), fill=INK)

    # marketing right panel
    card(im, (860, 490, 1660, 1030), 14, DARK)
    d = ImageDraw.Draw(im)
    lg = logo(56)
    im.paste(lg, (900, 530), lg)
    d = ImageDraw.Draw(im)
    d.text((900, 620), "FM105 ONE", font=F(32, True), fill=WHITE)
    d.text((900, 670), "Sistema Integral para Radioemisoras", font=F(14), fill=YELLOW)
    bullets = [
        "Automatiza la operación al aire",
        "Administra clientes y campañas",
        "Vende órdenes de transmisión",
        "Factura y cobra con control",
        "Analiza KPIs en tiempo real",
        "Haz crecer tu estación",
    ]
    y = 720
    for b in bullets:
        d.ellipse((900, y + 6, 916, y + 22), fill=RED)
        d.text((935, y), b, font=F(15), fill=WHITE)
        y += 38
    rr(d, (900, 960, 1200, 1005), 12, YELLOW)
    d.text((930, 972), "Brochure Comercial PDF", font=F(14, True), fill=DARK)

    # bottom feature banner
    d.rectangle((0, 1080, out_w, out_h), fill=DARK)
    feats = [
        (RED, "Siempre al aire", "Control de transmisión"),
        (BLUE, "Más ventas", "Clientes y campañas"),
        (ORANGE, "Control total", "Operación remota"),
        (GREEN, "Decisiones", "KPIs en tiempo real"),
        (PURPLE, "Cumplimiento", "Facturación fiscal"),
        (YELLOW, "Seguridad", "Protección de datos"),
    ]
    for i, (c, t, s) in enumerate(feats):
        x = 60 + i * 290
        d.ellipse((x, 1120, x + 54, 1174), fill=c)
        d.text((x + 70, 1125), t, font=F(14, True), fill=WHITE)
        d.text((x + 70, 1150), s, font=F(12), fill=(156, 163, 175))

    d.text((60, 1280), "FM 105 — EL PODER DE LA INFORMACIÓN… Y DE TU GESTIÓN.", font=F(18, True), fill=YELLOW)
    d.text((60, 1325), "Demo visual para cliente  ·  SaaS multiempresa", font=F(13), fill=(180, 190, 200))

    save(im, "07-mosaico-demos.png")


def main():
    for p in OUT.glob("*.png"):
        p.unlink()
    demo_portada()
    demo_portal()
    demo_ventas()
    demo_continuidad()
    demo_kpi()
    demo_app()
    demo_brochure()
    demo_mosaico_chatgpt()


if __name__ == "__main__":
    main()
