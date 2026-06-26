import argparse
import tkinter as tk

import estilo
from funcoes import Controles
from janela_copiar_arquivos import CopiarArquivos

# --- Configuração do CLI (Argparse) ---
parser = argparse.ArgumentParser(prog="copiararquivos")
parser.add_argument("--version", action="version", version=f"%(prog)s {estilo.VERSION}")
args = parser.parse_args()

# --- Inicialização da Interface ---
if __name__ == "__main__":
    # 1. Inicia a janela base do Tkinter
    root = tk.Tk()

    # 2. Cria a parte visual (passando o root e a versão)
    visual = CopiarArquivos(root)

    # 3. Passa a visão para a sua classe de Lógica controlar
    logica = Controles(visual)

    # 4. Inicia o programa
    root.mainloop()
