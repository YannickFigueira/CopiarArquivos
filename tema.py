from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

def iniciar_arraste(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
        self._pos_mouse_inicial = event.globalPosition().toPoint() - self.frameGeometry().topLeft()


def arrastar_janela(self, event):
    if event.buttons() == Qt.MouseButton.LeftButton:
        self.move(event.globalPosition().toPoint() - self._pos_mouse_inicial)

def conectar_mudanca_tema(self):
    """Conecta o sinal do sistema para detectar quando o usuário muda entre Claro/Escuro."""
    app = QGuiApplication.instance()
    if app:
        app.styleHints().colorSchemeChanged.connect(atualizar_tema)

def atualizar_tema(self):
    """Identifica a preferência do sistema e aplica as cores correspondentes."""
    app = QGuiApplication.instance()
    # Verifica se o sistema está em Dark Mode
    modo_escuro = app.styleHints().colorScheme() == Qt.ColorScheme.Dark

    if modo_escuro:
        # Paleta Escura
        bg_container = "#242424"
        bg_card = "#2f2f2f"
        text_color = "#ffffff"
        text_subtle = "#cccccc"
        accent_color = "#1f538d"
        accent_hover = "#2a6ab3"
        border_menu = "#444444"
    else:
        # Paleta Clara
        bg_container = "#f3f3f3"
        bg_card = "#ffffff"
        text_color = "#1c1c1c"
        text_subtle = "#555555"
        accent_color = "#2b73c5"
        accent_hover = "#1f538d"
        border_menu = "#dddddd"

    self.setStyleSheet(f"""
            #ContainerPrincipal {{
                background-color: {bg_container};
                border-radius: 10px;
            }}
            #BarraTitulo {{
                background-color: {bg_card};
                border-radius: 6px;
            }}
            #LblTitulo {{
                color: {text_color};
                font-size: 14px;
                font-weight: bold;
                padding-left: 5px;
                padding-right: 5px;
            }}
            #BtnMenu {{
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 16px;
            }}
            /* Esconde a seta padrão que o PyQt adiciona ao QPushButton quando tem QMenu */
            #BtnMenu::menu-indicator {{
                image: none;
                width: 0px;
            }}
            #BtnFechar {{
                background-color: transparent;
                color: {text_subtle};
                border: none;
                font-size: 16px;
            }}
            #BtnFechar:hover {{
                background-color: #c0392b;
                color: white;
                border-radius: 4px;
            }}
            #BtnAcao {{
                background-color: {accent_color};
                color: white;
                border: none;
                padding: 7px;
                border-radius: 4px;
            }}
            #BtnAcao:hover {{ background-color: {accent_hover}; }}
            #MolduraTexto {{
                background-color: {bg_card};
                border-radius: 6px;
            }}
            QLineEdit {{
                background-color: {bg_card};
                color: {text_color};
                font-size: 12px;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px;
                min-width: 300px;
            }}
            QLineEdit:focus {{ border: 1px solid #1f538d; }}
            QComboBox {{
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px;
                font-size: 14px
            }}
            QProgressBar {{
                background-color: {bg_card};
                border-radius: 12px;
                text-align: center;
                color: {text_color};
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {accent_color};
                border-radius: 12px;
            }}
            QMenu {{
                background-color: {bg_card};
                color: {text_color};
                border: 1px solid {border_menu};
            }}
            QMenu::item:selected {{
                background-color: {accent_color};
                color: white;
            }}
        """)