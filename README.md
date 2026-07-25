# FM105 ONE — Borrador + demos para cliente

Producto: sistema integral SaaS para radioemisoras (tenant piloto FM105 Guaymas).

## Para enviar al cliente

Carpeta **[`cliente-demos/`](./cliente-demos/)** — mockups en **PNG** (estilo SaaS / ChatGPT):

| Archivo | Contenido |
| --- | --- |
| `00-portada-demos.png` | Portada del paquete |
| `01-portal-publico.png` | Sitio web público (radioescucha) |
| `02-sistema-comercial.png` | Ventas / órdenes / KPIs |
| `03-continuidad.png` | Operación al aire |
| `04-dashboard-ceo.png` | KPIs gerenciales |
| `05-app-movil.png` | App móvil (3 pantallas) |
| `06-brochure-comercial.png` | Brochure comercial |

Incluyen logo FM105 y fotos de Gerardo Castro, Iván Vaca, Karla Montaño y Ramón Barrera.

```bash
python3 scripts/generar_demos_cliente.py
```

## Documentación

- [BORRADOR.md](./BORRADOR.md)

> Solo borrador + demos visuales. Sin aplicación Laravel todavía.
