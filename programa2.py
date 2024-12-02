import tkinter as tk
from tkinter import messagebox
import json
import os

class ConsultaAmigoSecretoApp:
    def __init__(self, root):
        # Configurações do root
        self.root = root
        self.root.title("Consulta Amigo Secreto")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Estilo e Cores
        self.bg_color = "#2C2C54"  # Fundo roxo escuro
        self.primary_color = "#706FD3"  # Roxo mais claro
        self.secondary_color = "#F97F51"  # Laranja claro
        self.text_color = "#ffffff"  # Branco

        # Arquivo de resultados
        self.resultado_arquivo = "resultado_sorteio.json"

        # Layout Principal
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)

        # Título
        self.title_label = tk.Label(
            self.main_frame,
            text="🎁 Consulta Amigo Secreto 🎉",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
        )
        self.title_label.pack(pady=30)

        # Área de Conteúdo
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True)

        # Exibe a tela de consulta
        self.show_consulta()

    def show_consulta(self):
        tk.Label(
            self.content_frame,
            text="Ver Meu Amigo Secreto",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
        ).pack(pady=10)

        frame = tk.Frame(self.content_frame, bg=self.bg_color)
        frame.pack(pady=20)

        tk.Label(frame, text="Digite seu nome:", bg=self.bg_color, fg=self.text_color, font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        entry_nome = tk.Entry(frame, font=("Arial", 12))
        entry_nome.grid(row=0, column=1, padx=10, pady=5)

        def exibir_amigo_secreto():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite um nome válido!")
                return

            if not os.path.exists(self.resultado_arquivo):
                messagebox.showerror("Erro", "O sorteio ainda não foi realizado!")
                return

            with open(self.resultado_arquivo, "r") as f:
                resultado = json.load(f)

            if nome not in resultado:
                messagebox.showerror("Erro", "Nome não encontrado!")
                return

            amigo = resultado[nome]
            messagebox.showinfo("Amigo Secreto", f"{nome}, você tirou: {amigo}")

        tk.Button(
            frame,
            text="Ver Amigo Secreto",
            bg=self.secondary_color,
            fg=self.text_color,
            font=("Arial", 12),
            command=exibir_amigo_secreto,
        ).grid(row=1, column=0, columnspan=2, pady=10)

# Inicialização
root = tk.Tk()
app = ConsultaAmigoSecretoApp(root)
root.mainloop()
