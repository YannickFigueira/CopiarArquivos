import customtkinter as ctk
import tkinter as tk

import estilo

## variaveis da janela
padding_frame = 2
padding_controls = 5
largura_texto_entry = 350
largura_texto = 48

class CopiarArquivos:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.resizable(False, False)

        self.nome_janela = "copiararquivos"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Controles ---
        self.controles['janela_principal'] = self.janela_principal

        # CTkCTkFrame para alinhar label e campo de texto lado a lado
        self.top_frame = ctk.CTkFrame(self.janela_principal)
        self.top_frame.pack(fill="x", padx=padding_frame, pady=padding_frame)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.top_button_frame = ctk.CTkFrame(self.janela_principal)
        self.top_button_frame.pack(fill="x")
        # Configura as colunas 0, 1 e 2 para expandirem igualmente (weight=1)
        self.top_button_frame.grid_columnconfigure(0, weight=1)
        self.top_button_frame.grid_columnconfigure(1, weight=1)
        self.top_button_frame.grid_columnconfigure(2, weight=1)

        self.middle_frame = ctk.CTkFrame(self.janela_principal)
        self.middle_frame.pack(fill="x")

        self.checkbox_frame = ctk.CTkFrame(self.janela_principal)
        self.checkbox_frame.pack(fill="x")
        # Expandir colunas igualmente
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        self.checkbox_frame.grid_columnconfigure(1, weight=1)

        self.bottom_frame = ctk.CTkFrame(self.janela_principal)
        self.bottom_frame.pack(fill="x")

        ### Fim dos frames ###
        botao_sel = 30

        self.label_origem = ctk.CTkLabel(self.top_frame, text="Origem:")
        self.label_origem.grid(row=0, column=0, padx=padding_controls, pady=padding_controls)

        self.entrada_origem = ctk.CTkEntry(self.top_frame, width=largura_texto_entry)
        self.entrada_origem.grid(row=0, column=1, padx=padding_controls, pady=padding_controls, sticky="ew")
        self.controles['entrada_origem'] = self.entrada_origem

        self.button_selecionar_origem = ctk.CTkButton(self.top_frame, text="...", width=botao_sel)
        self.button_selecionar_origem.grid(row=0, column=2, padx=padding_controls, pady=padding_controls, sticky="ew")
        self.controles['button_selecionar_origem'] = self.button_selecionar_origem

        self.label_destino = ctk.CTkLabel(self.top_frame, text="Destino:")
        self.label_destino.grid(row=1, column=0, padx=padding_controls, pady=padding_controls)

        self.entrada_destino = ctk.CTkEntry(self.top_frame, width=largura_texto_entry)
        self.entrada_destino.grid(row=1, column=1, padx=padding_controls, pady=padding_controls, sticky="ew")
        self.controles['entrada_destino'] = self.entrada_destino

        self.button_selecionar_destino = ctk.CTkButton(self.top_frame, text="...", width=botao_sel)
        self.button_selecionar_destino.grid(row=1, column=2, padx=padding_controls, pady=padding_controls, sticky="ew")
        self.controles['button_selecionar_destino'] = self.button_selecionar_destino

        self.button_executar_copia = ctk.CTkButton(self.top_button_frame, text="Executar Cópia")
        self.button_executar_copia.grid(row=0, column=0, padx=padding_controls, pady=padding_controls, sticky="we")
        self.controles['button_executar_copia'] = self.button_executar_copia

        self.button_cancelar = ctk.CTkButton(self.top_button_frame, text="Cancelar")
        self.button_cancelar.grid(row=0, column=1, padx=padding_controls, pady=padding_controls, sticky="we")
        self.button_cancelar.configure(state=tk.DISABLED)
        self.controles['button_cancelar'] = self.button_cancelar

        self.button_pausar = ctk.CTkButton(self.top_button_frame, text="Pausar")
        self.button_pausar.grid(row=0, column=2, padx=padding_controls, pady=padding_controls, sticky="we")
        self.button_pausar.configure(state=tk.DISABLED)
        self.controles['button_pausar'] = self.button_pausar

        self.label_tamanho = ctk.CTkLabel(self.middle_frame, text="Tamanho:")
        self.label_tamanho.grid(row=0, column=0, padx=padding_controls, pady=padding_controls, sticky="w")

        self.label_tamanho_contagem = ctk.CTkLabel(self.middle_frame, text=8 * "--")
        self.label_tamanho_contagem.grid(row=0, column=1, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['label_tamanho_contagem'] = self.label_tamanho_contagem
        # Checkbox em baixo
        self.var_chk_origem = tk.BooleanVar(value=True)
        self.chk_nome_origem = ctk.CTkCheckBox(
            self.checkbox_frame,
            text="Usar nome de origem",
            variable=self.var_chk_origem,
            onvalue=True,
            offvalue=False
        )
        self.chk_nome_origem.grid(row=0, column=0, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['var_chk_origem'] = self.var_chk_origem
        self.controles['chk_nome_origem'] = self.chk_nome_origem

        self.var_chk_mover = tk.BooleanVar(value=False)
        self.chk_mover = ctk.CTkCheckBox(
            self.checkbox_frame,
            text="Mover arquivos",
            variable=self.var_chk_mover,
            onvalue=True,
            offvalue=False
        )
        self.chk_mover.grid(row=1, column=0, padx=padding_controls, pady=padding_controls, sticky="w")
        # CORREÇÃO: No CustomTkinter usa-se configure em vez de config
        self.chk_mover.configure(state="disabled")
        self.controles['var_chk_mover'] = self.var_chk_mover
        self.controles['chk_mover'] = self.chk_mover

        self.var_chk_encerrar = tk.BooleanVar(value=False)
        self.chk_encerrar = ctk.CTkCheckBox(
            self.checkbox_frame,
            text="Encerrar programa",
            variable=self.var_chk_encerrar,
            onvalue=True,
            offvalue=False
        )
        self.chk_encerrar.grid(row=0, column=2, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['var_chk_encerrar'] = self.var_chk_encerrar
        self.controles['chk_encerrar'] = self.chk_encerrar

        self.var_chk_desligar = tk.BooleanVar(value=False)
        self.chk_desligar = ctk.CTkCheckBox(
            self.checkbox_frame,
            text="Desligar sistema",
            variable=self.var_chk_desligar,
            onvalue=True,
            offvalue=False
        )
        self.chk_desligar.grid(row=1, column=2, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['var_chk_desligar'] = self.var_chk_desligar
        self.controles['chk_desligar'] = self.chk_desligar

        # Área de texto em baixo da checkbox
        self.text_area = tk.Text(self.bottom_frame, width=largura_texto, height=8)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=padding_controls, pady=padding_controls, sticky="we")
        self.controles['text_area'] = self.text_area

        self.label_arquivo_atual = ctk.CTkLabel(self.bottom_frame, text="Progresso total:")
        self.label_arquivo_atual.grid(row=1, column=0, padx=padding_controls, pady=padding_controls, sticky="w")

        self.progress_canvas = tk.Canvas(self.bottom_frame, height=25, bg="white", highlightthickness=1,
                                    highlightbackground="black")
        self.progress_canvas.grid(row=1, column=1, columnspan=3, padx=padding_controls, pady=padding_controls, sticky="e")
        self.controles['progress_canvas'] = self.progress_canvas

        self.label_copiado = ctk.CTkLabel(self.bottom_frame, text="Copiado:")
        self.label_copiado.grid(row=2, column=0, padx=padding_controls, pady=padding_controls, sticky="w")

        self.label_copiado_contagem = ctk.CTkLabel(self.bottom_frame, text=8 * "--")
        self.label_copiado_contagem.grid(row=2, column=1, padx=padding_controls, pady=padding_controls, sticky="w")
        self.controles['label_copiado_contagem'] = self.label_copiado_contagem

        self.label_tempo = ctk.CTkLabel(self.bottom_frame, text="Tempo decorrido:")
        self.label_tempo.grid(row=2, column=2, padx=padding_controls, pady=padding_controls, sticky="e")

        self.label_tempo_decorrido = ctk.CTkLabel(self.bottom_frame, text="--:--:--.----")
        self.label_tempo_decorrido.grid(row=2, column=3, padx=padding_controls, pady=padding_controls, sticky="e")
        self.controles['label_tempo_decorrido'] = self.label_tempo_decorrido

    def _criar_barra_menu(self):
        self.barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)

        # Menu Arquivo
        self.menu_arquivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.controles['menu_arquivo'] = self.menu_arquivo

        # Menu Ajuda
        self.menu_ajuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)
        self.controles['menu_ajuda'] = self.menu_ajuda
