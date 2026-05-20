# 📚 Lectorcitos — Aprende a Leer / Learn to Read

> Aplicación interactiva bilingüe (Español / English) para enseñar a leer a niños
> mediante sílabas, audio real, ejercicios gamificados y reportes descargables.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Módulos Implementados](#módulos-implementados)
4. [Requisitos](#requisitos)
5. [Instalación](#instalación)
6. [Configuración de Rutas](#configuración-de-rutas)
7. [Ejecución](#ejecución)
8. [Archivos Principales](#archivos-principales)
9. [Session State](#session-state)
10. [Caché de Audio](#caché-de-audio)
11. [Solución de Problemas](#solución-de-problemas)

---

## Descripción General

**Lectorcitos** es una aplicación Streamlit diseñada para niños en etapa inicial de
lectura. Combina texto, audio generado con `gTTS` (Google Text-to-Speech), ejercicios
interactivos y un sistema de gamificación con puntaje, rachas y medallas.

Características principales:

- Soporte bilingüe completo **Español / English** con cambio en tiempo real
- Audio HTML autoplay que evita el bloqueo del navegador
- Ejercicios de reconocimiento de sílabas con anti-repetición inteligente
- Avatar Búho 🦉 que guía al niño con mensajes y audio
- Generación de frases creativas contextualizadas (Módulo 4)
- PDF descargable de ejercicios por palabra (Módulo 6)
- Reporte de sesión en PDF con nombre, puntaje, racha y palabras practicadas
- Logo animado con efectos CSS (bounce + glow)
- Pantalla de cierre con resumen y opciones de nueva sesión

---

## Estructura del Proyecto

```
C:/apps-master/app_lectorcitos/
│
├── app/
│   ├── api/
│   │   ├── word_api.py          # API de palabras y sílabas
│   │   ├── tts_api.py           # API de Text-to-Speech (gTTS)
│   │   ├── exercise_api.py      # API de ejercicios interactivos
│   │   ├── phrase_api.py        # API de frases creativas (Módulo 4)  ← NUEVO
│   │   └── pdf_api.py           # API de generación de PDF (Módulo 6) ← NUEVO
│   │
│   └── components/
│       └── avatar.py            # Componente Avatar Búho 🦉
│
├── src/
│   └── lib/
│       ├── palabras_es.json     # Lista de palabras en español
│       └── palabras_en.json     # Lista de palabras en inglés
│
├── pages/
│   └── main_page.py             # Página principal (Módulos 1–7)
│
└── public/
    ├── favicon.ico
    ├── logo-lectorcitos.png
    ├── avatares/
    │   └── buho_guia.png
    └── audio_cache/             # Caché persistente de archivos .mp3
```

---

## Módulos Implementados

### Módulo 1 — Núcleo Léxico (`word_api.py`)
- Carga listas de palabras desde JSON (`palabras_es.json`, `palabras_en.json`)
- Extrae consonantes únicas de cada palabra
- Genera todas las combinaciones consonante+vocal (sílabas)
- Entrega un diccionario completo: `{ palabra, consonantes, silabas, idioma }`

### Módulo 2 — Ejercicio Interactivo (`exercise_api.py` + `main_page.py`)
- Selecciona sílaba objetivo con **anti-repetición inteligente** (ventana deslizante)
- Genera 6 palabras mezcladas (correctas + distractoras) con **anti-repetición de palabras**
- Maneja el caso especial donde ninguna palabra contiene la sílaba objetivo
- Verificación detallada: COMPLETO / FALTAN / ERRORES / MIXTO / NINGUNA

### Módulo 3 — Gamificación (`main_page.py`)
- Puntaje acumulado visible en sidebar con racha máxima histórica
- `st.toast()` con 4 variantes: acierto simple, racha ×3, racha ×5, errores específicos
- `st.balloons()` al completar ejercicio exitosamente
- Audio de celebración (`¡Bravo!`, `¡Aplausos!`) o ánimo (`¡Tú puedes!`) via gTTS
- Reproducción bilingüe de la palabra seleccionada correctamente (ES + EN)

### Módulo 4 — Generador de Frases (`phrase_api.py`)
- Genera frases creativas: `"El/La [Palabra] [verbo] [lugar]."`
- Maneja artículos masculino/femenino en español mediante lista de palabras femeninas conocidas
- Listas de verbos y lugares independientes por idioma (ES / EN)
- Se activa automáticamente al completar un ejercicio con éxito
- Botones: 🔊 Escuchar frase / 🔀 Nueva frase

### Módulo 5 — Multi-idioma (`main_page.py` + todos los módulos)
- Selector ES/EN en sidebar — recarga palabra, sílabas, mensajes y audio
- Todos los textos de UI, avatar, ejercicios y PDFs respetan el idioma seleccionado
- `st.session_state.idioma` persiste durante toda la sesión

### Módulo 6 — Exportación PDF (`pdf_api.py`)
**Ficha de ejercicios por palabra** — se activa tras completar un ejercicio:
1. Portada: palabra grande + cuadrícula de sílabas en colores
2. Frase creativa del Módulo 4
3. Hoja de ejercicios: sílaba faltante, rodear sílabas, copiar palabra, contar sílabas, oración libre

**Reporte de sesión** — desde pantalla de cierre:
- Nombre del niño, fecha y hora
- Puntaje y racha máxima
- Medalla de nivel: `...` Aprendiz / `*` Buen Lector / `**` Experto / `***` Maestro
- Cuadrícula de palabras practicadas
- Frase motivacional aleatoria

> **Nota:** Ambos PDFs usan fuente Helvetica (built-in). Todos los emojis y
> caracteres fuera de Latin-1 se filtran con `limpiar_texto()` para evitar errores.

### Módulo 7 — Estética y Validaciones (`main_page.py`)
- CSS con animaciones: `pulse-syl`, `logo-bounce`, `logo-glow`
- Logo animado en sidebar (bounce 3s + glow pulsante) via base64 inline
- `st.toast()` contextual en todos los eventos
- Anti-repetición de sílabas y palabras entre ejercicios consecutivos
- Pantalla de cierre con resumen, descarga de reporte y opción de nueva sesión

---

## Requisitos

**Python:** 3.12.9

**Dependencias:**

```txt
streamlit>=1.35.0
gtts>=2.5.1
fpdf2>=2.7.9
```

Instalar con:

```bash
pip install streamlit gtts fpdf2
```

> En entornos con restricciones del sistema (Linux/Podman):
> ```bash
> pip install streamlit gtts fpdf2 --break-system-packages
> ```

---

## Instalación

```bash
# 1. Clonar o copiar el proyecto
cd C:/apps-master/app_lectorcitos

# 2. Instalar dependencias
pip install streamlit gtts fpdf2

# 3. Crear carpetas necesarias si no existen
mkdir -p public/audio_cache
mkdir -p public/avatares
mkdir -p src/lib
```

Asegurarse de tener los archivos de datos:

```
src/lib/palabras_es.json   → { "palabras": ["TOMATE", "CASA", ...] }
src/lib/palabras_en.json   → { "words":    ["TOMATO", "HOUSE", ...] }
```

---

## Configuración de Rutas

Las rutas absolutas de Windows están definidas en el código. Si el proyecto se
mueve de ubicación, actualizar estas constantes en `main_page.py`:

```python
# Sidebar — logo
logo_path = Path("C:/apps-master/public/logo-lectorcitos.png")

# Expander de sílabas — mini búho
ruta_buho = Path("C:/apps-master/public/avatares/buho_guia.png")
```

Y en `tts_api.py`:

```python
# Caché de audio
self.cache_dir = Path("C:/apps-master/app_lectorcitos/public/audio_cache")
```

Y en `word_api.py`:

```python
# Fallback absoluto para las listas de palabras
Path("C:/apps-master/app_lectorcitos/src/lib")
```

---

## Ejecución

```bash
# Desde la raíz del proyecto
streamlit run pages/main_page.py

# O con puerto específico
streamlit run pages/main_page.py --server.port 8501
```

La aplicación abre en `http://localhost:8501`

---

## Archivos Principales

### `main_page.py`
Página principal. Contiene los módulos 1–7 integrados.

| Función | Descripción |
|---|---|
| `init_session_state()` | Inicializa todas las variables de sesión |
| `reproducir_audio_html(texto, idioma)` | Reproduce audio via componente HTML (evita bloqueo del navegador) |
| `preload_audio(...)` | Pre-genera mp3 en hilo separado al cargar nueva palabra |
| `seleccionar_silaba_sin_repetir(silabas)` | Anti-repetición con ventana deslizante |
| `iniciar_ejercicio()` | Genera ejercicio con anti-repetición de palabras |
| `comprobar_ejercicio()` | Verifica selección, actualiza puntaje, dispara toast y audio |
| `_generar_pdf_reporte()` | Genera PDF de reporte de sesión inline |

### `phrase_api.py`
Generador de frases creativas bilingüe.

| Método | Descripción |
|---|---|
| `generar_frase(palabra, idioma)` | Genera una frase: `"El/La [palabra] [verbo] en [lugar]."` |
| `generar_varias_frases(palabra, idioma, cantidad)` | Genera N frases únicas |
| `get_emoji_frase(idioma)` | Emoji decorativo aleatorio |

### `pdf_api.py`
Generador de fichas PDF de ejercicios.

| Método | Descripción |
|---|---|
| `limpiar_texto(texto)` | Filtra caracteres fuera de Latin-1 (emojis, símbolos) |
| `generar_pdf(palabra, silabas, frase, idioma)` | Genera ficha de ejercicios, retorna `bytes` |
| `nombre_archivo(palabra, idioma)` | Nombre sugerido para la descarga |

---

## Session State

Variables gestionadas en `st.session_state`:

| Clave | Tipo | Descripción |
|---|---|---|
| `idioma` | `str` | `'es'` o `'en'` |
| `palabra_actual` | `str` | Palabra del día en mayúsculas |
| `consonantes` | `list` | Consonantes únicas de la palabra |
| `silabas` | `list` | Todas las sílabas generadas |
| `puntaje` | `int` | Puntaje acumulado de la sesión |
| `racha_aciertos` | `int` | Racha actual de aciertos consecutivos |
| `racha_maxima` | `int` | Mejor racha de la sesión |
| `nombre_nino` | `str` | Nombre ingresado para el reporte |
| `palabras_practicadas` | `list` | Palabras vistas en ejercicios (para reporte) |
| `silabas_usadas` | `list` | Historial de sílabas objetivo (anti-repetición) |
| `palabras_usadas` | `list` | Historial de palabras en ejercicios (anti-repetición) |
| `ejercicio_activo` | `bool` | Si hay un ejercicio en curso |
| `silaba_objetivo` | `str` | Sílaba que el niño debe buscar |
| `palabras_ejercicio` | `list` | Palabras mostradas en el ejercicio actual |
| `palabras_correctas` | `list` | Palabras que sí contienen la sílaba objetivo |
| `hay_correctas` | `bool` | `False` si ninguna palabra tiene la sílaba |
| `seleccion_usuario` | `list` | Palabras seleccionadas por el niño |
| `ejercicio_completado` | `bool` | Si el ejercicio actual fue superado |
| `frase_actual` | `str` | Frase creativa generada tras el acierto |
| `mostrar_frase` | `bool` | Controla visibilidad del Módulo 4 |
| `tocar_aplauso` | `bool` | Flag para disparar audio de celebración en el render |
| `tocar_animo` | `bool` | Flag para disparar audio de ánimo en el render |
| `pantalla_salida` | `bool` | Muestra pantalla de cierre/reporte |
| `audio_preloaded` | `bool` | Evita re-generar mp3 en cada render |
| `bienvenida_reproducida` | `bool` | Evita reproducir bienvenida en cada render |

---

## Caché de Audio

Los archivos `.mp3` se generan con `gTTS` y se guardan en:

```
C:/apps-master/app_lectorcitos/public/audio_cache/
```

El nombre de cada archivo es el **MD5** del texto + idioma, lo que garantiza:
- Sin duplicados entre sesiones
- Recuperación instantánea si ya existe
- Independencia del proceso de Python (sin `hash()` que varía por seguridad)

**¿Cuántos archivos se acumulan?**
- Sílabas (por idioma): ~50 archivos × 2 idiomas = ~100 archivos fijos
- Palabras del día: 1 por palabra nueva que se consulte
- Frases creativas: 1 por frase única generada
- Audios de celebración/ánimo: ~10 archivos fijos

En uso normal se acumulan **cientos de archivos de 5–20 KB** cada uno.
No hay impacto en rendimiento porque el acceso es siempre por nombre directo (MD5),
nunca por listado del directorio. Se puede limpiar la carpeta periódicamente sin
consecuencias — simplemente se regenerarán los que se necesiten.

---

## Solución de Problemas

**Página en blanco al iniciar**
- Verificar que `st.set_page_config()` sea la primera llamada de Streamlit en el archivo
- Revisar la consola por errores de import — ejecutar `streamlit run` desde el directorio raíz

**Audio no se reproduce**
- El navegador puede bloquear autoplay sin interacción previa del usuario
- La primera reproducción puede requerir un clic manual en la página
- Verificar que `gTTS` tenga acceso a internet para generar nuevos archivos
- Los archivos ya cacheados funcionan sin internet

**Error en PDF: `Character outside range`**
- Ocurre cuando se pasa un emoji o carácter Unicode > 255 a Helvetica
- Solución: envolver el texto con `limpiar_texto()` de `pdf_api.py` antes de pasarlo a fpdf

**Palabras o sílabas que se repiten mucho**
- El historial de anti-repetición se resetea al cambiar de palabra o iniciar nueva sesión
- Con listas pequeñas de palabras la variedad es limitada — ampliar `palabras_es.json`

**`exercise_api` no importa**
- Verificar que `exercise_api.py` exista en `app/api/` o `src/app/api/`
- El archivo no se incluye en este repositorio por ser parte del núcleo original

---

## Licencia

© 2026 Lectorcitos — Todos los derechos reservados.
Desarrollado con ❤️ para niños que están aprendiendo a leer.
