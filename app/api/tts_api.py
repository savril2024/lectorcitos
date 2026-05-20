import hashlib
import tempfile
from gtts import gTTS

_cache: dict = {}

class TTSAPI:
    def generar_audio(self, texto: str, idioma: str = "es") -> str | None:
        lang = "es" if idioma == "es" else "en"
        clave = hashlib.md5(f"{texto}_{lang}".encode()).hexdigest()
        if clave in _cache:
            return _cache[clave]
        try:
            tts = gTTS(text=texto, lang=lang, slow=False)
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tts.save(tmp.name)
            tmp.close()
            _cache[clave] = tmp.name
            return tmp.name
        except Exception as e:
            print(f"Error TTS ({texto!r}, {lang}): {e}")
            return None

    def limpiar_archivos_temporales(self):
        _cache.clear()

tts_api = TTSAPI()
