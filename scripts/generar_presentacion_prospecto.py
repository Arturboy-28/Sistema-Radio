#!/usr/bin/env python3
"""Presentación comercial FM105 ONE — Smart Apps → prospecto FM105."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdfcanvas

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "presentacion" / "assets"
OUT = ROOT / "presentacion" / "slides"
ART = Path("/opt/cursor/artifacts/presentacion")
PDF_PATH = ROOT / "presentacion" / "FM105-ONE-Presentacion-Prospecto.pdf"

# Brand
NAVY = (20, 39, 78)
NAVY_DEEP = (12, 22, 44)
RED = (214, 40, 40)
YELLOW = (255, 195, 0)
WHITE = (255, 255, 255)
INK = (28, 35, 48)
MUTED = (100, 112, 128)
GRAY = (244, 246, 249)
LINE = (220, 226, 234)
OK = (34, 160, 90)

W, H = 1920, 1080


def F(size: int, bold: bool = False):
    path = (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    )
    return ImageFont.truetype(path, size)


def rr(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def load(path: Path, h=None, w=None):
    im = Image.open(path).convert("RGBA")
    if h and not w:
        w = int(im.width * h / im.height)
        im = im.resize((w, h), Image.Resampling.LANCZOS)
    elif w and h:
        im = im.resize((w, h), Image.Resampling.LANCZOS)
    return im


def paste(base, im, xy):
    base.paste(im, xy, im if im.mode == "RGBA" else None)


def card(base, box, r=18, fill=WHITE):
    x1, y1, x2, y2 = box
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x1 + 3, y1 + 5, x2 + 3, y2 + 5), r, fill=(0, 0, 0, 35))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(base).rounded_rectangle(box, r, fill=fill)


def footer(d, page: str, total: int):
    d.rectangle((0, H - 56, W, H), fill=NAVY_DEEP)
    d.text((48, H - 38), "Smart Apps  ·  FM105 ONE  ·  Documento comercial", font=F(14), fill=(180, 190, 210))
    d.text((W - 120, H - 38), f"{page}/{total}", font=F(14, True), fill=YELLOW)


def header_bar(im, title: str, subtitle: str = ""):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 110), fill=NAVY)
    smart = load(ASSETS / "logo-smart-apps.png", h=54)
    # crop white bg loosely by using as-is
    paste(im, smart, (36, 28))
    fm = load(ASSETS / "logo-fm105.png", h=58)
    paste(im, fm, (W - fm.width - 40, 26))
    d = ImageDraw.Draw(im)
    d.text((360, 28), title, font=F(32, True), fill=WHITE)
    if subtitle:
        d.text((360, 70), subtitle, font=F(16), fill=YELLOW)


def save_slide(im: Image.Image, name: str, slides: list):
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    rgb = im.convert("RGB")
    rgb.save(path, "PNG", optimize=True)
    rgb.save(ART / name, "PNG", optimize=True)
    slides.append(path)
    print("OK", name)


# ───────────────── SLIDES ─────────────────

def slide_portada(slides, total):
    im = Image.new("RGBA", (W, H), NAVY_DEEP)
    d = ImageDraw.Draw(im)
    # accent shapes
    d.ellipse((1200, -200, 2100, 700), fill=(140, 25, 35))
    d.ellipse((1350, -80, 2000, 580), fill=RED)
    d.rectangle((0, H - 140, W, H), fill=NAVY)

    smart = load(ASSETS / "logo-smart-apps.png", h=90)
    paste(im, smart, (80, 70))
    fm = load(ASSETS / "logo-fm105.png", h=110)
    paste(im, fm, (W - fm.width - 80, 70))

    d = ImageDraw.Draw(im)
    d.text((80, 280), "PROPUESTA COMERCIAL", font=F(20, True), fill=YELLOW)
    d.text((80, 340), "FM105 ONE", font=F(84, True), fill=WHITE)
    d.text((80, 450), "Sistema Integral para Radioemisoras", font=F(34), fill=(210, 220, 235))
    d.text((80, 520), "Automatiza · Administra · Vende · Factura · Analiza · Crece", font=F(22), fill=YELLOW)

    rr(d, (80, 620, 520, 700), 16, RED)
    d.text((120, 645), "Documento para prospecto", font=F(22, True), fill=WHITE)

    d.text((80, H - 100), "Presentado por Smart Apps", font=F(18, True), fill=WHITE)
    d.text((80, H - 68), "Cliente / estación de referencia: FM105 Guaymas, Sonora", font=F(16), fill=(180, 190, 205))
    d.text((W - 160, H - 68), f"1/{total}", font=F(16, True), fill=YELLOW)
    save_slide(im, "01-portada.png", slides)


def slide_agenda(slides, total):
    im = Image.new("RGBA", (W, H), GRAY)
    header_bar(im, "Agenda", "Contenido de la presentación")
    items = [
        ("01", "El reto de la radio moderna"),
        ("02", "La solución FM105 ONE"),
        ("03", "Beneficios clave"),
        ("04", "Módulos de operación"),
        ("05", "Módulos comerciales y financieros"),
        ("06", "Audiencia y canales digitales"),
        ("07", "Plataforma y gobierno"),
        ("08", "Flujo de valor"),
    ]
    for i, (n, t) in enumerate(items):
        col, row = i % 2, i // 2
        x = 80 + col * 900
        y = 180 + row * 180
        card(im, (x, y, x + 840, y + 150), 18)
        d = ImageDraw.Draw(im)
        rr(d, (x + 30, y + 35, x + 130, y + 115), 14, RED)
        d.text((x + 52, y + 55), n, font=F(28, True), fill=WHITE)
        d.text((x + 170, y + 55), t, font=F(26, True), fill=NAVY)
    footer(ImageDraw.Draw(im), "2", total)
    save_slide(im, "02-agenda.png", slides)


def slide_problema(slides, total):
    im = Image.new("RGBA", (W, H), GRAY)
    header_bar(im, "El reto", "Lo que viven muchas radioemisoras hoy")
    probs = [
        ("Herramientas dispersas", "Excel, WhatsApp, aire y facturación sin integración."),
        ("Spots sin evidencia", "Dificultad para comprobar al anunciante qué se transmitió."),
        ("Poca visibilidad", "La dirección no ve ventas, ocupación y cobranza en tiempo real."),
        ("Experiencia digital débil", "Web/app desactualizadas frente a la audiencia actual."),
    ]
    for i, (t, s) in enumerate(probs):
        x = 80 + (i % 2) * 900
        y = 180 + (i // 2) * 340
        card(im, (x, y, x + 840, y + 300), 20)
        d = ImageDraw.Draw(im)
        rr(d, (x + 36, y + 40, x + 100, y + 104), 16, RED)
        d.text((x + 56, y + 55), str(i + 1), font=F(28, True), fill=WHITE)
        d.text((x + 130, y + 50), t, font=F(28, True), fill=NAVY)
        d.text((x + 130, y + 120), s, font=F(20), fill=MUTED)
    footer(ImageDraw.Draw(im), "3", total)
    save_slide(im, "03-problema.png", slides)


def slide_solucion(slides, total):
    im = Image.new("RGBA", (W, H), GRAY)
    header_bar(im, "La solución", "FM105 ONE — una plataforma, todo el flujo")
    d = ImageDraw.Draw(im)
    card(im, (80, 160, 1840, 420), 20, NAVY)
    d = ImageDraw.Draw(im)
    d.text((120, 210), "Unifica aire · comercial · finanzas · audiencia", font=F(36, True), fill=WHITE)
    d.text(
        (120, 280),
        "Sistema SaaS integral para operar la estación, vender con control,\ncomprobar transmisión, facturar, cobrar y crecer con datos.",
        font=F(22),
        fill=(210, 220, 235),
    )
    pillars = [
        ("Operar", "Programación, continuidad,\nbiblioteca y streaming"),
        ("Vender", "CRM, órdenes, inventario\ny portal anunciante"),
        ("Comprobar", "Logger, testigos y\nreconciliación"),
        ("Crecer", "KPIs, app, engagement\ny multi-estación"),
    ]
    for i, (t, s) in enumerate(pillars):
        x = 80 + i * 455
        card(im, (x, 480, x + 430, 900), 18)
        d = ImageDraw.Draw(im)
        rr(d, (x + 30, y := 520, x + 140, 590), 14, YELLOW if i % 2 == 0 else RED)
        d.text((x + 50, 538), f"0{i+1}", font=F(24, True), fill=NAVY if i % 2 == 0 else WHITE)
        d.text((x + 30, 630), t, font=F(30, True), fill=NAVY)
        d.text((x + 30, 700), s, font=F(18), fill=MUTED)
    footer(ImageDraw.Draw(im), "4", total)
    save_slide(im, "04-solucion.png", slides)


def slide_beneficios(slides, total):
    im = Image.new("RGBA", (W, H), GRAY)
    header_bar(im, "Beneficios clave", "Valor para dirección, comercial y operación")
    bens = [
        "Un solo sistema para aire, comercial y finanzas",
        "Prueba de transmisión (testigos) para anunciantes",
        "Control de inventario y ocupación comercial",
        "Facturación y cobranza alineadas a lo transmitido",
        "KPIs gerenciales en tiempo real",
        "Portal y app para oyentes y anunciantes",
        "Arquitectura lista para múltiples estaciones",
        "Menos Excel, menos retrabajo, más control",
    ]
    for i, t in enumerate(bens):
        col, row = i % 2, i // 2
        x = 80 + col * 900
        y = 170 + row * 180
        card(im, (x, y, x + 840, y + 150), 16)
        d = ImageDraw.Draw(im)
        d.ellipse((x + 40, y + 50, x + 90, y + 100), fill=OK)
        d.text((x + 55, y + 58), "✓", font=F(24, True), fill=WHITE)
        d.text((x + 120, y + 55), t, font=F(22, True), fill=NAVY)
    footer(ImageDraw.Draw(im), "5", total)
    save_slide(im, "05-beneficios.png", slides)


def modules_slide(slides, total, num, fname, title, subtitle, modules):
    """modules: list of (name, desc) — up to 6 per slide."""
    im = Image.new("RGBA", (W, H), GRAY)
    header_bar(im, title, subtitle)
    for i, (name, desc) in enumerate(modules):
        col, row = i % 2, i // 2
        x = 70 + col * 920
        y = 150 + row * 270
        card(im, (x, y, x + 880, y + 240), 16)
        d = ImageDraw.Draw(im)
        rr(d, (x + 28, y + 28, x + 100, y + 90), 12, RED)
        d.text((x + 48, y + 42), f"{i+1:02d}", font=F(22, True), fill=WHITE)
        d.text((x + 120, y + 40), name, font=F(24, True), fill=NAVY)
        # wrap desc simply
        words = desc.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if len(test) > 48:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
        yy = y + 105
        for line in lines[:4]:
            d.text((x + 120, yy), line, font=F(17), fill=MUTED)
            yy += 30
    footer(ImageDraw.Draw(im), str(num), total)
    save_slide(im, fname, slides)


def slide_flujo(slides, total):
    im = Image.new("RGBA", (W, H), GRAY)
    header_bar(im, "Flujo de valor", "Del lead a la cobranza con evidencia")
    steps = [
        ("1", "Cotizar", "Ventas arma\npropuesta"),
        ("2", "Orden", "Se reserva\ninventario"),
        ("3", "Producir", "Se carga\nel spot"),
        ("4", "Al aire", "Continuidad\ntransmite"),
        ("5", "Testigo", "Se comprueba\nla emisión"),
        ("6", "Cobrar", "Factura y\ncobranza"),
    ]
    for i, (n, t, s) in enumerate(steps):
        x = 70 + i * 310
        card(im, (x, 220, x + 280, 620), 18)
        d = ImageDraw.Draw(im)
        d.ellipse((x + 95, 270, x + 185, 360), fill=RED)
        d.text((x + 125, 290), n, font=F(32, True), fill=WHITE)
        d.text((x + 40, 400), t, font=F(26, True), fill=NAVY)
        d.text((x + 40, 470), s, font=F(18), fill=MUTED)
        if i < 5:
            d = ImageDraw.Draw(im)
            d.polygon([(x + 285, 400), (x + 305, 420), (x + 285, 440)], fill=YELLOW)
    card(im, (70, 700, 1850, 940), 18, NAVY)
    d = ImageDraw.Draw(im)
    d.text((110, 760), "Resultado:", font=F(24, True), fill=YELLOW)
    d.text(
        (110, 820),
        "Operación ordenada + evidencia comercial + visibilidad gerencial en un solo sistema.",
        font=F(22),
        fill=WHITE,
    )
    footer(ImageDraw.Draw(im), "11", total)
    save_slide(im, "11-flujo.png", slides)


def slide_cierre(slides, total):
    im = Image.new("RGBA", (W, H), NAVY_DEEP)
    d = ImageDraw.Draw(im)
    d.ellipse((-200, 600, 600, 1400), fill=(30, 50, 90))
    d.ellipse((1400, -100, 2100, 500), fill=(140, 30, 40))
    smart = load(ASSETS / "logo-smart-apps.png", h=80)
    paste(im, smart, (80, 80))
    fm = load(ASSETS / "logo-fm105.png", h=100)
    paste(im, fm, (W - fm.width - 80, 80))
    d = ImageDraw.Draw(im)
    d.text((80, 280), "FM105 ONE", font=F(22, True), fill=YELLOW)
    d.text((80, 340), "Sistema Integral\npara Radioemisoras", font=F(52, True), fill=WHITE)
    d.text(
        (80, 520),
        "Operar el aire, vender con control, comprobar transmisión\ny crecer con datos — en una sola plataforma.",
        font=F(24),
        fill=(200, 210, 225),
    )
    rr(d, (80, 660, 620, 760), 18, YELLOW)
    d.text((130, 690), "Smart Apps × FM105 ONE", font=F(26, True), fill=NAVY)
    d.text((80, 900), "Gracias", font=F(36, True), fill=WHITE)
    d.text((80, 960), f"{total}/{total}", font=F(16, True), fill=YELLOW)
    save_slide(im, "12-cierre.png", slides)


def build_pdf(slides: list[Path]):
    c = pdfcanvas.Canvas(str(PDF_PATH), pagesize=(W, H))
    for p in slides:
        c.drawImage(ImageReader(str(p)), 0, 0, width=W, height=H)
        c.showPage()
    c.save()
    # also copy to artifacts
    ART.mkdir(parents=True, exist_ok=True)
    import shutil

    shutil.copy(PDF_PATH, ART / PDF_PATH.name)
    print("PDF", PDF_PATH)


def main():
    slides: list[Path] = []
    # Clean previous generated slides
    if OUT.exists():
        for old in OUT.glob("*.png"):
            old.unlink()
    if ART.exists():
        for old in ART.glob("*.png"):
            old.unlink()

    total = 12

    slide_portada(slides, total)
    slide_agenda(slides, total)
    slide_problema(slides, total)
    slide_solucion(slides, total)
    slide_beneficios(slides, total)

    modules_slide(
        slides,
        total,
        6,
        "06-modulos-operacion-1.png",
        "Módulos · Operación (1/2)",
        "Núcleo para poner y controlar el aire",
        [
            ("Dashboard", "Estado general de la estación: aire, ventas, alertas y accesos rápidos."),
            ("Portal público", "Sitio web moderno: en vivo, noticias, programación, locutores y contacto."),
            ("Radio en vivo / Streaming", "Control de señal Icecast/Shoutcast, oyentes, bitrate y metadata."),
            ("Noticias / Newsroom", "Gestión de notas, categorías, publicación web/app y apoyo a cabina."),
            ("Programación", "Parrilla diaria/semanal/mensual con locutor, horarios y patrocinios."),
            ("Locutores", "Perfiles con foto, bio, programas, redes y contenido asociado."),
        ],
    )
    modules_slide(
        slides,
        total,
        7,
        "07-modulos-operacion-2.png",
        "Módulos · Operación (2/2)",
        "Producción, continuidad y cumplimiento al aire",
        [
            ("Producción", "Jingles, promocionales, comerciales, IDs y control de vigencia."),
            ("Biblioteca de audios", "Repositorio MP3/WAV con categorías, metadatos y búsqueda."),
            ("Continuidad", "Consola al aire con semáforo de spots y siguiente programa."),
            ("Music scheduling", "Rotación inteligente de música con reglas por horario/categoría."),
            ("Voice tracking remoto", "Locuciones grabadas fuera de cabina e insertadas en parrilla."),
            ("Logger / Testigos", "Grabación 24/7 y comprobantes de transmisión para anunciantes."),
        ],
    )
    modules_slide(
        slides,
        total,
        8,
        "08-modulos-comercial.png",
        "Módulos · Comercial y finanzas",
        "De la cotización a la cobranza con evidencia",
        [
            ("CRM / Clientes", "Prospectos, contactos, seguimiento, visitas, notas y archivos."),
            ("Cotizaciones y campañas", "Propuestas, paquetes, vigencia y campañas activas."),
            ("Órdenes de transmisión", "Spots a emitir: fechas, cantidad, total y estatus."),
            ("Inventario + Rate card", "Avails por franja y tarifas oficiales por horario/producto."),
            ("Portal anunciante + reconciliación", "El cliente ve campañas/testigos; se cruza vendido vs aire."),
            ("CFDI, cobranza, pagos y crédito", "Facturación 4.0, estados de cuenta, SPEI/tarjeta y límites."),
        ],
    )
    modules_slide(
        slides,
        total,
        9,
        "09-modulos-audiencia.png",
        "Módulos · Audiencia y canales",
        "Engagement digital y presencia multiplataforma",
        [
            ("Mensajes a cabina", "Saludos y reportes desde web, WhatsApp y app con moderación."),
            ("Concursos, encuestas y clubes", "Dinámicas, votaciones y fidelización de oyentes."),
            ("Mapa / analytics de oyentes", "Ubicación, picos de audiencia y retención del stream."),
            ("Podcast CMS + Radio visual", "Episodios/RSS y experiencia visual para redes/video."),
            ("App móvil oyentes", "En vivo, noticias, programación, podcasts y push."),
            ("App operador + Alexa", "Control remoto de operación y sintonía por voz."),
        ],
    )
    modules_slide(
        slides,
        total,
        10,
        "10-modulos-plataforma.png",
        "Módulos · Plataforma",
        "Gobierno, alertas, KPIs e infraestructura SaaS",
        [
            ("Alertas", "Avisos de stream caído, spots retrasados o cobranza vencida."),
            ("Reportes / KPIs", "Tableros comercial y CEO exportables a PDF/Excel."),
            ("Usuarios y roles", "Permisos por perfil: locutor, ventas, continuidad, dirección."),
            ("Integraciones", "WhatsApp Business, Meta Ads, Contpaqi/Aspel y PAC CFDI."),
            ("Whitelabel multi-tenant", "Varias estaciones en una plataforma, cada una con su marca."),
            ("Configuración", "Identidad, stream, catálogos, notificaciones y parámetros."),
        ],
    )

    slide_flujo(slides, total)
    slide_cierre(slides, total)

    build_pdf(slides)
    print(f"Total slides: {len(slides)}")


if __name__ == "__main__":
    main()
