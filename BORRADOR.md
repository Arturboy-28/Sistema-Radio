# FM105 ONE — Sistema Integral para Radioemisoras

> **Borrador de producto.** No es implementación ni código.
> Fuente: prompt original (ChatGPT). Documento de trabajo para alinear alcance antes de programar.

---

## 1. Objetivo

Plataforma web **SaaS** moderna para administrar una radioemisora de forma integral, unificando en un solo sistema:

| Área | Módulos |
| --- | --- |
| Público | Sitio web, streaming en vivo, podcast CMS, radio visual |
| Operación | Programación, producción, continuidad, music scheduling, voice tracking, logger, newsroom |
| Comercial | Ventas, CRM, inventario de aire, testigos, portal anunciante, comisiones, rate card |
| Finanzas | Facturación CFDI, cobranza, pagos en línea, crédito |
| Audiencia | Mensajes a cabina, concursos, encuestas, clubes, mapa de oyentes |
| Dirección | KPI gerenciales, alertas, reportes |
| Canales | App móvil, app operador, Alexa / smart speakers |
| Plataforma | Multi-tenant whitelabel, integraciones (WhatsApp, Meta, Contpaqi, PAC) |

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

### Núcleo

1. Dashboard  
2. Portal Público  
3. Radio en Vivo  
4. Noticias / Newsroom  
5. Programación  
6. Locutores  
7. Producción  
8. Biblioteca de Audios  
9. Continuidad  
10. Music Scheduling  
11. Voice Tracking  
12. Logger / Testigos  

### Comercial y finanzas

13. Clientes / CRM  
14. Cotizaciones  
15. Campañas  
16. Órdenes de Transmisión  
17. Inventario de aire (avails)  
18. Rate card  
19. Portal anunciante  
20. Reconciliación orden ↔ aire  
21. Comisiones de vendedores  
22. Facturación CFDI  
23. Cobranza y pagos en línea  
24. Crédito / límites  

### Audiencia y canales

25. Mensajes a cabina  
26. Concursos y dinámicas  
27. Encuestas / votaciones  
28. Clubes de oyentes  
29. Mapa / analytics de oyentes  
30. Podcast CMS  
31. Radio visual  
32. App móvil (oyentes)  
33. App operador  
34. Alexa / smart speakers  

### Plataforma

35. Alertas  
36. Reportes / KPIs  
37. Usuarios y roles  
38. Integraciones  
39. Whitelabel / multi-tenant  
40. Configuración  

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

## 19. Módulos ampliados (ideas incorporadas)

Referencia de mercado: WideOrbit, Marketron, MediaAdmin (MX), RCS, Caster.fm.  
**Estado:** incluidos en alcance de producto (borrador). Prioridad de construcción se define por fases.

### 19.1 Alta prioridad FM105 / México

| # | Módulo | Qué resuelve |
| --- | --- | --- |
| 1 | Testigos / Proof of Performance | Comprobante al anunciante de que el spot salió (hora exacta) |
| 2 | Portal del cliente anunciante | El cliente ve campañas, spots TX, facturas y descarga testigos |
| 3 | Inventario de aire (avails) | Horarios libres para vender por daypart |
| 4 | Reconciliación automática | Cruza orden vendida vs lo transmitido realmente |
| 5 | Logger de audio | Grabación 24/7 legal/operativa de la señal |

### 19.2 Engagement / audiencia

| # | Módulo | Qué resuelve |
| --- | --- | --- |
| 6 | Mensajes a cabina | Web + WhatsApp + app, con moderación |
| 7 | Concursos y dinámicas | Premios, ganadores, historial |
| 8 | Encuestas / votaciones | Interacción en vivo con oyentes |
| 9 | Clubes de oyentes | Registro, puntos, beneficios |
| 10 | Mapa de oyentes | Ciudad, picos, retención del stream |

### 19.3 Contenido

| # | Módulo | Qué resuelve |
| --- | --- | --- |
| 11 | Music scheduling | Rotación inteligente de música (estilo Selector/RCS) |
| 12 | Voice tracking remoto | Locutor graba desde casa e inserta en parrilla |
| 13 | Redacción / newsroom | Guiones, notas al aire, wire de noticias |
| 14 | Podcast CMS | Episodios, RSS, stats de descargas |
| 15 | Radio visual | Artwork/canción para YouTube / Facebook Live |

### 19.4 Comercial avanzado

| # | Módulo | Qué resuelve |
| --- | --- | --- |
| 16 | Paquetes + digital | Aire + redes + banner web en una cotización |
| 17 | Comisiones de vendedores | Metas, ranking, liquidación |
| 18 | Credit check / límites | Tope de crédito por cliente |
| 19 | Pagos en línea | SPEI/tarjeta ligados a cobranza |
| 20 | Rate card | Tarifas por horario y tipo de spot |

### 19.5 Operación / SaaS

| # | Módulo | Qué resuelve |
| --- | --- | --- |
| 21 | App de operador | Control remoto de continuidad / cabina |
| 22 | Alertas | Stream caído, spot retrasado, cobranza vencida |
| 23 | Whitelabel multi-tenant | Cada estación con su marca y dominio |
| 24 | Integraciones | WhatsApp Business, Meta Ads, Contpaqi/Aspel, PAC CFDI |
| 25 | Alexa / smart speakers | “Alexa, pon FM105” |

---

## 20. Fases sugeridas (borrador de roadmap)

Sin programar aún; solo orden de valor:

| Fase | Enfoque |
| --- | --- |
| 0 | Borrador + identidad + catálogo completo de módulos |
| 1 | Auth, multi-tenant, usuarios/roles, configuración, alertas base |
| 2 | Portal público + streaming + programación + locutores + newsroom |
| 3 | Producción + continuidad + logger + testigos |
| 4 | CRM + ventas + órdenes + inventario de aire + rate card |
| 5 | Reconciliación + portal anunciante + comisiones + crédito |
| 6 | Facturación CFDI + cobranza + pagos en línea |
| 7 | Dashboards comercial/CEO + mapa de oyentes |
| 8 | Engagement: mensajes, concursos, encuestas, clubes |
| 9 | Music scheduling + voice tracking + podcast CMS + radio visual |
| 10 | App móvil oyentes + app operador + Alexa + integraciones + whitelabel |

---

## 21. Decisiones abiertas

- ¿App móvil nativa (Flutter/RN) o PWA primero?  
- ¿Proveedor de facturación CFDI (PAC) preferido?  
- ¿Hosting / aislamiento de tenants (DB compartida vs schema/DB por tenant)?  
- ¿Prioridad de MVP interno FM105 vs producto SaaS multiestación desde el día 1?  
- ¿Logger: grabación propia vs integración con equipo existente?  
- ¿Voice tracking y music scheduling nativos o integración con terceros (RCS/Radix/etc.)?  
- Assets: logo oficial, fotos de locutores, imágenes de estudio.  

---

## 22. Assets para demos (recibidos)

| Asset | Uso |
| --- | --- |
| Logo FM105 (`logo2026final`) | Portal, menú admin, splash |
| Gerardo Castro | Locutores / programación / continuidad |
| Iván Vaca | Locutores / programación |
| Karla Montaño | Locutores / programación |
| Ramón Barrera E. | Locutores / programación |

Ubicación en repo: `demo/assets/`

## 23. Demos para cliente (PNG)

Paquete en carpeta `cliente-demos/` (referencia visual ChatGPT).  
Regenerar: `python3 scripts/generar_demos_cliente.py`

## 24. Próximos pasos

1. Validar este catálogo ampliado de módulos.  
2. Marcar qué entra en el **MVP FM105** vs fases posteriores.  
3. Usar demos visuales de ChatGPT para presentación a cliente.  
4. Recién después: scaffolding Laravel por módulos priorizados.

---

*Documento de trabajo — FM105 ONE. Sin implementación de backend.*
