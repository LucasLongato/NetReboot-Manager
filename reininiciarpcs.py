import subprocess
import datetime
import time
import logging
from concurrent.futures import ThreadPoolExecutor

ARQUIVO_PCS = "computadores.txt"
ARQUIVO_PENDENTES = "pendentes.txt"
LOG_FILE = "reinicio.log"

MAX_THREADS = 200  # ajuste conforme sua rede

# configuração de log
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def carregar_lista(arquivo):
    try:
        with open(arquivo, "r") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        logging.warning(f"Arquivo {arquivo} não encontrado.")
        return []

def salvar_lista(lista, arquivo):
    with open(arquivo, "w") as f:
        f.write("\n".join(lista))

def disparar_reinicio(pc):
    try:
        subprocess.Popen(
            ["shutdown", "/r", "/m", f"\\\\{pc}", "/t", "0", "/f"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logging.info(f"Disparo enviado: {pc}")
        return None
    except Exception as e:
        logging.error(f"Erro ao disparar {pc}: {e}")
        return pc

def reiniciar_lista(lista):
    pendentes = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        resultados = executor.map(disparar_reinicio, lista)

    for r in resultados:
        if r:
            pendentes.append(r)

    return pendentes

def executar_1800():
    logging.info("===== INÍCIO DO DISPARO 18:00 =====")
    print("\n🚀 Iniciando disparo de reinício...")

    pcs = carregar_lista(ARQUIVO_PCS)
    logging.info(f"Total de PCs na lista: {len(pcs)}")

    inicio = time.time()

    pendentes = reiniciar_lista(pcs)
    salvar_lista(pendentes, ARQUIVO_PENDENTES)

    duracao = time.time() - inicio

    logging.info(f"Disparos concluídos em {duracao:.2f} segundos")
    logging.info(f"Pendentes: {len(pendentes)}")
    logging.info("===== FIM DO PROCESSO =====\n")

    print(f"⏱️ Finalizado em {duracao:.2f} segundos")

ultima_execucao = None

while True:
    agora = datetime.datetime.now()
    hora = agora.strftime("%H:%M")

    if hora == "18:00" and ultima_execucao != "18:00":
        executar_1800()
        ultima_execucao = "18:00"

    time.sleep(20)