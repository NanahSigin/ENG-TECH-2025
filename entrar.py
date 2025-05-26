import tkinter as tk
import subprocess
import os

diretorio = os.path.abspath(os.path.dirname(__file__))

def abrir_login():
    caminho = os.path.join(diretorio, "eu_indico.py")
    subprocess.Popen(["python", caminho])

root = tk.Tk()
root.title("Tela Inicial")
root.geometry("300x200")
root.configure(bg="#fff6f0")

btn_login = tk.Button(root, text="Login", command=abrir_login,
                      bg="#FFB6C1", fg="white", font=("Georgia", 15, "bold"), width=20)
btn_login.pack(expand=True)

root.mainloop()
