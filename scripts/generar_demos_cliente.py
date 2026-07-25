#!/usr/bin/env python3
"""Mockups PNG estilo ChatGPT / SaaS empresarial — FM105 ONE (para cliente)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "demo" / "assets"
OUT = ROOT / "cliente-demos"
ART = Path("/opt/cursor/artifacts/screenshots")

# Paleta institucional FM105 (como en el ejemplo ChatGPT)
NAVY = (10, 26, 48)
NAVY2 = (20, 39, 78)
RED = (217, 32, 39)
YELLOW = (255, 205, 60)
GRAY = (244, 246, 249)
WHITE = (255, 255, 255)
INK = (33, 37, 41)
MUTED = (108, 117, 125)
OK = (40, 167, 69)
LINE = (222, 226, 230)
SIDE = (10, 26, 48)

W, H = 1600, 1000


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    )
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        alt = (
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
        )
        return ImageFont.truetype(alt, size)


def rr(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def load_logo(h=56):
    img = Image.open(ASSETS / "logo-fm105.png").convert("RGBA")
    ratio = h / img.height
    return img.resize((max(1, int(img.width * ratio)), h), Image.Resampling.LANCZOS)


def load_talent(name: str, size=(280, 320)):
    img = Image.open(ASSETS / "locutores" / name).convert("RGBA")
    w, h = img.size
    tw, th = size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = max(0, int((nh - th) * 0.12))
    return img.crop((left, top, left + tw, top + th))


def paste_rounded(base, img, xy, radius=14):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, fill=255)
    base.paste(img, xy, mask)


def card(base, box, radius=14):
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x1 + 3, y1 + 5, x2 + 3, y2 + 5), radius, fill=(0, 0, 0, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(shadow)
    ImageDraw.Draw(base).rounded_rectangle(box, radius, fill=WHITE)


def save(img: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    rgb = img.convert("RGB")
    rgb.save(OUT / name, "PNG", optimize=True)
    rgb.save(ART / name, "PNG", optimize=True)
    print("OK", name)


def sidebar(img, active: str, items: list[str]):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 250, H), fill=SIDE)
    logo = load_logo(40)
    img.paste(logo, (18, 22), logo)
    d.text((78, 28), "FM105 ONE", font=font(17, True), fill=WHITE)
    d.text((78, 50), "SaaS Radio", font=font(11), fill=(170, 180, 195))
    y = 110
    for item in items:
        if item == active:
            rr(d, (12, y - 6, 238, y + 34), 10, (28, 48, 82))
            d.rectangle((12, y - 6, 17, y + 34), fill=YELLOW)
            col = WHITE
        else:
            col = (170, 180, 195)
        d.text((36, y + 4), item, font=font(15, item == active), fill=col)
        y += 46


def waveform(draw, x, y, w, h, color=RED, bars=42):
    import random

    rng = random.Random(105)
    bw = w / bars
    for i in range(bars):
        bh = h * (0.25 + 0.75 * abs(math.sin(i / 3.2)) * (0.55 + 0.45 * rng.random()))
        bx = x + i * bw
        by = y + (h - bh) / 2
        rr(draw, (bx, by, bx + bw * 0.55, by + bh), 2, color)


def badge(draw, x, y, text, bg, fg, pad_x=10, pad_y=5):
    f = font(12, True)
    tw = draw.textlength(text, font=f)
    rr(draw, (x, y, x + tw + pad_x * 2, y + 22 + pad_y), 11, bg)
    draw.text((x + pad_x, y + 4 + pad_y // 2), text, font=f, fill=fg)


# ───────────────────────── 01 PORTAL ─────────────────────────
def demo_portal():
    img = Image.new("RGBA", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # white header
    d.rectangle((0, 0, W, 72), fill=WHITE)
    d.line((0, 72, W, 72), fill=LINE, width=1)
    logo = load_logo(46)
    img.paste(logo, (36, 12), logo)
    nav = ["Inicio", "En Vivo", "Noticias", "Programación", "Locutores", "Podcasts", "Contacto"]
    x = 280
    for n in nav:
        d.text((x, 28), n, font=font(14), fill=MUTED)
        x += 105
    # social dots
    for i, col in enumerate([RED, NAVY2, YELLOW, MUTED]):
        d.ellipse((1280 + i * 28, 28, 1296 + i * 28, 44), fill=col)
    rr(d, (1400, 18, 1565, 54), 20, RED)
    d.text((1422, 28), "▶  Escuchar en Vivo", font=font(13, True), fill=WHITE)

    # hero band
    d.rectangle((0, 72, W, 430), fill=NAVY)
    # subtle gradient accent
    for i in range(12):
        d.rectangle((0, 72 + i * 4, W, 76 + i * 4), fill=(10 + i, 26 + i, 48 + i * 2))

    d.text((48, 105), "FM105  ·  Guaymas, Sonora", font=font(14, True), fill=YELLOW)
    d.text((48, 140), "La Madre de Todas", font=font(48, True), fill=WHITE)
    d.text((48, 205), "Noticias, música regional y la voz de casa.", font=font(18), fill=(210, 218, 230))
    rr(d, (48, 255, 280, 305), 22, RED)
    d.text((78, 270), "Escuchar en Vivo", font=font(16, True), fill=WHITE)
    waveform(d, 48, 340, 320, 48, YELLOW, 36)

    # 4 talent photos in hero
    files = [
        ("gerardo-castro.png", "Gerardo Castro"),
        ("ivan-vaca.png", "Iván Vaca"),
        ("karla-montano.png", "Karla Montaño"),
        ("ramon-barrera.png", "Ramón Barrera"),
    ]
    for i, (file, name) in enumerate(files):
        t = load_talent(file, (210, 250))
        x0 = 620 + i * 230
        paste_rounded(img, t, (x0, 110), 16)
        # name strip
        strip = Image.new("RGBA", (210, 40), (*RED, 230))
        img.paste(strip, (x0, 320), strip)
        ImageDraw.Draw(img).text((x0 + 12, 328), name.split()[0], font=font(16, True), fill=WHITE)

    # content row
    card(img, (40, 460, 520, 700), 14)
    d = ImageDraw.Draw(img)
    d.text((60, 480), "AHORA SUENA", font=font(12, True), fill=RED)
    d.text((60, 510), "Despierta Guaymas", font=font(26, True), fill=NAVY2)
    t = load_talent("gerardo-castro.png", (70, 80))
    paste_rounded(img, t, (60, 560), 10)
    d = ImageDraw.Draw(img)
    d.text((150, 575), "Gerardo Castro", font=font(16, True), fill=INK)
    d.text((150, 600), "06:00 – 10:00  ·  En vivo", font=font(13), fill=MUTED)
    d.ellipse((60, 660, 76, 676), fill=OK)
    d.text((88, 658), "1,284 oyentes  ·  128 kbps", font=font(13, True), fill=OK)

    card(img, (540, 460, 980, 700), 14)
    d = ImageDraw.Draw(img)
    d.text((560, 480), "PRÓXIMO PROGRAMA", font=font(12, True), fill=MUTED)
    d.text((560, 510), "Enlace 105", font=font(26, True), fill=NAVY2)
    t = load_talent("karla-montano.png", (70, 80))
    paste_rounded(img, t, (560, 560), 10)
    d = ImageDraw.Draw(img)
    d.text((650, 575), "Karla Montaño", font=font(16, True), fill=INK)
    d.text((650, 600), "10:00 – 14:00", font=font(13), fill=MUTED)
    badge(d, 560, 655, "En 45 min", (255, 243, 205), (154, 116, 0))

    # weather + whatsapp
    card(img, (1000, 460, 1560, 700), 14)
    d = ImageDraw.Draw(img)
    d.text((1025, 480), "CLIMA · GUAYMAS", font=font(12, True), fill=MUTED)
    d.text((1025, 515), "34°", font=font(48, True), fill=NAVY2)
    d.text((1140, 545), "Soleado", font=font(18), fill=MUTED)
    rr(d, (1025, 610, 1525, 675), 14, OK)
    d.text((1060, 630), "WhatsApp  ·  Envíanos un mensaje a cabina", font=font(15, True), fill=WHITE)

    # news
    d.text((48, 730), "Noticias destacadas", font=font(22, True), fill=NAVY2)
    news = [
        ("Obras en Unidad Deportiva", "Local · hace 2 h"),
        ("Reapertura ganadera en Sonora", "Estatal · hace 4 h"),
        ("Operativo en zona centro", "Policiaca · ayer"),
    ]
    colors = [NAVY2, RED, (61, 90, 128)]
    for i, ((title, meta), col) in enumerate(zip(news, colors)):
        x1 = 40 + i * 520
        card(img, (x1, 770, x1 + 500, 960), 14)
        d = ImageDraw.Draw(img)
        rr(d, (x1 + 16, 790, x1 + 484, 870), 10, col)
        d.text((x1 + 16, 890), title, font=font(16, True), fill=INK)
        d.text((x1 + 16, 920), meta, font=font(13), fill=MUTED)

    save(img, "01-portal-publico.png")


# ───────────────────────── 02 COMERCIAL ─────────────────────────
def demo_comercial():
    img = Image.new("RGBA", (W, H), GRAY)
    sidebar(img, "Ventas", ["Dashboard", "Clientes", "Cotizaciones", "Órdenes", "Ventas", "Facturación", "Reportes"])
    d = ImageDraw.Draw(img)
    d.text((280, 28), "Sistema Comercial — Ventas", font=font(28, True), fill=NAVY2)
    d.text((280, 68), "Julio 2026  ·  FM105 Guaymas", font=font(14), fill=MUTED)
    rr(d, (1380, 30, 1560, 70), 18, RED)
    d.text((1410, 40), "+ Nueva orden", font=font(14, True), fill=WHITE)

    kpis = [
        ("$215,450", "Ventas del mes", "+12.4%"),
        ("28", "Órdenes activas", "+3"),
        ("$185,300", "Ingresos del mes", "+8.1%"),
        ("78%", "Ocupación inventario", "+5%"),
    ]
    for i, (val, label, delta) in enumerate(kpis):
        x = 280 + i * 325
        card(img, (x, 110, x + 310, 230), 14)
        d = ImageDraw.Draw(img)
        d.text((x + 22, 128), label, font=font(13), fill=MUTED)
        d.text((x + 22, 158), val, font=font(30, True), fill=NAVY2)
        d.text((x + 22, 200), delta + " vs mes ant.", font=font(13, True), fill=OK)

    # bar chart
    card(img, (280, 250, 980, 620), 14)
    d = ImageDraw.Draw(img)
    d.text((305, 270), "Ingresos por mes", font=font(18, True), fill=NAVY2)
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"]
    vals = [140, 155, 168, 175, 190, 182, 215]
    base = 560
    for i, (m, v) in enumerate(zip(months, vals)):
        x = 340 + i * 85
        h = int(v * 1.2)
        rr(d, (x, base - h, x + 42, base), 8, NAVY2)
        d.text((x + 6, 575), m, font=font(12, True), fill=MUTED)

    # doughnut
    card(img, (1000, 250, 1560, 620), 14)
    d = ImageDraw.Draw(img)
    d.text((1025, 270), "Órdenes por estatus", font=font(18, True), fill=NAVY2)
    cx, cy, r = 1280, 430, 100
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=NAVY2)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, 40, fill=OK)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 40, 130, fill=YELLOW)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 130, 200, fill=RED)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 200, 270, fill=(108, 117, 125))
    d.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=WHITE)
    d.text((cx - 18, cy - 10), "28", font=font(20, True), fill=NAVY2)
    legend = [(OK, "Activas 12"), (YELLOW, "Programadas 8"), (RED, "Pendientes 5"), (MUTED, "Canceladas 3")]
    y = 360
    for col, lab in legend:
        d.ellipse((1420, y, 1436, y + 16), fill=col)
        d.text((1445, y - 2), lab, font=font(13), fill=INK)
        y += 32

    # table
    card(img, (280, 640, 1560, 960), 14)
    d = ImageDraw.Draw(img)
    d.text((305, 660), "Órdenes recientes", font=font(18, True), fill=NAVY2)
    headers = ["Cliente", "Campaña", "Fecha", "Spots", "Total", "Estatus"]
    xs = [305, 560, 820, 980, 1120, 1300]
    for htxt, x in zip(headers, xs):
        d.text((x, 700), htxt.upper(), font=font(11, True), fill=MUTED)
    rows = [
        ("Padilla Hermanos", "Verano 2026", "22 jul", "40", "$48,000", "Activa", OK),
        ("Funeraria San Carlos", "Institucional", "20 jul", "30", "$32,500", "Programada", (0, 123, 255)),
        ("Materiales Moreno", "Promo julio", "18 jul", "24", "$21,800", "Activa", OK),
        ("Autos Guaymas", "Lanzamiento", "15 jul", "18", "$19,200", "Pendiente", WARN if False else YELLOW),
    ]
    y = 735
    for cliente, camp, fecha, spots, total, est, col in rows:
        d.text((305, y), cliente, font=font(14, True), fill=INK)
        d.text((560, y), camp, font=font(14), fill=MUTED)
        d.text((820, y), fecha, font=font(14), fill=MUTED)
        d.text((980, y), spots, font=font(14), fill=MUTED)
        d.text((1120, y), total, font=font(14, True), fill=NAVY2)
        badge(d, 1300, y - 2, est, (*col, ) if len(col) == 3 else col, WHITE if col in (OK, RED, NAVY2, (0, 123, 255)) else NAVY2)
        # fix badge colors for readability
        y += 48

    # rewrite badges cleanly on last pass - already drawn; for yellow pending use dark text
    # Re-draw pending badge properly
    d = ImageDraw.Draw(img)
    # cover last badge area and redraw
    rr(d, (1295, 735 + 48 * 3 - 2, 1420, 735 + 48 * 3 + 24), 11, (255, 243, 205))
    d.text((1310, 735 + 48 * 3 + 2), "Pendiente", font=font(12, True), fill=(154, 116, 0))
    rr(d, (1295, 735 + 48 - 2, 1435, 735 + 48 + 24), 11, (220, 237, 255))
    d.text((1310, 735 + 48 + 2), "Programada", font=font(12, True), fill=(0, 86, 179))

    save(img, "02-sistema-comercial.png")


# ───────────────────────── 03 CONTINUIDAD ─────────────────────────
def demo_continuidad():
    img = Image.new("RGBA", (W, H), GRAY)
    sidebar(img, "Continuidad", ["Dashboard", "Producción", "Biblioteca", "Continuidad", "Alertas", "Reportes"])
    d = ImageDraw.Draw(img)

    d.text((280, 24), "Continuidad — Operación al aire", font=font(26, True), fill=NAVY2)
    rr(d, (280, 70, 420, 110), 18, RED)
    d.text((305, 80), "●  AL AIRE", font=font(16, True), fill=WHITE)
    d.text((450, 80), "10:15:30 a.m.", font=font(22, True), fill=NAVY2)
    d.text((700, 84), "Cumplimiento del día", font=font(13), fill=MUTED)
    # gauge
    rr(d, (880, 78, 1100, 108), 12, (220, 245, 228))
    d.text((910, 84), "96%  en tiempo", font=font(16, True), fill=OK)

    # live green card
    card(img, (280, 140, 900, 420), 16)
    d = ImageDraw.Draw(img)
    rr(d, (300, 160, 880, 400), 14, (232, 248, 238))
    d.text((330, 185), "SPOT EN AIRE", font=font(13, True), fill=OK)
    d.text((330, 220), "Súper del Norte", font=font(34, True), fill=NAVY2)
    d.text((330, 275), "Campaña verano  ·  30 segundos", font=font(16), fill=MUTED)
    d.text((330, 330), "00:04:15", font=font(48, True), fill=OK)
    d.text((560, 355), "restante", font=font(16), fill=MUTED)

    # next / host
    card(img, (920, 140, 1560, 420), 16)
    t = load_talent("karla-montano.png", (150, 175))
    paste_rounded(img, t, (950, 180), 14)
    d = ImageDraw.Draw(img)
    d.text((1130, 175), "PROGRAMA ACTUAL", font=font(12, True), fill=RED)
    d.text((1130, 210), "Enlace 105", font=font(28, True), fill=NAVY2)
    d.text((1130, 255), "Karla Montaño", font=font(18), fill=INK)
    d.text((1130, 290), "10:00 – 14:00", font=font(15), fill=MUTED)
    d.text((1130, 340), "Siguiente: Tarde Poderosa · Iván Vaca", font=font(14), fill=MUTED)

    # agenda
    card(img, (280, 450, 1560, 900), 16)
    d = ImageDraw.Draw(img)
    d.text((305, 470), "Agenda del día", font=font(18, True), fill=NAVY2)
    headers = ["Hora", "Tipo", "Contenido", "Duración", "Estatus"]
    xs = [305, 430, 620, 1180, 1350]
    for htxt, x in zip(headers, xs):
        d.text((x, 515), htxt.upper(), font=font(11, True), fill=MUTED)
    rows = [
        ("10:12", "Música", "Regional hit — AutoDJ", "03:40", "Al aire", OK),
        ("10:16", "Spot", "Súper del Norte · 30s", "00:30", "Al aire", OK),
        ("10:17", "ID", "Identificador FM105", "00:10", "En espera", YELLOW),
        ("10:18", "Spot", "Padilla Hermanos · 30s", "00:30", "En espera", YELLOW),
        ("10:20", "Música", "Éxito grupero", "03:12", "En espera", MUTED),
        ("10:24", "Spot", "Funeraria San Carlos · 20s", "00:20", "En espera", MUTED),
    ]
    y = 555
    for hora, tipo, cont, dur, est, col in rows:
        d.text((305, y), hora, font=font(14, True), fill=NAVY2)
        badge(d, 430, y - 2, tipo, GRAY, NAVY2)
        d.text((620, y), cont, font=font(14), fill=INK)
        d.text((1180, y), dur, font=font(14), fill=MUTED)
        bg = (220, 245, 228) if col == OK else ((255, 243, 205) if col == YELLOW else GRAY)
        fg = OK if col == OK else ((154, 116, 0) if col == YELLOW else MUTED)
        badge(d, 1350, y - 2, est, bg, fg)
        y += 48

    # footer stats
    for i, (val, lab) in enumerate([("152/240", "Spots hoy"), ("8", "Pendientes"), ("2", "Alertas")]):
        x = 280 + i * 420
        card(img, (x, 920, x + 400, 980), 12)
        d = ImageDraw.Draw(img)
        d.text((x + 24, 938), val, font=font(20, True), fill=NAVY2)
        d.text((x + 140, 944), lab, font=font(14), fill=MUTED)

    save(img, "03-continuidad.png")


# ───────────────────────── 04 CEO ─────────────────────────
def demo_ceo():
    img = Image.new("RGBA", (W, H), GRAY)
    sidebar(img, "CEO", ["CEO", "Ventas", "Cobranza", "Audiencia", "Reportes"])
    d = ImageDraw.Draw(img)
    d.text((280, 24), "Dashboard Gerencial — CEO", font=font(28, True), fill=NAVY2)
    d.text((280, 64), "01 jul 2026  –  25 jul 2026", font=font(14), fill=MUTED)
    rr(d, (1280, 28, 1400, 64), 14, WHITE)
    d.text((1305, 38), "PDF", font=font(14, True), fill=NAVY2)
    rr(d, (1420, 28, 1560, 64), 14, YELLOW)
    d.text((1455, 38), "Excel", font=font(14, True), fill=NAVY2)

    kpis = [
        ("$842k", "Ventas"),
        ("$910k", "Facturación"),
        ("$724k", "Cobranza"),
        ("78%", "Inventario"),
        ("128", "Clientes activos"),
    ]
    for i, (val, lab) in enumerate(kpis):
        x = 280 + i * 258
        card(img, (x, 100, x + 245, 210), 14)
        d = ImageDraw.Draw(img)
        d.text((x + 18, 120), lab, font=font(13), fill=MUTED)
        d.text((x + 18, 150), val, font=font(30, True), fill=NAVY2)

    # line chart sales vs goal
    card(img, (280, 230, 1000, 620), 14)
    d = ImageDraw.Draw(img)
    d.text((305, 250), "Ventas vs Meta", font=font(18, True), fill=NAVY2)
    pts_a, pts_b = [], []
    for i, (a, b) in enumerate(zip([55, 58, 62, 66, 70, 74, 84], [60, 60, 65, 70, 75, 80, 85])):
        x = 340 + i * 85
        ya = 560 - a * 3.2
        yb = 560 - b * 3.2
        pts_a.append((x, ya))
        pts_b.append((x, yb))
        d.text((x - 8, 575), ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"][i], font=font(11, True), fill=MUTED)
    d.line(pts_b, fill=YELLOW, width=4)
    d.line(pts_a, fill=RED, width=4)
    for p in pts_a:
        d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=RED)
    for p in pts_b:
        d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=YELLOW)
    d.text((305, 585), "● Ventas", font=font(12, True), fill=RED)
    d.text((400, 585), "● Meta", font=font(12, True), fill=(180, 140, 0))

    # pie
    card(img, (1020, 230, 1560, 620), 14)
    d = ImageDraw.Draw(img)
    d.text((1045, 250), "Ingresos por tipo de cliente", font=font(16, True), fill=NAVY2)
    cx, cy, r = 1220, 420, 105
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, 40, fill=NAVY2)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 40, 130, fill=RED)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 130, 220, fill=YELLOW)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 220, 270, fill=(108, 117, 125))
    d.ellipse((cx - 45, cy - 45, cx + 45, cy + 45), fill=WHITE)
    legend = [(NAVY2, "Comercial 42%"), (RED, "Gobierno 28%"), (YELLOW, "Servicios 20%"), (MUTED, "Otros 10%")]
    y = 340
    for col, lab in legend:
        d.ellipse((1380, y, 1396, y + 16), fill=col)
        d.text((1405, y - 2), lab, font=font(13), fill=INK)
        y += 36

    # bottom cards
    card(img, (280, 640, 700, 960), 14)
    d = ImageDraw.Draw(img)
    d.text((305, 660), "Top 5 anunciantes", font=font(16, True), fill=NAVY2)
    tops = [("Padilla Hermanos", "$128k"), ("Funeraria S. Carlos", "$96k"), ("Materiales Moreno", "$84k"), ("Autos Guaymas", "$71k"), ("Clínica del Puerto", "$58k")]
    y = 710
    for i, (n, v) in enumerate(tops, 1):
        d.text((305, y), f"{i}.  {n}", font=font(14), fill=INK)
        d.text((600, y), v, font=font(14, True), fill=NAVY2)
        y += 42

    card(img, (720, 640, 1120, 960), 14)
    d = ImageDraw.Draw(img)
    d.text((745, 660), "Programas más rentables", font=font(16, True), fill=NAVY2)
    progs = [("Despierta Guaymas", "28%"), ("Enlace 105", "22%"), ("Tarde Poderosa", "20%"), ("Trayecto a Casa", "18%")]
    y = 720
    for n, v in progs:
        d.text((745, y), n, font=font(14), fill=INK)
        d.text((1020, y), v, font=font(14, True), fill=RED)
        y += 48

    card(img, (1140, 640, 1560, 960), 14)
    d = ImageDraw.Draw(img)
    d.text((1165, 660), "Audiencia estimada", font=font(16, True), fill=NAVY2)
    d.text((1165, 720), "85,400", font=font(44, True), fill=NAVY2)
    d.text((1165, 780), "oyentes / mes", font=font(16), fill=MUTED)
    d.text((1165, 840), "Mensajes a cabina: 1,240", font=font(14), fill=INK)
    d.text((1165, 875), "Tickets soporte: 36", font=font(14), fill=MUTED)

    save(img, "04-dashboard-ceo.png")


# ───────────────────────── 05 APP MÓVIL ─────────────────────────
def phone_frame(base, x, y, w=300, h=620):
    d = ImageDraw.Draw(base)
    rr(d, (x, y, x + w, y + h), 36, (20, 20, 24))
    rr(d, (x + 8, y + 8, x + w - 8, y + h - 8), 30, NAVY)
    # notch
    rr(d, (x + w // 2 - 40, y + 18, x + w // 2 + 40, y + 34), 10, (10, 10, 12))
    return x + 8, y + 8, w - 16, h - 16  # inner


def demo_app():
    img = Image.new("RGBA", (W, H), (235, 238, 243))
    d = ImageDraw.Draw(img)
    d.text((60, 40), "App Móvil — Radioescucha", font=font(30, True), fill=NAVY2)
    d.text((60, 85), "Splash / Player · Noticias · Programación  ·  iOS & Android", font=font(16), fill=MUTED)

    # Phone 1: Player
    ix, iy, iw, ih = phone_frame(img, 120, 160)
    d = ImageDraw.Draw(img)
    logo = load_logo(36)
    img.paste(logo, (ix + 20, iy + 40), logo)
    d = ImageDraw.Draw(img)
    d.text((ix + 20, iy + 100), "EN VIVO", font=font(12, True), fill=YELLOW)
    d.text((ix + 20, iy + 130), "Despierta\nGuaymas", font=font(28, True), fill=WHITE)
    d.text((ix + 20, iy + 220), "Gerardo Castro", font=font(14), fill=(200, 210, 220))
    waveform(d, ix + 20, iy + 270, iw - 40, 40, RED, 28)
    # play button
    d.ellipse((ix + iw // 2 - 36, iy + 340, ix + iw // 2 + 36, iy + 412), fill=RED)
    d.polygon([(ix + iw // 2 - 10, iy + 360), (ix + iw // 2 - 10, iy + 392), (ix + iw // 2 + 18, iy + 376)], fill=WHITE)
    # tab bar
    rr(d, (ix + 10, iy + ih - 70, ix + iw - 10, iy + ih - 16), 18, (15, 30, 55))
    for i, lab in enumerate(["Inicio", "Vivo", "News", "Más"]):
        d.text((ix + 30 + i * 65, iy + ih - 48), lab, font=font(11, True), fill=YELLOW if lab == "Vivo" else (160, 170, 185))

    # Phone 2: News
    ix, iy, iw, ih = phone_frame(img, 520, 160)
    d = ImageDraw.Draw(img)
    rr(d, (ix, iy, ix + iw, iy + ih), 30, WHITE)
    # redraw top dark strip
    rr(d, (ix, iy, ix + iw, iy + 70), 30, NAVY)
    d.rectangle((ix, iy + 40, ix + iw, iy + 70), fill=NAVY)
    d.text((ix + 20, iy + 28), "Noticias", font=font(20, True), fill=WHITE)
    news = [
        (NAVY2, "Obras en Unidad Deportiva"),
        (RED, "Reapertura ganadera"),
        ((61, 90, 128), "Operativo zona centro"),
        (YELLOW, "Liga de tenis en Guaymas"),
    ]
    y = iy + 90
    for col, title in news:
        rr(d, (ix + 14, y, ix + iw - 14, y + 95), 12, GRAY)
        rr(d, (ix + 24, y + 12, ix + 90, y + 78), 8, col)
        d.text((ix + 105, y + 25), title, font=font(13, True), fill=INK)
        d.text((ix + 105, y + 52), "Hoy · FM105", font=font(11), fill=MUTED)
        y += 110
    rr(d, (ix + 10, iy + ih - 70, ix + iw - 10, iy + ih - 16), 18, NAVY)
    for i, lab in enumerate(["Inicio", "Vivo", "News", "Más"]):
        d.text((ix + 30 + i * 65, iy + ih - 48), lab, font=font(11, True), fill=YELLOW if lab == "News" else (160, 170, 185))

    # Phone 3: Programs
    ix, iy, iw, ih = phone_frame(img, 920, 160)
    d = ImageDraw.Draw(img)
    rr(d, (ix, iy, ix + iw, iy + ih), 30, WHITE)
    rr(d, (ix, iy, ix + iw, iy + 70), 30, NAVY)
    d.rectangle((ix, iy + 40, ix + iw, iy + 70), fill=NAVY)
    d.text((ix + 20, iy + 28), "Programación", font=font(20, True), fill=WHITE)
    progs = [
        ("gerardo-castro.png", "Despierta Guaymas", "06:00"),
        ("karla-montano.png", "Enlace 105", "10:00"),
        ("ivan-vaca.png", "Tarde Poderosa", "14:00"),
        ("ramon-barrera.png", "Trayecto a Casa", "18:00"),
    ]
    y = iy + 90
    for file, title, hour in progs:
        t = load_talent(file, (58, 66))
        paste_rounded(img, t, (ix + 20, y), 10)
        d = ImageDraw.Draw(img)
        d.text((ix + 95, y + 8), title, font=font(13, True), fill=INK)
        d.text((ix + 95, y + 34), hour + " hrs", font=font(12), fill=MUTED)
        y += 90
    d = ImageDraw.Draw(img)
    rr(d, (ix + 10, iy + ih - 70, ix + iw - 10, iy + ih - 16), 18, NAVY)
    for i, lab in enumerate(["Inicio", "Vivo", "News", "Más"]):
        d.text((ix + 30 + i * 65, iy + ih - 48), lab, font=font(11, True), fill=(160, 170, 185))

    # side notes
    d = ImageDraw.Draw(img)
    card(img, (1280, 200, 1540, 720), 14)
    d = ImageDraw.Draw(img)
    d.text((1305, 230), "Incluye", font=font(18, True), fill=NAVY2)
    for i, t in enumerate(["Splash + Login", "Player en vivo", "Noticias", "Programación", "Locutores", "Push notifications", "Mensaje a cabina"]):
        d.ellipse((1305, 285 + i * 50, 1321, 301 + i * 50), fill=RED)
        d.text((1335, 280 + i * 50), t, font=font(14), fill=INK)

    save(img, "05-app-movil.png")


# ───────────────────────── 06 BROCHURE ─────────────────────────
def demo_brochure():
    img = Image.new("RGBA", (W, H), (230, 233, 238))
    d = ImageDraw.Draw(img)

    # perspective-ish card
    card(img, (220, 80, 1380, 920), 20)
    d = ImageDraw.Draw(img)
    # top brand band
    rr(d, (220, 80, 1380, 360), 20, NAVY)
    d.rectangle((220, 300, 1380, 360), fill=NAVY)
    logo = load_logo(70)
    img.paste(logo, (280, 130), logo)
    d = ImageDraw.Draw(img)
    d.text((280, 220), "FM105 ONE", font=font(48, True), fill=WHITE)
    d.text((280, 285), "Sistema Integral para Radioemisoras", font=font(20), fill=YELLOW)

    d.text((280, 420), "Automatiza, administra y haz crecer\ntu estación de radio.", font=font(28, True), fill=NAVY2)
    d.text(
        (280, 520),
        "Plataforma SaaS multiempresa: portal público, streaming,\nprogramación, continuidad, ventas, CRM, facturación,\nKPIs gerenciales y app móvil.",
        font=font(16),
        fill=MUTED,
    )

    modules = [
        (RED, "Ventas"),
        (NAVY2, "Continuidad"),
        (YELLOW, "Producción"),
        (OK, "Finanzas"),
        ((61, 90, 128), "Reportes"),
    ]
    x = 280
    for col, name in modules:
        rr(d, (x, 680, x + 180, 820), 16, GRAY)
        d.ellipse((x + 65, 710, x + 115, 760), fill=col)
        d.text((x + 35, 780), name, font=font(14, True), fill=NAVY2)
        x += 200

    d.text((280, 860), "Demo comercial  ·  Tenant piloto: FM105 Guaymas, Sonora", font=font(14), fill=MUTED)
    save(img, "06-brochure-comercial.png")


def demo_portada():
    img = Image.new("RGBA", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for i in range(18):
        d.ellipse((1100 - i * 10, -100 - i * 4, 1900 + i * 10, 700 + i * 4), fill=(217, 32, 39, max(0, 16 - i)))
    logo = load_logo(80)
    img.paste(logo, (80, 80), logo)
    d = ImageDraw.Draw(img)
    d.text((80, 200), "FM105 ONE", font=font(64, True), fill=WHITE)
    d.text((80, 280), "Paquete de demos visuales", font=font(28), fill=YELLOW)
    d.text((80, 340), "Estilo SaaS empresarial · listo para cliente", font=font(18), fill=(190, 200, 215))

    thumbs = [
        "01 Portal público",
        "02 Sistema comercial",
        "03 Continuidad",
        "04 Dashboard CEO",
        "05 App móvil",
        "06 Brochure",
    ]
    y = 420
    for t in thumbs:
        rr(d, (80, y, 700, y + 70), 12, (255, 255, 255, 18))
        d.text((110, y + 20), t, font=font(22, True), fill=WHITE)
        y += 80

    t = load_talent("gerardo-castro.png", (380, 450))
    paste_rounded(img, t, (1050, 280), 22)
    save(img, "00-portada-demos.png")


def main():
    # clean old names that no longer apply
    for old in [
        "02-programacion.png",
        "04-clientes-crm.png",
        "05-kpi-gerenciales.png",
    ]:
        p = OUT / old
        if p.exists():
            p.unlink()
        p2 = ART / old
        if p2.exists():
            p2.unlink()

    demo_portada()
    demo_portal()
    demo_comercial()
    demo_continuidad()
    demo_ceo()
    demo_app()
    demo_brochure()


if __name__ == "__main__":
    main()
