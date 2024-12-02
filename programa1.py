import tkinter as tk
from tkinter import messagebox
import random
import json
import os


class AmigoSecretoApp:
    def __init__(self, root):
        # Configurações do root
        self.root = root
        self.root.title("Amigo Secreto")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Estilo e Cores
        self.bg_color = "#2C2C54"  # Fundo roxo escuro
        self.primary_color = "#706FD3"  # Roxo mais claro
        self.secondary_color = "#F97F51"  # Laranja claro
        self.text_color = "#ffffff"  # Branco
        self.card_color = "#3B3B98"  # Azul escuro

        # Variáveis
        self.participantes = []
        self.restricoes = {}
        self.valor_maximo = tk.DoubleVar(value=100.0)
        self.resultado_sorteio = {}

        # Arquivo de resultados
        self.resultado_arquivo = "resultado_sorteio.json"

        # Layout Principal
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)

        # Título
        self.title_label = tk.Label(
            self.main_frame,
            text="🎁 Amigo Secreto 🎉",
            font=("Arial", 30, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
        )
        self.title_label.pack(pady=20)

        # Área de Conteúdo
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True)

        # Botões de Navegação
        self.nav_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.nav_frame.pack(pady=10)
        self.create_nav_buttons()

        # Exibe a tela inicial
        self.show_cadastro()

    def create_nav_buttons(self):
        buttons = [
            ("Cadastrar Participantes", self.show_cadastro),
            ("Definir Restrições", self.show_restricoes),
            ("Realizar Sorteio", self.realizar_sorteio),
            ("Ver Meu Amigo Secreto", self.ver_amigo_secreto),
        ]
        for text, command in buttons:
            tk.Button(
                self.nav_frame,
                text=text,
                bg=self.primary_color,
                fg=self.text_color,
                font=("Arial", 12),
                command=command,
            ).pack(side="left", padx=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_cadastro(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="Adicionar Participantes",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
        ).pack(pady=10)

        frame = tk.Frame(self.content_frame, bg=self.bg_color)
        frame.pack(pady=20)

        tk.Label(frame, text="Nome:", bg=self.bg_color, fg=self.text_color, font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        entry_nome = tk.Entry(frame, font=("Arial", 12))
        entry_nome.grid(row=0, column=1, padx=10, pady=5)

        def adicionar_participante():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite um nome válido!")
                return

            if nome in [p["nome"] for p in self.participantes]:
                messagebox.showerror("Erro", "Participante já cadastrado!")
                return

            self.participantes.append({"nome": nome})
            messagebox.showinfo("Sucesso", f"{nome} foi adicionado com sucesso!")
            entry_nome.delete(0, tk.END)

        tk.Button(
            frame,
            text="Adicionar",
            bg=self.secondary_color,
            fg=self.text_color,
            font=("Arial", 12),
            command=adicionar_participante,
        ).grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(
            self.content_frame,
            text=f"Participantes cadastrados: {', '.join([p['nome'] for p in self.participantes])}",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 12),
        ).pack(pady=10)

    def show_restricoes(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="Definir Restrições",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
        ).pack(pady=10)

        frame = tk.Frame(self.content_frame, bg=self.bg_color)
        frame.pack(pady=20)

        participantes_nomes = [p["nome"] for p in self.participantes]

        tk.Label(frame, text="Quem:", bg=self.bg_color, fg=self.text_color, font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        quem_var = tk.StringVar(value=participantes_nomes[0] if participantes_nomes else "")
        quem_menu = tk.OptionMenu(frame, quem_var, *participantes_nomes)
        quem_menu.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Não pode sortear:", bg=self.bg_color, fg=self.text_color, font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
        nao_pode_var = tk.StringVar(value=participantes_nomes[0] if participantes_nomes else "")
        nao_pode_menu = tk.OptionMenu(frame, nao_pode_var, *participantes_nomes)
        nao_pode_menu.grid(row=1, column=1, padx=10, pady=5)

        def adicionar_restricao():
            quem = quem_var.get()
            nao_pode = nao_pode_var.get()
            if quem == nao_pode:
                messagebox.showerror("Erro", "Um participante não pode se restringir a si mesmo!")
                return

            if quem not in self.restricoes:
                self.restricoes[quem] = []

            if nao_pode in self.restricoes[quem]:
                messagebox.showerror("Erro", "Restrição já cadastrada!")
                return

            self.restricoes[quem].append(nao_pode)
            messagebox.showinfo("Sucesso", f"Restrição adicionada: {quem} não pode sortear {nao_pode}")

        tk.Button(
            frame,
            text="Adicionar",
            bg=self.secondary_color,
            fg=self.text_color,
            font=("Arial", 12),
            command=adicionar_restricao,
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def realizar_sorteio(self):
        if len(self.participantes) < 2:
            messagebox.showerror("Erro", "É necessário pelo menos 2 participantes para o sorteio!")
            return

        participantes = [p["nome"] for p in self.participantes]
        resultado = {}
        tentativas = 0
        max_tentativas = 1000

        while tentativas < max_tentativas:
            tentativas += 1
            random.shuffle(participantes)
            resultado = {p: participantes[(i + 1) % len(participantes)] for i, p in enumerate(participantes)}

            if all(resultado[p] not in self.restricoes.get(p, []) for p in resultado):
                break
        else:
            messagebox.showerror("Erro", "Não foi possível realizar o sorteio com as restrições impostas!")
            return

        # Salva o resultado em um arquivo JSON
        self.resultado_sorteio = resultado
        with open(self.resultado_arquivo, "w") as f:
            json.dump(resultado, f)

        valor_max = self.valor_maximo.get()
        messagebox.showinfo("Sucesso", f"Sorteio realizado com sucesso!\n\nValor Máximo: R$ {valor_max:.2f}")

    def ver_amigo_secreto(self):
        self.clear_content()

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
app = AmigoSecretoApp(root)
root.mainloop()
