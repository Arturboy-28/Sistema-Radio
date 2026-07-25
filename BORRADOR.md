# Sistema Radio Fusion — Borrador inicial

> Documento de trabajo. No es especificación final ni implementación.
> Objetivo: alinear idea, alcance y piezas del producto antes de programar.

---

## 1. Idea en una frase

Plataforma para operar y fusionar señales de radio (emisoras / fuentes) en un flujo único de control, programación y reproducción, pensada para uso interno o de estación.

## 2. Problema que busca resolver

Hoy la operación de radio suele repartirse entre herramientas sueltas: playlist, locución, entradas externas, monitoreo y publicación. Sistema Radio Fusion centraliza esa operación en un solo lugar.

## 3. Usuarios previstos (borrador)

| Rol | Qué hace |
| --- | --- |
| Operador / locutor | Controla el aire, cruces, micrófono, fuentes en vivo |
| Programador | Arma parrilla, bloques, rotación musical |
| Administrador | Usuarios, permisos, configuración de fuentes y salidas |
| Oyente (opcional, fase 2) | Escucha el stream público si se publica |

## 4. Alcance propuesto (MVP conceptual)

Incluir en una primera versión:

1. **Catálogo de fuentes** — emisoras, archivos, micrófono, entrada remota.
2. **Mezcla / fusión** — elegir qué fuente va al aire; transición simple (corte o fundido).
3. **Cola / playlist** — orden de reproducción y bloques básicos.
4. **Panel de control** — vista única de “qué está al aire” y controles esenciales.
5. **Registro** — historial mínimo de qué se emitió y cuándo.

Fuera del MVP (para después):

- App móvil nativa
- Automatización avanzada con IA
- Monetización / ads
- Multi-estación con permisos complejos
- Integraciones con redes sociales

## 5. Flujos principales (borrador)

### 5.1 Poner una fuente al aire

1. Operador abre el panel.
2. Selecciona fuente (playlist, micrófono u otra entrada).
3. Confirma cruce / fundido.
4. El sistema deja esa fuente como “al aire” y registra el cambio.

### 5.2 Programar un bloque

1. Programador crea un bloque (hora inicio / fin).
2. Asigna piezas o fuente.
3. En horario, el operador (o el automatismo) lo pone al aire.

### 5.3 Monitoreo

1. Ver estado: al aire, en cola, mute, nivel aproximado.
2. Revisar historial del turno.

## 6. Módulos tentativos

```
Sistema Radio Fusion
├── Fuentes (inputs)
├── Mezcla / Aire
├── Programación
├── Biblioteca / Playlist
├── Usuarios y roles
├── Historial / Logs
└── Salida / Stream (opcional en MVP)
```

## 7. Decisiones abiertas (para definir después)

- ¿Es solo panel de operación, o también stream público?
- ¿Un solo “aire” o varias salas / emisoras?
- ¿Prioridad: escritorio web, desktop app, o ambos?
- ¿Offline / local-first, o siempre en la nube?
- ¿Nombre comercial final: “Sistema Radio”, “Radio Fusion”, otro?

## 8. Criterio de éxito del borrador

Este documento sirve si permite responder:

1. Para quién es.
2. Qué problema ataca.
3. Qué entra en la primera versión.
4. Qué queda fuera a propósito.

Cuando eso esté claro, recién ahí se diseña UI y se programa.

## 9. Próximo paso sugerido (sin código)

- Revisar y corregir este borrador (alcance y roles).
- Acordar las decisiones abiertas de la sección 7.
- Recién después: bosquejo de pantallas (wireframe) y luego implementación.

---

*Última actualización: borrador inicial — sin implementación.*
