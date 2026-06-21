import argparse, platform, subprocess, os
import tkinter as tk
from pathlib import Path

import metodos
import verificarversao
from tkinter import ttk, messagebox

VERSION = "4.1.10"
repo = "CopiarArquivos"
nome_programa = "Cópia de arquivos"

parser = argparse.ArgumentParser(prog="copiararquivos")
parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
args = parser.parse_args()

root = tk.Tk()
root.title(f"{nome_programa} {VERSION}")
root.resizable(False, False)

# Criar barra de menu
barra_menu = tk.Menu(root)
root.config(menu=barra_menu)

def visitar_site():
    pagina = f"https://github.com/YannickFigueira"
    resposta = messagebox.askyesno("Sobre", f"{nome_programa} v{VERSION}\n"
                                 f"Deseja visitar a página\n"
                                 f"Desenvolvedor YannickFigueira\n"
                                 f"chronostimeinchain@gmail.com")
    if resposta:
        verificarversao.webbrowser.open(pagina)

def abrir_logs():
    home_dir = os.path.expanduser('~')
    if platform.system() == "Windows":
        arquivo = "C:\\temp\\copiararquivos.log"
        subprocess.run(["notepad", arquivo])
    elif platform.system() == "Linux":
        arquivo = f"{home_dir}/log/copiararquivos.log"
        subprocess.run(["xdg-open", arquivo])  # ou "gedit"
    else:
        print("Sistema não suportado")

# Menu Arquivo
menu_arquivo = tk.Menu(barra_menu, tearoff=0)
menu_arquivo.add_command(label="Abrir log de ERRO", command=lambda: abrir_logs())
barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

# Menu Ajuda
menu_ajuda = tk.Menu(barra_menu, tearoff=0)
menu_ajuda.add_command(label="Verificar atualização", command=lambda: verificarversao.consultar_lancamento(repo, VERSION))
menu_ajuda.add_command(label="Sobre",
                       command=lambda: visitar_site())
barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

# Menu Sair
barra_menu.add_command(label="Sair", command=root.quit)

## variaveis da janela
espaco = 5

# Frame para alinhar label e campo de texto lado a lado
largura_frame = 400
top_frame = ttk.Frame(root, padding=0, width=largura_frame)
top_frame.pack(fill="x")
top_frame.grid_columnconfigure(2, weight=1)

top_button_frame = ttk.Frame(root, padding=0, width=largura_frame)
top_button_frame.pack(fill="x")
# Configura as colunas 0, 1 e 2 para expandirem igualmente (weight=1)
top_button_frame.grid_columnconfigure(0, weight=1)
top_button_frame.grid_columnconfigure(1, weight=1)
top_button_frame.grid_columnconfigure(2, weight=1)

middle_frame = ttk.Frame(root, padding=0, width=largura_frame)
middle_frame.pack(fill="x")

checkbox_frame = ttk.Frame(root, padding=0, width=largura_frame)
checkbox_frame.pack(fill="x")
# Expandir colunas igualmente
checkbox_frame.grid_columnconfigure(0, weight=1)
checkbox_frame.grid_columnconfigure(1, weight=1)

bottom_frame = ttk.Frame(root, padding=0, width=largura_frame)
bottom_frame.pack(fill="x")

### Fim dos frames ###

label_origem = ttk.Label(top_frame, text="Origem:")
label_origem.grid(row=0, column=0, padx=espaco, pady=espaco)

largura_entradas = 48
entrada_origem = ttk.Entry(top_frame, width=largura_entradas)
entrada_origem.grid(row=0, column=1, padx=espaco, pady=espaco)

sel = 7
button_selecionar_origem = ttk.Button(top_frame, text="...", command=lambda: (entrada_origem.delete(0, "end"),
                                                                              entrada_origem.insert(0, metodos.selecionar_pasta())))
button_selecionar_origem.grid(row=0, column=2, padx=espaco, pady=espaco, sticky="we")

label_destino = ttk.Label(top_frame, text="Destino:")
label_destino.grid(row=1, column=0, padx=espaco, pady=espaco)

entrada_destino = ttk.Entry(top_frame, width=largura_entradas)
entrada_destino.grid(row=1, column=1, padx=espaco, pady=espaco)

button_selecionar_destino = ttk.Button(top_frame, text="...", command=lambda: (entrada_destino.delete(0, "end"),
                                                                              entrada_destino.insert(0, metodos.selecionar_pasta())))
button_selecionar_destino.grid(row=1, column=2, padx=espaco, pady=espaco, sticky="we")

# Botão em baixo da área de texto
button_executar_copia = ttk.Button(top_button_frame, text="Executar Cópia", command=lambda: executar_acao())
button_executar_copia.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="we")

# Botão em baixo da área de texto
button_cancelar = ttk.Button(top_button_frame, text="Cancelar", command=lambda: metodos.parar_copia(button_cancelar))
button_cancelar.grid(row=0, column=1, padx=espaco, pady=espaco, sticky="we")
button_cancelar.config(state=tk.DISABLED)

button_pausar = ttk.Button(top_button_frame, text="Pausar", command=lambda: metodos.pausar_copia())
button_pausar.grid(row=0, column=2, padx=espaco, pady=espaco, sticky="we")
button_pausar.config(state=tk.DISABLED)

label_tamanho = ttk.Label(middle_frame, text="Tamanho:")
label_tamanho.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="w")

label_tamanho_contagem = ttk.Label(middle_frame, text=8 * "--")
label_tamanho_contagem.grid(row=0, column=1, padx=espaco, pady=espaco, sticky="w")

# Checkbox em baixo
checkbox_origem = tk.BooleanVar()
checkbox_origem.set(True)
checkbox = ttk.Checkbutton(checkbox_frame, text="Usar nome de origem", variable=checkbox_origem)
checkbox.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="w")

checkbox_mover = tk.BooleanVar()
checkbox = ttk.Checkbutton(checkbox_frame, text="Mover arquivos", variable=checkbox_mover)
checkbox.grid(row=1, column=0, padx=espaco, pady=espaco, sticky="w")
checkbox.config(state="disabled")

checkbox_encerrar = tk.BooleanVar()
checkbox = ttk.Checkbutton(checkbox_frame, text="Encerrar programa", variable=checkbox_encerrar)
checkbox.grid(row=0, column=2, padx=espaco, pady=espaco, sticky="w")

checkbox_desligar = tk.BooleanVar()
checkbox = ttk.Checkbutton(checkbox_frame, text="Desligar sistema", variable=checkbox_desligar)
checkbox.grid(row=1, column=2, padx=espaco, pady=espaco, sticky="w")

# Área de texto em baixo da checkbox
text_area = tk.Text(bottom_frame, width=largura_entradas, height=8)
text_area.grid(row=0, column=0, columnspan=4, padx=espaco, pady=espaco, sticky="we")

label_arquivo_atual = ttk.Label(bottom_frame, text="Progresso total:")
label_arquivo_atual.grid(row=1, column=0, padx=espaco, pady=espaco, sticky="w")

progress_canvas = tk.Canvas(bottom_frame, height=25, bg="white", highlightthickness=1, highlightbackground="black")
progress_canvas.grid(row=1, column=1, columnspan=3, padx=espaco, pady=espaco, sticky="e")

label_copiado = ttk.Label(bottom_frame, text="Copiado:")
label_copiado.grid(row=2, column=0, padx=espaco, pady=espaco, sticky="w")

label_copiado_contagem = ttk.Label(bottom_frame, text=8*"--")
label_copiado_contagem.grid(row=2, column=1, padx=espaco, pady=espaco, sticky="w")

label_tempo = ttk.Label(bottom_frame, text="Tempo decorrido:")
label_tempo.grid(row=2, column=2, padx=espaco, pady=espaco, sticky="e")

label_tempo_decorrido = ttk.Label(bottom_frame, text="--:--:--.----")
label_tempo_decorrido.grid(row=2, column=3, padx=espaco, pady=espaco, sticky="e")

### Comandos ###
def executar_acao():
    widgets = [entrada_origem, entrada_destino, button_selecionar_origem, button_selecionar_destino, button_executar_copia]

    origem = Path(entrada_origem.get().replace("\\", "/"))
    destino = entrada_destino.get().replace("\\", "/")
    verificar_destino = destino.split("/")

    if not entrada_origem.get() == "":
        if origem.is_dir():
            if not entrada_destino.get() == "":
                if Path(f"/{verificar_destino[0]}").is_dir():
                    button_cancelar.config(state="normal")
                    button_pausar.config(state="normal")
                    metodos.iniciar_copia(entrada_origem.get().replace("\\", "/"),
                                          entrada_destino.get().replace("\\", "/"),
                                          root,
                                          progress_canvas,
                                          widgets,
                                          button_pausar,
                                          text_area,
                                          label_copiado_contagem,
                                          label_tempo_decorrido,
                                          checkbox_origem.get(),
                                          checkbox_encerrar.get(),
                                          checkbox_desligar.get()),
                    metodos.iniciar_contagem(entrada_origem.get().replace("\\", "/"),
                                             label_tamanho_contagem)
                else:
                    messagebox.showwarning("Aviso", "Selecionar pasta de destino válida")
                    entrada_destino.focus_set()
            else:
                messagebox.showwarning("Aviso", "Selecione a pasta de destino, ou cole o caminho")
                entrada_destino.focus_set()
        else:
            messagebox.showwarning("Aviso", "Pasta não existe, verifique")
            entrada_origem.focus_set()
    else:
        messagebox.showwarning("Aviso", "Selecionar a pasta de origem, ou colar o caminho")
        entrada_origem.focus_set()

### Fim dos comandos ###

metodos.clipboard(root, entrada_origem)
metodos.clipboard(root, entrada_destino)

root.mainloop()
