import os
import subprocess
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def escutar() -> str:
    arquivo_audio = "comando.mp3"

    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)

    print("\n[Ouvindo... Pode falar com o Jarvis]")

    try:
        # Inicia a gravacao do microfone nativo via Termux:API
        subprocess.run(
            ["termux-microphone-record", "-f", arquivo_audio, "-l", "6"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Aguarda o tempo de escuta
        time.sleep(6)

        # Para a gravacao
        subprocess.run(
            ["termux-microphone-record", "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if os.path.exists(arquivo_audio) and os.path.getsize(arquivo_audio) > 0:
            print("[Analisando comando...]")
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

            # Envia o arquivo de audio para a API
            audio_file = client.files.upload(file=arquivo_audio)

            texto_transcrito = ""
            try:
                # Usa generate_content com AFC desativado para evitar warnings
                resposta = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[
                        audio_file,
                        "Transcreva exatamente o que foi dito neste audio em portugues. Responda APENAS com o texto transcrito, sem explicacoes.",
                    ],
                    config=types.GenerateContentConfig(
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(
                            disable=True
                        )
                    ),
                )
                texto_transcrito = resposta.text.strip()
            except Exception as e:
                print(f"[AVISO Transcricao]: {e}")

            # Limpa o arquivo da nuvem e do celular
            try:
                client.files.delete(name=audio_file.name)
            except Exception:
                pass

            if os.path.exists(arquivo_audio):
                os.remove(arquivo_audio)

            if texto_transcrito and "Nenhum som" not in texto_transcrito:
                print(f"[Voce]: {texto_transcrito}")
                return texto_transcrito

    except Exception as e:
        print(f"[AVISO]: Falha ao capturar audio: {e}")
        subprocess.run(
            ["termux-microphone-record", "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if os.path.exists(arquivo_audio):
            os.remove(arquivo_audio)

    # Fallback para entrada de texto via teclado
    texto_digitado = input(
        "[Digite seu comando ou Pressione ENTER para tentar novamente]: "
    ).strip()
    if texto_digitado:
        print(f"[Voce (digitado)]: {texto_digitado}")
        return texto_digitado

    return ""
