import streamlit as st
from pathlib import Path
import sys

current_dir = Path(__file__).resolve().parent
project_root = current_dir
sys.path.insert(0, str(project_root))

try:
    from src.app.api.tts_api import tts_api
except:
    try:
        from app.api.tts_api import tts_api
    except:
        st.error("No se puede importar tts_api")
        st.stop()

st.title("🔊 Prueba de Audio")

texto = st.text_input("Texto a reproducir:", "hola, soy el búho")

if st.button("Probar audio"):
    try:
        with st.spinner("Generando audio..."):
            tts_api.reproducir_texto(texto, "es")
        st.success("Audio reproducido (si escuchaste algo)")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Si no escuchas nada, verifica:")
st.markopen("- Altavoces conectados")
st.markdown("- Volumen del navegador")
st.markdown("- Permisos de audio en el navegador")