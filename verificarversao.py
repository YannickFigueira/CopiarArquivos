from tkinter import messagebox

import requests

# Substitua pelo seu repositório
def consultar_lancamento(repo, version):
    owner = "YannickFigueira"
    #repo = "CopiarArquivos"

    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    response = requests.get(url)
    if response.status_code == 200:
        release = response.json()
        if not release["tag_name"] == version:
            messagebox.showinfo("Lancamento", f"Nova versão\n{release['name']}")
            #print("Última versão:", release["tag_name"])
            #print("Nome:", release["name"])
            #print("Publicado em:", release["published_at"])
        else:
            messagebox.showinfo("Lancamento", "Já está usando a versão mais recente")
    else:
        messagebox.showwarning("Erro ao consultar:", str(response.status_code))
