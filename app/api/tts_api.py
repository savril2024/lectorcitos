import hashlib
import tempfile
import os
from pathlib import Path
from gtts import gTTS

_cache: dict = {}
_temp_dir = Path(tempfile.gettempdir()) / "lectorcitos_tts"
_temp_dir.mkdir(exist_ok=True)

class TTSAPI:
    def generar_audio(self, texto: str, idioma: str = "es") -> str | None:
        # Validación estricta del idioma
        if idioma not in ["es", "en"]:
            print(f"⚠️ Idioma inválido: {idioma!r}. Usando 'es' por defecto.")
            lang = "es"
        else:
            lang = idioma
        
        # Limpiar y normalizar texto
        texto_limpio = texto.strip().lower()
        
        # Clave única que incluye idioma EXPLÍCITO
        clave = f"{texto_limpio}_{lang}_{hash(texto_limpio) % 10000}"
        clave_hash = hashlib.md5(clave.encode()).hexdigest()
        
        if clave_hash in _cache:
            ruta_cache = _cache[clave_hash]
            # Verificar que el archivo exista
            if os.path.exists(ruta_cache):
                return ruta_cache
            else:
                # Archivo fue eliminado, remover del caché
                del _cache[clave_hash]
        
        try:
            # Crear gTTS con idioma correcto
            tts = gTTS(text=texto_limpio, lang=lang, slow=False)
            
            # Nombre de archivo único con idioma en el nombre
            nombre_archivo = f"tts_{clave_hash}_{lang}.mp3"
            ruta_archivo = _temp_dir / nombre_archivo
            
            # Generar audio
            tts.save(str(ruta_archivo))
            
            # Guardar en caché
            _cache[clave_hash] = str(ruta_archivo)
            
            return str(ruta_archivo)
            
        except Exception as e:
            print(f"❌ Error TTS - Texto: {texto_limpio!r}, Idioma: {lang}, Error: {e}")
            return None

    def limpiar_archivos_temporales(self):
        """Elimina todos los archivos temporales y limpia el caché."""
        _cache.clear()
        try:
            for archivo in _temp_dir.glob("tts_*.mp3"):
                archivo.unlink()
        except Exception as e:
            print(f"⚠️ Error limpiando archivos: {e}")

tts_api = TTSAPI()