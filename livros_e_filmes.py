import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from cone import conectar
import sys
import os


# Recebe o ID do usuário como argumento ao abrir o programa
user_id = int(sys.argv[1]) if len(sys.argv) > 1 else None

# Cria a janela principal
janela = tk.Tk()
janela.title("Avaliação de Filmes e Livros")
janela.configure(bg="#fff6f0")
janela.geometry("1200x800")
janela.resizable(False, False)

# Carrega e redimensiona a imagem da logo
imagem = Image.open("C:/Users/marya/Downloads/teste/imagens/logo.png")
imagem = imagem.resize((300, 300)) 
imagem_tk = ImageTk.PhotoImage(imagem)

# Coloca a imagem como ícone da janela
janela.iconphoto(False, imagem_tk)

# Frame para o conteúdo das telas
tela_anterior = []   # guarda o histórico das telas para permitir voltar
conteudo_frame = tk.Frame(janela, bg="#fff6f0")
conteudo_frame.pack(pady=20)

nota_var = tk.IntVar(value=0)
func_atual = None

# Limpa os widgets da tela
def limpar_conteudo():
    for widget in conteudo_frame.winfo_children():
        widget.destroy()

# Função para selecionar estrelas (nota de 1 a 5)
def avaliar_estrelas(n):
    for i in range(5):
        estrelas[i].config(text="★" if i < n else "☆")
    nota_var.set(n)

# Botão de voltar à tela anterior
def adicionar_botao_voltar():
    btn_voltar = tk.Button(conteudo_frame, text="Voltar", bg="#f0a500", font=("Georgia", 11, "bold"), command=botao_voltar)
    btn_voltar.pack(side=tk.BOTTOM, pady=15)

def botao_voltar():
    if tela_anterior:
        func = tela_anterior.pop()
        func()
    else:
        mostrar_inicio()

# Busca os gêneros no banco de dados
def buscar_generos(tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT gen_id, gen_nome FROM genero")
    generos = cursor.fetchall()
    cursor.close()
    conn.close()
    return generos

# Busca filmes ou livros de um determinado gênero
def buscar_obras(genero_id, tipo):
    conn = conectar()
    cursor = conn.cursor()
    tabela = "filmes" if tipo == "filme" else "livros"
    campo_genero = "genero_filme_id" if tipo == "filme" else "genero_livro_id"
    cursor.execute(f"SELECT * FROM {tabela} WHERE {campo_genero} = %s", (genero_id,))
    obras = cursor.fetchall()
    cursor.close()
    conn.close()
    return obras

# Salva a avaliação do usuário no banco
def salvar_avaliacao(obra_id, tipo, nota, comentario):
    conn = conectar()
    cursor = conn.cursor()
    if tipo == "filme":
        cursor.execute("INSERT INTO avaliacao (usuario_id, filme_id, livro_id, aval_nota, aval_texto) VALUES (%s, %s, NULL, %s, %s)",
                       (user_id, obra_id, nota, comentario))
    else:
        cursor.execute("INSERT INTO avaliacao (usuario_id, filme_id, livro_id, aval_nota, aval_texto) VALUES (%s, NULL, %s, %s, %s)",
                       (user_id, obra_id, nota, comentario))
    conn.commit()
    cursor.close()
    conn.close()

# Busca as avaliações feitas pelo usuário
def buscar_avaliacoes(tipo):
    conn = conectar()
    cursor = conn.cursor()
    join = "filmes.fil_id = avaliacao.filme_id" if tipo == "filme" else "livros.liv_id = avaliacao.livro_id"
    nome = "filmes.fil_nome" if tipo == "filme" else "livros.liv_nome"
    tabela = "filmes" if tipo == "filme" else "livros"
    cursor.execute(f'''
        SELECT {nome}, avaliacao.aval_nota, avaliacao.aval_texto, {tabela}.{ 'fil_capa' if tipo == 'filme' else 'liv_capa' }
        FROM avaliacao
        JOIN {tabela} ON {join}
        WHERE usuario_id = %s AND {tabela}.{ 'fil_id' if tipo == 'filme' else 'liv_id' } IS NOT NULL
        ORDER BY avaliacao.aval_data DESC
    ''', (user_id,))
    avals = cursor.fetchall()
    cursor.close()
    conn.close()
    return avals

# Tela inicial com as opções de filmes ou livros
def mostrar_inicio():
    global func_atual
    func_atual = mostrar_inicio
    limpar_conteudo()
    tela_anterior.clear()

      # ✅ Aqui: coloca a imagem no topo
    label = tk.Label(conteudo_frame, image=imagem_tk, bg="#fff6f0")
    label.pack(pady= 10)
    

    tk.Label(conteudo_frame, text="Escolha uma opção:", font=("Georgia", 18, "bold"), bg="#fff6f0").pack(pady=20)
    tk.Button(conteudo_frame, text="Filmes", font=("Georgia", 14), bg="#c0e8e0", width=20,
              command=lambda: mudar_tela(lambda: mostrar_generos("filme"))).pack(pady=10)
    tk.Button(conteudo_frame, text="Livros", font=("Georgia", 14), bg="#f4cccc", width=20,
              command=lambda: mudar_tela(lambda: mostrar_generos("livro"))).pack(pady=10)

# Gerencia a navegação entre as telas
def mudar_tela(func):
    global func_atual
    if func_atual:
        tela_anterior.append(func_atual)
    func_atual = func
    func()

# Gerencia a navegação entre as telas
def mostrar_generos(tipo):
    global func_atual
    func_atual = lambda: mostrar_generos(tipo)
    limpar_conteudo()
    tk.Label(conteudo_frame, text="Escolha um gênero:", font=("Georgia", 16, "bold"), bg="#fff6f0").pack(pady=10)
    for gen_id, nome in buscar_generos(tipo):
        tk.Button(conteudo_frame, text=nome, font=("Georgia", 13), bg="#d9ead3", width=20,
                  command=lambda g=gen_id: mudar_tela(lambda: mostrar_obras(g, tipo))).pack(pady=5)
    adicionar_botao_voltar()

# Mostra os gêneros disponíveis
def mostrar_obras(genero_id, tipo):
    global func_atual
    func_atual = lambda: mostrar_obras(genero_id, tipo)
    limpar_conteudo()
    obras = buscar_obras(genero_id, tipo)
    titulo = "Filmes" if tipo == "filme" else "Livros"
    tk.Label(conteudo_frame, text=f"{titulo} do gênero selecionado", font=("Georgia", 16, "bold"), bg="#fff6f0").pack(pady=10)
    for obra in obras:
        id_, _, nome, *_ = obra
        tk.Button(conteudo_frame, text=nome, font=("Georgia", 12), width=30,
                  bg="#f9cb9c", command=lambda o=obra: mudar_tela(lambda: mostrar_avaliacao(o, tipo))).pack(pady=5)
    adicionar_botao_voltar()

# Mostra a lista de obras do gênero escolhido
def mostrar_avaliacao(obra, tipo):
    global func_atual
    func_atual = lambda: mostrar_avaliacao(obra, tipo)
    limpar_conteudo()
    nome = obra[2]
    sinopse = obra[-2]  # penúltimo campo
    id_obra = obra[0]
    imagem_path = obra[-1]  # último campo

    tk.Label(conteudo_frame, text=nome, font=("Georgia", 16, "bold"), bg="#fff6f0").pack(pady=5)

        # Container lado a lado
    info_frame = tk.Frame(conteudo_frame, bg="#fff6f0")
    info_frame.pack(pady=5, padx=20, fill="x")

    # Capa do livro
    if imagem_path and os.path.exists(imagem_path):
        imagem_pil = Image.open(imagem_path).resize((180, 260))
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        img_label = tk.Label(info_frame, image=imagem_tk, bg="#fff6f0")
        img_label.image = imagem_tk
        img_label.pack(side="left", padx=10)

    # Sinopse ao lado da imagem
    sinopse_frame = tk.Frame(info_frame, bg="#fff6f0")
    sinopse_frame.pack(side="left", fill="both", expand=True)

    if sinopse:
        tk.Label(sinopse_frame, text="Sinopse:", font=("Georgia", 12, "bold"), bg="#fff6f0").pack(anchor="nw")
        tk.Label(sinopse_frame, text=sinopse, font=("Palatino Linotype", 12),
                 wraplength=500, justify="left", bg="#fff6f0").pack(anchor="nw", pady=5)


    tk.Label(conteudo_frame, text="Comentário:", font=("Georgia", 12), bg="#fff6f0").pack(pady=5)
    comentario_entry = tk.Text(conteudo_frame, height=4, width=60, font=("Palatino Linotype", 12))
    comentario_entry.pack()

    global estrelas
    estrelas = []
    estrela_frame = tk.Frame(conteudo_frame, bg="#fff6f0")
    estrela_frame.pack(pady=10)
    for i in range(1, 6):
        estrela = tk.Label(estrela_frame, text="☆", font=("Arial", 24), fg="#FFD700", bg="#fff6f0", cursor="hand2")
        estrela.pack(side=tk.LEFT)
        estrela.bind("<Button-1>", lambda e, n=i: avaliar_estrelas(n))
        estrelas.append(estrela)

    def salvar():
        nota = nota_var.get()
        comentario = comentario_entry.get("1.0", tk.END).strip()
        if nota == 0 or not comentario:
            messagebox.showwarning("Atenção", "Dê uma nota e escreva um comentário.")
            return
        salvar_avaliacao(id_obra, tipo, nota, comentario)
        messagebox.showinfo("Sucesso", "Avaliação salva com sucesso!")
        mostrar_inicio()

    # Botões para salvar e ver avaliações
    tk.Button(conteudo_frame, text="Salvar Avaliação", command=salvar,
              bg="#b6d7a8", font=("Georgia", 12)).pack(pady=10)

    tk.Button(conteudo_frame, text="Ver Avaliações", command=lambda: mudar_tela(lambda: mostrar_avaliacoes(tipo)),
              bg="#c0e8e0", font=("Georgia", 11), width=20).pack(pady=5)

    adicionar_botao_voltar()

# Mostra a tela para avaliar uma obra
def mostrar_avaliacoes(tipo):
    global func_atual
    func_atual = lambda: mostrar_avaliacoes(tipo)
    limpar_conteudo()
    titulo = "Filmes" if tipo == "filme" else "Livros"
    tk.Label(conteudo_frame, text=f"Avaliações de {titulo}", font=("Georgia", 16, "bold"), bg="#fff6f0").pack(pady=10)
    avals = buscar_avaliacoes(tipo)

    if not avals:
        tk.Label(conteudo_frame, text="Nenhuma avaliação feita ainda.", font=("Palatino Linotype", 12), bg="#fff6f0").pack()
        adicionar_botao_voltar()
        return

    LIMITE_SCROLL = 2

    if len(avals) > LIMITE_SCROLL:
        container = tk.Frame(conteudo_frame, bg="#fff6f0", width=600)
        container.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container, bg="#fff6f0", highlightthickness=0, width=580)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#fff6f0", width=660)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)



        canvas.pack(side="left", fill="both", expand=True)
        
        container.grid_columnconfigure(0, weight=1)

        scrollbar.pack(side="right", fill="y")

        frame_pai = scroll_frame
    else:
        frame_pai = conteudo_frame

    for nome, nota, comentario, imagem_path in avals:
        frame = tk.Frame(frame_pai, bg="#fdf4f4", bd=1, relief="solid", padx=10, pady=5)
        frame.pack(pady=5, padx=20, fill="x")

        container = tk.Frame(frame, bg="#fdf4f4")
        container.pack(fill="x")

        # 🔹 Imagem da obra
        if imagem_path and os.path.exists(imagem_path):
            try:
                imagem_pil = Image.open(imagem_path).resize((80, 110))
                imagem_tk = ImageTk.PhotoImage(imagem_pil)
                img_label = tk.Label(container, image=imagem_tk, bg="#fdf4f4")
                img_label.image = imagem_tk  # mantém referência
                img_label.pack(side="left", padx=5)
            except:
                pass  # imagem inválida ou erro ao abrir
        # Frame para o conteúdo textual ao lado da imagem
        texto_frame = tk.Frame(container, bg="#fdf4f4", width=450)
        texto_frame.pack(side="left", fill="both", expand=True)

        tk.Label(texto_frame, text=f"{'🎬' if tipo == 'filme' else '📚'} {nome}", font=("Georgia", 12, "bold"), bg="#fdf4f4", wraplength=425).pack(anchor="w")
        estrelas_text = "★" * nota + "☆" * (5 - nota)
        tk.Label(texto_frame, text=f"Avaliação: {estrelas_text}", font=("Arial", 12), fg="#FFD700", bg="#fdf4f4", wraplength=425).pack(anchor="w")
        tk.Label(texto_frame, text=f"Comentário: {comentario}", font=("Palatino Linotype", 11),
                wraplength=425, justify="left", bg="#fdf4f4").pack(anchor="w")
    adicionar_botao_voltar()


mostrar_inicio()
janela.mainloop()