import platform
from pathlib import Path
from tkinter import messagebox

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFileDialog, QMessageBox

import verificarversao, estilo, copiar_arquivos
from janela_logs import JanelaLogs
from arquivo_log import ler_pasta_log, abrir_logs

# Detecta sistema operacional
system = platform.system()  # Retorna 'Linux', 'Windows', 'Darwin' (Mac)

# --- Variáveis globais ---
cancelar = False
pausar = False

class Funcoes:
    def __init__(self, view):
        self.view = view

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "copiararquivos":
                self._vincular_copiar_arquivos()
            elif view.nome_janela == "logs":
                self._vincular_logs()

    def _vincular_copiar_arquivos(self):
        # --- Controle do Menu ---
        self.view.controles['menu_arquivo'].addAction("Abrir logs", lambda: self.abrir_janela_logs())
        self.view.controles['menu_arquivo'].addAction("Sair",
                                                        lambda: self.view.close())

        self.view.controles['menu_ajuda'].addAction("Verificar atualização",
                               lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].addAction("Sobre",
                               lambda: self.visitar_site())

        # --- Controles da Janela Principal ---
        self.view.controles['btn_origem'].clicked.connect(lambda: self.selecionar_origem())
        self.view.controles['btn_destino'].clicked.connect(lambda: self.selecionar_destino())
        self.view.controles['btn_exec'].clicked.connect(lambda: self.executar_acao())
        """
        # --- Controles da Janela Principal ---
        self.view.controles['button_cancelar'].configure(command=lambda: copiar_arquivos.cancelar_copia(self.view))
        self.view.controles['button_pausar'].configure(command=lambda: copiar_arquivos.pausar_copia())
        """

    def _vincular_logs(self):
        # --- Inicialização da janela logs ---
        arquivos_log = ler_pasta_log()
        texto_log = "\n".join([f"{item}" for item in arquivos_log])

        # --- Controles da Janlea Logs ---
        self.view.controles['lbl_logs'].setText(texto_log)
        # 1. Atualiza as opções do ComboBox
        combo = self.view.controles['cmb_selecao']
        combo.clear()
        combo.addItems(arquivos_log)

        # 2. Define o valor selecionado usando o funcao .set()
        if arquivos_log:
            self.view.controles['cmb_selecao'].setCurrentIndex(0)
        self.view.controles['btn_abrir_logs'].clicked.connect(lambda: abrir_logs(self.view))
        #self.view.controles['btn_abrir_logs'].configure(command=lambda: abrir_logs(self.view))

    # --- Inicialização das janelas ---
    def abrir_janela_logs(self):
        # Passamos self.view como parent para centralizar e manter por cima
        visual = JanelaLogs(parent=self.view)

        # Se precisar de uma classe de controle dedicada para os logs:
        logica = Funcoes(visual)

        # .exec() bloqueia a execução até que o QDialog seja fechado
        visual.exec()

    # --- Comando dos Controles ---
    def selecionar_origem(self):
        self.view.controles['entrada_origem'].clear()
        self.view.controles['entrada_origem'].setText(self.selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['entrada_destino'].clear()
        self.view.controles['entrada_destino'].setText(self.selecionar_pasta())

    def selecionar_pasta(self=None):
        """Abre o seletor de pastas centralizado na janela do aplicativo."""
        pasta = QFileDialog.getExistingDirectory(
            parent=self.view,
            caption="Selecione uma pasta",
            directory=""  # Caminho inicial opcional
        )
        return pasta  # Retorna a string do caminho ou "" se o usuário cancelar

    def visitar_site(self=None):
        pagina = "https://github.com/YannickFigueira"

        # Instancia a caixa de mensagem do PyQt6
        msg_box = QMessageBox(self.view)
        msg_box.setWindowTitle("Sobre")
        msg_box.setText(
            f"<b>{estilo.NOME_PROGRAMA} {estilo.VERSION}</b><br>"
            f"Desenvolvedor: YannickFigueira<br>"
            f"chronostimeinchain@gmail.com<br><br>"
            f"Deseja visitar a página?"
        )
        msg_box.setIcon(QMessageBox.Icon.Information)

        # Configura os botões em português
        btn_sim = msg_box.addButton("Sim", QMessageBox.ButtonRole.YesRole)
        btn_nao = msg_box.addButton("Não", QMessageBox.ButtonRole.NoRole)

        msg_box.setDefaultButton(btn_sim)
        msg_box.exec()

        # Verifica qual botão foi clicado
        if msg_box.clickedButton() == btn_sim:
            # Abre a URL (usando QDesktopServices ou webbrowser.open)
            QDesktopServices.openUrl(QUrl(pagina))

    # --- FUNCIONALIDADES ---
    def executar_acao(self):
        texto_origem = self.view.controles['entrada_origem'].text().strip().replace("\\", "/")
        destino = self.view.controles['entrada_destino'].text().strip().replace("\\", "/")
        verificar_destino = destino.split("/")

        verificar = ""
        if system == 'Windows':
            verificar = f"{verificar_destino[0]}"
        elif system == 'Linux':
            verificar = f"/{verificar_destino[0]}"

        if not texto_origem == "":
            if Path(texto_origem).is_dir():
                if not destino == "":
                    if Path(verificar).is_dir():
                        self.view.controles['btn_cancel'].setEnabled(True)
                        self.view.controles['btn_pause'].setEnabled(True)
                        origem_pasta = [texto_origem]
                        destino_pasta = [destino]
                        copiar_arquivos.iniciar_copiar_arquivos(self.view, origem_pasta, destino_pasta)
                    else:
                        messagebox.showwarning("Aviso", "Selecionar pasta de destino válida")
                else:
                    messagebox.showwarning("Aviso", "Selecione a pasta de destino, ou cole o caminho")
            else:
                messagebox.showwarning("Aviso", "Pasta não existe, verifique")
        else:
            messagebox.showwarning("Aviso", "Selecionar a pasta de origem, ou colar o caminho")

    def atualizar_barra(self, valor, total):
        if total <= 0:
            return
        porcentagem = (valor / total) * 100
        pbar = self.view.controles['progress_bar']
        pbar.setFormat(f"{porcentagem:.3f}%")
        pbar.setValue(int(porcentagem))

    def exibir_mensagem(self, tipo, titulo, mensagem):
        # Substitui os messageboxes do Tkinter pelos nativos do PyQt6
        if tipo == "warning":
            QMessageBox.warning(self.view, titulo, mensagem)
        elif tipo == "critical":
            QMessageBox.critical(self.view, titulo, mensagem)
        else:
            QMessageBox.information(self.view, titulo, mensagem)