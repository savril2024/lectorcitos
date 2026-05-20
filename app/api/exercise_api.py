"""
API de Ejercicios - Módulo 2 MEJORADO
Maneja casos donde no hay palabras y da feedback detallado
"""

import random
from typing import List, Tuple, Dict

class ExerciseAPI:
    """API para generar y evaluar ejercicios de sílabas"""
    
    def __init__(self, word_api):
        self.word_api = word_api
        self.palabras_es = word_api.palabras_es
        self.palabras_en = word_api.palabras_en
    
    def seleccionar_silaba_objetivo(self, silabas: List[str]) -> str:
        """Selecciona una sílaba aleatoria de la lista"""
        return random.choice(silabas)
    
    def buscar_palabras_con_silaba(self, silaba: str, idioma: str = "es") -> List[str]:
        """Busca todas las palabras que contienen una sílaba específica"""
        lista_palabras = self.palabras_es if idioma == "es" else self.palabras_en
        palabras_con_silaba = []
        
        for palabra in lista_palabras:
            if silaba in palabra:
                palabras_con_silaba.append(palabra)
        
        return palabras_con_silaba
    
    def generar_palabras_ejercicio(
        self, 
        silaba_objetivo: str, 
        idioma: str = "es", 
        num_palabras: int = 6
    ) -> Tuple[List[str], List[str], bool, str]:
        """
        Genera lista de palabras para el ejercicio
        
        Returns:
            (lista_mezclada, palabras_correctas, hay_correctas, mensaje_info)
        """
        # Buscar palabras que contienen la sílaba
        palabras_correctas = self.buscar_palabras_con_silaba(silaba_objetivo, idioma)
        todas_palabras = self.palabras_es if idioma == "es" else self.palabras_en
        
        # CASO 1: No hay palabras con esa sílaba
        if not palabras_correctas:
            # Seleccionar palabras que NO tienen la sílaba
            palabras_incorrectas = [p for p in todas_palabras if silaba_objetivo not in p]
            
            # Asegurar que tenemos suficientes palabras
            num_a_mostrar = min(num_palabras, len(palabras_incorrectas))
            if num_a_mostrar < num_palabras:
                # Si no hay suficientes, repetir algunas
                palabras_seleccionadas = random.choices(palabras_incorrectas, k=num_palabras)
            else:
                palabras_seleccionadas = random.sample(palabras_incorrectas, num_a_mostrar)
            
            random.shuffle(palabras_seleccionadas)
            mensaje = f"⚠️ ¡Sorpresa! No hay palabras con la sílaba **{silaba_objetivo}**. Debes seleccionar **NINGUNA** palabra."
            return palabras_seleccionadas, [], False, mensaje
        
        # CASO 2: Hay palabras con esa sílaba
        palabras_incorrectas = [p for p in todas_palabras if silaba_objetivo not in p]
        
        # Determinar cuántas correctas mostrar (máximo 3)
        num_correctas = min(len(palabras_correctas), 3)
        num_incorrectas = num_palabras - num_correctas
        
        # Seleccionar palabras
        seleccion_correctas = random.sample(palabras_correctas, num_correctas)
        
        # Asegurar que tenemos suficientes incorrectas
        if len(palabras_incorrectas) < num_incorrectas:
            # Si no hay suficientes, permitir repetición
            seleccion_incorrectas = random.choices(palabras_incorrectas, k=num_incorrectas)
        else:
            seleccion_incorrectas = random.sample(palabras_incorrectas, num_incorrectas)
        
        # Mezclar
        lista_mezclada = seleccion_correctas + seleccion_incorrectas
        random.shuffle(lista_mezclada)
        
        mensaje = f"🔍 Busca las {num_correctas} palabra(s) que tienen **{silaba_objetivo}**"
        return lista_mezclada, seleccion_correctas, True, mensaje
    
    def verificar_seleccion(
        self, 
        seleccionadas: List[str], 
        correctas: List[str],
        hay_correctas: bool
    ) -> Tuple[bool, List[str], List[str], str, str]:
        """
        Verifica la selección del usuario con mensaje detallado
        
        Returns:
            (exito, aciertos, errores, tipo_resultado, mensaje_usuario)
        """
        aciertos = [p for p in seleccionadas if p in correctas]
        errores = [p for p in seleccionadas if p not in correctas]
        
        # CASO ESPECIAL: No hay palabras correctas
        if not hay_correctas:
            if len(seleccionadas) == 0:
                return True, [], [], "NINGUNA", "✅ ¡Excelente! No hay palabras con esa sílaba y no seleccionaste ninguna. ¡Muy bien!"
            else:
                return False, [], errores, "SOBRANTE", f"❌ Seleccionaste {len(errores)} palabra(s), pero no hay ninguna con esa sílaba. Debes dejar TODO sin seleccionar."
        
        # CASO NORMAL: Hay palabras correctas
        if set(aciertos) == set(correctas) and len(errores) == 0:
            # Éxito total
            return True, aciertos, [], "COMPLETO", f"✅ ¡Perfecto! Encontraste TODAS las palabras ({len(correctas)}) con la sílaba."
        elif set(aciertos) != set(correctas) and len(errores) == 0:
            # Faltan algunas
            faltan = set(correctas) - set(aciertos)
            return False, aciertos, [], "FALTAN", f"🔍 Te faltan {len(faltan)} palabra(s). ¡Sigue buscando!"
        elif set(aciertos) == set(correctas) and len(errores) > 0:
            # Sobran algunas (tiene las correctas pero también incorrectas)
            return False, aciertos, errores, "ERRORES", f"⚠️ Tienes las palabras correctas, pero también seleccionaste {len(errores)} que no tienen la sílaba."
        else:
            # Mezcla: faltan y sobran
            faltan = set(correctas) - set(aciertos)
            return False, aciertos, errores, "MIXTO", f"❌ Te faltan {len(faltan)} y seleccionaste {len(errores)} incorrectas. ¡Intenta de nuevo!"



# Instancia global (se inicializará después con word_api)
exercise_api = None