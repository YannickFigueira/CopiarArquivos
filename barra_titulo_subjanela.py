from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class BarraTituloSubjanela(QFrame):
    def __init__(self, parent_window, titulo="Subjanela"):
        super().__init__(parent_window)
        self.janela = parent_window
        self._pos_mouse_inicial = QPoint()

        self.setFixedHeight(40)  # Levemente menor para subjanelas
        self.setObjectName("BarraTituloSubjanela")

        layout_barra = QHBoxLayout(self)
        layout_barra.setContentsMargins(8, 0, 8, 0)

        # Título Centralizado
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titulo.setObjectName("LblTituloSubjanela")

        # Botão Fechar (Usa reject para fechar QDialog adequadamente)
        self.btn_fechar = QPushButton("✕")
        self.btn_fechar.setFixedSize(30, 30)
        self.btn_fechar.setObjectName("BtnFecharSubjanela")

        # Se for um QDialog, usa .reject() ou .close()
        if hasattr(self.janela, "reject"):
            self.btn_fechar.clicked.connect(self.janela.reject)
        else:
            self.btn_fechar.clicked.connect(self.janela.close)

        # Adiciona os elementos ao layout
        # (Um espaçador invisível na esquerda com a mesma largura do botão fechar
        # garante que o título fique 100% centralizado matematicamente)
        layout_barra.addSpacing(30)
        layout_barra.addWidget(self.lbl_titulo, stretch=1)
        layout_barra.addWidget(self.btn_fechar)

    # --- Lógica de Arraste da Subjanela ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pos_mouse_inicial = (
                event.globalPosition().toPoint()
                - self.janela.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.janela.move(
                event.globalPosition().toPoint() - self._pos_mouse_inicial
            )