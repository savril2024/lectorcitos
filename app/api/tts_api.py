"""
API de Text-to-Speech para Lectorcitos
Usa gTTS (Google Text-to-Speech)
"""

import hashlib
from pathlib import Path
from gtts import gTTS
import streamlit as st


def _resolver_cache_dir() -> Path:
    """Raíz del proyecto: /app en contenedor, app_lectorcitos en desarrollo."""
    # app/api/tts_api.py -> subir 2 niveles = raíz del proyecto
    por_modulo = Path(__file__).resolve().parent.parent.parent
    candidatos = [
        por_modulo / "public" / "audio_cache",
        Path("/app/public/audio_cache"),
        Path.cwd() / "public" / "audio_cache",
    ]
    for ruta in candidatos:
        try:
            ruta.mkdir(parents=True, exist_ok=True)
            return ruta
        except OSError:
            continue
    return candidatos[0]


class TTSAPI:
    """API para convertir texto a audio con caché persistente"""
    
    def __init__(self):
        """Inicializa la API de TTS con carpeta local del proyecto"""
        self.cache_dir = _resolver_cache_dir()
        
    def generar_audio(self, texto: str, idioma: str = "es") -> str:
        """
        Genera un archivo de audio a partir de texto con MD5 estable
        """
        idiomas = {
            "es": "es",
            "en": "en"
        }
        
        lang = idiomas.get(idioma, "es")
        
        try:
            # MD5 es estable entre sesiones (hash() de Python varía por seguridad)
            hash_texto = hashlib.md5(f"{texto}_{lang}".encode()).hexdigest()
            nombre_archivo = f"{hash_texto}.mp3"
            ruta_audio = self.cache_dir / nombre_archivo
            
            # Si ya existe en caché, devolver inmediatamente (¡Instantáneo!)
            if ruta_audio.exists():
                return str(ruta_audio)
            
            # Solo si no existe, llamar a Google (esto es lo que tarda)
            tts = gTTS(text=texto, lang=lang, slow=False)
            tts.save(str(ruta_audio))
            
            return str(ruta_audio)
            
        except Exception as e:
            print(f"Error generando audio ({texto!r}, {lang}): {e}")
            return None

    
    def reproducir_texto(self, texto: str, idioma: str = "es"):
        """
        Reproduce un texto en la aplicación Streamlit
        
        Args:
            texto: Texto a reproducir
            idioma: Código de idioma
        """
        ruta_audio = self.generar_audio(texto, idioma)
        if ruta_audio:
            with open(ruta_audio, 'rb') as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)

    
    def limpiar_archivos_temporales(self):
        """Limpia archivos de audio temporales"""
        for archivo in self.cache_dir.glob("*.mp3"):
            try:
                archivo.unlink()
            except:
                pass


# Instancia global
tts_api = TTSAPI()