import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class JarvisEngine:
    def __init__(self):
            self.api_key = os.getenv("GEMINI_API_KEY")
                    if not self.api_key:
                                raise ValueError("[ERRO] A chave GEMINI_API_KEY nao foi encontrada no .env!")

                                        self.client = genai.Client(api_key=self.api_key)
                                                self.system_instruction = (
                                                            "Voce e o J.A.R.V.I.S., o assistente pessoal de inteligencia artificial inspirado na Marvel. "
                                                                        "Responda sempre em portugues, de forma breve, concisa, extremamente eficiente, educada e com refinamento. "
                                                                                    "Suas respostas serao lidas em voz alta, entao evite caracteres especiais, tabelas ou listas longas."
                                                                                            )
                                                                                                    self.chat = self.client.chats.create(
                                                                                                                model="gemini-2.5-flash",
                                                                                                                            config=types.GenerateContentConfig(
                                                                                                                                            system_instruction=self.system_instruction,
                                                                                                                                                            temperature=0.7
                                                                                                                                                                        )
                                                                                                                                                                                )

                                                                                                                                                                                    def enviar_mensagem(self, texto: str) -> str:
                                                                                                                                                                                            try:
                                                                                                                                                                                                        resposta = self.chat.send_message(texto)
                                                                                                                                                                                                                    return resposta.text
                                                                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                                                                        print(f"[ERRO na IA]: {e}")
                                                                                                                                                                                                                                                    return "Perdao, Senhor. Ocorreu uma falha ao processar sua solicitacao."
                                                                                                                                                                                                                                                    