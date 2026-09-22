import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class JarvisEngine:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "[ERRO] Chave GEMINI_API_KEY nao encontrada no .env!"
            )

        self.client = genai.Client(api_key=self.api_key)
        self.system_instruction = (
            "Voce e o J.A.R.V.I.S., assistente pessoal inspirado na Marvel. "
            "Responda em portugues do Brasil, de forma breve, eficiente e educada. "
            "Suas respostas serao lidas em voz alta, evite caracteres especiais ou listas longas."
        )

        # Modelo atualizado e suportado
        self.modelo = "gemini-3.6-flash"
        self._iniciar_chat()

    def _iniciar_chat(self):
        self.chat = self.client.chats.create(
            model=self.modelo,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
            ),
        )

    def enviar_mensagem(self, texto: str) -> str:
        try:
            resposta = self.chat.send_message(texto)
            return resposta.text
        except Exception as e:
            print(f"[ERRO na IA]: {e}")
            return (
                "Perdao, Senhor. Ocorreu uma falha ao processar sua solicitacao no momento."
            )

