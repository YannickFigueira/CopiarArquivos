import customtkinter as ctk
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QLabel, QHBoxLayout, \
    QFrame

import estilo
import tema
from barra_titulo_subjanela import BarraTituloSubjanela

class JanelaLogs(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.resize(300, 400)

        # Remove a borda/barra de título padrão do SO e define como Diálogo
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog
        )
        # 2. TORNA O FUNDO DO DIÁLOGO TRANSPARENTE (Remove as pontas brancas/escuras)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Garante que fique por cima da janela principal (Transient/Modal)
        if parent:
            self.setWindowModality(Qt.WindowModality.WindowModal)

        self.nome_janela = "logs"
        self.controles = {}

        # Guarda a referência da própria janela no dicionário de controles
        self.controles["janela_logs"] = self

        self._criar_layout()

    def _criar_layout(self):
        # 1. Layout Raiz da Janela (Margens ZERADAS para o container encostar nas bordas)
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # 2. Container Principal (QFrame)
        self.container = QFrame()
        self.container.setObjectName("ContainerPrincipal")
        layout_raiz.addWidget(self.container)

        # 3. Layout INTERNO do Container Principal
        layout_container = QVBoxLayout(self.container)
        layout_container.setContentsMargins(10, 10, 10, 10)
        layout_container.setSpacing(10)

        # --- A) Barra de título personalizada no topo (colada nas bordas) ---
        self.barra_titulo = BarraTituloSubjanela(self, titulo="Logs")
        layout_container.addWidget(self.barra_titulo)

        # --- B) Corpo do Conteúdo (com margens e espaçamentos internos) ---
        layout_corpo = QVBoxLayout()
        layout_corpo.setContentsMargins(
            estilo.ESPACO, estilo.ESPACO, estilo.ESPACO, estilo.ESPACO
        )
        layout_corpo.setSpacing(estilo.ESPACO)

        # --- Frame da Lista de Logs ---
        self.moldura_log_lista = QFrame()
        self.moldura_log_lista.setFrameShape(QFrame.Shape.StyledPanel)
        self.moldura_log_lista.setFixedHeight(300)
        self.moldura_log_lista.setFixedWidth(250)
        self.moldura_log_lista.setObjectName("FrmDescricao")

        # Layout interno da moldura
        layout_frame_logs = QVBoxLayout(self.moldura_log_lista)
        layout_frame_logs.setContentsMargins(10, 4, 10, 0)

        # Label simples para o conteúdo dos logs
        self.lbl_logs = QLabel("")
        self.lbl_logs.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.lbl_logs.setWordWrap(True)
        self.lbl_logs.setStyleSheet("border: none; color: #ffffff;")

        layout_frame_logs.addWidget(self.lbl_logs)
        self.controles["lbl_logs"] = self.lbl_logs

        # Adiciona a moldura de logs ao corpo
        layout_corpo.addWidget(self.moldura_log_lista)

        # --- Linha do ComboBox (Label + Seleção) ---
        layout_selecao = QHBoxLayout()
        layout_selecao.setSpacing(estilo.ESPACO)

        self.lbl_logs_backup = QLabel("Selecionar logs:")
        layout_selecao.addWidget(self.lbl_logs_backup)

        self.cmb_selecao = QComboBox()
        self.cmb_selecao.setEditable(False)
        layout_selecao.addWidget(self.cmb_selecao, stretch=1)
        self.controles["cmb_selecao"] = self.cmb_selecao

        layout_corpo.addLayout(layout_selecao)

        # --- Botão "Abrir log" ---
        self.btn_abrir_logs = QPushButton("Abrir log")
        self.btn_abrir_logs.setObjectName("BtnAcao")
        layout_corpo.addWidget(self.btn_abrir_logs)
        self.controles["btn_abrir_logs"] = self.btn_abrir_logs

        # Insere o corpo dentro do layout do container
        layout_container.addLayout(layout_corpo)

        # --- MONITORAMENTO E APLICAÇÃO DO TEMA ---
        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

        """
        self.janela_logs = ctk.CTkToplevel()
        self.janela_logs.title("Logs")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_logs.transient()

        self.nome_janela = "logs"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()
        """
    def _criar_layout_old(self):
        self.controles['janela_logs'] = self.janela_logs

        altura_linha = 10

        # Frame da lista de logs
        self.moldura_log_lista = ctk.CTkFrame(
            self.janela_logs,
            width=200,
            height=220,
            border_width=1,
            border_color="gray"
        )
        self.moldura_log_lista.grid(
            row=0,
            rowspan=altura_linha,
            columnspan=2,
            padx=estilo.ESPACO,
            pady=estilo.ESPACO,
            sticky="ew"
        )
        self.moldura_log_lista.grid_propagate(False)
        self.moldura_log_lista.pack_propagate(False)

        # Label simples fixo para os 10 itens
        self.lbl_logs = ctk.CTkLabel(
            self.moldura_log_lista,
            text="",
            justify="left",
            font=estilo.FONTE_VAZIA
        )
        self.lbl_logs.pack(anchor="w", padx=10, pady=(4, 0))
        self.controles['lbl_logs'] = self.lbl_logs

        altura_linha += 1
        self.lbl_logs_backup = ctk.CTkLabel(self.janela_logs, text="Selecionar logs: ", font=estilo.FONTE_VAZIA)
        self.lbl_logs_backup.grid(row=altura_linha, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.cmb_selecao = ctk.CTkComboBox(self.janela_logs, font=estilo.FONTE_VAZIA, state="readonly",)
        self.cmb_selecao.grid(column=1, row=altura_linha, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.controles['cmb_selecao'] = self.cmb_selecao
        altura_linha += 1

        self.btn_abrir_logs = ctk.CTkButton(self.janela_logs, text="Abrir log")
        self.btn_abrir_logs.grid(row=altura_linha, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.controles['btn_abrir_logs'] = self.btn_abrir_logs
