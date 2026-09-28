import sys
from core.ai_engine import JarvisBrain
from services.listener import escutar
from services.speaker import falar


def capturar_entrada_usuario():
    """Se o usuário só apertar ENTER, ativa o microfone. Se digitar algo, usa como texto."""
    texto_digitado = input("\n[Digite seu comando ou pressione ENTER para falar]: ").strip()

    if texto_digitado:
        return texto_digitado

    print("[Ouvindo... Pode falar com o Jarvis]")
    return escutar()


def main():
    print("=" * 50)
    print("         J.A.R.V.I.S. - PROTOCOLO ONLINE        ")
    print("=" * 50)

    try:
        jarvis = JarvisBrain()
    except Exception as e:
        print(f"\n[ERRO DE INICIALIZAÇÃO]: {e}")
        return

    falar("Sistemas online e operacionais, Senhor. Em que posso ser útil?")

    while True:
        try:
            comando = capturar_entrada_usuario()

            if not comando:
                continue

            print(f"\n[Você]: {comando}")

            if comando.lower() in ["sair", "desligar", "encerrar", "parar"]:
                falar("Desativando sistemas. Tenha um bom dia, Senhor.")
                break

            resposta = jarvis.processar_comando(comando)
            falar(resposta)

        except (KeyboardInterrupt, SystemExit):
            print("\n\n[J.A.R.V.I.S.]: Encerramento forçado solicitado. Desconectando...")
            break


if __name__ == "__main__":
    main()