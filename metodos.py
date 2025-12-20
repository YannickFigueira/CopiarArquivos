import time
from pathlib import Path
import threading
import shutil
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import platform

# Configuração do logger
# Detecta sistema operacional
system = platform.system()  # Retorna 'Linux', 'Windows', 'Darwin' (Mac)

home_dir = os.path.expanduser('~')
if system == 'Linux':

    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/copiararquivos.log",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
elif system == 'Windows':

    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename="c:/temp/copiararquivos.log",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Evento para parar a thread do tempo
parar_tempo = threading.Event()

cancelar = False
def parar_copia():
    global cancelar
    cancelar = True

def copiando_arquivos(texto_origem,
                      texto_destino,
                      root,
                      progress_canvas,
                      entrada_origem,
                      entrada_destino,
                      button_executar_copia,
                      text_area,
                      label_copiado_contagem,
                      label_tempo_decorrido,
                      checkbox_origem,
                      checkbox_encerrar):
    global cancelar

    pasta_matriz = str(texto_origem).split("/")

    origem = Path(texto_origem)
    if checkbox_origem:
        texto_destino = f"{texto_destino}/{pasta_matriz[len(pasta_matriz) - 1]}"

    destino = Path(texto_destino)
    destino.mkdir(parents=True, exist_ok=True)

    # desabilita entradas e botão
    root.after(0, lambda: entrada_origem.config(state="disabled"))
    root.after(0, lambda: entrada_destino.config(state="disabled"))
    root.after(0, lambda: button_executar_copia.config(state="disabled"))

    # lista todos os arquivos e subpastas
    arquivos = []
    for raiz, dirs, files in os.walk(origem, onerror=lambda e: None):
        for f in files:
            arquivos.append(Path(raiz) / f)

    total = len(arquivos)

    #progress_bar["maximum"] = total # define o valor máximo da barra
    #progress_bar["value"] = 0 # inicia em zero

    tamanho_item = 0
    inicio = time.time() # marca o início da execução

    # inicia a thread do tempo (daemon para não travar saída)
    thread_tempo = threading.Thread(target=atualiza_tempo, args=(inicio, label_tempo_decorrido), daemon=True)
    thread_tempo.start()

    try:
        for i, item in enumerate(arquivos, start=1):
            if cancelar:
                text_area.delete(1.0, "end") # apaga tudo
                progress_canvas.delete("all")
                cancelar = False
                break

            destino_item = destino / item.relative_to(origem)
            try:
                if item.is_dir():
                    destino_item.mkdir(parents=True, exist_ok=True)
                else:
                    text_area.delete("1.0", "end")  # apaga tudo
                    text_area.insert("1.0", item)
                    destino_item.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, destino_item)
                    tamanho_item += item.stat().st_size
                    label_copiado_contagem.config(text=formatar_tamanho(tamanho_item))

            except Exception as e:
                # Mostra o erro mas continua
                logging.error(f"Erro ao copiar {item}: {e}")

            atualizar_barra(i, total, progress_canvas)

            # atualiza a barra de progresso
            #progress_bar["value"] = i
            root.update_idletasks()  # força atualização da ‘interface’
    finally:
        # sinaliza para parar a thread de tempo e aguarda encerrar
        parar_tempo.set()
        # small join com timeout para evitar travar se a GUI encerrar
        thread_tempo.join(timeout=1.0)

    text_area.insert("2.0", "\nFinalizado!")

    entrada_origem.config(state="enabled")
    entrada_destino.config(state="enabled")
    button_executar_copia.config(state="enabled")

    if checkbox_encerrar:
        messagebox.showinfo("Encerrando", "Programa será encerrado")
        root.destroy()

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

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return None
def formatar_tamanho(tamanho):
    tamanho_kb = tamanho / 1024
    tamanho_mb = tamanho / 1024 / 1024
    tamanho_gb = tamanho / 1024 / 1024 / 1024

    if tamanho > (1024 * 1024 * 1024):
        return f"{tamanho_gb:.2f} GiB"
    elif tamanho > (1024 * 1024):
        return f"{tamanho_mb:.2f} MB"
    elif tamanho > 1024:
        return f"{tamanho_kb:.2f} KB"
    else:
        return f"{tamanho:.2f} B"

def tamanho_pasta(entrada_origem, label_tamanho_contagem):
    origem = Path(entrada_origem)
    arquivos = list(origem.rglob("*"))

    tamanho_total = sum(f.stat().st_size for f in arquivos if f.is_file())

    label_tamanho_contagem.config(text=formatar_tamanho(tamanho_total))

def iniciar_contagem(entrada_origem,
                    label_tamanho_contagem):
    t = threading.Thread(
        target=tamanho_pasta,
        args=(entrada_origem,
              label_tamanho_contagem),
        daemon=True
    )
    t.start()

def atualiza_tempo(inicio, label):
    """Thread que atualiza o label de tempo decorrido em paralelo."""
    while not parar_tempo.is_set():
        decorrido = time.time() - inicio
        minutos, segundos = divmod(decorrido, 60)

        # agenda a atualização do label na thread principal do Tkinter
        def _set_label():
            label.config(text=f"{int(minutos)}:{segundos:04.1f}")

        label.after(0, _set_label)

        # frequência de atualização (ajuste conforme desejar)
        time.sleep(0.2)

# --- Inicia a cópia --- #
def iniciar_copia(texto_origem,
                      texto_destino,
                      root,
                      progress_canvas,
                      entrada_origem,
                      entrada_destino,
                      button_executar_copia,
                      text_area,
                  label_copiado_contagem,
                  label_tempo_decorrido,
                  checkbox_origem,
                  checkbox_encerrar):
    t = threading.Thread(
        target=copiando_arquivos,
        args=(texto_origem,
              texto_destino,
              root,
              progress_canvas,
              entrada_origem,
              entrada_destino,
              button_executar_copia,
              text_area,
              label_copiado_contagem,
              label_tempo_decorrido,
              checkbox_origem,
              checkbox_encerrar),
        daemon=True
    )
    t.start()

def clipboard(root, entrada):
    def mostrar_menu(event):
        # Guardar qual Entry foi clicado
        global entry_atual
        entry_atual = event.widget
        menu_popup.tk_popup(event.x_root, event.y_root)

    def copiar():
        try:
            root.clipboard_clear()
            root.clipboard_append(entry_atual.selection_get())
        except tk.TclError:
            pass  # nada selecionado

    def colar():
        try:
            entry_atual.insert(tk.INSERT, root.clipboard_get())
        except tk.TclError:
            pass  # clipboard vazio

    def recortar():
        try:
            root.clipboard_clear()
            root.clipboard_append(entry_atual.selection_get())
            entry_atual.delete("sel.first", "sel.last")
        except tk.TclError:
            pass  # nada selecionado

    # Criar menu único
    menu_popup = tk.Menu(root, tearoff=0)
    menu_popup.add_command(label="Copiar", command=copiar)
    menu_popup.add_command(label="Colar", command=colar)
    menu_popup.add_command(label="Recortar", command=recortar)

    # Associar clique direito a ambos os Entry
    entrada.bind("<Button-3>", mostrar_menu)
