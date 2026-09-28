import subprocess
import os


def falar(texto: str):
    if not texto:
        return

    # Limpa aspas do texto para evitar erros ao passar o comando no terminal
    texto_limpo = texto.replace('"', "").replace("'", "")

    # Exibe a resposta formatada do Jarvis na tela
    print(f"\n[J.A.R.V.I.S.]: {texto}\n")

    try:
        # Executa o termux-tts-speak sem poluir a tela com logs
        subprocess.run(
            ["termux-tts-speak", texto_limpo],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except Exception:
        # Silencioso caso a emissão de voz falhe, mantendo apenas o texto impresso
        pass
