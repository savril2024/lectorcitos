"""
Componente del Avatar Buho
Mensajes con imagen local, audio y explicaciones del juego
Python 3.12.9
Búho avatar principal — tiene 3 modos:

buho-caminar — se balancea de lado a lado, se voltea (scaleX) como si caminara de ida y vuelta. Es el modo normal.
buho-hablar — pulsa arriba/abajo rápido con glow rojo cuando se reproduce audio de bienvenida.
buho-idle — respiración suave (fallback).
"""

import streamlit as st
from pathlib import Path
import sys
import base64

# Ajustar path para imports
current_dir  = Path(__file__).resolve().parent
project_root = current_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.app.api.tts_api import tts_api
except ImportError:
    try:
        from app.api.tts_api import tts_api
    except ImportError:
        try:
            from api.tts_api import tts_api
        except ImportError:
            tts_api = None


def _reproducir_audio_avatar(texto: str, idioma: str) -> None:
    """
    Reproduce audio dentro del avatar usando <audio autoplay> HTML.
    Evita el error: st.audio() got unexpected keyword argument autoplay
    que aparece en versiones modernas de Streamlit cuando se llama
    tts_api.reproducir_texto() que internamente usa st.audio(autoplay=True).
    """
    if tts_api is None:
        return
    try:
        ruta = tts_api.generar_audio(texto.lower(), idioma)
        if not ruta:
            return
        with open(str(ruta), "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        uid = abs(hash(texto + idioma + "avatar")) % 999999
        st.components.v1.html(
            f"""
            <audio id="av_{uid}" autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var a = document.getElementById('av_{uid}');
                if(a) a.play().catch(function(){{}});
            </script>
            """,
            height=0,
        )
    except Exception:
        pass  # Audio es opcional — no romper la UI si falla


def _buscar_imagen_buho() -> Path | None:
    """
    Busca la imagen del buho en todas las rutas posibles:
    desarrollo Windows, contenedor Linux, rutas relativas.
    """
    posibles = [
        # Dentro del proyecto (contenedor /app/ y Windows app_lectorcitos/)
        Path(__file__).resolve().parent.parent.parent.parent / "public" / "avatares" / "buho_guia.png",
        Path("/app/public/avatares/buho_guia.png"),
        # Windows legacy
        Path("C:/apps-master/app_lectorcitos/public/avatares/buho_guia.png"),
        Path("C:/apps-master/public/avatares/buho_guia.png"),
    ]
    for ruta in posibles:
        if ruta.exists():
            return ruta
    return None


class AvatarBuho:
    """Clase para manejar los mensajes del buho guia con imagen y audio"""

    def __init__(self):
        self.ruta_imagen = _buscar_imagen_buho()

        self.mensajes = {
            "es": {
                "bienvenida":          "Hola! Soy Buho. Voy a ayudarte a aprender a leer. Estas listo para divertirte?",
                "palabra_dia":         "Esta es nuestra palabra de hoy. Haz clic en el altavoz para escucharla. Repite despues de mi!",
                "silabas":             "Mira todas las silabas que podemos formar. Cada una tiene un sonido especial! Haz clic en cualquier silaba para escucharla.",
                "explicacion_silabas": "Las silabas son como los ladrillos para construir palabras.",
                "selecciona_silaba":   "Excelente! Sigue explorando. Cada silaba que toques te ensenara un nuevo sonido.",
                "como_jugar":          "Ahora viene lo divertido! Vamos a jugar a encontrar palabras.",
                "inicio_ejercicio":    "Busca todas las palabras que tengan la silaba {silaba}. Haz clic en las palabras para seleccionarlas!",
                "acierto":             "Muy bien! Esa palabra tiene la silaba. Sigue asi.",
                "error":               "Casi... Esa palabra no tiene la silaba. Probamos con otra? Tu puedes!",
                "completado":          "Excelente! Encontraste todas las palabras. Ganaste un punto. Eres un campeon!",
                "incompleto":          "Te falta encontrar algunas palabras. Sigue buscando, tu puedes!",
                "demasiadas":          "Algunas palabras que seleccionaste no tienen la silaba. Intenta de nuevo!",
                "frase":               "Mira la historia que invente con nuestra palabra. Es muy divertida!",
                "audio_instruccion":   "Puedes hacer clic en el boton de audio cuando quieras escuchar de nuevo.",
                "practica":            "Quieres practicar mas? Podemos intentar con otra palabra.",
                "celebracion":         "FELICIDADES! Has aprendido mucho hoy. Sigue asi!",
            },
            "en": {
                "bienvenida":          "Hi! I am Owl. I will help you learn to read. Are you ready to have fun?",
                "palabra_dia":         "This is our word of the day. Click the speaker to hear it. Repeat after me!",
                "silabas":             "Look at all the syllables we can make. Each one has a special sound! Click any syllable to hear it.",
                "explicacion_silabas": "Syllables are like building blocks for words.",
                "selecciona_silaba":   "Great! Keep exploring. Every syllable you touch will teach you a new sound.",
                "como_jugar":          "Now comes the fun part! Let us play a word game.",
                "inicio_ejercicio":    "Find all the words that have the syllable {silaba}. Click on the words to select them!",
                "acierto":             "Great job! That word has the syllable. Keep going!",
                "error":               "Almost! That word does not have the syllable. Want to try another? You can do it!",
                "completado":          "Excellent! You found all the words. You earned a point. You are a champion!",
                "incompleto":          "You are missing some words. Keep looking, you can do it!",
                "demasiadas":          "Some words you selected do not have the syllable. Try again!",
                "frase":               "Look at the story I made with our word. It is so fun!",
                "audio_instruccion":   "You can click the audio button anytime to hear it again.",
                "practica":            "Want to practice more? We can try another word.",
                "celebracion":         "CONGRATULATIONS! You have learned a lot today. Keep it up!",
            }
        }

        self.instrucciones = {
            "es": {
                "silaba":    "INSTRUCCION: Haz clic en cualquier silaba para escuchar su sonido",
                "palabra":   "INSTRUCCION: Haz clic en el altavoz para escuchar la palabra completa",
                "ejercicio": "INSTRUCCION: Selecciona TODAS las palabras que contengan la silaba. Luego presiona COMPROBAR",
                "seleccion": "Palabras seleccionadas: {count}",
            },
            "en": {
                "silaba":    "INSTRUCTION: Click any syllable to hear its sound",
                "palabra":   "INSTRUCTION: Click the speaker to hear the full word",
                "ejercicio": "INSTRUCTION: Select ALL the words that contain the syllable. Then press CHECK",
                "seleccion": "Selected words: {count}",
            }
        }

    def get_mensaje(self, clave: str, idioma: str = "es", **kwargs) -> str:
        mensaje = self.mensajes.get(idioma, self.mensajes["es"]).get(
            clave, self.mensajes["es"]["bienvenida"]
        )
        if kwargs:
            try:
                mensaje = mensaje.format(**kwargs)
            except Exception:
                pass
        # Agregar emoji del buho al inicio si no lo tiene
        if not mensaje.startswith("Hola") and "🦉" not in mensaje:
            mensaje = f"🦉 {mensaje}"
        return mensaje

    def get_instruccion(self, clave: str, idioma: str = "es", **kwargs) -> str:
        instruccion = self.instrucciones.get(idioma, self.instrucciones["es"]).get(
            clave, "🦉 Sigue las instrucciones"
        )
        if kwargs:
            try:
                instruccion = instruccion.format(**kwargs)
            except Exception:
                pass
        return instruccion

    def mostrar(
        self,
        mensaje: str,
        instruccion: str = None,
        reproducir_audio: bool = False,
        clave_audio: str = None,
    ) -> None:
        """
        Muestra el avatar con su mensaje y opcion de audio.
        Usa _reproducir_audio_avatar() en lugar de tts_api.reproducir_texto()
        para evitar el error: st.audio() got unexpected keyword argument autoplay
        """
        col_img, col_msg, col_audio = st.columns([1, 5, 1])

        with col_img:
            if self.ruta_imagen and self.ruta_imagen.exists():
                import base64 as _b64av
                with open(str(self.ruta_imagen), "rb") as _fav:
                    _buho_b64 = _b64av.b64encode(_fav.read()).decode()
                # Estado de animación según si hay reproducción activa
                _hablando = reproducir_audio
                _anim_css = "buho-hablar" if _hablando else "buho-caminar"
                st.markdown(f"""
                <style>
                /* Caminar: balanceo lateral suave */
                @keyframes buho-caminar {{
                    0%   {{ transform: translateX(0px) rotate(0deg) scaleX(1); }}
                    15%  {{ transform: translateX(4px) rotate(4deg) scaleX(1); }}
                    30%  {{ transform: translateX(8px) rotate(0deg) scaleX(1); }}
                    45%  {{ transform: translateX(4px) rotate(-4deg) scaleX(1); }}
                    50%  {{ transform: translateX(0px) rotate(0deg) scaleX(-1); }}
                    65%  {{ transform: translateX(-4px) rotate(4deg) scaleX(-1); }}
                    80%  {{ transform: translateX(-8px) rotate(0deg) scaleX(-1); }}
                    92%  {{ transform: translateX(-4px) rotate(-4deg) scaleX(-1); }}
                    100% {{ transform: translateX(0px) rotate(0deg) scaleX(1); }}
                }}
                /* Hablar: pulso vertical + glow */
                @keyframes buho-hablar {{
                    0%,100% {{ transform: scale(1) translateY(0); filter: drop-shadow(0 0 4px #FF6B6B88); }}
                    20%     {{ transform: scale(1.08) translateY(-4px); filter: drop-shadow(0 0 12px #FF6B6B); }}
                    40%     {{ transform: scale(0.96) translateY(2px); filter: drop-shadow(0 0 6px #FFD93D88); }}
                    60%     {{ transform: scale(1.06) translateY(-3px); filter: drop-shadow(0 0 14px #FF6B6B); }}
                    80%     {{ transform: scale(0.98) translateY(1px); filter: drop-shadow(0 0 4px #FF6B6B88); }}
                }}
                /* Idle: respiración suave */
                @keyframes buho-idle {{
                    0%,100% {{ transform: scale(1) translateY(0px); }}
                    50%     {{ transform: scale(1.03) translateY(-3px); }}
                }}
                .buho-caminar {{
                    animation: buho-caminar 3s ease-in-out infinite;
                    display: block; margin: 0 auto; width: 100px;
                    transform-origin: center bottom;
                }}
                .buho-hablar {{
                    animation: buho-hablar 0.6s ease-in-out infinite;
                    display: block; margin: 0 auto; width: 100px;
                }}
                .buho-idle {{
                    animation: buho-idle 3s ease-in-out infinite;
                    display: block; margin: 0 auto; width: 100px;
                }}
                </style>
                <img src='data:image/png;base64,{_buho_b64}'
                     class='{_anim_css}' alt='Buho guia'/>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <style>
                @keyframes emoji-buho {{
                    0%,100% {{ transform: translateX(0) rotate(0deg); }}
                    25%     {{ transform: translateX(6px) rotate(8deg); }}
                    75%     {{ transform: translateX(-6px) rotate(-8deg); }}
                }}
                .buho-emoji {{ animation: emoji-buho 2s ease-in-out infinite;
                               font-size:4rem; text-align:center; display:block; }}
                </style>
                <span class='buho-emoji'>🦉</span>""", unsafe_allow_html=True)

        with col_msg:
            st.markdown(f"""
            <div style="
                background: #FFE3E3;
                padding: 1.2rem 1.8rem;
                border-radius: 40px 40px 40px 10px;
                border: 3px solid #FF6B6B;
                box-shadow: 0 6px 12px rgba(0,0,0,0.1);
                margin: 0.5rem 0;
                min-height: 80px;
                display: flex;
                align-items: center;
            ">
                <p style="font-size:1.2rem;color:#4A5568;margin:0;font-weight:500;line-height:1.5;">
                    {mensaje}
                </p>
            </div>
            """, unsafe_allow_html=True)

            if instruccion:
                st.markdown(f"""
                <div style="
                    background: #E3F2FD;
                    padding: 0.8rem 1.2rem;
                    border-radius: 20px;
                    margin-top: 0.5rem;
                    font-size: 1rem;
                    color: #2C3E50;
                    text-align: center;
                    border-left: 5px solid #3498DB;
                    font-weight: 600;
                ">
                    {instruccion}
                </div>
                """, unsafe_allow_html=True)

        with col_audio:
            texto_audio = clave_audio if clave_audio else mensaje
            texto_limpio = texto_audio.replace("🦉", "").strip()
            idioma = st.session_state.get("idioma", "es")

            if st.button("🔊", key=f"audio_avatar_{abs(hash(texto_limpio)) % 999999}",
                         help="Escuchar mensaje"):
                _reproducir_audio_avatar(texto_limpio, idioma)

        # Audio automático desactivado: gTTS bloquea el primer render y provoca
        # "Connection error" en Streamlit. Usar el botón 🔊 para escuchar.
        if reproducir_audio:
            import threading
            texto_limpio = mensaje.replace("🦉", "").strip()
            idioma = st.session_state.get("idioma", "es")
            threading.Thread(
                target=_reproducir_audio_avatar,
                args=(texto_limpio, idioma),
                daemon=True,
            ).start()


# Instancia global
avatar = AvatarBuho()