import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re

#registros para el servidor
logger = logging.getLogger(__name__)

def extraer_datos_calendario():
    """Extrae datos básicos del calendario académico. Limitado a 4000 caracteres por motivos de límite de contexto"""
    try:
        url = "https://www.ucm.es/master-letrasdigitales/calendario-clases"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'} #necesario para scraping
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        
        # Limpiar mediante una expresión regular y limitar
        cleaned = re.sub(r'\s+', ' ', text)[:4000]
        
        return f"""
CALENDARIO ACADÉMICO MÁSTER EN LETRAS DIGITALES - CURSO 2025-26

INFORMACIÓN BÁSICA:
- Inicio: 1 septiembre 2025
- Asignaturas obligatorias: 29 septiembre 2025  
- Asignaturas optativas: 2 febrero 2026
- Lugar: Lab 1007, Edificio Multiusos E

EXTRACTO DEL CALENDARIO:
{cleaned}

NOTA: Información parcial por limitaciones técnicas.
"""
        
    except Exception as e:
        logger.error(f"Error calendario: {e}")
        return None

def query_calendario(user_question, groq_client):
    """Procesa consulta del calendario y devuelve URL web si no puede"""
    try:
        datos_calendario = extraer_datos_calendario()
        if not datos_calendario: # si hay un error extrayendo los datos del calendario
            return "Lo siento, poeta, pero ahora mismo no puedo acceder al calendario. Mis disculpas. Consulta esta dirección https://www.ucm.es/master-letrasdigitales/calendario-clases"
        
        # Fecha actual en español (hay que construirla en texto para que el modelo la comprenda mejor)
        fecha = datetime.now()
        meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
        días = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
        fecha_completa = f"{días[fecha.weekday()]}, {fecha.day} de {meses[fecha.month-1]} de {fecha.year}"
        
        system_prompt = f"""Eres VirgiBot, asistente del Máster en Letras Digitales UCM. Eres amable y servicial y estás inspirado en el personaje de Virgilio. No hace falta que te presentes, pues el usuario ya te conoce.

FECHA ACTUAL: {fecha_completa}

Tienes información PARCIAL del calendario 2025-26. Si no tienes la respuesta exacta, di que tienes información limitada y proporciona la URL: https://www.ucm.es/master-letrasdigitales/calendario-clases
NO digas hasta donde llega tu información. Intenta responder y, si no estás seguro de la respuesta, insta al usuario a dirigirse a la web.
Si puedes responder a la pregunta, NO digas que tienes información limitada. Adapta tu respuesta a unas 120 palabras como máximo, pero no es necesario que llegues.
CALENDARIO (PARCIAL):
{datos_calendario}"""

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            max_tokens=280,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error procesando calendario: {e}")
        return "Lo siento, poeta, pero ahora mismo no puedo acceder al calendario. Mis disculpas. Consulta esta dirección https://www.ucm.es/master-letrasdigitales/calendario-clases"