import os
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt


class SistemaNutricional:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Nutricional - Fast Food")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f4f6f8")

        self.df = None
        self.df_clean = None

        self.nutri_cols = [
            "Energy (kCal)",
            "Protein (g)",
            "Carbohydrates (g)",
            "Sugar (g)",
            "Fiber (g)",
            "Total Fat (g)",
            "Saturated Fat (g)",
            "Trans Fat (g)",
            "Cholesterol (mg)",
            "Sodium (mg)"
        ]

        self.criar_interface()

    def criar_interface(self):
        titulo = tk.Label(
            self.root,
            text="Sistema de Análise Nutricional",
            font=("Arial", 24, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        )
        titulo.pack(pady=15)

        frame_botoes = tk.Frame(self.root, bg="#f4f6f8")
        frame_botoes.pack(pady=10)

        botoes = [
            ("Carregar CSV", self.carregar_csv),
            ("Top Calorias", self.top_calorias),
            ("Top Sódio", self.top_sodio),
            ("Açúcar por Categoria", self.acucar_categoria),
            ("Índice de Saudabilidade", self.indice_saudabilidade),
            ("Gráfico Calorias", self.grafico_calorias),
            ("Gráfico Proteína x Gordura", self.grafico_proteina_gordura),
            ("Gráfico Açúcar", self.grafico_acucar),
            ("Limpar Tela", self.limpar_tabela)
        ]

        for texto, comando in botoes:
            btn = tk.Button(
                frame_botoes,
                text=texto,
                command=comando,
                font=("Arial", 10, "bold"),
                bg="#2563eb",
                fg="white",
                activebackground="#1d4ed8",
                activeforeground="white",
                relief="flat",
                padx=12,
                pady=8,
                cursor="hand2"
            )
            btn.pack(side="left", padx=5, pady=5)

        self.status = tk.Label(
            self.root,
            text="Nenhum CSV carregado.",
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#374151"
        )
        self.status.pack(pady=8)

        frame_tabela = tk.Frame(self.root, bg="white")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabela = ttk.Treeview(frame_tabela)
        self.tabela.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.tabela.xview)
        scroll_x.pack(fill="x", padx=20)

        self.tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    def carregar_csv(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv")]
        )

        if not caminho:
            return

        if not os.path.exists(caminho):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        if os.path.getsize(caminho) == 0:
            messagebox.showerror("Erro", "O arquivo CSV está vazio.")
            return

        try:
            self.df = pd.read_csv(caminho)
        except pd.errors.EmptyDataError:
            messagebox.showerror("Erro", "O CSV está vazio ou sem colunas.")
            return
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao ler CSV:\n{erro}")
            return

        colunas_faltando = [col for col in self.nutri_cols if col not in self.df.columns]

        if colunas_faltando:
            messagebox.showerror(
                "Erro",
                "O CSV está faltando estas colunas:\n\n" + "\n".join(colunas_faltando)
            )
            return

        self.df_clean = self.df.dropna(subset=self.nutri_cols).copy()

        self.status.config(
            text=f"CSV carregado com sucesso! Linhas: {len(self.df_clean)}"
        )

        self.mostrar_tabela(self.df_clean.head(20))

    def verificar_dados(self):
        if self.df_clean is None:
            messagebox.showwarning("Aviso", "Carregue um CSV primeiro.")
            return False
        return True

    def mostrar_tabela(self, dados):
        self.limpar_tabela()

        self.tabela["columns"] = list(dados.columns)
        self.tabela["show"] = "headings"

        for coluna in dados.columns:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=150, anchor="center")

        for _, linha in dados.iterrows():
            self.tabela.insert("", "end", values=list(linha))

    def limpar_tabela(self):
        self.tabela.delete(*self.tabela.get_children())
        self.tabela["columns"] = []

    def top_calorias(self):
        if not self.verificar_dados():
            return

        resultado = self.df_clean.sort_values("Energy (kCal)", ascending=False)[
            ["Company", "Category", "Product", "Energy (kCal)"]
        ].head(10)

        self.mostrar_tabela(resultado)

    def top_sodio(self):
        if not self.verificar_dados():
            return

        resultado = self.df_clean.sort_values("Sodium (mg)", ascending=False)[
            ["Company", "Category", "Product", "Sodium (mg)"]
        ].head(10)

        self.mostrar_tabela(resultado)

    def acucar_categoria(self):
        if not self.verificar_dados():
            return

        resultado = (
            self.df_clean.groupby("Category", as_index=False)["Sugar (g)"]
            .mean()
            .sort_values("Sugar (g)", ascending=False)
        )

        self.mostrar_tabela(resultado)

    def indice_saudabilidade(self):
        if not self.verificar_dados():
            return

        den = self.df_clean["Energy (kCal)"].replace(0, np.nan)

        self.df_clean["IS"] = (
            self.df_clean["Protein (g)"]
            + self.df_clean["Fiber (g)"]
            - self.df_clean["Sugar (g)"]
            - self.df_clean["Total Fat (g)"]
        ) / den

        self.df_clean["IS"] = (
            self.df_clean["IS"]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0)
        )

        resultado = self.df_clean.sort_values("IS", ascending=False)[
            ["Company", "Category", "Product", "IS"]
        ].head(10)

        self.mostrar_tabela(resultado)

    def grafico_calorias(self):
        if not self.verificar_dados():
            return

        dados = (
            self.df_clean.groupby("Company")["Energy (kCal)"]
            .mean()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(10, 5))
        plt.bar(dados.index, dados.values)
        plt.title("Calorias médias por empresa")
        plt.xlabel("Empresa")
        plt.ylabel("Calorias")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def grafico_proteina_gordura(self):
        if not self.verificar_dados():
            return

        plt.figure(figsize=(8, 5))
        plt.scatter(
            self.df_clean["Protein (g)"],
            self.df_clean["Total Fat (g)"]
        )
        plt.title("Proteína x Gordura Total")
        plt.xlabel("Proteína (g)")
        plt.ylabel("Gordura Total (g)")
        plt.tight_layout()
        plt.show()

    def grafico_acucar(self):
        if not self.verificar_dados():
            return

        plt.figure(figsize=(8, 5))
        plt.hist(self.df_clean["Sugar (g)"], bins=20)
        plt.title("Distribuição de Açúcar")
        plt.xlabel("Açúcar (g)")
        plt.ylabel("Frequência")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaNutricional(root)
    root.mainloop()