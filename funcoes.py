import logging
import os
import platform
import shutil
import subprocess
import threading
import time
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, filedialog

import verificarversao, estilo

# Detecta sistema operacional
system = platform.system()  # Retorna 'Linux', 'Windows', 'Darwin' (Mac)

# Evento para parar a thread do tempo
parar_tempo = threading.Event()
pausar_tempo = threading.Event()

# --- Registro de erros ---
arquivo_erro = estilo.ARQUIVO_ERRO
home_dir = os.path.expanduser('~')
if system == 'Linux':
    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/{arquivo_erro}",        # nome do arquivo
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
    home_dir = os.path.expanduser('~')
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

def atualiza_tempo(inicio, label):
    """Thread que atualiza o label de tempo decorrido em paralelo."""
    while not parar_tempo.is_set():
        # Se estiver pausado, espera até ser liberado
        while pausar_tempo.is_set() and not parar_tempo.is_set():
            time.sleep(0.1)

        decorrido = time.time() - inicio
        horas, resto = divmod(decorrido, 3600)  # divide em horas
        minutos, segundos = divmod(resto, 60)  # divide o restante em minutos e segundos

        # agenda a atualização do label na thread principal do Tkinter
        def _set_label():
            label.config(text=f"{int(horas):02}:{int(minutos):02}:{segundos:04.1f}")

        label.after(0, _set_label)
        # frequência de atualização (ajuste conforme desejar)
        time.sleep(0.2)

# --- Formatar exibição dos tamanhos dos arquivos
def formatar_tamanho(tamanho):
    tamanho_kb = tamanho / 1024
    tamanho_mb = tamanho / 1024 / 1024
    tamanho_gb = tamanho / 1024 / 1024 / 1024

    if tamanho > (1024 ** 3):
        return f"{tamanho_gb:.2f} GB"
    elif tamanho > (1024 ** 2):
        return f"{tamanho_mb:.2f} MB"
    elif tamanho > 1024:
        return f"{tamanho_kb:.2f} KB"
    else:
        return f"{tamanho:.2f} B"

### Atualiza a barra de progresso ###
def atualizar_barra(valor, total, progress_canvas):
    progress_canvas.delete("all")
    largura = int((valor / total) * progress_canvas.winfo_width())
    # desenha a barra preenchida
    progress_canvas.create_rectangle(0, 0, largura, 25, fill="green")
    # escreve a porcentagem dentro da barra
    porcentagem = (valor / total) * 100
    x = progress_canvas.winfo_width() // 2
    progress_canvas.create_text(x, 12, text=f"{porcentagem:.3f}%", fill="black", font=("Arial", 10, "bold"))

# --- Desliga o equipamento
def desligar_computador():
    # Detecta o sistema operacional atual
    sistema = platform.system().lower()

    if "windows" in sistema:
        # /s = desligar, /t 0 = tempo de espera (0 segundos)
        os.system("shutdown /s /t 0")
    elif "linux" in sistema:
        # h = halt/desligar, now = imediatamente
        # Nota: no Linux, pode ser necessário privilégios de root (sudo) dependendo da distro
        os.system("shutdown -h now")
    else:
        print("Sistema operacional não suportado para esta ação.")

def pausar_copia():
    global pausar
    pausar = True

# --- Inicio dos Controles
class Controles:
    def __init__(self, view):
        self.view = view
        self.repo = self.view.controles['var_repo'].get()
        self.version = self.view.controles['var_version'].get()
        self.programa_title = self.view.controles['var_title'].get()

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "copiararquivos":
                self._vincular_copiar_arquivos()

    def _vincular_copiar_arquivos(self):
        # --- Controle do Menu ---
        self.view.controles['menu_arquivo'].add_command(label="Abrir log de ERRO", command=lambda: abrir_logs())
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                               command=lambda: verificarversao.consultar_lancamento(self.repo, self.version))
        self.view.controles['menu_ajuda'].add_command(label="Sobre",
                               command=lambda: self.visitar_site())
        self.view.controles['menu_ajuda'].add_command(label="Sair",
                                                        command=lambda: self.fechar())
        # --- Controles da Janela Principal ---
        self.view.controles['button_selecionar_origem'].config(command=lambda: self.selecionar_origem())
        self.view.controles['button_selecionar_destino'].config(command=lambda: self.selecionar_destino())
        self.view.controles['button_executar_copia'].config(command=lambda: self.executar_acao())
        self.view.controles['button_cancelar'].config(command=lambda: self.parar_copia())
        self.view.controles['button_pausar'].config(command=lambda: pausar_copia())

        self.clipboard(self.view.controles['entrada_origem'])
        self.clipboard(self.view.controles['entrada_destino'])

    # --- Comandos dos Menus
    def visitar_site(self):
        pagina = "https://github.com/YannickFigueira"
        resposta = messagebox.askyesno(
            "Sobre",
            f"{estilo.NOME_PROGRAMA} v{estilo.VERSION}\n"
            f"Desenvolvedor YannickFigueira\n"
            f"chronostimeinchain@gmail.com\n\n"
            f"Deseja visitar a página?"
        )
        if resposta:
            webbrowser.open(pagina)

    def fechar(self):
        self.view.controles['janela_principal'].quit()

    # --- Comando dos Controles ---
    def selecionar_origem(self):
        self.view.controles['entrada_origem'].delete(0, 'end')
        self.view.controles['entrada_origem'].insert(0, selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['entrada_destino'].delete(0, 'end')
        self.view.controles['entrada_destino'].insert(0, selecionar_pasta())

    def executar_acao(self):
        widgets = [self.view.controles['entrada_origem'],
                   self.view.controles['entrada_destino'],
                   self.view.controles['button_selecionar_origem'],
                   self.view.controles['button_selecionar_destino'],
                   self.view.controles['button_executar_copia']]

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
                        self.iniciar_copia(texto_origem, destino, widgets)
                        self.iniciar_contagem()
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

    # --- Execução da cópia dos arquivos
    def iniciar_copia(self, origem, destino, widgets):
        t = threading.Thread(
            target=self.copiando_arquivos,
            args=(origem,
                  destino,
                  widgets),
            daemon=True
        )
        t.start()

    def copiando_arquivos(self, texto_origem, texto_destino, widgets):
        erro = False
        global cancelar
        global pausar
        parar_tempo.clear()
        pasta_matriz = texto_origem.split("/")
        origem = Path(texto_origem)

        if self.view.controles['checkbox_origem'].get():
            texto_destino = f"{texto_destino}/{pasta_matriz[len(pasta_matriz) - 1]}"

        destino = Path(texto_destino)
        destino.mkdir(parents=True, exist_ok=True)

        for widget in widgets:
            widget.config(state="disabled")

        self.view.controles['janela_principal'].update_idletasks()
        # lista todos os arquivos e subpastas
        arquivos = []
        for raiz, dirs, files in os.walk(origem, onerror=lambda a: None):
            for f in files:
                arquivos.append(Path(raiz) / f)

        total = len(arquivos)
        tamanho_item = 0
        inicio = time.time()  # marca o início da execução
        # inicia a thread do tempo (daemon para não travar saída)
        thread_tempo = threading.Thread(target=atualiza_tempo, args=(inicio, self.view.controles['label_tempo_decorrido']), daemon=True)
        thread_tempo.start()

        try:
            for i, item in enumerate(arquivos, start=1):
                if cancelar:
                    self.view.controles['text_area'].delete(1.0, "end")  # apaga tudo
                    self.view.controles['progress_canvas'].delete("all")
                    cancelar = False
                    break

                destino_item = destino / item.relative_to(origem)
                try:
                    if item.is_dir():
                        destino_item.mkdir(parents=True, exist_ok=True)
                    else:
                        self.view.controles['text_area'].delete("1.0", "end")  # apaga tudo
                        self.view.controles['text_area'].insert("1.0", f"{formatar_tamanho(item.stat().st_size)} -> {item}")

                        disco = ""
                        if system == 'Windows':
                            separar = widgets[1].get().split("/")
                            disco = separar[0]
                        elif system == 'Linux':
                            disco = widgets[1].get()

                        uso = shutil.disk_usage(disco)
                        if item.stat().st_size > uso.free:
                            pausar_tempo.set()
                            messagebox.showwarning("Sem espaço em disco",
                                                   f"Espaço necessário {formatar_tamanho(item.stat().st_size - uso.free)}")
                            pausar_tempo.clear()

                        if pausar:
                            pausar_tempo.set()
                            messagebox.showinfo("Pausado", "Clique em OK para continuar")
                            pausar_tempo.clear()
                            pausar = False

                        destino_item.parent.mkdir(parents=True, exist_ok=True)

                        # 1. Se o arquivo não existe no destino, copia direto
                        if not destino_item.is_file():
                            shutil.copy2(item, destino_item)

                        # 2. Se ele existe, compara as datas de modificação
                        elif item.stat().st_mtime > destino_item.stat().st_mtime:
                            shutil.copy2(item, destino_item)

                        tamanho_item += item.stat().st_size
                        self.view.controles['label_copiado_contagem'].config(text=formatar_tamanho(tamanho_item))

                except Exception as e:
                    # Mostra o erro mas continua
                    logging.error(f"Erro ao copiar {item}: {e}")
                    erro = True

                atualizar_barra(i, total, self.view.controles['progress_canvas'])
                self.view.controles['janela_principal'].update_idletasks()  # força atualização da ‘interface’
        finally:
            # sinaliza para parar a thread de tempo e aguarda encerrar
            parar_tempo.set()
            # small join com timeout para evitar travar se a GUI encerrar
            thread_tempo.join(timeout=1.0)

        self.view.controles['text_area'].insert("2.0", "\nFinalizado!")

        for widget in widgets:
            widget.config(state="normal")
        self.view.controles['button_pausar'].config(state="disabled")

        if erro:
            messagebox.showwarning("Erro", "Foi encontrado erros durante a cópia, vá em Arquivos -> Abrir log de ERRO")

        if self.view.controles['checkbox_desligar'].get():
            desligar_computador()
            self.view.controles['janela_principal'].destroy()

        if self.view.controles['checkbox_encerrar'].get():
            self.view.controles['janela_principal'].destroy()

    # --- Contagem do tempo

    def iniciar_contagem(self):
        t = threading.Thread(
            target=self.tamanho_pasta,
            args=(),
            daemon=True
        )
        t.start()

    def tamanho_pasta(self):
        origem = Path(self.view.controles['entrada_origem'].get().strip().replace("\\", "/"))
        arquivos = list(origem.rglob("*"))
        tamanho_total = sum(f.stat().st_size for f in arquivos if f.is_file())
        self.view.controles['label_tamanho_contagem'].config(text=formatar_tamanho(tamanho_total))

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

    def parar_copia(self):
        sim = messagebox.askyesno("Cancelar", "Quer realmente cancelar?")
        if sim:
            global cancelar
            cancelar = True
            self.view.controles['button_cancelar'].config(state="disabled")
