from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout, \
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
        #self.controles["janela_logs"] = self

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
        self.moldura_log_lista.setFixedHeight(220)
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