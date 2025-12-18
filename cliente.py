import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente - Inicializador de Processamento")
        self.root.geometry("500x250")

        tk.Label(root, text="Arquivo de Entrada:").pack(pady=5)
        self.entry_arquivo = tk.Entry(root, width=50)
        self.entry_arquivo.pack(pady=5)
        tk.Button(root, text="Selecionar Arquivo", command=self.selecionar_arquivo).pack(pady=2)

        tk.Label(root, text="Palavras-chave (separadas por vírgula):").pack(pady=5)
        self.entry_keywords = tk.Entry(root, width=50)
        self.entry_keywords.pack(pady=5)

        tk.Button(root, text="INICIAR PROCESSAMENTO", command=self.iniciar_processamento, bg="green", fg="white", font=("Arial", 11, "bold")).pack(pady=20)

    def selecionar_arquivo(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename:
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, filename)

    
    def iniciar_processamento(self):
        arquivo = self.entry_arquivo.get()
        keywords = self.entry_keywords.get()

        if not arquivo or not os.path.exists(arquivo):
            messagebox.showerror("Erro", "Arquivo inválido.")
            return
        if not keywords:
            messagebox.showerror("Erro", "Digite as palavras-chave.")
            return

        if getattr(sys, 'frozen', False):
            # Se estiver congelado, chama o leitor.exe
            cmd_base = ["leitor.exe"] 
        else:
            # Se estiver em script, chama python leitor.py
            cmd_base = ["python", "leitor.py"]

        try:
            print("Iniciando Leitor Par...")
            # Aqui usamos o cmd_base que definimos lá em cima
            subprocess.Popen(cmd_base + [arquivo, "par", keywords])
            
            print("Iniciando Leitor Ímpar...")
            subprocess.Popen(cmd_base + [arquivo, "impar", keywords])
            
            messagebox.showinfo("Sucesso", "Leitores instanciados!")
            
        except Exception as e:
            messagebox.showerror("Erro CRÍTICO", f"Falha ao iniciar leitores:\n{e}\n\nVerifique se o arquivo leitor.exe está na mesma pasta.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()