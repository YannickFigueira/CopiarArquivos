import logging
import os
import platform
import subprocess
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, filedialog

import verificarversao, estilo, copiar_arquivos

# Detecta sistema operacional
system = platform.system()  # Retorna 'Linux', 'Windows', 'Darwin' (Mac)

# --- Registro de erros ---
arquivo_erro = estilo.ARQUIVO_ERRO

if system == 'Linux':
    logging.basicConfig(
        filename=f"{estilo.home_dir}/log/{arquivo_erro}",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

elif system == 'Windows':
    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename=f"c:/temp/{arquivo_erro}",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

# --- Variáveis globais ---
cancelar = False
pausar = False

# --- Comandos dos Menus
def abrir_logs():
    if platform.system() == "Windows":
        arquivo = f"C:\\temp\\{estilo.ARQUIVO_ERRO}"
        subprocess.run(["notepad", arquivo])
    elif platform.system() == "Linux":
        arquivo = f"{home_dir}/log/{estilo.ARQUIVO_ERRO}"
        subprocess.run(["xdg-open", arquivo])  # ou "gedit"
    else:
        print("Sistema não suportado")

# --- Comandos gerais ---
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""


# --- Inicio dos Controles
def visitar_site():
    pagina = "https://github.com/YannickFigueira"
    resposta = messagebox.askyesno(
        "Sobre",
        f"{estilo.NOME_PROGRAMA} {estilo.VERSION}\n"
        f"Desenvolvedor YannickFigueira\n"
        f"chronostimeinchain@gmail.com\n\n"
        f"Deseja visitar a página?"
    )
    if resposta:
        webbrowser.open(pagina)

class Controles:
    def __init__(self, view):
        self.view = view

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "copiararquivos":
                self._vincular_copiar_arquivos()

    def _vincular_copiar_arquivos(self):
        # --- Controle do Menu ---
        self.view.controles['menu_arquivo'].add_command(label="Abrir log de ERRO", command=lambda: abrir_logs())
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                               command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Sobre",
                               command=lambda: visitar_site())
        self.view.controles['menu_ajuda'].add_command(label="Sair",
                                                        command=lambda: self.fechar('janela_principal'))
        # --- Controles da Janela Principal ---
        self.view.controles['button_selecionar_origem'].config(command=lambda: self.selecionar_origem())
        self.view.controles['button_selecionar_destino'].config(command=lambda: self.selecionar_destino())
        self.view.controles['button_executar_copia'].config(command=lambda: self.executar_acao())
        self.view.controles['button_cancelar'].config(command=lambda: copiar_arquivos.cancelar_copia())
        self.view.controles['button_pausar'].config(command=lambda: copiar_arquivos.pausar_copia())

        self.clipboard(self.view.controles['entrada_origem'])
        self.clipboard(self.view.controles['entrada_destino'])

    # --- Comandos dos Menus ---

    def fechar(self, nome):
        self.view.controles[nome].quit()

    # --- Comando dos Controles ---
    def selecionar_origem(self):
        self.view.controles['entrada_origem'].delete(0, 'end')
        self.view.controles['entrada_origem'].insert(0, selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['entrada_destino'].delete(0, 'end')
        self.view.controles['entrada_destino'].insert(0, selecionar_pasta())

    def executar_acao(self):
        texto_origem = self.view.controles['entrada_origem'].get().strip().replace("\\", "/")
        destino = self.view.controles['entrada_destino'].get().strip().replace("\\", "/")
        verificar_destino = destino.split("/")

        verificar = ""
        if system == 'Windows':
            verificar = f"{verificar_destino[0]}"
        elif system == 'Linux':
            verificar = f"/{verificar_destino[0]}"

        if not texto_origem == "":
            if Path(texto_origem).is_dir():
                if not destino == "":
                    if Path(verificar).is_dir():
                        self.view.controles['button_cancelar'].config(state="normal")
                        self.view.controles['button_pausar'].config(state="normal")
                        origem_pasta = [texto_origem]
                        destino_pasta = [destino]
                        copiar_arquivos.iniciar_copiar_arquivos(self.view, origem_pasta, destino_pasta)
                    else:
                        messagebox.showwarning("Aviso", "Selecionar pasta de destino válida")
                        self.view.controles['entrada_destino'].focus_set()
                else:
                    messagebox.showwarning("Aviso", "Selecione a pasta de destino, ou cole o caminho")
                    self.view.controles['entrada_destino'].focus_set()
            else:
                messagebox.showwarning("Aviso", "Pasta não existe, verifique")
                self.view.controles['entrada_origem'].focus_set()
        else:
            messagebox.showwarning("Aviso", "Selecionar a pasta de origem, ou colar o caminho")
            self.view.controles['entrada_origem'].focus_set()

    def clipboard(self, entrada):
        def mostrar_menu(event):
            # Guardar qual Entry foi clicado
            global entry_atual
            entry_atual = event.widget
            menu_popup.tk_popup(event.x_root, event.y_root)

        def copiar():
            try:
                self.view.controles['janela_principal'].clipboard_clear()
                self.view.controles['janela_principal'].clipboard_append(entry_atual.selection_get())
            except tk.TclError:
                pass  # nada selecionado

        def colar():
            try:
                entry_atual.insert(tk.INSERT, self.view.controles['janela_principal'].clipboard_get())
            except tk.TclError:
                pass  # clipboard vazio

        def recortar():
            try:
                self.view.controles['janela_principal'].clipboard_clear()
                self.view.controles['janela_principal'].clipboard_append(entry_atual.selection_get())
                entry_atual.delete("sel.first", "sel.last")
            except tk.TclError:
                pass  # nada selecionado

        # Criar menu único
        menu_popup = tk.Menu(self.view.controles['janela_principal'], tearoff=0)
        menu_popup.add_command(label="Copiar", command=copiar)
        menu_popup.add_command(label="Colar", command=colar)
        menu_popup.add_command(label="Recortar", command=recortar)

        # Associar clique direito a ambos os Entry
        entrada.bind("<Button-3>", mostrar_menu)
