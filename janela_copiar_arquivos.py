import tkinter as tk
from tkinter import ttk

PROGRAMA_TITLE = "Copiar Arquivos"
## variaveis da janela
padding_frame = 2
padding_controls = 5
largura_texto = 48

class CopiarArquivos:
    def __init__(self, janela_principal, repo, version):
        super().__init__()
        self.janela_principal = janela_principal
        self.janela_principal.title(f"{PROGRAMA_TITLE} {version}")
        self.janela_principal.resizable(False, False)

        self.nome_janela = "copiararquivos"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout(repo, version)
        self._criar_barra_menu()

    def _criar_layout(self, repo, version):
        # --- Variáveis ---
        self.controles['var_repo'] = tk.StringVar(value=repo)
        self.controles['var_version'] = tk.StringVar(value=version)
        self.controles['var_title'] = tk.StringVar(value=f"{PROGRAMA_TITLE}")

        # --- Controles ---
        self.controles['janela_principal'] = self.janela_principal

        # Frame para alinhar label e campo de texto lado a lado
        self.top_frame = ttk.Frame(self.janela_principal, padding=padding_frame)
        self.top_frame.pack(fill="x")
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.top_button_frame = ttk.Frame(self.janela_principal, padding=0)
        self.top_button_frame.pack(fill="x")
        # Configura as colunas 0, 1 e 2 para expandirem igualmente (weight=1)
        self.top_button_frame.grid_columnconfigure(0, weight=1)
        self.top_button_frame.grid_columnconfigure(1, weight=1)
        self.top_button_frame.grid_columnconfigure(2, weight=1)

        self.middle_frame = ttk.Frame(self.janela_principal, padding=0)
        self.middle_frame.pack(fill="x")

        self.checkbox_frame = ttk.Frame(self.janela_principal, padding=0)
        self.checkbox_frame.pack(fill="x")
        # Expandir colunas igualmente
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        self.checkbox_frame.grid_columnconfigure(1, weight=1)

        self.bottom_frame = ttk.Frame(self.janela_principal, padding=0)
        self.bottom_frame.pack(fill="x")

        ### Fim dos frames ###

        self.label_origem = ttk.Label(self.top_frame, text="Origem:")
        self.label_origem.grid(row=0, column=0, padx=padding_controls, pady=padding_controls)

        self.entrada_origem = ttk.Entry(self.top_frame, width=largura_texto)
        self.entrada_origem.grid(row=0, column=1, padx=padding_controls, pady=padding_controls)
        self.controles['entrada_origem'] = self.entrada_origem

        self.button_selecionar_origem = ttk.Button(self.top_frame, text="...")
        self.button_selecionar_origem.grid(row=0, column=2, padx=padding_controls, pady=padding_controls, sticky="we")
        self.controles['button_selecionar_origem'] = self.button_selecionar_origem

        self.label_destino = ttk.Label(self.top_frame, text="Destino:")
        self.label_destino.grid(row=1, column=0, padx=padding_controls, pady=padding_controls)

        self.entrada_destino = ttk.Entry(self.top_frame, width=largura_texto)
        self.entrada_destino.grid(row=1, column=1, padx=padding_controls, pady=padding_controls)
        self.controles['entrada_destino'] = self.entrada_destino

        self.button_selecionar_destino = ttk.Button(self.top_frame, text="...")
        self.button_selecionar_destino.grid(row=1, column=2, padx=padding_controls, pady=padding_controls, sticky="we")
        self.controles['button_selecionar_destino'] = self.button_selecionar_destino

        self.button_executar_copia = ttk.Button(self.top_button_frame, text="Executar Cópia")
        self.button_executar_copia.grid(row=0, column=0, padx=padding_controls, pady=padding_controls, sticky="we")
        self.controles['button_executar_copia'] = self.button_executar_copia

        self.button_cancelar = ttk.Button(self.top_button_frame, text="Cancelar")
        self.button_cancelar.grid(row=0, column=1, padx=padding_controls, pady=padding_controls, sticky="we")
        self.button_cancelar.config(state=tk.DISABLED)
        self.controles['button_cancelar'] = self.button_cancelar

        self.button_pausar = ttk.Button(self.top_button_frame, text="Pausar")
        self.button_pausar.grid(row=0, column=2, padx=padding_controls, pady=padding_controls, sticky="we")
        self.button_pausar.config(state=tk.DISABLED)
        self.controles['button_pausar'] = self.button_pausar

        self.label_tamanho = ttk.Label(self.middle_frame, text="Tamanho:")
        self.label_tamanho.grid(row=0, column=0, padx=padding_controls, pady=padding_controls, sticky="w")

        self.label_tamanho_contagem = ttk.Label(self.middle_frame, text=8 * "--")
        self.label_tamanho_contagem.grid(row=0, column=1, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['label_tamanho_contagem'] = self.label_tamanho_contagem

        # Checkbox em baixo
        self.checkbox_origem = tk.BooleanVar()
        self.checkbox_origem.set(True)
        self.checkbox = ttk.Checkbutton(self.checkbox_frame, text="Usar nome de origem", variable=self.checkbox_origem)
        self.checkbox.grid(row=0, column=0, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['checkbox_origem'] = self.checkbox_origem

        self.checkbox_mover = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self.checkbox_frame, text="Mover arquivos", variable=self.checkbox_mover)
        self.checkbox.grid(row=1, column=0, padx=padding_controls, pady=padding_controls, sticky="w")
        self.checkbox.config(state="disabled")

        self.checkbox_encerrar = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self.checkbox_frame, text="Encerrar programa", variable=self.checkbox_encerrar)
        self.checkbox.grid(row=0, column=2, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['checkbox_encerrar'] = self.checkbox_encerrar

        self.checkbox_desligar = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self.checkbox_frame, text="Desligar sistema", variable=self.checkbox_desligar)
        self.checkbox.grid(row=1, column=2, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['checkbox_desligar'] = self.checkbox_desligar

        # Área de texto em baixo da checkbox
        self.text_area = tk.Text(self.bottom_frame, width=largura_texto, height=8)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=padding_controls, pady=padding_controls, sticky="we")
        self.controles['text_area'] = self.text_area

        self.label_arquivo_atual = ttk.Label(self.bottom_frame, text="Progresso total:")
        self.label_arquivo_atual.grid(row=1, column=0, padx=padding_controls, pady=padding_controls, sticky="w")

        self.progress_canvas = tk.Canvas(self.bottom_frame, height=25, bg="white", highlightthickness=1,
                                    highlightbackground="black")
        self.progress_canvas.grid(row=1, column=1, columnspan=3, padx=padding_controls, pady=padding_controls, sticky="e")
        self.controles['progress_canvas'] = self.progress_canvas

        self.label_copiado = ttk.Label(self.bottom_frame, text="Copiado:")
        self.label_copiado.grid(row=2, column=0, padx=padding_controls, pady=padding_controls, sticky="w")

        self.label_copiado_contagem = ttk.Label(self.bottom_frame, text=8 * "--")
        self.label_copiado_contagem.grid(row=2, column=1, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['label_copiado_contagem'] = self.label_copiado_contagem

        self.label_tempo = ttk.Label(self.bottom_frame, text="Tempo decorrido:")
        self.label_tempo.grid(row=2, column=2, padx=padding_controls, pady=padding_controls, sticky="e")

        self.label_tempo_decorrido = ttk.Label(self.bottom_frame, text="--:--:--.----")
        self.label_tempo_decorrido.grid(row=2, column=3, padx=padding_controls, pady=padding_controls, sticky="e")
        self.controles['label_tempo_decorrido'] = self.label_tempo_decorrido

    def _criar_barra_menu(self):
        barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=barra_menu)

        # Menu Arquivo
        menu_arquivo = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)
        self.controles['menu_arquivo'] = menu_arquivo

        # Menu Ajuda
        menu_ajuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)
        self.controles['menu_ajuda'] = menu_ajuda
