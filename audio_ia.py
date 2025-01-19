import speech_recognition as sr
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


reconhecedor = sr.Recognizer()


with sr.Microphone() as fonte:
    print("Escutando..")
    try:

        audio = reconhecedor.listen(fonte)
        texto = reconhecedor.recognize_google(audio, language="pt-BR")

        response = model.generate_content(texto)
        print(f"Você disse: {texto}")
        print(response.text)
    except sr.UnknownValueError:
        print("Não foi possível reconhecer o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao se conectar ao serviço de reconhecimento de fala: {e}")
