import subprocess

def escutar() -> str:
    print("\n[Ouvindo... Fale com o Jarvis]")
        try:
                resultado = subprocess.check_output(["termux-speech-to-text"], text=True).strip()
                        if resultado:
                                    print(f"[Voce]: {resultado}")
                                                return resultado
                                                    except Exception as e:
                                                            print("[AVISO]: Nao foi possivel capturar voz ou o comando foi cancelado.")
                                                                return ""
                                                                