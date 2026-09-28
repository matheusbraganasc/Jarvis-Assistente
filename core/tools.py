import os
import sys
import subprocess


def _rodando_no_termux() -> bool:
    return "termux" in os.getenv("PREFIX", "").lower()


def checar_bateria() -> str:
    """Verifica a porcentagem da bateria e se o dispositivo está carregando."""
    try:
        if _rodando_no_termux():
            res = subprocess.getoutput("termux-battery-status")
            return f"Status da bateria no celular: {res}"
        else:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                status = "conectado à tomada" if battery.power_plugged else "na bateria"
                return f"O computador está em {battery.percent}% de carga e {status}."
            return "Não foi possível ler a bateria do computador."
    except Exception as e:
        return f"Não consegui verificar a bateria agora. Erro: {e}"


def controlar_lanterna(estado: str) -> str:
    """Liga ou desliga a lanterna do celular.

    Args:
        estado: Deve ser exatamente 'on' para ligar ou 'off' para desligar.
    """
    if not _rodando_no_termux():
        return "Controle de lanterna disponível apenas no smartphone."
    if estado not in ("on", "off"):
        return "Estado inválido para a lanterna. Use 'on' ou 'off'."
    try:
        os.system(f"termux-torch {estado}")
        return f"Lanterna alterada para {estado}."
    except Exception as e:
        return f"Não consegui controlar a lanterna. Erro: {e}"


def abrir_aplicativo(nome_app: str) -> str:
    """Abre um aplicativo ou site no computador ou celular.

    Args:
        nome_app: Nome do aplicativo ou URL a ser aberto, ex: 'notepad' ou 'https://google.com'.
    """
    try:
        if sys.platform == "win32":
            os.system(f"start {nome_app}")
            return f"Tentando abrir {nome_app} no Windows."
        elif sys.platform == "darwin":
            os.system(f"open {nome_app}")
            return f"Tentando abrir {nome_app} no macOS."
        elif _rodando_no_termux():
            os.system(f"termux-open-url {nome_app}")
            return f"Tentando abrir {nome_app} no celular."
        return f"Não sei como abrir aplicativos nesta plataforma ainda."
    except Exception as e:
        return f"Não consegui abrir {nome_app}. Erro: {e}"


FERRAMENTAS_DISPONIVEIS = [checar_bateria, controlar_lanterna, abrir_aplicativo]