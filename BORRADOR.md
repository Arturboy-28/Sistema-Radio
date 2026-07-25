# FM105 ONE — Sistema Integral para Radioemisoras

> **Borrador de producto.** No es implementación ni código.
> Fuente: prompt original (ChatGPT). Documento de trabajo para alinear alcance antes de programar.

---

## 1. Objetivo

Plataforma web **SaaS** moderna para administrar una radioemisora de forma integral, unificando en un solo sistema:

| Área | Módulos |
| --- | --- |
| Público | Sitio web, streaming en vivo |
| Operación | Programación, producción, continuidad |
| Comercial | Ventas, CRM, clientes, facturación, cobranza |
| Dirección | KPI gerenciales |
| Canales | Aplicación móvil |

El sistema debe ser **multiempresa (multi-tenant)** para venderse como SaaS a múltiples estaciones de radio.

**Referencia de calidad:** producto SaaS empresarial (Salesforce / HubSpot / Dynamics), con UX moderna, responsive y altamente visual. Priorizar UX/UI, rendimiento y escalabilidad.

**Nombre de producto (estación piloto):** FM105 ONE  
**Referencia pública actual:** [fm105.com.mx](https://fm105.com.mx) (rediseño total, no copia 1:1)

---

## 2. Stack propuesto (pendiente de arranque)

### Backend

- Laravel 12
- PHP 8.4
- MySQL 8
- Autenticación: Laravel Breeze
- Roles/permisos: Spatie Laravel Permission

### Frontend (admin / portal)

- Bootstrap 5.3
- AdminLTE 4
- Vue.js (componentes)
- ChartJS
- DataTables
- SweetAlert2
- Select2
- AJAX
- REST API

### Arquitectura Laravel (cuando se programe)

Modular, con buenas prácticas:

- Service Layer
- Repository Pattern
- Policies
- Form Requests
- API Resources
- Events

Cada módulo debe poder mantenerse y ampliarse de forma independiente.

---

## 3. Identidad visual FM105

| Token | Color | Hex |
| --- | --- | --- |
| Principal | Azul marino | `#14274E` |
| Acento fuerte | Rojo | `#D62828` |
| Acento CTA | Amarillo | `#FFC300` |
| Superficie | Gris | `#ECECEC` |
| Fondo / texto inverso | Blanco | `#FFFFFF` |

**Referencias de estilo (inspiración, no copia):** Spotify, HubSpot, Power BI, Apple, Microsoft Fluent.

---

## 4. Menú principal (backoffice)

1. Dashboard  
2. Portal Público  
3. Radio en Vivo  
4. Noticias  
5. Programación  
6. Locutores  
7. Producción  
8. Biblioteca de Audios  
9. Continuidad  
10. Ventas  
11. Clientes  
12. Cotizaciones  
13. Campañas  
14. Órdenes de Transmisión  
15. Facturación  
16. Cobranza  
17. Reportes  
18. KPIs  
19. Usuarios  
20. Configuración  

---

## 5. Portal público

Sitio moderno inspirado en fm105.com.mx, totalmente rediseñado.

### 5.1 Header

- Logo FM105  
- Menú: Inicio · En Vivo · Noticias · Programación · Podcasts · Locutores · Galería · Contacto  
- Botón rojo: **ESCUCHAR EN VIVO**

### 5.2 Hero

- Imagen grande del estudio / micrófono / locutores  
- Botón amarillo: **Escuchar en Vivo**  
- Panel lateral **Ahora Suena**: nombre del programa, conductor, horario  

### 5.3 Programación

Cards con: fotografía del conductor, horario, programa, descripción.

### 5.4 Noticias

Cards con: imagen, título, fecha, categoría.

### 5.5 Clima

Guaymas, Sonora — temperatura y estado del tiempo.

### 5.6 Redes sociales

Facebook · Instagram · TikTok · X · YouTube · WhatsApp

### 5.7 Footer

Streaming · Apps · Aviso de privacidad · Contacto

---

## 6. Módulo de streaming

Mostrar:

| Bloque | Datos |
| --- | --- |
| Estado | Conectado / Desconectado |
| Audiencia | Oyentes |
| Señal | Bitrate, servidor |
| Automatización | AutoDJ |
| Servidores | Icecast / Shoutcast |
| Metadata | Canción, artista, álbum, tiempo restante |

---

## 7. Locutores

Cada locutor tendrá:

- Fotografía  
- Nombre  
- Biografía  
- Programas  
- Horario  
- Redes sociales  
- Galería  
- Podcast  

**Locutores iniciales (fotos a proporcionar):**

1. Gerardo Castro  
2. Iván Vaca  
3. Karla Montaño  
4. Ramón Barrera  

---

## 8. Programación

- Calendario semanal  
- Vista diaria / semanal / mensual  
- Drag and drop  

Cada programa: color, horario, locutor, patrocinadores, publicidad.

---

## 9. Producción / biblioteca

Biblioteca de audios:

- Jingles  
- Promocionales  
- Comerciales  
- Identificaciones  
- Fondos musicales  

Metadatos: categorías, versiones, fechas de vigencia.  
Subida: MP3, WAV.

---

## 10. Continuidad

Vista estilo consola:

- Horario actual  
- Programa actual  
- Siguiente programa  
- Spots pendientes  

**Semáforo**

| Color | Significado |
| --- | --- |
| Verde | Transmitido |
| Amarillo | Próximo |
| Rojo | Retrasado |

---

## 11. CRM

- Clientes  
- Contactos  
- Prospectos  
- Seguimiento  
- Visitas  
- Llamadas  
- Notas  
- Archivos  

---

## 12. Ventas

- Cotizaciones  
- Contratos  
- Campañas  
- Órdenes  
- Comerciales  
- Calendario / agenda  

---

## 13. Facturación y cobranza

- CFDI 4.0 (XML / PDF)  
- Cancelaciones  
- Complementos  
- Estados de cuenta  
- Cobranza  

---

## 14. Dashboard comercial

Indicadores:

- Ventas del mes  
- Ingresos  
- Campañas activas  
- Clientes activos  
- Spots vendidos  
- Meta mensual  
- Top vendedores  
- Facturación  
- Cobranza  

Gráficas: ChartJS.

---

## 15. Dashboard CEO

Diseño tipo Power BI — tarjetas KPI:

- Ingresos del mes, facturación, cobranza  
- Utilidad, margen  
- Programas rentables  
- Top clientes / anunciantes  
- Ocupación comercial  
- Horas disponibles  
- Spots transmitidos  
- Audiencia  
- Ingresos por horario / por programa  

Comparativos: mensual, anual, por sucursal.  
Exportar: PDF, Excel.

---

## 16. App móvil

Pantallas:

1. Splash  
2. Login  
3. Escuchar en vivo  
4. Noticias  
5. Programación  
6. Locutores  
7. Podcast  
8. Enviar mensaje  
9. Notificaciones push  

---

## 17. Datos, seguridad y API

### Base de datos

- Migraciones normalizadas  
- Foreign keys  
- Soft deletes  
- Auditoría / bitácora / historial  

### Seguridad

- 2FA  
- Logs  
- Roles y permisos  
- Bloqueo por intentos  
- Gestión de sesiones  

### REST API (consumidores)

Streaming · Noticias · Programación · Locutores · Clientes · Ventas · Dashboard · App móvil

---

## 18. Multi-tenant (SaaS)

- Una instancia / lógica que atienda **múltiples radioemisoras**  
- Aislamiento de datos por empresa (tenant)  
- Configuración por estación (marca, stream, usuarios, comercial)  
- FM105 como estación piloto / tenant de referencia  

---

## 19. Fases sugeridas (borrador de roadmap)

Sin programar aún; solo orden de valor:

| Fase | Enfoque |
| --- | --- |
| 0 | Este borrador + identidad + estructura de módulos |
| 1 | Auth, multi-tenant, usuarios/roles, configuración |
| 2 | Portal público + streaming + programación + locutores |
| 3 | Producción + continuidad |
| 4 | CRM + ventas + órdenes de transmisión |
| 5 | Facturación CFDI + cobranza |
| 6 | Dashboards comercial y CEO |
| 7 | App móvil + API completa |

---

## 20. Decisiones abiertas

- ¿App móvil nativa (Flutter/RN) o PWA primero?  
- ¿Proveedor de facturación CFDI (PAC) preferido?  
- ¿Hosting / aislamiento de tenants (DB compartida vs schema/DB por tenant)?  
- ¿Prioridad de MVP interno FM105 vs producto SaaS multiestación desde el día 1?  
- Assets: logo oficial, fotos de locutores, imágenes de estudio.  

---

## 21. Assets para demos (recibidos)

| Asset | Uso |
| --- | --- |
| Logo FM105 (`logo2026final`) | Portal, menú admin, splash |
| Gerardo Castro | Locutores / programación / continuidad |
| Iván Vaca | Locutores / programación |
| Karla Montaño | Locutores / programación |
| Ramón Barrera E. | Locutores / programación |

Ubicación en repo: `demo/assets/`

## 22. Demos para cliente (PNG)

Paquete listo para enviar: carpeta `cliente-demos/`

1. `01-portal-publico.png`  
2. `02-programacion.png`  
3. `03-continuidad.png`  
4. `04-clientes-crm.png`  
5. `05-kpi-gerenciales.png`  

Regenerar: `python3 scripts/generar_demos_cliente.py`

## 23. Próximos pasos

1. Validar demos con el cliente y ajustar textos/programas reales.  
2. Definir MVP de FM105.  
3. Wireframes faltantes (facturación, app móvil).  
4. Recién después: scaffolding Laravel y módulos.

---

*Documento de trabajo — FM105 ONE. Demos HTML únicamente; sin backend.*
