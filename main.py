from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPEN_AI_KEY")  # Obtiene la API Key desde las variables de entorno en Railway

@app.route('/traducir', methods=['POST'])
def traducir():
    try:
        # Obtiene el texto y el idioma objetivo desde el JSON enviado
        data = request.get_json()
        texto = data.get("texto", "")
        idioma_objetivo = data.get("idiomaObjetivo", "en")

        # Crea el mensaje para OpenAI en formato de chat
        prompt = f"Traduce este texto al {'inglés' if idioma_objetivo == 'en' else 'español'}: '{texto}'"

        # Realiza la solicitud a la API de OpenAI con ChatCompletion
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # Obtiene y envía la traducción
        traduccion = respuesta['choices'][0]['message']['content'].strip()
        return jsonify({"traduccion": traduccion})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Railway usará el puerto 8080


