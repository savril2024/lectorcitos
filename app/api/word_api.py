"""
API de Palabras - Módulo 1: Núcleo Léxico
Python 3.12.9
"""

import json
import random
from typing import List
from pathlib import Path

class WordAPI:
    """API para gestión de palabras y sílabas"""
    
    def __init__(self):
        """Inicializa la API cargando las listas de palabras"""
        # Obtener la ruta absoluta del archivo actual
        current_file = Path(__file__).resolve()  # src/app/api/word_api.py
        print(f"📂 Archivo actual: {current_file}")
        
        # Subir hasta src/app/api -> src/app -> src -> app_lectorcitos
        # Intentar diferentes combinaciones
        posibles_rutas = [
            # Opción 1: subir 4 niveles (src/app/api -> src/app -> src -> app_lectorcitos)
            current_file.parent.parent.parent.parent / "src" / "lib",
            # Opción 2: subir 3 niveles y luego buscar src/lib
            current_file.parent.parent.parent / "lib",
            # Opción 3: ruta absoluta en contenedor (WORKDIR /app)
            Path("/app/src/lib"),
            # Opción 4: ruta absoluta directa (para Windows/local)
            Path("C:/apps-master/app_lectorcitos/src/lib"),
            # Opción 5: ruta relativa desde el directorio de trabajo
            Path.cwd() / "src" / "lib",
        ]
        
        self.base_path = None
        for ruta in posibles_rutas:
            print(f"🔍 Probando: {ruta}")
            if ruta.exists():
                self.base_path = ruta
                print(f"✅ Encontrado: {ruta}")
                break
        
        if not self.base_path:
            # Si no encuentra, usar la ruta del contenedor como fallback
            self.base_path = Path("/app/src/lib")
            print(f"⚠️ Usando ruta por defecto: {self.base_path}")
            # Crear el directorio si no existe
            self.base_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Directorio base: {self.base_path}")
        
        # Listar archivos en el directorio
        if self.base_path.exists():
            archivos = list(self.base_path.glob("*.json"))
            print(f"📄 Archivos encontrados: {[f.name for f in archivos]}")
        
        self.palabras_es = self._cargar_palabras("palabras_es.json", "palabras")
        self.palabras_en = self._cargar_palabras("palabras_en.json", "words")
        
        print(f"📊 Español: {len(self.palabras_es)} palabras cargadas")
        print(f"📊 Inglés: {len(self.palabras_en)} palabras cargadas")
        
    def _cargar_palabras(self, archivo: str, clave: str) -> List[str]:
        """Carga las palabras desde el archivo JSON"""
        ruta = self.base_path / archivo
        print(f"   Intentando cargar: {ruta}")
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                palabras = data.get(clave, [])
                print(f"   ✅ Cargadas {len(palabras)} palabras de {archivo}")
                return palabras
        except FileNotFoundError:
            print(f"   ❌ Archivo no encontrado: {ruta}")
            print(f"   📝 Usando lista por defecto")
            # Lista por defecto en caso de error
            if archivo == "palabras_es.json":
                return ["TOMATE", "CASA", "PERRO", "GATO", "SOL", "LUNA", "MESA", "SILLA"]
            else:
                return ["TOMATO", "HOUSE", "DOG", "CAT", "SUN", "MOON", "TABLE", "CHAIR"]
        except json.JSONDecodeError as e:
            print(f"   ❌ Error al decodificar JSON: {e}")
            return ["TOMATE", "CASA"] if "es" in archivo else ["TOMATO", "HOUSE"]
    
    def generar_palabra_aleatoria(self, idioma: str = "es") -> str:
        """
        Genera una palabra aleatoria según el idioma
        
        Args:
            idioma: "es" para español, "en" para inglés
            
        Returns:
            Palabra aleatoria en mayúsculas
        """
        if idioma == "en":
            lista = self.palabras_en
        else:
            lista = self.palabras_es
            
        if not lista:
            print(f"⚠️ Lista vacía para {idioma}, usando default")
            return "TOMATE" if idioma == "es" else "TOMATO"
        
        palabra = random.choice(lista).upper()
        return palabra
    
    def extraer_consonantes(self, palabra: str) -> List[str]:
        """
        Extrae las consonantes únicas de una palabra
        
        Args:
            palabra: Palabra en mayúsculas (ej: "TOMATE")
            
        Returns:
            Lista de consonantes únicas (ej: ["T", "M"])
        """
        vocales = "AEIOU"
        consonantes = []
        
        for letra in palabra:
            if letra not in vocales and letra not in consonantes:
                consonantes.append(letra)
        
        return consonantes
    
    def generar_silabas(self, consonantes: List[str]) -> List[str]:
        """
        Genera todas las combinaciones de consonantes con vocales
        
        Args:
            consonantes: Lista de consonantes (ej: ["T", "M"])
            
        Returns:
            Lista de sílabas (ej: ["TA", "TE", "TI", "TO", "TU", "MA", "ME", "MI", "MO", "MU"])
        """
        vocales = ["A", "E", "I", "O", "U"]
        silabas = []
        
        for cons in consonantes:
            for vocal in vocales:
                silabas.append(f"{cons}{vocal}")
        
        return silabas
    
    def obtener_info_palabra(self, idioma: str = "es") -> dict:
        """
        Obtiene toda la información de una palabra aleatoria
        
        Args:
            idioma: "es" o "en"
            
        Returns:
            Diccionario con palabra, consonantes y sílabas
        """
        palabra = self.generar_palabra_aleatoria(idioma)
        consonantes = self.extraer_consonantes(palabra)
        silabas = self.generar_silabas(consonantes)
        
        return {
            "palabra": palabra,
            "consonantes": consonantes,
            "silabas": silabas,
            "idioma": idioma,
            "total_silabas": len(silabas)
        }


# Instancia global
word_api = WordAPI()