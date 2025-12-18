import argparse
import tkinter as tk
import metodos
import verificarversao
from tkinter import ttk

VERSION = "4.0.2"
repo = "CopiarArquivos"

parser = argparse.ArgumentParser(prog="copiararquivos")
parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
args = parser.parse_args()

root = tk.Tk()
root.title(f"Cópia de arquivos {VERSION}")
root.resizable(False, False)

# Frame para alinhar label e campo de texto lado a lado
top_frame = ttk.Frame(root, padding=10)
top_frame.grid(row=0, column=0, columnspan=2, sticky="w")

midle_frame = ttk.Frame(root, padding=10)
midle_frame.grid(row=2, column=0, columnspan=2, sticky="w")

bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.grid(row=6, column=0, columnspan=2, sticky="w")

label_origem = ttk.Label(top_frame, text="Origem:")
label_origem.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

largura_entradas = 50
entrada_origem = ttk.Entry(top_frame, width=largura_entradas)
entrada_origem.grid(row=0, column=1, pady=(0, 8), sticky="w")

button_selecionar_origem = ttk.Button(top_frame, text="...", command=lambda: (entrada_origem.delete(0, "end"),
                                                                              entrada_origem.insert(0, metodos.selecionar_pasta())))
button_selecionar_origem.grid(row=0, column=2, padx=(10, 0), pady=(0, 8), sticky="we")

label_destino = ttk.Label(top_frame, text="Destino:")
label_destino.grid(row=1, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

entrada_destino = ttk.Entry(top_frame, width=largura_entradas)
entrada_destino.grid(row=1, column=1, pady=(0, 8), sticky="w")

button_selecionar_destino = ttk.Button(top_frame, text="...", command=lambda: (entrada_destino.delete(0, "end"),
                                                                              entrada_destino.insert(0, metodos.selecionar_pasta())))
button_selecionar_destino.grid(row=1, column=2, padx=(10, 0), pady=(0, 8), sticky="we")

largura = int(60 / 2)
# Botão em baixo da área de texto
button_executar_copia = ttk.Button(root, text="Executar Cópia", width=largura,
                                   command=lambda: (metodos.iniciar_copia(entrada_origem.get(),
                                                                             entrada_destino.get(),
                                                                             root,
                                                                             progress_canvas,
                                                                             entrada_origem,
                                                                             entrada_destino,
                                                                             button_executar_copia,
                                                                             text_area,
                                                                          label_copiado_contagem,
                                                                          label_tempo_decorrido,
                                                                          checkbox_origem.get(),
                                                                          checkbox_encerrar.get()),
                                                    metodos.iniciar_contagem(entrada_origem.get(),
                                                                            label_tamanho_contagem)))
button_executar_copia.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")

# Botão embaixo da área de texto
button_cancelar = ttk.Button(root, text="Cancelar", width=largura, command=lambda: metodos.parar_copia())
button_cancelar.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="we")

label_tamanho = ttk.Label(midle_frame, text="Tamanho:")
label_tamanho.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

label_tamanho_contagem = ttk.Label(midle_frame, text=8*"--")
label_tamanho_contagem.grid(row=0, column=1, padx=(0, 8), pady=(0, 8), sticky="w")

# Checkbox embaixo
checkbox_origem = tk.BooleanVar()
checkbox_origem.set(True)
checkbox = ttk.Checkbutton(root, text="Usar nome de origem", variable=checkbox_origem)
checkbox.grid(row=3, column=0, padx=10, pady=(0, 8), sticky="w")

checkbox_mover = tk.BooleanVar()
checkbox = ttk.Checkbutton(root, text="Mover arquivos", variable=checkbox_mover)
checkbox.grid(row=4, column=0, padx=10, pady=(0, 8), sticky="w")
checkbox.config(state="disabled")

checkbox_encerrar = tk.BooleanVar()
checkbox = ttk.Checkbutton(root, text="Encerrar programa", variable=checkbox_encerrar)
checkbox.grid(row=3, column=1, padx=10, pady=(0, 8), sticky="w")

checkbox_desligar = tk.BooleanVar()
checkbox = ttk.Checkbutton(root, text="Desligar sistema", variable=checkbox_desligar)
checkbox.grid(row=4, column=1, padx=10, pady=(0, 8), sticky="w")
checkbox.config(state="disabled")

# Área de texto embaixo da checkbox
text_area = tk.Text(root, width=50, height=8)
text_area.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="we")

label_arquivo_atual = ttk.Label(bottom_frame, text="Progresso total:")
label_arquivo_atual.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

# Barra de progresso
#progress_bar = ttk.Progressbar(bottom_frame, orient="horizontal", length=300, mode="determinate")
#progress_bar.grid(row=0, column=1, columnspan=3, padx=10, pady=(0, 8), sticky="w")
#progress_bar["value"] = 18

progress_canvas = tk.Canvas(bottom_frame, width=300, height=25, bg="white", highlightthickness=1, highlightbackground="black")
progress_canvas.grid(row=0, column=1, columnspan=3, padx=10, pady=(0, 8), sticky="w")

label_copiado = ttk.Label(bottom_frame, text="Copiado:")
label_copiado.grid(row=1, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

label_copiado_contagem = ttk.Label(bottom_frame, text=8*"--")
label_copiado_contagem.grid(row=1, column=1, padx=(0, 8), pady=(0, 8), sticky="w")

label_tempo = ttk.Label(bottom_frame, text="Tempo decorrido:")
label_tempo.grid(row=1, column=2, padx=(0, 8), pady=(0, 8), sticky="e")

label_tempo_decorrido = ttk.Label(bottom_frame, text="00:00:00.0000")
label_tempo_decorrido.grid(row=1, column=3, padx=(0, 8), pady=(0, 8), sticky="e")

# verificar versão
button_update = ttk.Button(root, text="Verificar atualização", command=lambda: verificarversao.consultar_lancamento(repo, VERSION))
button_update.grid(row=7, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="we")

# Tornar a coluna expansível para a área de texto crescer horizontalmente
root.columnconfigure(0, weight=1)

metodos.clipboard(root, entrada_origem)
metodos.clipboard(root, entrada_destino)

root.mainloop()
