"""
API de imágenes - Pixabay
Busca imagen automáticamente según la palabra del día
"""
import requests
import streamlit as st

class ImageAPI:
    BASE_URL = "https://pixabay.com/api/"

    def obtener_imagen(self, palabra: str, idioma: str = "es") -> str | None:
        """
        Busca imagen en Pixabay para la palabra dada.
        Retorna URL de imagen o None si no encuentra.
        """
        try:
            api_key = st.secrets.get("PIXABAY_API_KEY", "")
            if not api_key:
                return None

            # Pixabay acepta búsqueda en español e inglés
            lang = "es" if idioma == "es" else "en"

            params = {
                "key":          api_key,
                "q":            palabra.lower(),
                "lang":         lang,
                "image_type":   "photo",
                "orientation":  "horizontal",
                "category":     "nature,animals,food,objects,places",
                "safesearch":   "true",
                "per_page":     5,
                "order":        "popular",
            }

            resp = requests.get(self.BASE_URL, params=params, timeout=5)
            data = resp.json()

            hits = data.get("hits", [])
            if hits:
                return hits[0]["webformatURL"]

            # Si no encontró en español, intentar en inglés
            if idioma == "es":
                params["lang"] = "en"
                resp2 = requests.get(self.BASE_URL, params=params, timeout=5)
                hits2 = resp2.json().get("hits", [])
                if hits2:
                    return hits2[0]["webformatURL"]

            return None

        except Exception as e:
            print(f"Error Pixabay ({palabra}): {e}")
            return None

image_api = ImageAPI()