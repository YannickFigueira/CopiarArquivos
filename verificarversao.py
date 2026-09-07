import requests
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QMessageBox


def consultar_lancamento(repo, version, janela_parent=None):
    owner = "YannickFigueira"
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    pagina = f"https://github.com/{owner}/{repo}/releases"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            release = response.json()
            tag_atual = release.get("tag_name", "")
            nome_release = release.get("name", tag_atual)

            # Verifica se há uma versão diferente/mais recente
            if tag_atual != version:
                msg_box = QMessageBox(janela_parent)
                msg_box.setWindowTitle("Atualização Disponível")
                msg_box.setText(
                    f"<b>Nova versão disponível!</b><br><br>"
                    f"Versão atual: {version}<br>"
                    f"Nova versão: <b>{repo}</b> ({tag_atual})<br><br>"
                    f"Deseja abrir a página de download?"
                )
                msg_box.setIcon(QMessageBox.Icon.Information)

                btn_sim = msg_box.addButton("Sim", QMessageBox.ButtonRole.YesRole)
                btn_nao = msg_box.addButton("Não", QMessageBox.ButtonRole.NoRole)
                msg_box.setDefaultButton(btn_sim)

                msg_box.exec()

                if msg_box.clickedButton() == btn_sim:
                    QDesktopServices.openUrl(QUrl(pagina))
            else:
                QMessageBox.information(
                    janela_parent,
                    "Atualização",
                    "Você já está usando a versão mais recente."
                )
        else:
            QMessageBox.warning(
                janela_parent,
                "Verificação de Versão",
                "Não foi possível localizar o repositório ou não há lançamentos públicos."
            )

    except requests.exceptions.RequestException as e:
        QMessageBox.warning(
            janela_parent,
            "Erro de Conexão",
            f"Falha ao conectar com o servidor para verificar atualizações.\n\n{e}"
        )