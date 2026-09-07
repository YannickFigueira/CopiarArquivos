from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, \
    QProgressBar

import estilo
import tema
from barra_titulo import BarraTituloCustomizada

## variaveis da janela
padding_frame = 2
padding_controls = 5
largura_texto_entry = 300
largura_texto = 55

class CopiarArquivos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._pos_mouse_inicial = QPoint()

        # Container Principal
        self.container = QFrame()
        self.container.setObjectName("ContainerPrincipal")
        self.setCentralWidget(self.container)

        self.nome_janela = "copiararquivos"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        layout_raiz = QVBoxLayout(self.container)
        layout_raiz.setContentsMargins(10, 10, 10, 10)
        layout_raiz.setSpacing(10)

        # 1. Instancia e adiciona a barra de título APENAS UMA VEZ
        titulo_app = f"{estilo.NOME_PROGRAMA} {estilo.VERSION}"
        self.barra_titulo = BarraTituloCustomizada(self, titulo=titulo_app)
        layout_raiz.addWidget(self.barra_titulo)

        # --- CONTEÚDO ---
        layout_conteudo = QHBoxLayout()
        layout_conteudo.setSpacing(10)

        # Painel Principal
        frame = QFrame()
        layout_controles = QVBoxLayout(frame)
        layout_controles.setContentsMargins(0, 0, 0, 0)
        layout_controles.setSpacing(8)

        # Definimos um tamanho fixo para as legendas ficarem perfeitamente alinhadas
        LARGURA_LEGENDA = 65

        # --- LINHA ORIGEM ---
        layout_origem = QHBoxLayout()
        lbl_origem = QLabel("Origem:")
        lbl_origem.setFixedWidth(LARGURA_LEGENDA)
        txt_origem = QLineEdit()
        txt_origem.setPlaceholderText("Digite/Cole a pasta de origem ou clique no botão ... ")
        btn_origem = QPushButton("...")
        btn_origem.setFixedWidth(36)
        btn_origem.setObjectName("BtnAcao")

        self.controles['entrada_origem'] = txt_origem
        self.controles['btn_origem'] = btn_origem

        #layout_origem.addWidget(lbl_origem)
        layout_origem.addWidget(txt_origem, stretch=1)
        layout_origem.addWidget(btn_origem)
        layout_controles.addLayout(layout_origem)

        # --- LINHA DESTINO ---
        layout_destino = QHBoxLayout()
        lbl_destino = QLabel("Destino:")
        lbl_destino.setFixedWidth(LARGURA_LEGENDA)
        txt_destino = QLineEdit()
        txt_destino.setPlaceholderText("Digite/Cole a pasta de destino ou clique no botão ... ")
        btn_destino = QPushButton("...")
        btn_destino.setFixedWidth(36)
        btn_destino.setObjectName("BtnAcao")

        self.controles['entrada_destino'] = txt_destino
        self.controles['btn_destino'] = btn_destino

        #layout_destino.addWidget(lbl_destino)
        layout_destino.addWidget(txt_destino, stretch=1)
        layout_destino.addWidget(btn_destino)
        layout_controles.addLayout(layout_destino)

        # --- LINHA BOTOES ---
        layout_exec = QHBoxLayout()
        btn_exec = QPushButton("Executar Cópia")
        btn_cancel = QPushButton("Cancelar")
        btn_pause = QPushButton("Pause")
        btn_exec.setObjectName("BtnAcao")
        btn_cancel.setObjectName("BtnAcao")
        btn_pause.setObjectName("BtnAcao")

        btn_cancel.setEnabled(False)
        btn_pause.setEnabled(False)

        self.controles['btn_exec'] = btn_exec
        self.controles['btn_cancel'] = btn_cancel
        self.controles['btn_pause'] = btn_pause

        layout_exec.addWidget(btn_exec, stretch=1)
        layout_exec.addWidget(btn_cancel, stretch=1)
        layout_exec.addWidget(btn_pause, stretch=1)
        layout_controles.addLayout(layout_exec)

        # --- LINHA LABEL TAMANHO TOTAL ---
        layout_tamanho = QHBoxLayout()
        layout_tamanho.setSpacing(5)  # Espaço pequeno entre os dois labels
        lbl_tamanho = QLabel("Tamanho total:")
        #lbl_tamanho.setFixedWidth(LARGURA_LEGENDA)
        lbl_total = QLabel(f"{10*"-"}")
        lbl_total.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.controles['label_tamanho_contagem'] = lbl_total
        layout_tamanho.addWidget(lbl_tamanho)
        layout_tamanho.addWidget(lbl_total)
        layout_tamanho.addStretch(1)
        layout_controles.addLayout(layout_tamanho)

        # --- LINHA DE CHECKBOX TOP ---
        # Criando a caixa de seleção com o texto explicativo
        layout_chk_top = QHBoxLayout()
        self.chk_nome_origem = QCheckBox("Usar nome da pasta")
        self.chk_nome_origem.setObjectName("ChkOpcao")  # Para estilização via QSS se necessário

        self.chk_encerrar = QCheckBox("Encerrar programa")
        self.chk_encerrar.setObjectName("ChkOpcao")

        # Adicionando ao layout
        layout_chk_top.addWidget(self.chk_nome_origem, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_chk_top.addStretch(1)
        layout_chk_top.addWidget(self.chk_encerrar, alignment=Qt.AlignmentFlag.AlignRight)
        layout_controles.addLayout(layout_chk_top)

        # Guardando no dicionário de controles para acesso no controlador
        self.chk_nome_origem.setChecked(True)
        self.controles['chk_nome_origem'] = self.chk_nome_origem
        self.controles['chk_encerrar'] = self.chk_encerrar

        # --- LINHA DE CHECKBOX FUNDO ---
        # Criando a caixa de seleção com o texto explicativo
        layout_chk_fundo = QHBoxLayout()
        self.chk_mover = QCheckBox("Mover")
        self.chk_mover.setObjectName("ChkOpcao")  # Para estilização via QSS se necessário
        self.chk_mover.setChecked(False)
        self.chk_mover.setEnabled(False)

        self.chk_desligar = QCheckBox("Desligar")
        self.chk_desligar.setObjectName("ChkOpcao")

        # Adicionando ao layout
        layout_chk_fundo.addWidget(self.chk_mover, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_chk_fundo.addStretch(1)
        layout_chk_fundo.addWidget(self.chk_desligar, alignment=Qt.AlignmentFlag.AlignRight)
        layout_controles.addLayout(layout_chk_fundo)

        # Guardando no dicionário de controles para acesso no controlador
        self.chk_mover.setChecked(True)
        self.controles['chk_mover'] = self.chk_mover
        self.controles['chk_desligar'] = self.chk_desligar

        # --- LINHA VISOR DOS ARQUIVOS COPIADOS ---
        # 1. Cria o QFrame container
        frame_info = QFrame()
        frame_info.setFrameShape(QFrame.Shape.StyledPanel)

        # 2. Cria o Layout do Frame
        layout_frame = QVBoxLayout(frame_info)
        layout_frame.setContentsMargins(10, 10, 10, 10)
        frame_info.setObjectName("FrmDescricao")

        # 3. Cria o QLabel com Quebra Automática de Linha

        lbl_descricao = QLabel()
        lbl_descricao.setObjectName("LblDescricao")

        # Ativa o 'wraplength' nativo do PyQt6
        lbl_descricao.setWordWrap(True)

        # Alinhamento do texto no topo e à esquerda
        lbl_descricao.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # (Opcional) Trava a altura do Label para comportar aproximadamente 5 linhas de texto
        # Para fonte de 13px, ~80px a 90px de altura comportam exatamente 5 linhas
        lbl_descricao.setFixedHeight(85)
        self.controles['lbl_descricao'] = lbl_descricao

        # 4. Adiciona o Label ao Layout do Frame
        layout_frame.addWidget(lbl_descricao)
        layout_controles.addWidget(frame_info)

        # --- LINHA PROGRESSO ---
        layout_prog = QHBoxLayout()
        pbar = QProgressBar()
        pbar.setValue(0)
        pbar.setFormat("0.000%")
        pbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_prog.addWidget(pbar, stretch=1)
        layout_controles.addLayout(layout_prog)

        self.controles['progress_bar'] = pbar

        # --- LINHA TEMPO E ARQUIVOS COPIADOS ---
        layout_arquivo_tempo = QHBoxLayout()
        lbl_copiado = QLabel("Copiado:")
        lbl_copiado_valor = QLabel(f"{10*"-"}")
        lbl_tempo = QLabel("Tempo decorrido:")
        lbl_tempo_valor = QLabel(f"{"--:--:--:-"}")

        self.controles['label_copiado_contagem'] = lbl_copiado_valor
        self.controles['label_tempo_decorrido'] = lbl_tempo_valor

        layout_arquivo_tempo.addWidget(lbl_copiado)
        layout_arquivo_tempo.addWidget(lbl_copiado_valor)
        layout_arquivo_tempo.addWidget(lbl_tempo)
        layout_arquivo_tempo.addWidget(lbl_tempo_valor)

        layout_controles.addLayout(layout_arquivo_tempo)

        # --- CARREGAMENTO DOS CONTROLES ---
        layout_conteudo.addWidget(frame)
        layout_raiz.addLayout(layout_conteudo)

        # Ajuste do tamanho mínimo da janela para evitar cortar o título
        self.setMinimumWidth(450)

        # --- MONITORAMENTO E APLICAÇÃO DO TEMA ---
        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

    def _criar_barra_menu(self):
        menu_arquivo = self.barra_titulo.adicionar_submenu("Arquivo")
        self.controles['menu_arquivo'] = menu_arquivo

        menu_ajuda = self.barra_titulo.adicionar_submenu("Ajuda")
        self.controles['menu_ajuda'] = menu_ajuda
