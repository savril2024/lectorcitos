# #def generar_pdf_ejercicios(palabra, silabas, frase, idioma):
#     """Crea PDF con:
#     - Portada con palabra
#     - Lista de sílabas
#     - Frase creativa
#     - 6 ejercicios (completar, unir, etc.)
#     """
"""
API de PDF - Módulo 6
Genera fichas de ejercicios descargables con fpdf2
Python 3.12.9
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import random
import re
from pathlib import Path
from typing import List
import io


def limpiar_texto(texto: str) -> str:
    """
    Elimina emojis y cualquier carácter fuera del rango Latin-1
    para que Helvetica no lance errores de codificación.
    Conserva acentos y caracteres españoles normales (ñ, á, é, etc.)
    """
    # Eliminar emojis y símbolos Unicode fuera de Latin-1 (rango > 0xFF)
    return "".join(c for c in texto if ord(c) <= 0xFF)


class LectorcitoPDF(FPDF):
    """PDF personalizado con encabezado y pie de página de Lectorcitos"""

    def __init__(self, idioma: str = "es"):
        super().__init__()
        self.idioma = idioma

    def header(self):
        self.set_fill_color(255, 107, 107)   # #FF6B6B
        self.rect(0, 0, 210, 18, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        titulo = "Lectorcitos - Aprende a Leer" if self.idioma == "es" else "Lectorcitos - Learn to Read"
        self.cell(0, 18, titulo, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        pie = "Aprendiendo con diversión | © 2026 Lectorcitos" if self.idioma == "es" else "Learning with fun | © 2026 Lectorcitos"
        self.cell(0, 10, pie, align="C")


class PDFApi:
    """API para generar fichas PDF de ejercicios"""

    COLORES = {
        "morado":    (102, 126, 234),   # #667EEA
        "rosa":      (255, 107, 107),   # #FF6B6B
        "verde":     (76,  175,  80),   # #4CAF50
        "azul":      (77,  150, 255),   # #4D96FF
        "amarillo":  (255, 211,  77),   # #FFD34D
        "naranja":   (255, 179,  71),   # #FFB347
    }

    # ─────────────────────────────────────────────────────────────
    # Helpers de dibujo
    # ─────────────────────────────────────────────────────────────

    def _caja_coloreada(self, pdf: FPDF, texto: str, color_rgb: tuple, ancho: int = 170, alto: int = 18):
        """Dibuja una caja con fondo de color y texto centrado."""
        r, g, b = color_rgb
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(ancho, alto, texto, align="C", fill=True,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

    def _linea_punteada(self, pdf: FPDF, largo: int = 60):
        """Dibuja una línea de puntos para completar."""
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(largo, 10, "_ " * 15, align="L",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _silabas_grid(self, pdf: FPDF, silabas: List[str], cols: int = 5):
        """Dibuja las sílabas en una cuadrícula de colores."""
        colores_lista = list(self.COLORES.values())
        ancho_celda = 30
        alto_celda = 14
        pdf.set_font("Helvetica", "B", 13)

        for i, silaba in enumerate(silabas):
            r, g, b = colores_lista[i % len(colores_lista)]
            pdf.set_fill_color(r, g, b)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(ancho_celda, alto_celda, silaba, align="C", fill=True, border=1)
            if (i + 1) % cols == 0:
                pdf.ln()

        # Cerrar última fila si quedó incompleta
        resto = len(silabas) % cols
        if resto != 0:
            pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

    # ─────────────────────────────────────────────────────────────
    # Secciones del PDF
    # ─────────────────────────────────────────────────────────────

    def _seccion_palabra(self, pdf: FPDF, palabra: str, idioma: str):
        titulo = "Palabra del Día" if idioma == "es" else "Word of the Day"
        self._caja_coloreada(pdf, titulo, self.COLORES["morado"], alto=14)
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 48)
        pdf.set_text_color(*self.COLORES["rosa"])
        pdf.cell(170, 24, palabra.upper(), align="C",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

    def _seccion_silabas(self, pdf: FPDF, silabas: List[str], idioma: str):
        titulo = "Sus Sílabas" if idioma == "es" else "Its Syllables"
        self._caja_coloreada(pdf, titulo, self.COLORES["azul"], alto=12)
        pdf.ln(3)
        self._silabas_grid(pdf, silabas)

    def _seccion_frase(self, pdf: FPDF, frase: str, idioma: str):
        titulo = "¡Mi Historia!" if idioma == "es" else "My Story!"
        self._caja_coloreada(pdf, titulo, self.COLORES["verde"], alto=12)
        pdf.ln(3)
        pdf.set_font("Helvetica", "I", 13)
        pdf.set_text_color(60, 60, 60)
        frase_limpia = limpiar_texto(frase)
        pdf.multi_cell(170, 9, f'"{frase_limpia}"', align="C",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

    def _seccion_ejercicios(self, pdf: FPDF, palabra: str, silabas: List[str], idioma: str):
        titulo = "¡A Practicar!" if idioma == "es" else "Let's Practice!"
        self._caja_coloreada(pdf, titulo, self.COLORES["naranja"], alto=12)
        pdf.ln(5)

        ejercicios_es = [
            ("1. Escribe la sílaba que falta:", self._ej_silaba_faltante),
            ("2. Rodea las sílabas que tiene la palabra:", self._ej_rodear_silabas),
            ("3. Copia la palabra 3 veces:", self._ej_copiar_palabra),
            ("4. ¿Cuántas sílabas tiene la palabra? Escribe el número:", self._ej_contar_silabas),
            ("5. Forma una oración con la palabra:", self._ej_oracion_libre),
        ]
        ejercicios_en = [
            ("1. Write the missing syllable:", self._ej_silaba_faltante),
            ("2. Circle the syllables in the word:", self._ej_rodear_silabas),
            ("3. Copy the word 3 times:", self._ej_copiar_palabra),
            ("4. How many syllables does the word have? Write the number:", self._ej_contar_silabas),
            ("5. Make a sentence with the word:", self._ej_oracion_libre),
        ]

        ejercicios = ejercicios_es if idioma == "es" else ejercicios_en

        for enunciado, fn in ejercicios:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(70, 70, 70)
            pdf.multi_cell(170, 8, enunciado, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            fn(pdf, palabra, silabas, idioma)
            pdf.ln(4)

    # ── Ejercicios individuales ───────────────────────────────────

    def _ej_silaba_faltante(self, pdf, palabra, silabas, idioma):
        """Muestra la palabra con una sílaba tapada por ___"""
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(0, 0, 0)
        if silabas:
            sil = random.choice(silabas[:min(3, len(silabas))])
            mostrar = palabra.upper().replace(sil, "___", 1) if sil in palabra.upper() else f"{palabra.upper()[:-2]}___"
            pdf.cell(170, 10, mostrar, align="C",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _ej_rodear_silabas(self, pdf, palabra, silabas, idioma):
        """Lista de sílabas para rodear las correctas"""
        pdf.set_font("Helvetica", "", 12)
        todas = list(set(silabas[:6]))
        # Añadir 2-3 sílabas "trampa" que no están en la palabra
        falsas = ["BU", "ZO", "FI", "XE", "QU"]
        todas += random.sample(falsas, min(2, len(falsas)))
        random.shuffle(todas)
        linea = "   ".join(todas)
        pdf.cell(170, 10, linea, align="C",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _ej_copiar_palabra(self, pdf, palabra, silabas, idioma):
        """3 líneas para copiar la palabra"""
        pdf.set_font("Helvetica", "", 13)
        for _ in range(3):
            pdf.cell(170, 10, "_ " * 20,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _ej_contar_silabas(self, pdf, palabra, silabas, idioma):
        """Cuadro para escribir el número"""
        pdf.set_font("Helvetica", "", 13)
        pista = "Número: [   ]" if idioma == "es" else "Number: [   ]"
        pdf.cell(170, 10, pista, align="C",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _ej_oracion_libre(self, pdf, palabra, silabas, idioma):
        """Líneas en blanco para escribir una oración"""
        pdf.set_font("Helvetica", "", 13)
        for _ in range(2):
            pdf.cell(170, 10, "_ " * 25,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ─────────────────────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────────────────────

    def generar_pdf(
        self,
        palabra: str,
        silabas: List[str],
        frase: str,
        idioma: str = "es",
    ) -> bytes:
        """
        Genera el PDF completo y devuelve los bytes para descarga.

        Args:
            palabra:  Palabra del día.
            silabas:  Lista de sílabas generadas.
            frase:    Frase creativa del Módulo 4.
            idioma:   'es' o 'en'.

        Returns:
            bytes del PDF listo para st.download_button.
        """
        pdf = LectorcitoPDF(idioma=idioma)
        pdf.set_margins(20, 25, 20)
        pdf.add_page()

        # Título de la ficha
        nombre_ficha = f"Mis ejercicios de: {palabra.upper()}" if idioma == "es" else f"My exercises: {palabra.upper()}"
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(*self.COLORES["morado"])
        pdf.cell(0, 12, limpiar_texto(nombre_ficha), align="C",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

        # Secciones
        self._seccion_palabra(pdf, palabra, idioma)
        self._seccion_silabas(pdf, silabas, idioma)
        self._seccion_frase(pdf, frase, idioma)

        pdf.add_page()
        self._seccion_ejercicios(pdf, palabra, silabas, idioma)

        # Devolver como bytes (sin escribir archivo en disco)
        return bytes(pdf.output())

    def nombre_archivo(self, palabra: str, idioma: str = "es") -> str:
        """Nombre sugerido para el archivo descargado."""
        sufijo = "ejercicios" if idioma == "es" else "exercises"
        return f"lectorcitos_{palabra.lower()}_{sufijo}.pdf"


# Instancia global
pdf_api = PDFApi()