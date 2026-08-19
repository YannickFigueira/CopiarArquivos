from datetime import datetime

from estilo import log_files

def gerar_arquivo_log():
    # Gera o nome dinâmico do arquivo
    log_files.mkdir(exist_ok=True)
    nome_arquivo = f"{datetime.now():%Y%m%d_%H%M}.log"
    caminho_log = log_files / nome_arquivo

    return caminho_log

def registrar_log(caminho_log, mensagem):

    """Abre o arquivo no modo append ('a') e escreve a mensagem com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 'a' abre o arquivo para escrita sem apagar o conteúdo existente
    # encoding='utf-8' previne erros de acentuação no arquivo
    with open(caminho_log, mode="a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{timestamp}] {mensagem}\n")

def limpar_logs(limite=10):
    if not log_files.exists():
        return

    # 1. Coleta todos os arquivos .log e ordena pelo mais antigo primeiro
    # Como o padrão do seu nome é AAAAMMDD_HHMM.log, a ordenação por nome/mtime funciona perfeitamente
    arquivos_log = sorted(
        [f for f in log_files.glob("*.log") if f.is_file()],
        key=lambda item: item.stat().st_mtime
    )

    # 2. Verifica se a quantidade excede o limite estipulado (10)
    quantidade_arquivos = len(arquivos_log)

    if quantidade_arquivos > limite:
        # Pega a quantidade exata de arquivos mais antigos que excederam o limite
        qtd_para_deletar = quantidade_arquivos - limite
        logs_para_deletar = arquivos_log[:qtd_para_deletar]

        # 3. Exclui com segurança diretamente no sistema de arquivos
        for log in logs_para_deletar:
            try:
                log.unlink()  # Deleta o arquivo
                print(f"Log antigo removido: {log.name}")
            except Exception as e:
                print(f"Erro ao deletar {log.name}: {e}")