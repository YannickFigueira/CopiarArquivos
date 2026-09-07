import platform
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

from arquivo_log import gerar_arquivo_log, limpar_logs, registrar_log

# Aumenta o buffer interno do Windows no shutil para 16MB
shutil._WINDOWS_INTERNAL_BUFFER_SIZE = 16 * 1024 * 1024

SYSTEM_OS = platform.system().lower()


class WorkerCopia(QThread):
    # --- SINAIS PARA A INTERFACE GRÁFICA ---
    sinal_progresso = pyqtSignal(int, float)  # (porcentagem_int, bytes_copiados)
    sinal_status = pyqtSignal(str)  # Descrição do arquivo atual / avisos
    sinal_tempo = pyqtSignal(str)  # Cronômetro "HH:MM:SS"
    sinal_tamanho_calculado = pyqtSignal(str)  # Tamanho total atualizado
    sinal_alerta = pyqtSignal(str, str)  # (Título, Mensagem) para dialogs
    sinal_concluido = pyqtSignal(bool, bool)  # (teve_erro, foi_cancelado)
    sinal_pausado = pyqtSignal()  # Dispara a caixa de diálogo de pausa

    def __init__(
        self,
        pastas_origem,
        pastas_destino,
        incluir_pasta_origem=True,
        desligar=False,
        encerrar=False,
    ):
        super().__init__()
        self.pastas_origem = pastas_origem
        self.pastas_destino = pastas_destino
        self.incluir_pasta_origem = incluir_pasta_origem
        self.desligar = desligar
        self.encerrar = encerrar

        # Estado de Controle
        self.cancelar_solicitado = False
        self.pausado = False
        self.erro_encontrado = False

        # Totalizadores compartilhados com Locks
        self.tamanho_total = 0
        self.total_arquivos = 0
        self.bytes_copiados = 0
        self.lock = threading.Lock()

        # Flags de sincronização de threads internas
        self.evento_parar_tempo = threading.Event()
        self.caminho_log = ""

    def run(self):
        """A cópia se inicia IMEDIATAMENTE. O cálculo roda em background."""
        self.caminho_log = gerar_arquivo_log()
        registrar_log(self.caminho_log, "[INFO] Iniciando processo de cópia.")
        limpar_logs()

        inicio_tempo = time.time()

        # 1. DISPARA A THREAD DE CRONÔMETRO (Paralela)
        self.evento_parar_tempo.clear()
        thread_cronometro = threading.Thread(
            target=self._thread_atualizar_tempo,
            args=(inicio_tempo,),
            daemon=True,
        )
        thread_cronometro.start()

        # 2. DISPARA A THREAD DE CÁLCULO DE TAMANHO (Paralela e Dinâmica)
        # Não bloqueia a cópia! Os arquivos começam a ser copiados no segundo 0.
        thread_calculo = threading.Thread(
            target=self._thread_calcular_tamanho_dinamico, daemon=True
        )
        thread_calculo.start()

        # 3. PROCESSO DE CÓPIA IMEDIATO
        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                for origem, destino_base in zip(
                    self.pastas_origem, self.pastas_destino
                ):
                    if self.cancelar_solicitado:
                        break

                    if origem.endswith(":"):
                        origem += "\\"
                    if destino_base.endswith(":"):
                        destino_base += "\\"

                    caminho_origem = Path(origem)
                    base_destino = Path(destino_base)

                    pasta_destino_final = (
                        base_destino / caminho_origem.name
                        if self.incluir_pasta_origem
                        else base_destino
                    )

                    self.processar_pasta(
                        caminho_origem, pasta_destino_final, executor
                    )
        finally:
            # Encerra o cronômetro
            self.evento_parar_tempo.set()
            thread_cronometro.join(timeout=1.0)

        # Finalização
        registrar_log(
            self.caminho_log, "[INFO] Processo finalizado.\n" + ("_" * 40)
        )
        self.sinal_concluido.emit(
            self.erro_encontrado, self.cancelar_solicitado
        )

    def _thread_calcular_tamanho_dinamico(self):
        """Varre os arquivos em segundo plano SEM travar a cópia.

        Garante tolerância a falhas em discos danificados.
        """
        for pasta in self.pastas_origem:
            if self.cancelar_solicitado:
                return

            ver_pasta = Path(pasta)
            if not ver_pasta.exists():
                continue

            try:
                for item in ver_pasta.rglob("*"):
                    if self.cancelar_solicitado:
                        return
                    try:
                        # is_file() sem argumentos; o controle de symlink é feito no stat()
                        if item.is_file():
                            tamanho = item.stat(follow_symlinks=False).st_size
                            with self.lock:
                                self.total_arquivos += 1
                                self.tamanho_total += tamanho

                            # Envia o progresso do cálculo para a UI em tempo real
                            self.sinal_tamanho_calculado.emit(
                                self.formatar_tamanho(self.tamanho_total)
                            )
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
            except (PermissionError, FileNotFoundError, OSError) as e:
                registrar_log(
                    self.caminho_log,
                    f"[AVISO] Erro lendo diretório {pasta}: {e}",
                )
                continue

    def _thread_atualizar_tempo(self, inicio):
        """Thread paralela para atualizar o tempo decorrido."""
        while not self.evento_parar_tempo.is_set():
            while self.pausado and not self.evento_parar_tempo.is_set():
                time.sleep(0.1)

            decorrido = time.time() - inicio
            horas, resto = divmod(decorrido, 3600)
            minutos, segundos = divmod(resto, 60)
            self.sinal_tempo.emit(
                f"{int(horas):02}:{int(minutos):02}:{segundos:04.1f}"
            )
            time.sleep(0.2)

    def processar_pasta(self, origem, destino, executor):
        registrar_log(self.caminho_log, f"[INFO] Copiando pasta {origem}")

        for raiz, dirs, files in origem.walk(origem, on_error=lambda a: None):
            if self.cancelar_solicitado:
                break

            pasta_final = destino / raiz.relative_to(origem)
            try:
                if raiz.is_dir():
                    pasta_final.mkdir(parents=True, exist_ok=True)

                for f in files:
                    if self.cancelar_solicitado:
                        break

                    # Pausa
                    while self.pausado and not self.cancelar_solicitado:
                        time.sleep(0.2)

                    origem_arquivo = raiz / f
                    destino_arquivo = pasta_final / f

                    # Checagem de espaço em disco
                    if not self.verificar_espaco_disponivel(
                        origem_arquivo, destino_arquivo
                    ):
                        continue

                    executor.submit(
                        self.copiar_arquivo_task,
                        origem_arquivo,
                        destino_arquivo,
                    )

            except Exception as e:
                self.erro_encontrado = True
                registrar_log(self.caminho_log, f"[ERRO] Criando pasta -> {e}")

    def copiar_arquivo_task(self, origem_arquivo, destino_arquivo):
        if self.cancelar_solicitado:
            return

        # Evita tentar copiar soquetes ou atalhos de sistema (como os do .cache/ibus)
        try:
            if origem_arquivo.is_symlink() or origem_arquivo.is_socket() or origem_arquivo.is_fifo():
                return
        except OSError:
            return  # Se não conseguir checar o tipo do arquivo, ignora com segurança

        while self.pausado and not self.cancelar_solicitado:
            time.sleep(0.2)

        try:
            if "windows" in SYSTEM_OS:
                str_origem = f"\\\\?\\{origem_arquivo.resolve()}"
                str_destino = f"\\\\?\\{destino_arquivo.resolve()}"
            else:
                str_origem = str(origem_arquivo)
                str_destino = str(destino_arquivo)

            path_destino = Path(str_destino)
            path_origem = Path(str_origem)

            tamanho_arq = origem_arquivo.stat(follow_symlinks=False).st_size

            # Notifica arquivo sendo copiado
            texto_status = (
                f"{self.formatar_tamanho(tamanho_arq)} -> {origem_arquivo.name}"
            )
            self.sinal_status.emit(texto_status)

            # Efetua a cópia se não existir ou se for mais recente
            if not path_destino.is_file() or (
                path_origem.stat().st_mtime > path_destino.stat().st_mtime
            ):
                shutil.copy2(str_origem, str_destino, follow_symlinks=False)

            # Atualização do progresso com proteção de Threads
            with self.lock:
                self.bytes_copiados += tamanho_arq
                copiados = self.bytes_copiados
                total = self.tamanho_total

            porcentagem = int((copiados / total) * 100) if total > 0 else 0
            self.sinal_progresso.emit(porcentagem, copiados)

        except shutil.SameFileError:
            pass
        except Exception as e:
            self.erro_encontrado = True
            registrar_log(
                self.caminho_log,
                f"[ERRO] Copiando -> {e} -> Origem {origem_arquivo}",
            )

    def verificar_espaco_disponivel(self, origem_arquivo, destino_arquivo):
        try:
            disco = (
                destino_arquivo.drive
                if "windows" in SYSTEM_OS
                else str(destino_arquivo)
            )
            uso = shutil.disk_usage(Path(disco if disco else "/"))
            tamanho_arq = origem_arquivo.stat().st_size

            if tamanho_arq > uso.free:
                self.pausado = True
                msg = f"Espaço necessário: {self.formatar_tamanho(tamanho_arq - uso.free)}"
                self.sinal_alerta.emit("Sem espaço em disco", msg)
                return False
            return True
        except Exception:
            return True

    def pausar_copia(self):
        self.pausado = True
        self.sinal_pausado.emit()

    def alternar_pausa(self, pausar: bool):
        self.pausado = pausar

    def cancelar_copia(self):
        self.cancelar_solicitado = True
        self.pausado = False

    @staticmethod
    def formatar_tamanho(tamanho):
        try:
            tamanho = float(tamanho)
        except (ValueError, TypeError):
            return "0.00 B"

        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if tamanho < 1024.0:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024.0
        return f"{tamanho:.2f} PB"

    @staticmethod
    def desligar_computador():
        if "windows" in SYSTEM_OS:
            subprocess.run("shutdown /s /t 0")
        elif "linux" in SYSTEM_OS:
            subprocess.run("shutdown -h now")