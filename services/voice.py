import subprocess

def falar(texto: str):
    if not texto:
            return
                print(f"\n[Jarvis]: {texto}")
                    texto_limpo = texto.replace('"', '').replace("'", "")
                        try:
                                subprocess.run(["termux-tts-speak", texto_limpo], check=True)
                                    except Exception as e:
                                            print(f"[ERRO no TTS]: Nao foi possivel emitir voz. {e}")
                                            