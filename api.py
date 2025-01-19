from flask import Flask, request, jsonify
import speech_recognition as sr
from io import BytesIO

app = Flask(__name__)

@app.route('/transcrever-audio/', methods=['POST'])
def transcrever_audio():
    """
    Endpoint para transcrever um arquivo de áudio enviado pelo cliente.
    """
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado. Certifique-se de enviar um arquivo .wav"}), 400

    file = request.files['file']

    # Verificar se o arquivo é do tipo .wav
    if file.content_type not in ["audio/wav", "audio/x-wav"]:
        return jsonify({"erro": "Formato de arquivo inválido. Envie um arquivo .wav"}), 400

    # Carregar o arquivo de áudio para o reconhecedor
    audio_data = BytesIO(file.read())
    reconhecedor = sr.Recognizer()

    try:
        with sr.AudioFile(audio_data) as source:
            audio = reconhecedor.record(source)  # Lê todo o arquivo de áudio
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            return jsonify({"transcricao": texto}), 200
    except sr.UnknownValueError:
        return jsonify({"erro": "Não foi possível reconhecer o áudio."}), 400
    except sr.RequestError as e:
        return jsonify({"erro": f"Erro no serviço de reconhecimento de fala: {e}"}), 500

@app.route('/', methods=['GET'])
def root():

    return jsonify({"mensagem": "API Online"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
