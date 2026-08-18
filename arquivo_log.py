from datetime import datetime

import estilo

def gerar_arquivo_log():
    # Gera o nome dinâmico do arquivo
    estilo.log_files.mkdir(exist_ok=True)
    nome_arquivo = f"{datetime.now():%Y%m%d_%H%M}.log"
    caminho_log = estilo.log_files / nome_arquivo

    return caminho_log

def registrar_log(caminho_log, mensagem):

    """Abre o arquivo no modo append ('a') e escreve a mensagem com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 'a' abre o arquivo para escrita sem apagar o conteúdo existente
    # encoding='utf-8' previne erros de acentuação no arquivo
    with open(caminho_log, mode="a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{timestamp}] {mensagem}\n")