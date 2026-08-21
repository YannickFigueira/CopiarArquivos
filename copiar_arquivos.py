import platform
import shutil
import subprocess
import threading
import time
from pathlib import Path
from tkinter import messagebox

from arquivo_log import registrar_log, gerar_arquivo_log, limpar_logs

# Detecta sistema operacional
system = platform.system()  # Retorna 'Linux', 'Windows', 'Darwin' (Mac)

# Evento para parar a thread do tempo
parar_tempo = threading.Event()
pausar_tempo = threading.Event()

# Variável
tarefas_executando = []
cancelar = False
pausar = False
liberar_total = False
erro_encontrado = False
total_arquivos = 0
tamanho_total = 0
soma = 0

def atualiza_tempo(inicio, label):
    """Thread que atualiza o label de tempo decorrido em paralelo."""
    while not parar_tempo.is_set():
        # Se estiver pausado, espera até ser liberado
        while pausar_tempo.is_set() and not parar_tempo.is_set():
            time.sleep(0.1)

        decorrido = time.time() - inicio
        horas, resto = divmod(decorrido, 3600)  # divide em horas
        minutos, segundos = divmod(resto, 60)  # divide o restante em minutos e segundos

        # agenda a atualização do label na thread principal do Tkinter
        def _set_label():
            label.config(text=f"{int(horas):02}:{int(minutos):02}:{segundos:04.1f}")

        label.after(0, _set_label)
        # frequência de atualização (ajuste conforme desejar)
        time.sleep(0.2)

def pausar_copia():
    global pausar
    pausar = True

def cancelar_copia():
    global cancelar
    resposta = messagebox.askyesno("Cancelar", "Quer realmente cancelar?")
    if resposta:
        cancelar = True

### Atualiza a barra de progresso ###
def atualizar_barra(valor, total, progress_canvas):
    progress_canvas.delete("all")
    largura = int((valor / total) * progress_canvas.winfo_width())
    # desenha a barra preenchida
    progress_canvas.create_rectangle(0, 0, largura, 25, fill="green")
    # escreve a porcentagem dentro da barra
    porcentagem = (valor / total) * 100
    x = progress_canvas.winfo_width() // 2
    progress_canvas.create_text(x, 12, text=f"{porcentagem:.3f}%", fill="black", font=("Arial", 10, "bold"))

def alterar_estado_controles(view, estado):
    view.controles['entrada_origem'].config(state=estado)
    view.controles['entrada_destino'].config(state=estado)
    view.controles['button_selecionar_origem'].config(state=estado)
    view.controles['button_selecionar_destino'].config(state=estado)
    view.controles['button_executar_copia'].config(state=estado)
    view.controles['chk_nome_origem'].config(state=estado)

# --- Inicio do procedimento
def iniciar_calculo_tamanho(view, pastas_origem, liberar):
    t = threading.Thread(
        target=tamanho_pasta,
        args=(view, pastas_origem, liberar),
        daemon=True
    )
    t.start()

def tamanho_pasta(view, pastas_origem, liberar):
    global total_arquivos, liberar_total, tamanho_total
    lbl_tamanho_exibir = view.controles['label_tamanho_contagem']
    lbl_tamanho_exibir.after(0, lambda: view.controles['label_tamanho_contagem'].config(text="Atualizando..."))
    tamanho_total = 0
    total_arquivos = 0

    for pasta in pastas_origem:
        ver_pasta = Path(pasta)

        # Iteramos pelos arquivos para contar e somar o tamanho simultaneamente
        for item in ver_pasta.rglob("*"):
            if item.is_file():
                total_arquivos += 1
                tamanho_total += item.stat(follow_symlinks=False).st_size

    lbl_tamanho_exibir.after(0, lambda: view.controles['label_tamanho_contagem'].config(text=formatar_tamanho(tamanho_total)))

    match liberar:
        case "execucao":
            liberar_total = True
        case _:
            return

def formatar_tamanho(tamanho):
    # Converte o valor para float com segurança
    try:
        tamanho = float(tamanho)
    except (ValueError, TypeError):
        return "0.00 B"

    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho < 1024.0:
            return f"{tamanho:.2f} {unidade}"
        tamanho /= 1024.0
    return f"{tamanho:.2f} PB"

# --- Desliga o equipamento
def desligar_computador():
    # Detecta o sistema operacional atual
    sistema = platform.system().lower()
    if "windows" in sistema:
        # /s = desligar, /t 0 = tempo de espera (0 segundos)
        subprocess.run("shutdown /s /t 0")
    elif "linux" in sistema:
        # h = halt/desligar, now = imediatamente
        # Nota: no Linux, pode ser necessário privilégios de root (sudo) dependendo da distro
        subprocess.run("shutdown -h now")
    else:
        print("Sistema operacional não suportado para esta ação.")

# --- Execução da cópia dos arquivos ---
def iniciar_copiar_arquivos(view, pastas_origem, pastas_destino):
    global soma
    soma = 0
    alterar_estado_controles(view, "disabled")
    iniciar_calculo_tamanho(view, pastas_origem, "execucao")
    iniciar_copia(pastas_origem, pastas_destino, view)

def iniciar_copia(pastas_origem, pastas_destino, view):
    t = threading.Thread(
        target=copiando_pastas,
        args=(pastas_origem, pastas_destino, view),
        daemon=True
    )
    t.start()

def copiando_pastas(pastas_origem, pastas_destino, view):
    global erro_encontrado
    erro_encontrado = False
    caminho_log = gerar_arquivo_log()
    registrar_log(caminho_log, "[INFO] Iniciando processo de cópia.")
    limpar_logs()
    view.controles['text_area'].delete("1.0", "end")  # apaga tudo

    parar_tempo.clear()
    inicio = time.time()  # marca o início da execução
    # inicia a thread do tempo (daemon para não travar saída)
    thread_tempo = threading.Thread(target=atualiza_tempo, args=(inicio, view.controles['label_tempo_decorrido']),
                                    daemon=True)
    thread_tempo.start()

    try:
        # zip alinha origem/destino; enumerate fornece o índice 'i'
        for i, (origem, destino_base) in enumerate(zip(pastas_origem, pastas_destino)):
            caminho_origem = Path(origem)
            base_destino = Path(destino_base)
            # / une caminhos automaticamente independente do S.O.
            if view.controles['var_chk_origem'].get():
                pasta_destino_final = base_destino / caminho_origem.name
            else:
                pasta_destino_final = base_destino

            copiando_arquivos(caminho_origem, pasta_destino_final, view, caminho_log)

    finally:
        # sinaliza para parar a thread de tempo e aguarda encerrar
        parar_tempo.set()
        # small join com timeout para evitar travar se a GUI encerrar
        thread_tempo.join(timeout=1.0)

    # Atualiza a interface ao finalizar todas as cópias
    view.controles['text_area'].delete("1.0", "end")  # apaga tudo
    if not cancelar:
        view.controles['text_area'].insert("1.0", "Concluído cópia!")
    else:
        view.controles['text_area'].insert("1.0", "Execução cancelada!")

    alterar_estado_controles(view, "normal")
    view.controles['button_cancelar'].config(state="disabled")
    view.controles['button_pausar'].config(state="disabled")

    if erro_encontrado:
        messagebox.showwarning("Erro", "Foi encontrado erros durante a cópia, vá em Arquivos -> Abrir log, para verificar")

    if view.controles['var_chk_desligar'].get():
        desligar_computador()
        view.controles['janela_principal'].destroy()

    if view.controles['var_chk_encerrar'].get():
        view.controles['janela_principal'].destroy()

    registrar_log(caminho_log, "[INFO] Processo finalizado.\n" + ("_" * 40))

def copiando_arquivos(origem, destino, view, caminho_log):
    global cancelar, pausar, tamanho_total, soma, erro_encontrado
    lbl_copiado_tamanho = view.controles['label_copiado_contagem']
    registrar_log(caminho_log, f"[INFO] Copiando pasta {origem}")
    for raiz, dirs, files in origem.walk(origem, on_error=lambda a: None):
        destino_final = destino / raiz.relative_to(origem)
        try:
            if raiz.is_dir():
                destino_final.mkdir(parents=True, exist_ok=True)

            if cancelar:
                view.controles['text_area'].delete(1.0, "end")  # apaga tudo
                view.controles['progress_canvas'].delete("all")
                cancelar = False
                break

            for f in files:
                if pausar:
                    messagebox.showinfo("Pausa", "Tarefa pausada")
                    pausar = False

                origem_arquivo = raiz / f
                try:
                    # follow_symlinks=False evita tentar resolver atalhos/symlinks quebrados
                    soma += origem_arquivo.stat(follow_symlinks=False).st_size
                    view.controles['text_area'].delete("1.0", "end")  # apaga tudo
                    view.controles['text_area'].insert("1.0",
                                                       f"{formatar_tamanho(origem_arquivo.stat().st_size)} -> {origem_arquivo}")

                    destino_arquivo = destino / raiz.relative_to(origem) / f

                    disco = ""
                    if system == 'Windows':
                        separar = view.controles['entrada_destino'].get().split("/")
                        disco = separar[0]
                    elif system == 'Linux':
                        disco = view.controles['entrada_destino'].get()

                    uso = shutil.disk_usage(Path(disco))
                    if origem_arquivo.stat().st_size > uso.free:
                        pausar_tempo.set()
                        messagebox.showwarning("Sem espaço em disco",
                                               f"Espaço necessário {formatar_tamanho(origem_arquivo.stat().st_size - uso.free)}")
                        pausar_tempo.clear()

                    if pausar:
                        pausar_tempo.set()
                        messagebox.showinfo("Pausado", "Clique em OK para continuar")
                        pausar_tempo.clear()
                        pausar = False

                    lbl_copiado_tamanho.after(0, lambda: view.controles['label_copiado_contagem'].config(text=formatar_tamanho(soma)))


                    copiar(origem_arquivo, destino_arquivo)
                except Exception as e:
                    erro_encontrado = True
                    registrar_log(caminho_log, f"[ERRO] Copiando -> {e} -> {origem_arquivo}")

                if liberar_total:
                    atualizar_barra(soma, tamanho_total, view.controles['progress_canvas'])

        except Exception as e:
            erro_encontrado = True
            registrar_log(caminho_log, f"[ERRO] Criando pasta -> {e}")

    atualizar_barra(1, 1, view.controles['progress_canvas'])

def copiar(origem_arquivo, destino_arquivo):
    # 1. Se o arquivo não existe no destino, copia direto
    if not destino_arquivo.is_file():
        shutil.copy2(origem_arquivo, destino_arquivo, follow_symlinks=False)

    # 2. Se ele existe, compara as datas de modificação
    elif origem_arquivo.stat().st_mtime > destino_arquivo.stat().st_mtime:
        shutil.copy2(origem_arquivo, destino_arquivo, follow_symlinks=False)
