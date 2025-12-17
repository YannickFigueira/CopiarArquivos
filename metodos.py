import time
from pathlib import Path
import threading
import shutil
import os
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
        #print(verificar)

    destino = Path(texto_destino)

    #print(pasta_matriz[len(pasta_matriz) -1])
    destino.mkdir(parents=True, exist_ok=True)

    #entrada_origem.config(state="disabled")
    #entrada_destino.config(state="disabled")
    #button_executar_copia.config(state="disabled")

    # desabilita entradas e botão
    root.after(0, lambda: entrada_origem.config(state="disabled"))
    root.after(0, lambda: entrada_destino.config(state="disabled"))
    root.after(0, lambda: button_executar_copia.config(state="disabled"))

    # lista todos os arquivos e subpastas
    arquivos = list(origem.rglob("*"))
    total = len(arquivos)

    #progress_bar["maximum"] = total  # define o valor máximo da barra
    #progress_bar["value"] = 0  # inicia em zero

    tamanho_item = 0
    inicio = time.time() # marca o início da execução
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

        # tempo decorrido
        decorrido = time.time() - inicio
        # label_tempo_decorrido.config(text=f"{decorrido:.1f} s")
        minutos, segundos = divmod(decorrido, 60)
        label_tempo_decorrido.config(text=f"{int(minutos)}:{segundos:04.1f}")

        atualizar_barra(i, total, progress_canvas)

        # atualiza a barra de progresso
        #progress_bar["value"] = i
        root.update_idletasks()  # força atualização da interface

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
    largura = int((valor / total) * 300)
    # desenha a barra preenchida
    progress_canvas.create_rectangle(0, 0, largura, 25, fill="green")
    # escreve a porcentagem dentro da barra
    porcentagem = (valor / total) * 100
    progress_canvas.create_text(150, 12, text=f"{porcentagem:.3f}%", fill="black", font=("Arial", 10, "bold"))

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

def tamaho_pasta(entrada_origem, label_tamanho_contagem):
    origem = Path(entrada_origem)
    arquivos = list(origem.rglob("*"))

    tamanho_total = sum(f.stat().st_size for f in arquivos if f.is_file())

    label_tamanho_contagem.config(text=formatar_tamanho(tamanho_total))

def inciar_contagem(entrada_origem,
                    label_tamanho_contagem):
    t = threading.Thread(
        target=tamaho_pasta,
        args=(entrada_origem,
              label_tamanho_contagem),
        daemon=True
    )
    t.start()

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