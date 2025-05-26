import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from cone import conectar
import subprocess
import os
import sys

# Função para cadastrar um novo usuário no banco de dados
def cadastrar_usuario():
    nome = entry_nome.get().strip()
    senha = entry_senha.get().strip()
    email = entry_email.get().strip()

    if not nome or not senha or not email:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se o e-mail já está cadastrado
        cursor.execute("SELECT * FROM usuario WHERE user_email = %s", (email,))
        if cursor.fetchone():
            messagebox.showwarning("Atenção", "E-mail já cadastrado.")
            return

        # Insere novo usuário
        cursor.execute("INSERT INTO usuario (user_nome, user_email, user_senha) VALUES (%s, %s, %s)",
                       (nome, email, senha))
        conn.commit()

        # Busca o ID do novo usuário para enviar como argumento
        cursor.execute("SELECT user_id FROM usuario WHERE user_email = %s", (email,))
        user_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        limpar_campos()
        listar_usuarios()
        abrir_filme(user_id)
    except Exception as e:
        messagebox.showerror("Erro", "Erro ao cadastrar usuário:\n" + str(e))

# Função para fazer login do usuário
def entrar_usuario():
    email = entry_email.get().strip()
    senha = entry_senha.get().strip()

    if not email or not senha:
        messagebox.showwarning("Atenção", "Email e senha são obrigatórios para entrar.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, user_nome FROM usuario WHERE user_email = %s AND user_senha = %s", (email, senha))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            messagebox.showinfo("Bem-vindo", f"Olá, {usuario[1]}! Login efetuado com sucesso.")
            limpar_campos()
            abrir_filme(usuario[0])
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")
    except Exception as e:
        messagebox.showerror("Erro", "Erro ao tentar entrar:\n" + str(e))

# Função que abre a próxima interface (filmes e livros)
def abrir_filme(user_id):
    diretorio = os.path.abspath(os.path.dirname(__file__))
    caminho_filme = os.path.join(diretorio, "livros_e_filmes.py")
    subprocess.Popen(["python", caminho_filme, str(user_id)])
    janela.destroy()

# Limpa os campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Lista os usuários cadastrados no banco
def listar_usuarios():
    lista.delete(0, tk.END)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        for user in cursor.fetchall():
            lista.insert(tk.END, f"{user[0]} | {user[1]} | {user[2]}")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", "Erro ao listar usuários:\n" + str(e))

# Deleta o usuário selecionado na lista
def deletar_usuario():
    selecionado = lista.curselection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um usuário para deletar.")
        return

    item = lista.get(selecionado[0])
    user_id = item.split(" | ")[0]

    confirmar = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário ID {user_id}?")
    if not confirmar:
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM avaliacao WHERE usuario_id = %s", (user_id,))
        cursor.execute("DELETE FROM usuario WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Usuário deletado com sucesso.")
        listar_usuarios()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao deletar usuário:\n" + str(e))

# Interface Gráfica
janela = tk.Tk()
janela.title("Cadastro de Usuários")
janela.configure(bg="#fff6f0")
janela.geometry("800x700")
janela.resizable(False, False)

container = tk.Frame(janela, bg="#fff6f0")
container.pack(pady=40)

# Estilos de texto
estilo_label = {"font": ("Monotype Corsiva", 17), "fg": "#cc3366", "bg": "#fff6f0"}
estilo_entry = {"font": ("Palatino Linotype", 15), "width": 32, "bg": "#ffffff"}

# Carrega e redimensiona imagem
imagem = Image.open("C:\\Users\\marya\\Downloads\\teste\\imagens\\logo.png")
imagem = imagem.resize((200, 230), Image.Resampling.LANCZOS)
imagem_tk = ImageTk.PhotoImage(imagem)
janela.iconphoto(False, imagem_tk)

# Mostra imagem na interface
label_imagem = tk.Label(container, image=imagem_tk, bg="#fff6f0")
label_imagem.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

# Entradas de dados
# Nome
tk.Label(container, text="Nome:", **estilo_label).grid(row=0, column=1, sticky='e', padx=10, pady=10)
entry_nome = tk.Entry(container, **estilo_entry)
entry_nome.grid(row=0, column=2, padx=10, pady=10)

# Senha
tk.Label(container, text="Senha:", **estilo_label).grid(row=1, column=1, sticky='e', padx=10, pady=10)
entry_senha = tk.Entry(container, **estilo_entry, show="📚")
entry_senha.grid(row=1, column=2, padx=10, pady=10)

# Email
tk.Label(container, text="Email:", **estilo_label).grid(row=2, column=1, sticky='e', padx=10, pady=10)
entry_email = tk.Entry(container, **estilo_entry)
entry_email.grid(row=2, column=2, padx=10, pady=10)

# Botões de ação
botao_frame = tk.Frame(container, bg="#fff6f0")
botao_frame.grid(row=3, column=0, columnspan=3, pady=20)

btn_cadastrar = tk.Button(botao_frame, text="Cadastrar", command=cadastrar_usuario,
                         bg="#FFB6C1", fg="white", font=("Georgia", 15, "bold"), width=15, relief="raised", bd=2)
btn_cadastrar.pack(side=tk.LEFT, padx=10)

btn_entrar = tk.Button(botao_frame, text="Entrar", command=entrar_usuario,
                       bg="#66cc99", fg="white", font=("Georgia", 15, "bold"), width=15, relief="raised", bd=2)
btn_entrar.pack(side=tk.LEFT, padx=10)

btn_deletar = tk.Button(botao_frame, text="Deletar", command=deletar_usuario,
                        bg="#7BAFCB", fg="white", font=("Georgia", 15, "bold"), width=15, relief="raised", bd=2)
btn_deletar.pack(side=tk.LEFT, padx=10)

# Lista de usuários
lista = tk.Listbox(janela, width=80, font=("Courier", 13), bg="#ffe6f0", bd=1, relief="groove", fg="#333")
lista.pack(pady=10)

listar_usuarios()
janela.mainloop()