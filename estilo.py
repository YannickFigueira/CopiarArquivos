# Versão, repositório, program title
import os
from pathlib import Path

VERSION = "v4.3.13"
REPO = "CopiarArquivos"
NOME_PROGRAMA = "Cópia de Arquivos"

# Pastas do programa
home_dir = os.path.expanduser('~')
programa_dir = f"{home_dir}/.copiar arquivos"
notas = f"{home_dir}/.copiar arquivos/notas"
log_files = Path(f"{home_dir}/.copiar arquivos/logs")

if not os.path.exists(programa_dir):
    os.mkdir(programa_dir)
if not os.path.exists(notas):
    os.mkdir(notas)
if not os.path.exists(log_files):
    os.mkdir(log_files)

# Margens padrão para janelas e frames
# Medidas
ESPACO = 5
LINHA_PAINEL_ESQUERDO = 0

# Margens padrão para janelas e frames
PADX_JANELA = 20
PADY_JANELA = 20

# Margens padrão para componentes menores (botões, inputs, labels)
PADX_COMPONENTE = 10
PADY_COMPONENTE = 5

# Arquivo de log
ARQUIVO_ERRO = "copiar_arquivos.log"

# Estilo
FONTE_VAZIA=("", 14, "normal")
FONTE_ARIAL=("Arial", 11, "normal")