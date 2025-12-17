import tkinter as tk
from tkinter import ttk

def on_button_click():
    print("Texto:", entrada_origem.get())
    print("Checkbox marcada:", checkbox_var.get())
    print("Área de texto:\n", text_area.get("1.0", tk.END).strip())

root = tk.Tk()
root.title("Exemplo de Layout")

# Frame para alinhar label e campo de texto lado a lado
top_frame = ttk.Frame(root, padding=10)
top_frame.grid(row=0, column=0, sticky="w")

label_origem = ttk.Label(top_frame, text="Origem:")
label_origem.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

entrada_origem = ttk.Entry(top_frame, width=30)
entrada_origem.grid(row=0, column=1, pady=(0, 8), sticky="w")

label_destino = ttk.Label(top_frame, text="Destino:")
label_destino.grid(row=1, column=0, padx=(0, 8), pady=(0, 8), sticky="w")

entrada_destino = ttk.Entry(top_frame, width=30)
entrada_destino.grid(row=1, column=1, pady=(0, 8), sticky="w")

# Botão embaixo da área de texto
button_executar_copia = ttk.Button(root, text="Executar Cópia", width=24, command=on_button_click)
button_executar_copia.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="we")

# Botão embaixo da área de texto
button_cancelar = ttk.Button(root, text="Cancelar", width=24, command=on_button_click)
button_cancelar.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="we")

# Checkbox embaixo
checkbox_var = tk.BooleanVar()
checkbox = ttk.Checkbutton(root, text="Aceito os termos", variable=checkbox_var)
checkbox.grid(row=3, column=0, padx=10, pady=(0, 8), sticky="w")

# Área de texto embaixo da checkbox
text_area = tk.Text(root, width=50, height=8)
text_area.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="we")

# Tornar a coluna expansível para a área de texto crescer horizontalmente
root.columnconfigure(0, weight=1)

root.mainloop()
