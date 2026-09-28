import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from core.tools import FERRAMENTAS_DISPONIVEIS

load_dotenv()


class JarvisBrain:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("[ERRO] Chave GEMINI_API_KEY nao encontrada no .env!")

        self.client = genai.Client(api_key=self.api_key)

        self.system_instruction = (
            "Você é o J.A.R.V.I.S., assistente pessoal do Senhor. "
            "Responda sempre em português, de forma breve, eficiente e refinada. "
            "Suas respostas serão lidas por voz, evite caracteres especiais ou emojis."
        )

        self.chat = self.client.chats.create(
            model="gemini-3.8-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
                tools=FERRAMENTAS_DISPONIVEIS,
            ),
        )

    def processar_comando(self, texto: str, max_retries: int = 3) -> str:
        delay = 2  # Segundos de espera iniciais
        
        for tentativa in range(1, max_retries + 1):
            try:
                resposta = self.chat.send_message(texto)
                return resposta.text
            except Exception as e:
                erro_str = str(e)
                
                # Se for erro de sobrecarga (503) ou muitas requisições (429), tenta de novo
                if "503" in erro_str or "429" in erro_str or "UNAVAILABLE" in erro_str:
                    print(f"\n[AVISO]: Servidor ocupado. Reagendando tentativa {tentativa}/{max_retries} em {delay}s...")
                    time.sleep(delay)
                    delay *= 2  # Aumenta o tempo de espera exponencialmente (2s, 4s, 8s)
                else:
                    print(f"\n[ERRO na IA]: {e}")
                    return "Perdão, Senhor. Tive uma falha de conexão com meus servidores centrais."

        return "Perdão, Senhor. Os servidores da API estão com alta demanda no momento. Por favor, tente novamente em instantes."
