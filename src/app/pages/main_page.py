"""
Página Principal - Lectorcitos
Módulos 1-7 integrados
Python 3.12.9
Voy a animarlos con CSS puro — el favicon con bounce/glow en el sidebar, y el búho con animación de "hablar" (boca/cuerpo) y "caminar" (balanceo).Animar el favicon en el sidebar con CSS bounce+glow
"""

import streamlit as st  # SIEMPRE PRIMERO

# ── set_page_config DEBE ser la primera llamada Streamlit ──────
st.set_page_config(
    page_title="Lectorcitos - Aprende a Leer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import sys
import random
import threading
from pathlib import Path

# Ajustar path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

# Imports de módulos propios
# ─────────────────────────────────────────────────────────────────
# Estrategia de resolución de rutas:
#
#   Contenedor Linux (WORKDIR /app):
#     project_root = /app
#     módulos en  = /app/src/app/api/  y  /app/src/app/components/
#     sys.path necesita /app/src/app para que 'api.*' resuelva
#
#   Desarrollo Windows:
#     project_root = C:/apps-master/app_lectorcitos
#     módulos en  = project_root/src/app/api/
# ─────────────────────────────────────────────────────────────────
import importlib as _il

_import_ok     = False
_errores_import = []

# Rutas candidatas donde viven api/ y components/
_src_app_path = project_root / "src" / "app"   # /app/src/app  (contenedor)
_app_path     = project_root / "app"            # /app/app      (alternativa)

for _base in [_src_app_path, _app_path]:
    if not _base.exists():
        continue
    _base_str = str(_base)
    if _base_str not in sys.path:
        sys.path.insert(0, _base_str)
    # Limpiar módulos cacheados de intento anterior para evitar ImportError fantasma
    for _m in list(sys.modules.keys()):
        if _m.startswith(("api.", "components.")):
            del sys.modules[_m]
    _il.invalidate_caches()
    try:
        word_api   = _il.import_module("api.word_api").word_api
        tts_api    = _il.import_module("api.tts_api").tts_api
        phrase_api = _il.import_module("api.phrase_api").phrase_api
        pdf_api    = _il.import_module("api.pdf_api").pdf_api
        image_api  = _il.import_module("api.image_api").image_api
        avatar     = _il.import_module("components.avatar").avatar
        _import_ok = True
        break
    except Exception as _e:
        _errores_import.append(f"{_base_str}: {type(_e).__name__}: {_e}")
        # Limpiar módulos parcialmente importados para evitar conflictos
        for _mod in ["api.word_api","api.tts_api","api.phrase_api",
                     "api.pdf_api","components.avatar"]:
            _il.invalidate_caches()
        continue

if not _import_ok:
    st.error("❌ No se pudieron importar los módulos de Lectorcitos")
    for _err in _errores_import:
        st.error(_err)
    st.info(f"sys.path: {sys.path[:8]}")
    st.info(f"project_root: {project_root}  (existe: {project_root.exists()})")
    st.info(f"src/app existe: {_src_app_path.exists()}")
    st.stop()


# ══════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
* { font-family: 'Quicksand', sans-serif; }

.main-title {
    color: #FF6B6B; font-size: 3.5rem; font-weight: 700;
    text-align: center; margin: 0.5rem 0;
    text-shadow: 3px 3px 0px #FFE3E3;
}
.palabra-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem; border-radius: 30px; text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin: 1rem 0;
}
.palabra-card h2 { color:white; font-size:1.5rem; margin-bottom:0.5rem; opacity:0.9; }
.palabra-card h1 { color:white; font-size:5rem; font-weight:700; margin:0;
    text-shadow: 4px 4px 0px rgba(0,0,0,0.2); }
.section-title {
    color: #4A5568; font-size: 2rem; font-weight: 600;
    margin: 1.5rem 0 1rem 0; border-bottom: 3px solid #FFE3E3;
    padding-bottom: 0.5rem;
}
.frase-card {
    background: linear-gradient(135deg, #6BCB77, #4D9E52);
    padding: 1.5rem 2rem; border-radius: 25px; margin: 1rem 0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15); text-align: center;
}
.frase-card p { color:white; font-size:1.6rem; font-weight:600; margin:0;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }
.objetivo-especial {
    background: linear-gradient(45deg, #FF6B6B, #FFB347);
    color: white; font-size: 3rem; font-weight: bold;
    padding: 1rem; border-radius: 50px; text-align: center;
    box-shadow: 0 0 20px #FF6B6B; border: 4px solid white; margin: 1rem 0;
    animation: pulse-syl 2s ease-in-out infinite;
}
.seleccion-info {
    background: #E3F2FD; padding: 1rem; border-radius: 15px;
    text-align: center; font-size: 1.2rem; margin: 1rem 0;
}
.footer { text-align:center; color:#888; padding:2rem 0 1rem 0; font-size:0.9rem; }

@keyframes pulse-syl {
    0%,100% { transform: scale(1); }
    50%      { transform: scale(1.03); }
}
</style>
""", unsafe_allow_html=True)


# ── Favicon dinámico ─────────────────────────────────────────────
_fav_candidatos = [
    Path(__file__).resolve().parent.parent.parent.parent / "public" / "avatares" / "favicon.ico",
    project_root / "public" / "avatares" / "favicon.ico",
    Path("/app/public/avatares/favicon.ico"),
]
_fav_path = next((p for p in _fav_candidatos if p.exists()), None)
if _fav_path:
    import base64 as _b64fav
    with open(str(_fav_path), "rb") as _ff:
        _fav_b64 = _b64fav.b64encode(_ff.read()).decode()
    st.markdown(
        f'<link rel="shortcut icon" href="data:image/x-icon;base64,{_fav_b64}">',
        unsafe_allow_html=True,
    )



# ══════════════════════════════════════════════════════════════════
# AUDIO — función central con componente HTML (evita bloqueo del navegador)
# ══════════════════════════════════════════════════════════════════
def reproducir_audio_html(texto: str, idioma: str):
    """
    Reproduce audio usando un componente HTML <audio autoplay>.
    Esto evita que el navegador bloquee la reproducción automática
    y que st.rerun() corte el audio antes de terminar.
    """
    import base64
    import logging
    logging.warning(f"🔊 TTS REQUEST: texto='{texto}' | idioma='{idioma}'")
    
    ruta = tts_api.generar_audio(texto.lower(), idioma)
    ruta = tts_api.generar_audio(texto.lower(), idioma)
    if not ruta:
        return
    try:
        with open(ruta, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        # Cada llamada genera un id único para forzar recarga del elemento
        uid = abs(hash(texto + idioma)) % 999999
        st.components.v1.html(
            f"""
            <audio id="aud_{uid}" autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var a = document.getElementById('aud_{uid}');
                if(a) a.play().catch(()=>{{}});
            </script>
            """,
            height=0,
        )
    except Exception as e:
        st.warning(f"No se pudo reproducir: {e}")


# ══════════════════════════════════════════════════════════════════
# PRE-CARGA EN HILO SEPARADO
# ══════════════════════════════════════════════════════════════════
def preload_audio(palabra, silabas, consonantes, idioma):
    def task(p, s, c, i):
        try:
            tts_api.generar_audio(p.lower(), i)
            for x in s:
                try: tts_api.generar_audio(x.lower(), i)
                except: pass
            for x in c:
                try: tts_api.generar_audio(x.lower(), i)
                except: pass
        except: pass
    threading.Thread(target=task, args=(palabra, list(silabas), list(consonantes), idioma), daemon=True).start()


# ══════════════════════════════════════════════════════════════════
# INICIALIZACIÓN DE SESSION STATE
# ══════════════════════════════════════════════════════════════════
def init_session_state():
    if 'idioma' not in st.session_state:
        st.session_state.idioma = 'es'

    if 'palabra_actual' not in st.session_state:
        info = word_api.obtener_info_palabra(st.session_state.idioma)
        st.session_state.palabra_actual  = info['palabra']
        st.session_state.consonantes     = info['consonantes']
        st.session_state.silabas         = info['silabas']

    defaults = {
        'puntaje':               0,
        'mensaje_avatar':        None,
        'ejercicio_activo':      False,
        'silaba_objetivo':       None,
        'palabras_ejercicio':    [],
        'palabras_correctas':    [],
        'hay_correctas':         True,
        'seleccion_usuario':     [],
        'ejercicio_completado':  False,
        'mensaje_resultado':     "",
        'bienvenida_reproducida':False,
        'audio_preloaded':       False,
        # Módulo 4
        'frase_actual':          "",
        'mostrar_frase':         False,
        # Módulo 7 — anti-repetición y celebración
        'silabas_usadas':        [],    # historial para no repetir sílaba objetivo
        'palabras_usadas':       [],    # historial para no repetir palabras en ejercicios
        'tocar_aplauso':         False, # flag: reproducir aplauso en siguiente render
        'tocar_animo':           False, # flag: reproducir ánimo en siguiente render
        'racha_aciertos':        0,     # racha de ejercicios correctos seguidos
        'racha_maxima':          0,     # racha máxima histórica de la sesión
        # Cierre / reporte
        'nombre_nino':           "",    # nombre ingresado para el reporte
        'palabras_practicadas':  [],    # palabras vistas en ejercicios
        'pantalla_salida':       False, # mostrar pantalla de despedida
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.session_state.mensaje_avatar is None:
        st.session_state.mensaje_avatar = avatar.get_mensaje("bienvenida", st.session_state.idioma)

    # ExerciseAPI — usa la misma ruta ya resuelta por el bloque de imports
    if 'exercise_api' not in st.session_state:
        try:
            ExerciseAPI = _il.import_module("api.exercise_api").ExerciseAPI
            st.session_state.exercise_api = ExerciseAPI(word_api)
        except Exception as _e:
            st.error(f"Error importando ExerciseAPI: {_e}")
            st.stop()


init_session_state()

# ══════════════════════════════════════════════════════════════════
# MÓDULO 7 — Reproducir sonidos de celebración/ánimo al renderizar
# Se usan flags en session_state para que el audio se dispare UNA
# sola vez justo después del st.rerun() de comprobar_ejercicio.
# ══════════════════════════════════════════════════════════════════
def _audio_celebracion(idioma: str):
    """Audio inline de aplauso generado con gTTS (sin archivo .wav externo)."""
    textos = {
        'es': ["¡Bravo!", "¡Aplausos!", "¡Fantástico!", "¡Excelente trabajo!"],
        'en': ["Bravo!", "Great job!", "Fantastic!", "Excellent!"],
    }
    texto = random.choice(textos.get(idioma, textos['es']))
    reproducir_audio_html(texto, idioma)

def _audio_animo(idioma: str):
    """Audio inline de ánimo generado con gTTS."""
    textos = {
        'es': ["¡Tú puedes!", "¡Inténtalo de nuevo!", "¡Casi lo logras!"],
        'en': ["You can do it!", "Try again!", "Almost there!"],
    }
    texto = random.choice(textos.get(idioma, textos['en']))
    reproducir_audio_html(texto, idioma)

if not st.session_state.audio_preloaded:
    preload_audio(
        st.session_state.palabra_actual,
        st.session_state.silabas,
        st.session_state.consonantes,
        st.session_state.idioma,
    )
    st.session_state.audio_preloaded = True


# ══════════════════════════════════════════════════════════════════
# HELPERS DE AUDIO (usan la función central)
# ══════════════════════════════════════════════════════════════════
# Diccionario de traducción ES→EN
_TRADUCCION = {
    "TOMATE":"TOMATO","CASA":"HOUSE","PERRO":"DOG","GATO":"CAT",
    "SOL":"SUN","LUNA":"MOON","MESA":"TABLE","SILLA":"CHAIR",
    "AGUA":"WATER","FUEGO":"FIRE","PELOTA":"BALL","MOTOR":"MOTOR",
    "CAMINO":"ROAD","JARDIN":"GARDEN","FLOR":"FLOWER","ARBOL":"TREE",
    "LIBRO":"BOOK","LAPIZ":"PENCIL","MANZANA":"APPLE","PLATANO":"BANANA"
}
# Opción: fallback con deep-translator si la palabra no está en el diccionario
def _traducir_palabra(palabra: str, destino: str = 'en') -> str:
    if palabra in _TRADUCCION:
        return _TRADUCCION[palabra]
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='es', target=destino).translate(palabra)
    except:
        return palabra  # fallback seguro
        
def _get_palabra_idioma(idioma: str) -> str:
    """Retorna la palabra en el idioma correcto para el audio."""
    palabra = st.session_state.palabra_actual
    if idioma == 'en':
        return _TRADUCCION.get(palabra, palabra)
    return palabra

def reproducir_palabra():
    palabra = _get_palabra_idioma(st.session_state.idioma)
    reproducir_audio_html(palabra, st.session_state.idioma)
    st.session_state.mensaje_avatar = avatar.get_mensaje("audio_instruccion", st.session_state.idioma)

def reproducir_silaba(silaba: str):
    reproducir_audio_html(silaba, st.session_state.idioma)
    st.session_state.mensaje_avatar = (
        f"🦉 ¡Excelente! Escuchaste **{silaba}**. ¿Ves cómo suena?"
        if st.session_state.idioma == 'es'
        else f"🦉 Great! You heard **{silaba}**. See how it sounds?"
    )

def reproducir_consonante(consonante: str):
    reproducir_audio_html(consonante, st.session_state.idioma)
    st.session_state.mensaje_avatar = (
        f"🦉 Esta es la letra **{consonante}**. ¡Pon mucha atención!"
        if st.session_state.idioma == 'es'
        else f"🦉 This is the letter **{consonante}**. Listen closely!"
    )

def reproducir_frase():
    if st.session_state.frase_actual:
        reproducir_audio_html(st.session_state.frase_actual, st.session_state.idioma)


# ══════════════════════════════════════════════════════════════════
# LÓGICA DE EJERCICIO
# ══════════════════════════════════════════════════════════════════
def seleccionar_silaba_sin_repetir(silabas: list) -> str:
    """Elige sílaba evitando repetir las últimas usadas. Resetea cuando se agota la variedad."""
    usadas = st.session_state.silabas_usadas
    ventana = min(3, max(1, len(silabas) // 2))
    candidatas = [s for s in silabas if s not in usadas[-ventana:]]
    if not candidatas:
        st.session_state.silabas_usadas = []
        candidatas = silabas
    elegida = random.choice(candidatas)
    st.session_state.silabas_usadas.append(elegida)
    if len(st.session_state.silabas_usadas) > len(silabas):
        st.session_state.silabas_usadas = st.session_state.silabas_usadas[-len(silabas):]
    return elegida


def iniciar_ejercicio():
    silabas = st.session_state.silabas
    if not silabas or not st.session_state.exercise_api:
        return

    # Anti-repetición de sílaba objetivo
    silaba_obj = seleccionar_silaba_sin_repetir(silabas)
    palabras, correctas, hay_correctas, mensaje = st.session_state.exercise_api.generar_palabras_ejercicio(
        silaba_obj, st.session_state.idioma, num_palabras=6
    )

    # Anti-repetición de palabras: regenerar si hay demasiado solapamiento
    usadas = st.session_state.palabras_usadas
    for _ in range(4):
        solapamiento = len([p for p in palabras if p in usadas[-6:]])
        if solapamiento <= 2:
            break
        palabras, correctas, hay_correctas, mensaje = st.session_state.exercise_api.generar_palabras_ejercicio(
            silaba_obj, st.session_state.idioma, num_palabras=6
        )

    # Registrar palabras mostradas (historial acotado a 30)
    st.session_state.palabras_usadas = (usadas + palabras)[-30:]
    # Registrar palabra del día en practicadas (para reporte)
    pal = st.session_state.palabra_actual
    if pal not in st.session_state.palabras_practicadas:
        st.session_state.palabras_practicadas.append(pal)

    st.session_state.update({
        'ejercicio_activo':     True,
        'silaba_objetivo':      silaba_obj,
        'palabras_ejercicio':   palabras,
        'palabras_correctas':   correctas,
        'hay_correctas':        hay_correctas,
        'seleccion_usuario':    [],
        'ejercicio_completado': False,
        'mensaje_resultado':    "",
        'mensaje_avatar':       f"🦉 {mensaje}",
        'mostrar_frase':        False,
        'tocar_aplauso':        False,
        'tocar_animo':          False,
    })
    st.rerun()


def comprobar_ejercicio():
    exito, aciertos, errores, tipo, mensaje = st.session_state.exercise_api.verificar_seleccion(
        st.session_state.seleccion_usuario,
        st.session_state.palabras_correctas,
        st.session_state.hay_correctas,
    )
    idioma = st.session_state.idioma

    if exito:
        st.session_state.puntaje += 1
        st.session_state.racha_aciertos += 1
        if st.session_state.racha_aciertos > st.session_state.racha_maxima:
            st.session_state.racha_maxima = st.session_state.racha_aciertos
        st.session_state.ejercicio_completado = True
        st.session_state.tocar_aplauso = True
        st.session_state.tocar_animo   = False
        st.session_state.mensaje_resultado = f"✅ {mensaje}"

        # Toast de celebración con racha
        racha = st.session_state.racha_aciertos
        if racha >= 5:
            st.toast("🔥 ¡RACHA DE 5! ¡Eres increíble!" if idioma=="es" else "🔥 5 IN A ROW! You're amazing!", icon="🏆")
        elif racha >= 3:
            st.toast(f"⚡ ¡{racha} seguidas! ¡Sigue así!" if idioma=="es" else f"⚡ {racha} in a row! Keep it up!", icon="⭐")
        else:
            st.toast("¡Muy bien! +1 punto 🎉" if idioma=="es" else "Great job! +1 point 🎉", icon="✅")

        # Módulo 4 — frase creativa
        frase = phrase_api.generar_frase(st.session_state.palabra_actual, idioma)
        st.session_state.frase_actual  = frase
        st.session_state.mostrar_frase = True
        st.session_state.mensaje_avatar = phrase_api.get_instruccion(idioma)

    else:
        st.session_state.racha_aciertos = 0   # romper racha
        st.session_state.tocar_aplauso  = False
        st.session_state.tocar_animo    = True
        st.session_state.mensaje_resultado = mensaje
        st.session_state.mensaje_avatar    = f"🦉 {mensaje}"

        # Toast de ánimo según tipo de error
        mensajes_animo = {
            "FALTAN":   ("🔍 ¡Casi! Te faltan algunas palabras.", "🔍 Almost! You're missing some words."),
            "ERRORES":  ("🤔 Tienes de más. ¡Revisa tu selección!", "🤔 Too many selected. Review your choices!"),
            "MIXTO":    ("💪 ¡Tú puedes! Inténtalo de nuevo.", "💪 You can do it! Try again."),
            "SOBRANTE": ("⚠️ No hay palabras correctas aquí.", "⚠️ There are no correct words here."),
        }
        txt_es, txt_en = mensajes_animo.get(tipo, ("💪 ¡Inténtalo de nuevo!", "💪 Try again!"))
        st.toast(txt_es if idioma == "es" else txt_en, icon="🤔")

    st.rerun()


# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Favicon en sidebar ───────────────────────────────────────
    _fav_sb_candidatos = [
        Path(__file__).resolve().parent.parent.parent.parent / "public" / "avatares" / "favicon.ico",
        project_root / "public" / "avatares" / "favicon.ico",
        Path("/app/public/avatares/favicon.ico"),
    ]
    _fav_sb = next((p for p in _fav_sb_candidatos if p.exists()), None)
    if _fav_sb:
        import base64 as _b64
        with open(str(_fav_sb), "rb") as _f:
            _fav_sb_b64 = _b64.b64encode(_f.read()).decode()
        st.markdown(f"""
        <style>
        @keyframes fav-bounce {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg) scale(1); }}
            20%       {{ transform: translateY(-10px) rotate(-8deg) scale(1.1); }}
            40%       {{ transform: translateY(-18px) rotate(6deg) scale(1.15); }}
            60%       {{ transform: translateY(-10px) rotate(-4deg) scale(1.1); }}
            80%       {{ transform: translateY(-4px) rotate(2deg) scale(1.05); }}
        }}
        @keyframes fav-glow {{
            0%, 100% {{ filter: drop-shadow(0 0 4px #FF6B6B88); }}
            50%       {{ filter: drop-shadow(0 0 16px #FF6B6B) drop-shadow(0 0 32px #FFD93D); }}
        }}
        .fav-animado {{
            animation: fav-bounce 2.5s ease-in-out infinite,
                       fav-glow   2.5s ease-in-out infinite;
            display: block;
            margin: 0.5rem auto;
            width: 56px;
            cursor: pointer;
        }}
        </style>
        <div style='text-align:center;'>
            <img src='data:image/x-icon;base64,{_fav_sb_b64}'
                 class='fav-animado' alt='Lectorcitos'/>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        @keyframes emoji-bounce {{
            0%,100% {{ transform: translateY(0) scale(1); }}
            50%      {{ transform: translateY(-12px) scale(1.2); }}
        }}
        .emoji-bounce {{ animation: emoji-bounce 2s ease-in-out infinite;
                         display:block; text-align:center; font-size:2.5rem; }}
        </style>
        <div class='emoji-bounce'>📚</div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Nombre del niño ───────────────────────────────────────────
    lbl_nombre = "👦 Tu nombre:" if st.session_state.idioma == 'es' else "👦 Your name:"
    nombre_input = st.text_input(lbl_nombre, value=st.session_state.nombre_nino,
                                  key="input_nombre", max_chars=30)
    if nombre_input != st.session_state.nombre_nino:
        st.session_state.nombre_nino = nombre_input

    st.markdown("---")

    # ── Selector de idioma ────────────────────────────────────────
    nuevo_idioma = st.selectbox(
        "Idioma / Language",
        options=['es', 'en'],
        format_func=lambda x: '🇪🇸 Español' if x == 'es' else '🇬🇧 English',
        key='idioma_selector',
    )
    if nuevo_idioma != st.session_state.idioma:
        info = word_api.obtener_info_palabra(nuevo_idioma)
        st.session_state.update({
            'idioma':               nuevo_idioma,
            'palabra_actual':       info['palabra'],
            'consonantes':          info['consonantes'],
            'silabas':              info['silabas'],
            'mensaje_avatar':       avatar.get_mensaje("bienvenida", nuevo_idioma),
            'ejercicio_activo':     False,
            'audio_preloaded':      False,
            'bienvenida_reproducida': False,
            'mostrar_frase':        False,
            'frase_actual':         "",
        })
        st.rerun()

    if st.button("🔄 Nueva Palabra", use_container_width=True):
        info = word_api.obtener_info_palabra(st.session_state.idioma)
        st.session_state.update({
            'palabra_actual':   info['palabra'],
            'consonantes':      info['consonantes'],
            'silabas':          info['silabas'],
            'mensaje_avatar':   avatar.get_mensaje("palabra_dia", st.session_state.idioma),
            'ejercicio_activo': False,
            'audio_preloaded':  False,
            'mostrar_frase':    False,
            'frase_actual':     "",
        })
        st.rerun()

    st.markdown("---")

    # ── Puntaje ───────────────────────────────────────────────────
    st.markdown(f"""
    <div style='text-align:center; padding:1rem; background:#FFE3E3; border-radius:15px; margin-bottom:0.5rem;'>
        <h2 style='color:#FF6B6B; margin:0;'>🏆 {st.session_state.puntaje}</h2>
        <p style='margin:0; color:#666; font-size:0.85rem;'>{'puntos' if st.session_state.idioma=='es' else 'points'}</p>
        <p style='margin:0.3rem 0 0 0; color:#FF6B6B; font-size:0.8rem;'>
            🔥 {'Racha máx:' if st.session_state.idioma=='es' else 'Best streak:'} {st.session_state.racha_maxima}
        </p>
    </div>""", unsafe_allow_html=True)

    # ── Botón imprimir reporte ────────────────────────────────────
    lbl_rep = "📄 Imprimir reporte" if st.session_state.idioma == 'es' else "📄 Print report"
    if st.button(lbl_rep, use_container_width=True, key="btn_reporte"):
        st.session_state.pantalla_salida = True
        st.rerun()

    st.markdown("---")

    # ── Botón cerrar sesión ───────────────────────────────────────
    lbl_cerrar = "🚪 Cerrar sesión" if st.session_state.idioma == 'es' else "🚪 Close session"
    if st.button(lbl_cerrar, use_container_width=True, key="btn_cerrar", type="primary"):
        st.session_state.pantalla_salida = True
        st.rerun()


# ══════════════════════════════════════════════════════════════════
# PANTALLA DE SALIDA / REPORTE
# ══════════════════════════════════════════════════════════════════
def _generar_pdf_reporte() -> bytes:
    """Genera PDF de reporte de sesión con nombre, puntaje, racha y palabras."""
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
    from datetime import datetime

    idioma   = st.session_state.idioma
    nombre   = st.session_state.nombre_nino or ("Estudiante" if idioma=="es" else "Student")
    puntaje  = st.session_state.puntaje
    racha    = st.session_state.racha_maxima
    palabras = st.session_state.palabras_practicadas
    fecha    = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Medallas según puntaje
    def medalla(p):
        if p >= 20: return ("*** Maestro Lector", "*** Master Reader")
        if p >= 10: return ("**  Lector Experto", "**  Expert Reader")
        if p >= 5:  return ("*   Buen Lector",   "*   Good Reader")
        return ("... Aprendiz",  "... Apprentice")
    med_es, med_en = medalla(puntaje)
    medalla_txt = med_es if idioma == "es" else med_en

    # Frase motivacional
    frases_es = [
        "¡Cada palabra que aprendes te hace más inteligente!",
        "¡Seguir leyendo es el mejor superpoder!",
        "¡Los grandes lectores fueron primero grandes aprendices!",
    ]
    frases_en = [
        "Every word you learn makes you smarter!",
        "Keep reading - it's the best superpower!",
        "Great readers were once great learners too!",
    ]
    import random as _rnd
    frase_mot = _rnd.choice(frases_es if idioma=="es" else frases_en)

    pdf = FPDF()
    pdf.set_margins(20, 25, 20)
    pdf.add_page()

    # Encabezado
    pdf.set_fill_color(255, 107, 107)
    pdf.rect(0, 0, 210, 22, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    titulo_enc = "Lectorcitos - Mi Reporte de Aprendizaje" if idioma=="es" else "Lectorcitos - My Learning Report"
    pdf.cell(0, 22, titulo_enc, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # Nombre y fecha
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(102, 126, 234)
    lbl_nombre = "Nombre:" if idioma=="es" else "Name:"
    pdf.cell(0, 12, f"{lbl_nombre}  {nombre}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(150, 150, 150)
    lbl_fecha = f"Fecha: {fecha}" if idioma=="es" else f"Date: {fecha}"
    pdf.cell(0, 8, lbl_fecha, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # Tarjeta de puntaje
    pdf.set_fill_color(255, 227, 227)
    pdf.set_draw_color(255, 107, 107)
    pdf.set_line_width(0.8)
    pdf.rect(20, pdf.get_y(), 170, 36, "FD")
    pdf.set_xy(20, pdf.get_y() + 4)
    pdf.set_font("Helvetica", "B", 36)
    pdf.set_text_color(255, 107, 107)
    lbl_pts = f"{puntaje} pts"  # sin emoji para Helvetica
    # fpdf no soporta emojis en Helvetica - usar texto simple
    lbl_pts = f"{puntaje} {'puntos' if idioma=='es' else 'points'}"
    pdf.cell(170, 16, lbl_pts, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(80, 80, 80)
    lbl_racha = f"Racha maxima: {racha}" if idioma=="es" else f"Best streak: {racha}"
    pdf.cell(170, 10, lbl_racha, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    # Medalla
    pdf.set_fill_color(255, 243, 224)
    pdf.set_draw_color(255, 179, 71)
    pdf.rect(20, pdf.get_y(), 170, 18, "FD")
    pdf.set_xy(20, pdf.get_y() + 3)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(180, 100, 0)
    pdf.cell(170, 12, medalla_txt, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    # Palabras practicadas
    if palabras:
        pdf.set_fill_color(102, 126, 234)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 12)
        lbl_pals = "Palabras practicadas:" if idioma=="es" else "Words practiced:"
        pdf.cell(170, 12, lbl_pals, align="C", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)
        colores_pal = [(255,107,107),(77,150,255),(76,175,80),(255,179,71),(156,39,176)]
        ancho_cel = 34
        for i, pal in enumerate(palabras[:15]):  # máx 15
            r,g,b = colores_pal[i % len(colores_pal)]
            pdf.set_fill_color(r,g,b)
            pdf.set_text_color(255,255,255)
            pdf.set_font("Helvetica","B",11)
            pdf.cell(ancho_cel, 12, pal.upper(), align="C", fill=True, border=1)
            if (i+1) % 5 == 0:
                pdf.ln()
        resto = len(palabras[:15]) % 5
        if resto != 0:
            pdf.ln()
        pdf.ln(4)

    # Frase motivacional
    pdf.set_fill_color(232, 245, 233)
    pdf.set_draw_color(76, 175, 80)
    pdf.set_line_width(0.5)
    y_antes = pdf.get_y()
    pdf.rect(20, y_antes, 170, 20, "FD")
    pdf.set_xy(20, y_antes + 3)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(46, 125, 50)
    pdf.multi_cell(170, 7, f'"{frase_mot}"', align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # Pie
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(180, 180, 180)
    pie = "Aprendiendo a leer con Lectorcitos | 2026" if idioma=="es" else "Learning to read with Lectorcitos | 2026"
    pdf.cell(0, 10, pie, align="C")

    return bytes(pdf.output())


if st.session_state.get('pantalla_salida'):
    idioma = st.session_state.idioma
    nombre = st.session_state.nombre_nino or ("Estudiante" if idioma=="es" else "Student")

    # Fondo de celebración
    st.markdown("""
    <div style='background:linear-gradient(135deg,#667eea,#764ba2);
        padding:2rem; border-radius:30px; text-align:center; margin-bottom:1.5rem;'>
        <h1 style='color:white;font-size:3rem;margin:0;'>
            🎉 ¡Hasta pronto! 🎉
        </h1>
    </div>""", unsafe_allow_html=True)

    col_res1, col_res2, col_res3 = st.columns([1,2,1])
    with col_res2:
        lbl_res = "Resumen de tu sesión" if idioma=="es" else "Your session summary"
        st.markdown(f"""
        <div style='background:#FFF8F0;border:3px solid #FF6B6B;border-radius:25px;
            padding:2rem;text-align:center;box-shadow:0 8px 20px rgba(0,0,0,0.1);'>
            <h2 style='color:#667eea;margin-bottom:0.5rem;'>👦 {nombre}</h2>
            <h3 style='color:#888;font-weight:400;margin-top:0;'>{lbl_res}</h3>
            <hr style='border-color:#FFE3E3;'>
            <div style='display:flex;justify-content:space-around;margin:1rem 0;'>
                <div>
                    <div style='font-size:3rem;font-weight:bold;color:#FF6B6B;'>
                        {st.session_state.puntaje}
                    </div>
                    <div style='color:#888;font-size:0.9rem;'>
                        {'puntos' if idioma=='es' else 'points'}
                    </div>
                </div>
                <div>
                    <div style='font-size:3rem;font-weight:bold;color:#FF6B6B;'>
                        {st.session_state.racha_maxima}
                    </div>
                    <div style='color:#888;font-size:0.9rem;'>
                        {'racha max' if idioma=='es' else 'best streak'}
                    </div>
                </div>
                <div>
                    <div style='font-size:3rem;font-weight:bold;color:#FF6B6B;'>
                        {len(st.session_state.palabras_practicadas)}
                    </div>
                    <div style='color:#888;font-size:0.9rem;'>
                        {'palabras' if idioma=='es' else 'words'}
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Botón descargar PDF reporte
        try:
            pdf_rep = _generar_pdf_reporte()
            nombre_archivo_rep = f"lectorcitos_reporte_{nombre.lower().replace(' ','_')}.pdf"
            st.download_button(
                label="⬇️ Descargar reporte PDF" if idioma=="es" else "⬇️ Download PDF report",
                data=pdf_rep,
                file_name=nombre_archivo_rep,
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
        except Exception as e:
            st.error(f"Error generando reporte: {e}")

        st.markdown("<br>", unsafe_allow_html=True)
        c_volver, c_nuevo = st.columns(2)
        with c_volver:
            lbl_volver = "▶️ Seguir jugando" if idioma=="es" else "▶️ Keep playing"
            if st.button(lbl_volver, use_container_width=True):
                st.session_state.pantalla_salida = False
                st.rerun()
        with c_nuevo:
            lbl_nuevo = "🔄 Nueva sesión" if idioma=="es" else "🔄 New session"
            if st.button(lbl_nuevo, use_container_width=True, type="primary"):
                # Resetear todo excepto idioma y nombre
                keys_reset = [
                    'puntaje','racha_aciertos','racha_maxima','palabras_practicadas',
                    'palabras_usadas','silabas_usadas','ejercicio_activo',
                    'mostrar_frase','frase_actual','mensaje_resultado',
                    'pantalla_salida','tocar_aplauso','tocar_animo',
                ]
                for k in keys_reset:
                    if k in st.session_state:
                        del st.session_state[k]
                info = word_api.obtener_info_palabra(st.session_state.idioma)
                st.session_state.palabra_actual = info['palabra']
                st.session_state.consonantes    = info['consonantes']
                st.session_state.silabas        = info['silabas']
                st.rerun()

    st.stop()  # No renderizar el resto de la página

# ══════════════════════════════════════════════════════════════════
# CONTENIDO PRINCIPAL
# ══════════════════════════════════════════════════════════════════
st.markdown("<h1 class='main-title'>📚 Lectorcitos</h1>", unsafe_allow_html=True)

# Avatar — sin audio automático en el primer render (evita bloqueo por gTTS)
avatar.mostrar(
    st.session_state.mensaje_avatar,
    avatar.get_instruccion("silaba", st.session_state.idioma),
    reproducir_audio=False,
)
st.session_state.bienvenida_reproducida = True


# ── Palabra del Día ───────────────────────────────────────────────
st.markdown("<h2 class='section-title'>📚 Palabra del Día</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:

    img_url = image_api.obtener_imagen(
    st.session_state.palabra_actual,
    st.session_state.idioma
)
if img_url:
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:1rem;'>
        <img src='{img_url}'
             style='max-height:200px; border-radius:20px;
                    box-shadow:0 8px 20px rgba(0,0,0,0.2);
                    object-fit:cover; width:100%;'
             alt='{st.session_state.palabra_actual}'/>
    </div>""", unsafe_allow_html=True)


    col_audio1, col_audio2 = st.columns(2)
    with col_audio1:
        if st.button("🔊 Español", use_container_width=True, type="secondary"):
            reproducir_audio_html(_get_palabra_idioma("es"), "es")
    with col_audio2:
        if st.button("🔊 English", use_container_width=True, type="secondary"):
            reproducir_audio_html(_get_palabra_idioma("en"), "en")
            
# ── ¿Qué son las sílabas? ────────────────────────────────────────
_texto_silabas_es = (
    "Las sílabas son los sonidos que forman las palabras. "
    "Cada sílaba tiene una consonante y una vocal. "
    "Por ejemplo, en la palabra tomate, las consonantes son T y M. "
    "Con ellas formamos: ta, te, ti, to, tu, y ma, me, mi, mo, mu. "
    "Haz clic en cualquier sílaba para escucharla."
)
_texto_silabas_en = (
    "Syllables are the sounds that make up words. "
    "Each syllable has a consonant and a vowel. "
    "For example, in the word tomato, the consonants are T and M. "
    "With them we make: ta, te, ti, to, tu, and ma, me, mi, mo, mu. "
    "Click any syllable to hear it."
)

with st.expander("✨ ¿Qué son las sílabas?" if st.session_state.idioma=='es' else "✨ What are syllables?", expanded=True):
    col_av, col_txt, col_btn = st.columns([1, 7, 1])

    with col_av:
        _buho_candidatos = [
            Path(__file__).resolve().parent.parent.parent.parent / "public" / "avatares" / "buho_guia.png",
            project_root / "public" / "avatares" / "buho_guia.png",
            Path("/app/public/avatares/buho_guia.png"),
            Path("C:/apps-master/app_lectorcitos/public/avatares/buho_guia.png"),
            Path("C:/apps-master/public/avatares/buho_guia.png"),
        ]
        ruta_buho = next((p for p in _buho_candidatos if p.exists()), None)
        if ruta_buho:
            import base64 as _b64exp
            with open(str(ruta_buho), "rb") as _fexp:
                _buho_exp_b64 = _b64exp.b64encode(_fexp.read()).decode()
            st.markdown(f"""
            <style>
            @keyframes buho-exp-walk {{
                0%,100% {{ transform: translateX(0) rotate(0deg) scaleX(1); }}
                30%     {{ transform: translateX(5px) rotate(5deg) scaleX(1); }}
                50%     {{ transform: translateX(0) rotate(0deg) scaleX(-1); }}
                80%     {{ transform: translateX(-5px) rotate(-5deg) scaleX(-1); }}
            }}
            .buho-exp {{
                animation: buho-exp-walk 2.5s ease-in-out infinite;
                display: block; margin: 0 auto; width: 70px;
                transform-origin: center bottom;
            }}
            </style>
            <img src='data:image/png;base64,{_buho_exp_b64}' class='buho-exp' alt='Buho'/>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:3rem;text-align:center'>🦉</div>",
                        unsafe_allow_html=True)

    with col_txt:
        if st.session_state.idioma == 'es':
            st.markdown("""
            Las **sílabas** son los sonidos que forman las palabras. Cada sílaba tiene una **consonante** y una **vocal**.

            Por ejemplo, en **TOMATE**: consonantes **T** y **M** → sílabas **TA TE TI TO TU / MA ME MI MO MU**

            ¡Haz clic en cualquier sílaba para escucharla!
            """)
        else:
            st.markdown("""
            **Syllables** are the sounds that make up words. Each syllable has a **consonant** and a **vowel**.

            For example, in **TOMATO**: consonants **T** and **M** → syllables **TA TE TI TO TU / MA ME MI MO MU**

            Click any syllable to hear it!
            """)

    with col_btn:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        lbl = "🔊 ES+EN" if st.session_state.idioma == 'es' else "🔊 ES+EN"
        tip = "Escuchar en Español e Inglés" if st.session_state.idioma == 'es' else "Hear in Spanish & English"
        if st.button(lbl, key="btn_leer_explicacion", help=tip, use_container_width=True):
            if st.session_state.idioma == 'es':
                reproducir_audio_html(_texto_silabas_es, 'es')
            else:
                reproducir_audio_html(_texto_silabas_en, 'en')


# ── Consonantes y Sílabas ────────────────────────────────────────
st.markdown("<h2 class='section-title'>✨ Sílabas</h2>", unsafe_allow_html=True)
st.markdown(f"**{'🔤 ¡Haz clic en las letras para escucharlas!' if st.session_state.idioma=='es' else '🔤 Click on the letters to hear them!'}**")

cols_cons = st.columns(max(len(st.session_state.consonantes), 1))
for i, cons in enumerate(st.session_state.consonantes):
    with cols_cons[i]:
        if st.button(cons, key=f"cons_{cons}", use_container_width=True):
            reproducir_consonante(cons)

silabas = st.session_state.silabas
if silabas:
    colores = ['#FFE3E3', '#E3F2FD', '#E8F5E9', '#FFF3E0', '#F3E5F5']
    cols = st.columns(5)
    for i, silaba in enumerate(silabas):
        with cols[i % 5]:
            if st.button(silaba, key=f"sil_{i}", use_container_width=True, type="secondary"):
                reproducir_silaba(silaba)
            st.markdown(f"<div style='background:{colores[(i//5)%len(colores)]};height:5px;border-radius:0 0 10px 10px;margin-top:-5px;'></div>", unsafe_allow_html=True)
else:
    st.warning("No se generaron sílabas para esta palabra.")


# ══════════════════════════════════════════════════════════════════
# MÓDULO 2 — Ejercicio interactivo
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("<h2 class='section-title'>🎮 ¡A JUGAR!</h2>", unsafe_allow_html=True)

if not st.session_state.ejercicio_activo:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 ¡COMENZAR EJERCICIO!", use_container_width=True, type="primary"):
            iniciar_ejercicio()
else:
    col1, col2 = st.columns([2, 1])

    with col1:
        if st.session_state.hay_correctas:
            st.markdown(f"""
            <div class='objetivo-especial'>
                🔍 {st.session_state.silaba_objetivo}
                <div style='font-size:1rem;margin-top:0.5rem;background:rgba(255,255,255,0.3);padding:0.3rem;border-radius:20px;'>
                    {len(st.session_state.palabras_correctas)} palabra(s) con esta sílaba
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='objetivo-especial' style='background:#FFB347;'>
                🔍 {st.session_state.silaba_objetivo}
                <div style='font-size:1rem;margin-top:0.5rem;background:rgba(255,255,255,0.3);padding:0.3rem;border-radius:20px;'>
                    ⚠️ ¡NINGUNA palabra tiene esta sílaba!
                </div>
            </div>""", unsafe_allow_html=True)

        palabras = st.session_state.palabras_ejercicio
        for i in range(0, len(palabras), 2):
            cols_ej = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx < len(palabras):
                    palabra = palabras[idx]
                    seleccionada = palabra in st.session_state.seleccion_usuario
                    with cols_ej[j]:
                        if st.button(f"📝 {palabra}", key=f"ej_{idx}_{palabra}",
                                     use_container_width=True,
                                     type="primary" if seleccionada else "secondary"):
                            if seleccionada:
                                st.session_state.seleccion_usuario.remove(palabra)
                                st.session_state.mensaje_avatar = f"🦉 Quitaste {palabra}."
                            else:
                                st.session_state.seleccion_usuario.append(palabra)
                                es_correcta = palabra in st.session_state.palabras_correctas
                                if es_correcta:
                                    # Reproducir la palabra en ES y EN al seleccionar correcta
                                    reproducir_audio_html(palabra, 'es')
                                    reproducir_audio_html(palabra, 'en')
                                    encontradas = len([p for p in st.session_state.seleccion_usuario if p in st.session_state.palabras_correctas])
                                    total = len(st.session_state.palabras_correctas)
                                    st.session_state.mensaje_avatar = (
                                        f"🌟 ¡Encontraste todas! Dale a COMPROBAR."
                                        if encontradas >= total
                                        else f"✅ ¡Muy bien! **{palabra}** es correcta. ¡Sigue buscando!"
                                    )
                                else:
                                    st.session_state.mensaje_avatar = f"🦉 ¿Seguro que **{palabra}** tiene **{st.session_state.silaba_objetivo}**?"
                            st.rerun()

    with col2:
        st.markdown("### 📋 Tu selección")
        num_sel = len(st.session_state.seleccion_usuario)
        num_cor = len(st.session_state.palabras_correctas)

        bg = "#E3F2FD" if st.session_state.hay_correctas else "#FFE3E3"
        icono = "✅" if st.session_state.hay_correctas else "⚠️"
        conteo = f"{num_sel} / {num_cor}" if st.session_state.hay_correctas else str(num_sel)
        st.markdown(f"""
        <div class='seleccion-info' style='background:{bg};'>
            <div style='font-size:2rem;'>{icono}</div>
            <div style='font-size:2rem;font-weight:bold;'>{conteo}</div>
            <div>palabras seleccionadas</div>
        </div>""", unsafe_allow_html=True)

        for p in st.session_state.seleccion_usuario:
            if st.session_state.hay_correctas and p in st.session_state.palabras_correctas:
                st.markdown(f"✅ **{p}** (correcta)")
            else:
                st.markdown(f"❌ {p}")

        if st.session_state.mensaje_resultado:
            if "✅" in st.session_state.mensaje_resultado:
                st.success(st.session_state.mensaje_resultado)
            elif "❌" in st.session_state.mensaje_resultado:
                st.error(st.session_state.mensaje_resultado)
            else:
                st.warning(st.session_state.mensaje_resultado)

        st.markdown("---")
        if st.button("🚫 NO HAY PALABRAS", use_container_width=True,
                     type="secondary" if st.session_state.seleccion_usuario else "primary"):
            st.session_state.seleccion_usuario = []
            comprobar_ejercicio()

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔍 COMPROBAR", use_container_width=True, type="primary"):
                comprobar_ejercicio()
        with c2:
            if st.button("🔄 OTRO", use_container_width=True):
                iniciar_ejercicio()

    # ── Módulo 7 — Celebración/ánimo: se renderiza aquí, en el ciclo correcto ──
    if st.session_state.get('tocar_aplauso'):
        _audio_celebracion(st.session_state.idioma)
        st.session_state.tocar_aplauso = False
        st.balloons()

    if st.session_state.get('tocar_animo'):
        _audio_animo(st.session_state.idioma)
        st.session_state.tocar_animo = False

    # ── Módulo 4 — Frase creativa (aparece al completar) ──────────
    if st.session_state.mostrar_frase and st.session_state.frase_actual:
        st.markdown("---")
        st.markdown(
            "<h2 class='section-title'>📖 " +
            ("¡Mi Historia!" if st.session_state.idioma=='es' else "My Story!") +
            "</h2>",
            unsafe_allow_html=True,
        )
        col_f1, col_f2, col_f3 = st.columns([1, 4, 1])
        with col_f2:
            emoji = phrase_api.get_emoji_frase(st.session_state.idioma)
            st.markdown(f"""
            <div class='frase-card'>
                <p>{emoji} {st.session_state.frase_actual}</p>
            </div>""", unsafe_allow_html=True)

            c_a, c_b, c_c = st.columns([1, 1, 1])
            with c_a:
                if st.button("🔊 Escuchar frase" if st.session_state.idioma=='es' else "🔊 Hear story",
                             use_container_width=True):
                    reproducir_frase()
            with c_b:
                if st.button("🔀 Nueva frase" if st.session_state.idioma=='es' else "🔀 New story",
                             use_container_width=True):
                    st.session_state.frase_actual = phrase_api.generar_frase(
                        st.session_state.palabra_actual, st.session_state.idioma
                    )
                    st.rerun()

        # ── Módulo 6 — Descargar PDF ──────────────────────────────
        st.markdown("---")
        st.markdown(
            "<h2 class='section-title'>📄 " +
            ("Descargar ficha de ejercicios" if st.session_state.idioma=='es' else "Download exercise sheet") +
            "</h2>",
            unsafe_allow_html=True,
        )
        col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
        with col_p2:
            if st.button(
                "📄 Generar PDF" if st.session_state.idioma=='es' else "📄 Generate PDF",
                use_container_width=True, type="secondary", key="btn_generar_pdf"
            ):
                with st.spinner("Generando PDF..." if st.session_state.idioma=='es' else "Generating PDF..."):
                    try:
                        pdf_bytes = pdf_api.generar_pdf(
                            palabra=st.session_state.palabra_actual,
                            silabas=st.session_state.silabas,
                            frase=st.session_state.frase_actual,
                            idioma=st.session_state.idioma,
                        )
                        nombre = pdf_api.nombre_archivo(
                            st.session_state.palabra_actual, st.session_state.idioma
                        )
                        st.download_button(
                            label="⬇️ Descargar PDF" if st.session_state.idioma=='es' else "⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=nombre,
                            mime="application/pdf",
                            use_container_width=True,
                        )
                        st.success("¡PDF listo!" if st.session_state.idioma=='es' else "PDF ready!")
                    except Exception as e:
                        st.error(f"Error generando PDF: {e}")


# ══════════════════════════════════════════════════════════════════
# PIE DE PÁGINA
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<p class='footer'>🦉 Aprendiendo a leer con audio y diversión | © 2026 Lectorcitos</p>",
    unsafe_allow_html=True,
)