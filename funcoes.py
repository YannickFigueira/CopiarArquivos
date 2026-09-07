import platform

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFileDialog, QMessageBox

import verificarversao, estilo
from copiar_arquivos import WorkerCopia
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
        self.view.controles['btn_exec'].clicked.connect(lambda: self.executar_copia())
        self.view.controles['btn_cancel'].clicked.connect(lambda: self.worker.cancelar_copia())
        self.view.controles['btn_pause'].clicked.connect(lambda: self.acionar_botao_pausa())
        """
        # --- Controles da Janela Principal ---
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
    def executar_copia(self):
        # 1. Instancia o worker
        self.worker = WorkerCopia(
            pastas_origem=[self.view.controles['entrada_origem'].text().strip()],
            pastas_destino=[self.view.controles['entrada_destino'].text().strip()],
            incluir_pasta_origem=self.view.controles['chk_nome_origem'].isChecked(),
            desligar=self.view.controles['chk_desligar'].isChecked(),
            encerrar=self.view.controles['chk_encerrar'].isChecked(),
        )

        # 2. Conecta os Sinais às funções da sua interface gráfica
        # Conecta o sinal de pausa para exibir a caixa de diálogo
        self.worker.sinal_pausado.connect(self.ao_pausar_copia)
        self.worker.sinal_progresso.connect(self.ao_atualizar_progresso)
        self.worker.sinal_status.connect(
            self.view.controles['lbl_descricao'].setText
        )
        self.worker.sinal_tempo.connect(
            self.view.controles['label_tempo_decorrido'].setText
        )
        self.worker.sinal_tamanho_calculado.connect(
            self.view.controles['label_tamanho_contagem'].setText
        )
        self.worker.sinal_alerta.connect(self.exibir_alerta)
        self.worker.sinal_concluido.connect(self.ao_concluir_copia)

        # 3. ZERA A INTERFACE ANTES DE INICIAR
        self.zerar_barra_progresso()
        self.view.controles['label_tempo_decorrido'].setText("00:00:00.0")
        self.view.controles['label_tamanho_contagem'].setText("Calculando...")
        self.view.controles['lbl_descricao'].setText("Iniciando...")

        # 4. Bloqueia os controles e inicia a Thread
        self.alterar_estado_controles(False)
        self.worker.start()

    def ao_atualizar_progresso(self, porcentagem, bytes_copiados):
        pbar = self.view.controles['progress_bar']

        # Se bytes copiados for 0 ou se estiver no início, zera visualmente a barra e o texto
        if bytes_copiados <= 0 or self.worker.tamanho_total <= 0:
            pbar.setValue(0)
            pbar.setFormat("0.000%")
            self.view.controles['label_copiado_contagem'].setText("0.00 B")
            return

        # Calcula a porcentagem precisa em float para exibir no texto da barra
        porcentagem_float = (bytes_copiados / self.worker.tamanho_total) * 100

        # Atualiza o formato do texto (3 casas decimais) e o valor inteiro da barra
        pbar.setFormat(f"{porcentagem_float:.3f}%")
        pbar.setValue(porcentagem)

        # Atualiza o contador de tamanho
        self.view.controles['label_copiado_contagem'].setText(
            WorkerCopia.formatar_tamanho(bytes_copiados)
        )

    def exibir_alerta(self, titulo, mensagem):
        QMessageBox.warning(self.view, titulo, mensagem)

    def acionar_botao_pausa(self):
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.pausar_copia()

    def ao_pausar_copia(self):
        # 1. Abre a caixa de diálogo bloqueante na interface gráfica
        QMessageBox.information(
            self.view,
            "Pausado",
            "A cópia foi pausada. Clique em OK para continuar.",
        )

        # 2. Quando o usuário clica em OK, desfaz a pausa no Worker para retomar o fluxo
        if hasattr(self, "worker") and self.worker:
            self.worker.alternar_pausa(False)

    def ao_concluir_copia(self, teve_erro, foi_cancelado):
        # 1. Habilita os controles da interface novamente
        self.alterar_estado_controles(True)

        # 2. Atualiza a mensagem final
        if foi_cancelado:
            self.view.controles['lbl_descricao'].setText('Cópia cancelada pelo usuário!')
        else:
            self.view.controles['lbl_descricao'].setText('Cópia concluída!')

        # 3. Exibe alerta de erro se houver
        if teve_erro:
            QMessageBox.warning(
                self.view,
                'Aviso',
                'Erros encontrados. Consulte o log em Arquivos -> Abrir log.',
            )

        # 4. Processa as ações pós-cópia (Lendo o estado ATUAL dos checkboxes)
        if not foi_cancelado:
            # A) Se a opção "Desligar" estiver marcada no término
            if self.view.controles['chk_desligar'].isChecked():
                WorkerCopia.desligar_computador()
                self.view.close()
                return

            # B) Se apenas "Encerrar" estiver marcado no término
            if self.view.controles['chk_encerrar'].isChecked():
                self.view.close()

    def alterar_estado_controles(self, estado):
        self.view.controles['entrada_origem'].setEnabled(estado)
        self.view.controles['entrada_destino'].setEnabled(estado)
        self.view.controles['btn_origem'].setEnabled(estado)
        self.view.controles['btn_destino'].setEnabled(estado)
        self.view.controles['btn_exec'].setEnabled(estado)
        self.view.controles['btn_cancel'].setEnabled(not estado)
        self.view.controles['btn_pause'].setEnabled(not estado)
        self.view.controles['chk_nome_origem'].setEnabled(estado)

    def zerar_barra_progresso(self):
        pbar = self.view.controles['progress_bar']
        pbar.setValue(0)
        pbar.setFormat("0.000%")
        self.view.controles['label_copiado_contagem'].setText("0.00 B")