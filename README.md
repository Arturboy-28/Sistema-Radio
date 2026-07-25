# FM105 ONE — Borrador + demos para cliente

Producto: sistema integral SaaS para radioemisoras (tenant piloto FM105 Guaymas).

## Para enviar al cliente

Carpeta **[`cliente-demos/`](./cliente-demos/)** — mockups en **PNG** (fotos), no HTML:

| Archivo | Contenido |
| --- | --- |
| `00-portada-demos.png` | Portada del paquete |
| `01-portal-publico.png` | Sitio web público |
| `02-programacion.png` | Sistema de programación |
| `03-continuidad.png` | Consola de continuidad |
| `04-clientes-crm.png` | CRM / clientes |
| `05-kpi-gerenciales.png` | KPIs y gráficas gerenciales |

Incluyen logo FM105 y fotos de Gerardo Castro, Iván Vaca, Karla Montaño y Ramón Barrera.

Para regenerar las imágenes:

```bash
python3 scripts/generar_demos_cliente.py
```

## Documentación

- [BORRADOR.md](./BORRADOR.md) — especificación completa del producto

> No hay aplicación Laravel todavía. Solo borrador + demos visuales.
