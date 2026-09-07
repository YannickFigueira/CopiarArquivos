from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QMenu


class BarraTituloCustomizada(QFrame):
    def __init__(self, parent_window, titulo="Minha Aplicação"):
        super().__init__(parent_window)
        self.janela = parent_window
        self._pos_mouse_inicial = QPoint()

        self.setFixedHeight(45)
        self.setObjectName("BarraTitulo")

        layout_barra = QHBoxLayout(self)
        layout_barra.setContentsMargins(8, 0, 8, 0)

        # Botão Menu Hambúrguer
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setFixedSize(36, 32)
        self.btn_menu.setObjectName("BtnMenu")
        self.menu = QMenu(self)
        self.btn_menu.setMenu(self.menu)

        # Título da Janela (sem restrição excessiva de espaço)
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titulo.setObjectName("LblTitulo")

        # Botão Fechar
        self.btn_fechar = QPushButton("X")
        self.btn_fechar.setFixedSize(32, 32)
        self.btn_fechar.setObjectName("BtnFechar")
        self.btn_fechar.clicked.connect(self.janela.close)

        layout_barra.addWidget(self.btn_menu)
        layout_barra.addWidget(self.lbl_titulo, stretch=1)
        layout_barra.addWidget(self.btn_fechar)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pos_mouse_inicial = event.globalPosition().toPoint() - self.janela.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.janela.move(event.globalPosition().toPoint() - self._pos_mouse_inicial)

    def adicionar_submenu(self, titulo):
        return self.menu.addMenu(titulo)

    def adicionar_acao(self, texto, comando):
        return self.menu.addAction(texto, comando)