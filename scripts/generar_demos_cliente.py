#!/usr/bin/env python3
"""Genera mockups PNG listos para enviar al cliente (FM105 ONE)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "demo" / "assets"
OUT = ROOT / "cliente-demos"
ART = Path("/opt/cursor/artifacts/screenshots")

NAVY = (20, 39, 78)
NAVY_DEEP = (11, 23, 48)
RED = (214, 40, 40)
YELLOW = (255, 195, 0)
GRAY = (236, 236, 236)
WHITE = (255, 255, 255)
INK = (26, 35, 50)
MUTED = (92, 107, 122)
OK = (31, 157, 85)
WARN = (230, 167, 0)

W, H = 1600, 1000


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = (
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
    )
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def round_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def load_logo(h=70):
    img = Image.open(ASSETS / "logo-fm105.png").convert("RGBA")
    ratio = h / img.height
    return img.resize((max(1, int(img.width * ratio)), h), Image.Resampling.LANCZOS)


def load_talent(name: str, size=(280, 320)):
    img = Image.open(ASSETS / "locutores" / name).convert("RGBA")
    img.thumbnail((size[0] * 2, size[1] * 2), Image.Resampling.LANCZOS)
    # center-crop
    w, h = img.size
    tw, th = size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = max(0, (nh - th) // 5)  # bias to faces
    img = img.crop((left, top, left + tw, top + th))
    return img


def paste_rounded(base, img, xy, radius=18):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width, img.height), radius, fill=255)
    base.paste(img, xy, mask)


def shadow_panel(base, box, radius=20, fill=WHITE):
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x1 + 6, y1 + 10, x2 + 6, y2 + 10), radius, fill=(11, 23, 48, 45))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(shadow)
    ImageDraw.Draw(base).rounded_rectangle(box, radius, fill=fill)


def draw_sidebar(img, active: str, items: list[str]):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 280, H), fill=NAVY_DEEP)
    logo = load_logo(44)
    img.paste(logo, (24, 24), logo)
    draw.text((90, 32), "FM105 ONE", font=font(20, True), fill=WHITE)
    y = 120
    for item in items:
        if item == active:
            # solid highlight (RGBA alpha fills are unreliable in Pillow)
            round_rect(draw, (16, y - 8, 264, y + 36), 10, (36, 58, 102))
            draw.rectangle((16, y - 8, 22, y + 36), fill=YELLOW)
            fill = WHITE
        else:
            fill = (190, 200, 215)
        draw.text((40, y), item, font=font(18, True if item == active else False), fill=fill)
        y += 52


def save(img: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.convert("RGB").save(path, "PNG", optimize=True)
    img.convert("RGB").save(ART / name, "PNG", optimize=True)
    print(f"OK {path}")


def demo_portal():
    img = Image.new("RGBA", (W, H), NAVY_DEEP)
    draw = ImageDraw.Draw(img)

    # atmospheric background
    for i in range(20):
        alpha = 18 - i
        draw.ellipse((900 - i * 8, -80 - i * 5, 1900 + i * 8, 700 + i * 5), fill=(214, 40, 40, max(0, alpha)))
    draw.rectangle((0, 0, W, 78), fill=(11, 23, 48, 230))

    logo = load_logo(52)
    img.paste(logo, (40, 14), logo)
    draw.text((120, 22), "FM105", font=font(28, True), fill=WHITE)
    nav = ["Inicio", "En Vivo", "Noticias", "Programación", "Locutores", "Contacto"]
    x = 360
    for n in nav:
        draw.text((x, 30), n, font=font(18), fill=(230, 235, 245))
        x += 120
    round_rect(draw, (1360, 18, 1560, 60), 24, RED)
    draw.text((1390, 28), "ESCUCHAR EN VIVO", font=font(15, True), fill=WHITE)

    # hero copy
    draw.text((60, 150), "EL PODER DE LA", font=font(48, True), fill=YELLOW)
    draw.text((60, 210), "INFORMACIÓN", font=font(72, True), fill=WHITE)
    draw.text((60, 310), "Guaymas · Empalme · San Carlos", font=font(24), fill=(220, 225, 235))
    draw.text((60, 355), "Portal público rediseñado para FM105 ONE", font=font(20), fill=(190, 200, 215))
    round_rect(draw, (60, 420, 340, 485), 28, YELLOW)
    draw.text((95, 438), "Escuchar en Vivo", font=font(22, True), fill=NAVY)

    # now playing panel
    shadow_panel(img, (60, 560, 620, 920), 22, (255, 255, 255, 245))
    d = ImageDraw.Draw(img)
    d.text((90, 590), "AHORA SUENA", font=font(16, True), fill=RED)
    d.text((90, 630), "Despierta Guaymas", font=font(36, True), fill=NAVY)
    d.text((90, 685), "Conductor: Gerardo Castro", font=font(20), fill=MUTED)
    d.text((90, 725), "06:00 – 10:00  ·  Icecast 128 kbps", font=font(18), fill=MUTED)
    d.ellipse((95, 790, 120, 815), fill=OK)
    d.text((135, 790), "EN VIVO · 1,284 oyentes", font=font(18, True), fill=OK)

    # talent collage
    talents = [
        ("gerardo-castro.png", 740),
        ("ivan-vaca.png", 980),
        ("karla-montano.png", 1220),
        ("ramon-barrera.png", 1460),
    ]
    names = ["Gerardo", "Iván", "Karla", "Ramón"]
    for (file, x), name in zip(talents, names):
        t = load_talent(file, (210, 250))
        paste_rounded(img, t, (x - 210, 180), 18)
        banner = Image.new("RGBA", (210, 46), RED)
        img.paste(banner, (x - 210, 390), banner)
        ImageDraw.Draw(img).text((x - 195, 400), name, font=font(18, True), fill=WHITE)

    # bottom strip
    draw.rectangle((0, 940, W, H), fill=NAVY)
    draw.text((60, 958), "DEMO CLIENTE  ·  Portal público FM105 ONE  ·  Solo mockup visual", font=font(18, True), fill=YELLOW)

    save(img, "01-portal-publico.png")


def demo_programacion():
    img = Image.new("RGBA", (W, H), GRAY)
    draw = ImageDraw.Draw(img)
    draw_sidebar(img, "Programación", ["Dashboard", "Portal", "Programación", "Continuidad", "Clientes", "KPIs"])
    draw = ImageDraw.Draw(img)

    draw.text((320, 36), "PROGRAMACIÓN", font=font(40, True), fill=NAVY)
    draw.text((320, 90), "Calendario semanal · Locutor · Color · Patrocinio", font=font(18), fill=MUTED)

    # talent chips
    chips = [
        ("gerardo-castro.png", "Gerardo Castro", 320),
        ("ivan-vaca.png", "Iván Vaca", 620),
        ("karla-montano.png", "Karla Montaño", 920),
        ("ramon-barrera.png", "Ramón Barrera", 1220),
    ]
    for file, name, x in chips:
        shadow_panel(img, (x, 140, x + 270, 230), 16, WHITE)
        t = load_talent(file, (56, 64))
        paste_rounded(img, t, (x + 16, 153), 10)
        ImageDraw.Draw(img).text((x + 86, 168), name, font=font(16, True), fill=NAVY)

    # week grid
    shadow_panel(img, (320, 260, 1540, 920), 18, WHITE)
    d = ImageDraw.Draw(img)
    days = ["LUN", "MAR", "MIÉ", "JUE", "VIE"]
    colors = [NAVY, RED, (31, 111, 139), (139, 90, 31), (75, 63, 114)]
    programs = [
        ("06:00", "Despierta Guaymas", "Gerardo"),
        ("10:00", "Enlace 105", "Karla"),
        ("14:00", "Tarde Poderosa", "Iván"),
        ("18:00", "Trayecto a Casa", "Ramón"),
    ]
    for i, day in enumerate(days):
        d.text((420 + i * 220, 285), day, font=font(16, True), fill=MUTED)
    for r, (hour, title, host) in enumerate(programs):
        d.text((345, 350 + r * 130), hour, font=font(16, True), fill=MUTED)
        for c in range(5):
            x1 = 400 + c * 220
            y1 = 330 + r * 130
            round_rect(d, (x1, y1, x1 + 200, y1 + 100), 14, colors[r])
            d.text((x1 + 14, y1 + 18), title, font=font(15, True), fill=WHITE)
            d.text((x1 + 14, y1 + 48), host, font=font(14), fill=(235, 235, 245))
            d.text((x1 + 14, y1 + 72), "Spot · Patrocinio", font=font(12), fill=(220, 220, 230))

    save(img, "02-programacion.png")


def demo_continuidad():
    img = Image.new("RGBA", (W, H), GRAY)
    draw = ImageDraw.Draw(img)
    draw_sidebar(img, "Continuidad", ["Dashboard", "Programación", "Continuidad", "Producción", "Clientes"])
    draw = ImageDraw.Draw(img)

    draw.text((320, 36), "CONTINUIDAD", font=font(40, True), fill=NAVY)
    draw.text((320, 90), "Consola al aire · Semáforo de spots", font=font(18), fill=MUTED)
    draw.ellipse((1280, 50, 1305, 75), fill=OK)
    draw.text((1320, 50), "Stream conectado", font=font(18, True), fill=OK)

    shadow_panel(img, (320, 140, 1000, 520), 20, WHITE)
    t = load_talent("gerardo-castro.png", (180, 210))
    paste_rounded(img, t, (360, 190), 18)
    d = ImageDraw.Draw(img)
    d.text((580, 180), "AL AIRE AHORA", font=font(16, True), fill=RED)
    d.text((580, 220), "Despierta Guaymas", font=font(36, True), fill=NAVY)
    d.text((580, 280), "Gerardo Castro  ·  06:00 – 10:00", font=font(20), fill=MUTED)
    d.text((580, 330), "Siguiente: Enlace 105 · Karla Montaño · 10:00", font=font(18), fill=INK)

    # lights
    for i, (color, label) in enumerate([(OK, "Transmitido"), (WARN, "Próximo"), (RED, "Retrasado")]):
        x = 580 + i * 130
        d.ellipse((x, 400, x + 22, 422), fill=color)
        d.text((x + 32, 400), label, font=font(15, True), fill=INK)

    shadow_panel(img, (1030, 140, 1540, 920), 20, WHITE)
    d = ImageDraw.Draw(img)
    d.text((1060, 170), "SPOTS PENDIENTES", font=font(20, True), fill=NAVY)
    spots = [
        ("07:15", "Padilla Hnos · 30s", "Transmitido", OK),
        ("07:45", "Funeraria San Carlos · 20s", "Próximo", WARN),
        ("08:10", "Materiales Moreno · 30s", "Próximo", WARN),
        ("08:40", "Campaña gobierno · 40s", "Retrasado", RED),
        ("09:05", "ID estación · 10s", "Próximo", WARN),
    ]
    y = 230
    for hour, name, status, color in spots:
        round_rect(d, (1060, y, 1510, y + 90), 14, GRAY)
        d.text((1085, y + 18), hour, font=font(18, True), fill=NAVY)
        d.text((1085, y + 48), name, font=font(16), fill=MUTED)
        round_rect(d, (1360, y + 28, 1490, y + 62), 14, (*color, 30) if False else color)
        # readable badge
        badge_bg = (220, 245, 228) if color == OK else ((255, 243, 205) if color == WARN else (255, 225, 225))
        text_c = OK if color == OK else ((154, 116, 0) if color == WARN else RED)
        round_rect(d, (1345, y + 28, 1495, y + 62), 14, badge_bg)
        d.text((1360, y + 35), status, font=font(14, True), fill=text_c)
        y += 110

    # next host card
    shadow_panel(img, (320, 560, 1000, 920), 20, WHITE)
    t2 = load_talent("karla-montano.png", (160, 190))
    paste_rounded(img, t2, (360, 620), 16)
    d = ImageDraw.Draw(img)
    d.text((560, 620), "SIGUIENTE PROGRAMA", font=font(16, True), fill=YELLOW if False else RED)
    d.text((560, 665), "Enlace 105", font=font(34, True), fill=NAVY)
    d.text((560, 720), "Karla Montaño", font=font(22), fill=MUTED)
    d.text((560, 770), "Metadata: Canción demo · 02:14 restante", font=font(18), fill=INK)
    round_rect(d, (560, 830, 760, 885), 22, RED)
    d.text((595, 845), "Forzar spot", font=font(18, True), fill=WHITE)
    round_rect(d, (780, 830, 960, 885), 22, YELLOW)
    d.text((820, 845), "Siguiente", font=font(18, True), fill=NAVY)

    save(img, "03-continuidad.png")


def demo_clientes():
    img = Image.new("RGBA", (W, H), GRAY)
    draw = ImageDraw.Draw(img)
    draw_sidebar(img, "Clientes", ["Dashboard", "Clientes", "Cotizaciones", "Campañas", "Facturación", "KPIs"])
    draw = ImageDraw.Draw(img)

    draw.text((320, 36), "CLIENTES / CRM", font=font(40, True), fill=NAVY)
    draw.text((320, 90), "Cartera · seguimiento · campañas", font=font(18), fill=MUTED)
    round_rect(draw, (1320, 40, 1540, 90), 24, RED)
    draw.text((1355, 54), "+ Nuevo cliente", font=font(18, True), fill=WHITE)

    kpis = [("128", "Clientes activos"), ("37", "Prospectos"), ("19", "Campañas"), ("$186k", "Por cobrar")]
    for i, (val, label) in enumerate(kpis):
        x = 320 + i * 310
        shadow_panel(img, (x, 140, x + 290, 260), 18, WHITE)
        d = ImageDraw.Draw(img)
        d.text((x + 24, 165), label, font=font(16), fill=MUTED)
        d.text((x + 24, 200), val, font=font(40, True), fill=NAVY)

    shadow_panel(img, (320, 290, 1040, 940), 18, WHITE)
    d = ImageDraw.Draw(img)
    d.text((350, 320), "CARTERA", font=font(22, True), fill=NAVY)
    headers = ["Cliente", "Contacto", "Estado", "Última visita"]
    xs = [350, 560, 780, 920]
    for htxt, x in zip(headers, xs):
        d.text((x, 370), htxt.upper(), font=font(13, True), fill=MUTED)
    rows = [
        ("Padilla Hermanos", "Laura Padilla", "Activo", "22 jul", OK),
        ("Funeraria San Carlos", "Marco Ríos", "Activo", "20 jul", OK),
        ("Materiales Moreno", "Ana Moreno", "Seguimiento", "18 jul", WARN),
        ("Clínica del Puerto", "Dr. Elías Soto", "Prospecto", "17 jul", WARN),
        ("Autos Guaymas", "Iván López", "Moroso", "10 jul", RED),
    ]
    y = 410
    for cliente, contacto, estado, fecha, color in rows:
        d.line((350, y + 70, 1010, y + 70), fill=(230, 235, 240), width=1)
        d.text((350, y + 18), cliente, font=font(17, True), fill=NAVY)
        d.text((560, y + 18), contacto, font=font(16), fill=MUTED)
        badge_bg = (220, 245, 228) if color == OK else ((255, 243, 205) if color == WARN else (255, 225, 225))
        round_rect(d, (780, y + 12, 900, y + 46), 12, badge_bg)
        d.text((795, y + 18), estado, font=font(14, True), fill=color if color != WARN else (154, 116, 0))
        d.text((920, y + 18), fecha, font=font(16), fill=MUTED)
        y += 85

    shadow_panel(img, (1060, 290, 1540, 940), 18, WHITE)
    d = ImageDraw.Draw(img)
    d.text((1090, 320), "ACTIVIDAD", font=font(22, True), fill=NAVY)
    acts = [
        ("Llamada", "Padilla · renovación Q3", "Hoy"),
        ("Visita", "Materiales Moreno", "Mañana"),
        ("Nota", "Clínica pide matutino", "Ayer"),
        ("Archivo", "Contrato Funeraria.pdf", "20 jul"),
    ]
    y = 380
    for tipo, detail, when in acts:
        round_rect(d, (1090, y, 1510, y + 90), 14, GRAY)
        d.text((1115, y + 18), tipo, font=font(16, True), fill=RED)
        d.text((1115, y + 48), detail, font=font(15), fill=INK)
        d.text((1410, y + 30), when, font=font(14, True), fill=MUTED)
        y += 110
    round_rect(d, (1090, 820, 1510, 910), 16, NAVY)
    d.text((1115, 845), "Siguiente: cotizar 40 spots", font=font(18, True), fill=WHITE)
    d.text((1115, 875), "Horario 07:00–09:00 · Gerardo Castro", font=font(14), fill=YELLOW)

    save(img, "04-clientes-crm.png")


def demo_kpi():
    img = Image.new("RGBA", (W, H), GRAY)
    draw = ImageDraw.Draw(img)
    draw_sidebar(img, "Dashboard CEO", ["Dashboard CEO", "Clientes", "Programación", "Facturación", "Reportes"])
    draw = ImageDraw.Draw(img)

    draw.text((320, 30), "KPI GERENCIALES", font=font(40, True), fill=NAVY)
    draw.text((320, 85), "Julio 2026 · vista tipo Power BI · exportable PDF/Excel", font=font(18), fill=MUTED)
    round_rect(draw, (1240, 40, 1360, 88), 20, NAVY)
    draw.text((1275, 52), "PDF", font=font(18, True), fill=WHITE)
    round_rect(draw, (1380, 40, 1540, 88), 20, YELLOW)
    draw.text((1415, 52), "Excel", font=font(18, True), fill=NAVY)

    cards = [
        ("$842k", "Ingresos del mes", "+12%"),
        ("$910k", "Facturación", "Meta 92%"),
        ("$724k", "Cobranza", "79%"),
        ("$218k", "Utilidad", "Margen 26%"),
        ("78%", "Ocupación", "Horas vendidas"),
        ("4,812", "Spots TX", "+320"),
        ("1.4k", "Audiencia avg", "Oyentes"),
        ("146", "Horas libres", "Por vender"),
    ]
    for i, (val, label, delta) in enumerate(cards):
        col, row = i % 4, i // 4
        x = 320 + col * 310
        y = 130 + row * 130
        shadow_panel(img, (x, y, x + 290, y + 115), 16, WHITE)
        d = ImageDraw.Draw(img)
        d.text((x + 20, y + 18), label, font=font(14), fill=MUTED)
        d.text((x + 20, y + 45), val, font=font(34, True), fill=NAVY)
        d.text((x + 20, y + 88), delta, font=font(14, True), fill=OK)

    # bar chart panel
    shadow_panel(img, (320, 410, 1040, 940), 18, WHITE)
    d = ImageDraw.Draw(img)
    d.text((350, 435), "INGRESOS MENSUALES", font=font(20, True), fill=NAVY)
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"]
    vals_a = [62, 64, 70, 73, 78, 75, 84]
    vals_b = [54, 56, 59, 61, 65, 67, 71]
    base_y = 860
    for i, m in enumerate(months):
        x = 380 + i * 90
        h1 = vals_a[i] * 4
        h2 = vals_b[i] * 4
        round_rect(d, (x, base_y - h1, x + 28, base_y), 6, NAVY)
        round_rect(d, (x + 34, base_y - h2, x + 62, base_y), 6, YELLOW)
        d.text((x + 10, 875), m, font=font(14, True), fill=MUTED)
    round_rect(d, (350, 900, 375, 920), 4, NAVY)
    d.text((385, 900), "2026", font=font(14), fill=INK)
    round_rect(d, (460, 900, 485, 920), 4, YELLOW)
    d.text((495, 900), "2025", font=font(14), fill=INK)

    # doughnut-like legend panel
    shadow_panel(img, (1060, 410, 1540, 940), 18, WHITE)
    d = ImageDraw.Draw(img)
    d.text((1090, 435), "INGRESOS POR PROGRAMA", font=font(18, True), fill=NAVY)
    # simple donut
    cx, cy, r = 1300, 620, 110
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=NAVY)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 0, 100, fill=RED)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 100, 180, fill=YELLOW)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 250, fill=(61, 90, 128))
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 250, 360, fill=NAVY)
    d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), fill=WHITE)
    d.text((cx - 28, cy - 12), "100%", font=font(18, True), fill=NAVY)

    legend = [
        (NAVY, "Despierta Guaymas 28%"),
        (RED, "Enlace 105 22%"),
        (YELLOW, "Tarde Poderosa 20%"),
        ((61, 90, 128), "Trayecto a Casa 18%"),
    ]
    y = 780
    for color, label in legend:
        d.ellipse((1100, y + 4, 1120, y + 24), fill=color)
        d.text((1135, y), label, font=font(15), fill=INK)
        y += 32

    save(img, "05-kpi-gerenciales.png")


def main():
    assert (ASSETS / "logo-fm105.png").exists(), "Falta logo"
    for name in ["gerardo-castro.png", "ivan-vaca.png", "karla-montano.png", "ramon-barrera.png"]:
        assert (ASSETS / "locutores" / name).exists(), f"Falta {name}"
    demo_portal()
    demo_programacion()
    demo_continuidad()
    demo_clientes()
    demo_kpi()
    # cover / index image listing all
    cover = Image.new("RGBA", (W, H), NAVY_DEEP)
    d = ImageDraw.Draw(cover)
    logo = load_logo(70)
    cover.paste(logo, (70, 70), logo)
    d.text((70, 180), "FM105 ONE", font=font(64, True), fill=WHITE)
    d.text((70, 260), "Demos visuales para cliente", font=font(32), fill=YELLOW)
    d.text((70, 330), "Paquete de mockups PNG · sin código", font=font(22), fill=(200, 210, 225))
    files = [
        "01 Portal público",
        "02 Programación",
        "03 Continuidad",
        "04 Clientes / CRM",
        "05 KPI gerenciales",
    ]
    y = 420
    for f in files:
        round_rect(d, (70, y, 620, y + 70), 14, (255, 255, 255, 18))
        d.text((100, y + 20), f, font=font(24, True), fill=WHITE)
        y += 90
    t = load_talent("gerardo-castro.png", (420, 500))
    paste_rounded(cover, t, (1050, 220), 24)
    save(cover, "00-portada-demos.png")


if __name__ == "__main__":
    main()
