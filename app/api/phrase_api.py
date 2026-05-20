"""
API de Frases Creativas - Módulo 4
Genera frases divertidas contextualizando la palabra del día
Python 3.12.9
"""

import random
from typing import Tuple


class PhraseAPI:
    """Genera frases creativas con la palabra del día"""

    def __init__(self):
        # ── Español ──────────────────────────────────────────────
        self.verbos_es = [
            "saltó", "rodó", "voló", "cantó", "bailó", "corrió",
            "nadó", "durmió", "jugó", "gritó", "reía", "soñó",
            "cocinó", "pintó", "exploró", "descubrió", "encontró",
        ]
        self.lugares_es = [
            "la cocina", "el parque", "la escuela", "la luna",
            "el jardín", "la playa", "el bosque", "el mercado",
            "la montaña", "el río", "la ciudad", "el castillo",
            "el circo", "la biblioteca", "el estadio",
        ]
        # Artículos según primera letra (heurística simple)
        self._vocales = set("AEIOUaeiou")

        # ── Inglés ────────────────────────────────────────────────
        self.verbs_en = [
            "jumped", "rolled", "flew", "sang", "danced", "ran",
            "swam", "slept", "played", "laughed", "dreamed",
            "cooked", "painted", "explored", "discovered", "found",
        ]
        self.places_en = [
            "the kitchen", "the park", "the school", "the moon",
            "the garden", "the beach", "the forest", "the market",
            "the mountain", "the river", "the city", "the castle",
            "the circus", "the library", "the stadium",
        ]

        # Palabras con género femenino conocido (español)
        self._femeninas = {
            "CASA", "LUNA", "MESA", "SILLA", "PUERTA", "VENTANA",
            "FLOR", "NOCHE", "TARDE", "MAÑANA", "ESCUELA", "PLAYA",
            "MONTAÑA", "CIUDAD", "TORTUGA", "MARIPOSA", "NARANJA",
            "BANANA", "MANZANA", "SANDÍA", "CANCIÓN", "ESTRELLA",
        }

    # ─────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────

    def _articulo_es(self, palabra: str) -> str:
        """Devuelve 'El' o 'La' según si la palabra es femenina."""
        return "La" if palabra.upper() in self._femeninas else "El"

    def _preposicion_lugar_es(self, lugar: str) -> str:
        """Devuelve 'en' + lugar (ya incluye artículo en la lista)."""
        return f"en {lugar}"

    # ─────────────────────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────────────────────

    def generar_frase(self, palabra: str, idioma: str = "es") -> str:
        """
        Genera una frase creativa con la palabra.

        Args:
            palabra: Palabra del día (mayúsculas o minúsculas).
            idioma:  'es' o 'en'.

        Returns:
            Frase formateada lista para mostrar.
        """
        palabra_fmt = palabra.capitalize()

        if idioma == "en":
            verbo = random.choice(self.verbs_en)
            lugar = random.choice(self.places_en)
            frase = f"The {palabra_fmt} {verbo} through {lugar}."
        else:
            verbo = random.choice(self.verbos_es)
            lugar = random.choice(self.lugares_es)
            articulo = self._articulo_es(palabra)
            prep = self._preposicion_lugar_es(lugar)
            frase = f"{articulo} {palabra_fmt} {verbo} {prep}."

        return frase

    def generar_varias_frases(
        self, palabra: str, idioma: str = "es", cantidad: int = 3
    ) -> list[str]:
        """Genera varias frases únicas para la misma palabra."""
        frases = set()
        intentos = 0
        max_intentos = cantidad * 10

        while len(frases) < cantidad and intentos < max_intentos:
            frases.add(self.generar_frase(palabra, idioma))
            intentos += 1

        return list(frases)

    def get_emoji_frase(self, idioma: str = "es") -> str:
        """Emoji decorativo aleatorio para acompañar la frase."""
        emojis = ["📖", "✨", "🌟", "🎨", "🚀", "🌈", "🎭", "🦋", "🌺", "⭐"]
        return random.choice(emojis)

    def get_titulo(self, idioma: str = "es") -> str:
        return "¡Mira esta historia!" if idioma == "es" else "Check out this story!"

    def get_instruccion(self, idioma: str = "es") -> str:
        return (
            "🦉 ¡Inventé una frase con tu palabra! Haz clic en 🔊 para escucharla."
            if idioma == "es"
            else "🦉 I made a sentence with your word! Click 🔊 to hear it."
        )


# Instancia global
phrase_api = PhraseAPI()