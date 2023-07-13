import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Diretório oculto para armazenar o arquivo
diretorio_oculto = os.path.join(os.path.expanduser("~"), ".sfps")

# Cria o diretório oculto se não existir
if not os.path.exists(diretorio_oculto):
    os.makedirs(diretorio_oculto)

# Caminho completo do arquivo de senhas
ARQUIVO_SENHAS = os.path.join(diretorio_oculto, "senhas.json")

# Dicionário para armazenar as senhas
senha_armazenada = {}

def cadastrar_senha():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    descricao = entry_descricao.get()

    if not usuario or not senha:
        messagebox.showwarning("Cadastro de Senha", "Por favor, preencha todos os campos obrigatórios!")
        return

    senha_armazenada[usuario] = {'senha': senha, 'descricao': descricao}
    messagebox.showinfo("Cadastro de Senha", "Senha cadastrada com sucesso!")
    entry_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    update_lista()
    salvar_senhas()

def update_lista():
    lista_usuarios.delete(*lista_usuarios.get_children())
    for usuario, dados in senha_armazenada.items():
        descricao = dados['descricao']
        lista_usuarios.insert("", tk.END, text=usuario, values=(descricao,))

def exibir_informacoes(event):
    item_selecionado = lista_usuarios.focus()
    if item_selecionado:
        usuario_selecionado = lista_usuarios.item(item_selecionado)['text']
        senha = senha_armazenada[usuario_selecionado]['senha']
        descricao = senha_armazenada[usuario_selecionado]['descricao']

        janela_info = tk.Toplevel()
        janela_info.title("Informações do Usuário")

        frame = ttk.Frame(janela_info, padding="10")
        frame.pack()

        label_usuario = ttk.Label(frame, text=f"Usuário: {usuario_selecionado}")
        label_usuario.pack()

        label_descricao = ttk.Label(frame, text=f"Descrição: {descricao}")
        label_descricao.pack()

        label_senha = ttk.Label(frame, text=f"Senha: {senha}")
        label_senha.pack()

        botao_deletar = ttk.Button(frame, text="Deletar Usuário", command=lambda: deletar_usuario(usuario_selecionado))
        botao_deletar.pack()

def deletar_usuario(usuario):
    if messagebox.askyesno("Confirmação de exclusão", f"Deseja excluir o usuário '{usuario}'?"):
        del senha_armazenada[usuario]
        salvar_senhas()
        update_lista()
        messagebox.showinfo("Exclusão de Usuário", f"Usuário '{usuario}' excluído com sucesso!")

def salvar_senhas():
    # Salva as senhas no arquivo
    with open(ARQUIVO_SENHAS, "w") as arquivo:
        json.dump(senha_armazenada, arquivo)

def carregar_senhas():
    try:
        # Carrega as senhas do arquivo
        with open(ARQUIVO_SENHAS, "r") as arquivo:
            senha_armazenada.update(json.load(arquivo))
    except FileNotFoundError:
        # Se o arquivo não existir, continua com o dicionário vazio
        pass

def criar_interface():
    global entry_usuario, entry_senha, entry_descricao, lista_usuarios

    # Carrega as senhas do arquivo
    carregar_senhas()

    # Cria a janela principal
    janela = tk.Tk()
    janela.title("SafePass")

    estilo = ttk.Style()
    estilo.theme_use("clam")

    frame_principal = ttk.Frame(janela, padding="20")
    frame_principal.pack()

    # Cria os rótulos e campos de entrada
    label_usuario = ttk.Label(frame_principal, text="Usuário:")
    label_usuario.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    entry_usuario = ttk.Entry(frame_principal)
    entry_usuario.grid(row=0, column=1, padx=5, pady=5)

    label_senha = ttk.Label(frame_principal, text="Senha:")
    label_senha.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

    entry_senha = ttk.Entry(frame_principal, show="*")
    entry_senha.grid(row=1, column=1, padx=5, pady=5)

    label_descricao = ttk.Label(frame_principal, text="Descrição:")
    label_descricao.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

    entry_descricao = ttk.Entry(frame_principal)
    entry_descricao.grid(row=2, column=1, padx=5, pady=5)

    # Cria o botão Cadastrar Senha
    botao_cadastrar = ttk.Button(frame_principal, text="Cadastrar", command=cadastrar_senha)
    botao_cadastrar.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

    # Cria a lista de usuários e senhas cadastrados
    lista_usuarios = ttk.Treeview(frame_principal, columns=("descricao",), show="headings")
    lista_usuarios.heading("#0", text="Usuário")
    lista_usuarios.column("#0", width=120)
    lista_usuarios.heading("descricao", text="Descrição")
    lista_usuarios.column("descricao", width=180)
    lista_usuarios.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    lista_usuarios.bind("<Double-Button-1>", exibir_informacoes)

    # Atualiza a lista inicialmente
    update_lista()

    janela.mainloop()

# Execução do programa
criar_interface()