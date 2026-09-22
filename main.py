import sys
import time
from core.ai_engine import JarvisEngine
from services.listener import escutar
from services.voice import falar


def iniciar_jarvis():
    print("=" * 45)
    print("      J.A.R.V.I.S. - SISTEMA INTERATIVO     ")
    print("=" * 45)

    try:
        jarvis = JarvisEngine()
        falar("Sistemas online. Como posso ajudar, Senhor?")
    except Exception as e:
        print(f"[ERRO CRÍTICO]: {e}")
        sys.exit(1)

    while True:
        try:
            # Captura a voz pelo microfone do celular
            comando = escutar()

            if not comando:
                continue

            # Comandos de saída
            if any(p in comando.lower() for p in ["desligar", "sair", "parar"]):
                falar("Desconectando sistemas. Até logo, Senhor.")
                break

            # Processa a resposta pela IA Gemini
            resposta = jarvis.enviar_mensagem(comando)

            # Fala a resposta no alto-falante
            falar(resposta)

        except KeyboardInterrupt:
            print("\n[Jarvis desativado manualmente]")
            break


if __name__ == "__main__":
    iniciar_jarvis()
