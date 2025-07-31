from flask import Flask, request, jsonify
import logging
import os
from dotenv import load_dotenv
from groq import Groq
from función_calendario import query_calendario

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Configuración Groq
groq_client = None
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
except Exception as e:
    logger.error(f"Error inicializando Groq: {e}")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json() or {}
        intent_name = extraer_intent(data)
        
        if not intent_name:
            return mensaje_error("Se ha producido un error, poeta. Por favor, reformula tu consulta.")
        
        if not groq_client:
            return mensaje_error("El servicio no está disponible temporalmente, poeta. ¿Puedes volver a preguntar?")
        
        pregunta_usuario = extraer_entrada(data)
        
        # Procesar intents
        if intent_name == "WEB-CalendarioAcadémico":
            if pregunta_usuario:
                return intent_calendario_académico(pregunta_usuario)
            else:
                return jsonify({"output": {"generic": []}})  # Ignorar llamada vacía (debugging IBM Watsonx)
                
        elif intent_name == "WEB-Disciplinas":
            if pregunta_usuario:
                return intent_disciplinas(pregunta_usuario)
            else:
                return jsonify({"output": {"generic": []}})  # Ignorar segunda llamada vacía (debugging IBM Watsonx)
            
    except Exception as e:
        logger.error(f"Error procesando webhook: {e}")
        return mensaje_error("Se está produciendo un error técnico. Viajero, espera un momento y pregúntame de nuevo.")

def extraer_intent(data):
    try:
        return data['intents'][0]['intent']
    except (KeyError, IndexError, TypeError):
        return None

def extraer_entrada(data):
    # Watson envía la pregunta en 'user_input' o 'input_text'
    return data.get('user_input') or data.get('input_text')

def mensaje_error(mensaje):
    return jsonify({
        "output": {
            "generic": [
                {
                    "response_type": "text",
                    "text": mensaje
                }
            ]
        }
    })

def intent_calendario_académico(user_question):
    try:
        ai_response = query_calendario(user_question, groq_client)
        return jsonify({
            "output": {
                "generic": [
                    {
                        "response_type": "text",
                        "text": f"🗓️ {ai_response}"
                    }
                ]
            }
        })
    except Exception as e:
        logger.error(f"Error en calendario: {e}")
        return mensaje_error("No puedo acceder al calendario académico ahora mismo, poeta.")


def intent_disciplinas(user_question):
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un asistente llamado VirgiBot, inspirado en el personaje de Virgilio. Eres agradable, servicial y cumples con tu función. especializado en disciplinas de humanidades digitales, como la lingüística computacional, el e-learning y la creación de materiales multimedia. Responde en español de manera clara y concisa, limitando tu respuesta a aproximadamente 120 palabras. Siempre debes finalizar tu respuesta ofreciendo tu disposición a recibir más cuestiones."
                },
                {
                    "role": "user", 
                    "content": user_question
                }
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        return jsonify({
            "output": {
                "generic": [
                    {
                        "response_type": "text",
                        "text": f"📚 {ai_response}"
                    }
                ]
            }
        })
    except Exception as e:
        logger.error(f"Error en disciplinas: {e}")
        return mensaje_error("No puedo acceder a la información de disciplinas ahora mismo, poeta.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)