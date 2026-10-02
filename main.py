import os
import requests
from dotenv import load_dotenv
from services.listener import escutar
from services.speaker import falar
from core.tools import FERRAMENTAS_DISPONIVEIS

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
JARVIS_SECRET_KEY = os.getenv("JARVIS_SECRET_KEY", "")
HEADERS = {"X-API-Key": JARVIS_SECRET_KEY, "Content-Type": "application/json"}

FUNCOES_POR_NOME = {funcao.__name__: funcao for funcao in FERRAMENTAS_DISPONIVEIS}


def capturar_entrada_usuario():
    texto_digitado = input("\n[Digite seu comando ou pressione ENTER para falar]: ").strip()
    if texto_digitado:
        return texto_digitado
    print("[Ouvindo... Pode falar com o Jarvis]")
    return escutar()


def enviar_mensagem(texto: str) -> dict:
    try:
        resposta = requests.post(
            f"{BACKEND_URL}/chat",
            headers=HEADERS,
            json={"message": texto},
            timeout=60,
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"tipo": "texto", "resposta": f"Perdão, Senhor. Falha ao contatar o servidor central: {e}"}


def enviar_resultado_funcao(nome_funcao: str, resultado: str) -> dict:
    try:
        resposta = requests.post(
            f"{BACKEND_URL}/chat/resultado-funcao",
            headers=HEADERS,
            json={"nome_funcao": nome_funcao, "resultado": resultado},
            timeout=30,
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"tipo": "texto", "resposta": f"Perdão, Senhor. Falha ao enviar resultado: {e}"}


def processar_resposta(payload: dict) -> str:
    if payload.get("tipo") == "function_call":
        nome_funcao = payload["nome"]
        argumentos = payload.get("argumentos", {})

        funcao = FUNCOES_POR_NOME.get(nome_funcao)
        if not funcao:
            return f"O backend pediu a função '{nome_funcao}', que não existe neste dispositivo."

        print(f"[Executando]: {nome_funcao}({argumentos})")
        resultado_execucao = funcao(**argumentos)

        payload_final = enviar_resultado_funcao(nome_funcao, resultado_execucao)
        return processar_resposta(payload_final)

    return payload.get("resposta", "Não obtive uma resposta válida do servidor.")


def main():
    print("=" * 50)
    print("         J.A.R.V.I.S. - PROTOCOLO ONLINE        ")
    print("=" * 50)

    if not JARVIS_SECRET_KEY:
        print("\n[ERRO DE INICIALIZAÇÃO]: JARVIS_SECRET_KEY não encontrada no .env!")
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

            payload = enviar_mensagem(comando)
            resposta_final = processar_resposta(payload)
            falar(resposta_final)

        except (KeyboardInterrupt, SystemExit):
            print("\n\n[J.A.R.V.I.S.]: Encerramento forçado solicitado. Desconectando...")
            break


if __name__ == "__main__":
    main()