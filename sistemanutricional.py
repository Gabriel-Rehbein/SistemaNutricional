
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 


CSV_PATH = "fastfood_nutrition.csv" 
df = pd.read_csv(CSV_PATH)

print("\n=== HEAD ===")
print(df.head())

print("\n=== INFO ===")
print(df.info())

print("\n=== DESCRIBE (numéricos) ===")
print(df.describe(numeric_only=True).T)

# 3) Tratamento de dados ausentes
# Defina as colunas nutricionais essenciais (conforme enunciado)
nutri_cols = [
    "Energy (kCal)", "Protein (g)", "Carbohydrates (g)", "Sugar (g)", "Fiber (g)",
    "Total Fat (g)", "Saturated Fat (g)", "Trans Fat (g)", "Cholesterol (mg)", "Sodium (mg)"
]

# Dropa linhas com NA nas colunas essenciais
df_clean = df.dropna(subset=nutri_cols).copy()

# 4) Análise exploratória solicitada

# 4.1) Quais empresas têm os itens mais calóricos?
# Vamos pegar o top N por item e também a média por empresa
top_caloric_items = df_clean.sort_values("Energy (kCal)", ascending=False)[
    ["Company", "Category", "Product", "Energy (kCal)"]
].head(10)

calories_mean_by_company = (
    df_clean.groupby("Company", as_index=False)["Energy (kCal)"]
    .mean()
    .sort_values("Energy (kCal)", ascending=False)
)

print("\n=== Top 10 itens mais calóricos ===")
print(top_caloric_items)

print("\n=== Calorias médias por empresa (desc) ===")
print(calories_mean_by_company)

# 4.2) Quais os produtos com mais sódio?
top_sodium = df_clean.sort_values("Sodium (mg)", ascending=False)[
    ["Company", "Category", "Product", "Sodium (mg)"]
].head(10)

print("\n=== Top 10 produtos com mais sódio ===")
print(top_sodium)

# 4.3) Existe relação entre proteína e gordura? (vamos calcular correlação simples)
corr_protein_fat = df_clean[["Protein (g)", "Total Fat (g)"]].corr().iloc[0, 1]
print(f"\n=== Correlação (Protein x Total Fat): {corr_protein_fat:.3f} ===")

# 4.4) Qual categoria tem mais açúcar? (média)
sugar_by_category = (
    df_clean.groupby("Category", as_index=False)["Sugar (g)"]
    .mean()
    .sort_values("Sugar (g)", ascending=False)
)
print("\n=== Açúcar médio por categoria (desc) ===")
print(sugar_by_category.head(10))

# 5) Visualizações obrigatórias (usando matplotlib)

# 5.1) Gráfico de barras com calorias médias por empresa
plt.figure()
plt.bar(calories_mean_by_company["Company"], calories_mean_by_company["Energy (kCal)"])
plt.title("Calorias médias por empresa")
plt.xlabel("Empresa")
plt.ylabel("Calorias (kCal)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 5.2) Scatterplot comparando proteína × gordura (Total Fat)
plt.figure()
plt.scatter(df_clean["Protein (g)"], df_clean["Total Fat (g)"])
plt.title("Proteína (g) x Gordura Total (g)")
plt.xlabel("Proteína (g)")
plt.ylabel("Gordura Total (g)")
plt.tight_layout()
plt.show()

# 5.3) Histograma mostrando distribuição de açúcar
plt.figure()
plt.hist(df_clean["Sugar (g)"], bins=30)
plt.title("Distribuição de Açúcar (g)")
plt.xlabel("Açúcar (g)")
plt.ylabel("Frequência")
plt.tight_layout()
plt.show()

# 6) Nova coluna: Índice de Saudabilidade (IS)
# Fórmula sugerida: IS = (proteína + fibra - açúcar - gordura) / calorias
# Usaremos 'Total Fat (g)' como 'gordura'. Evita div. por zero:
den = df_clean["Energy (kCal)"].replace(0, np.nan)
df_clean["IS"] = (df_clean["Protein (g)"] + df_clean["Fiber (g)"]
                  - df_clean["Sugar (g)"] - df_clean["Total Fat (g)"]) / den

# Substitui inf e NaN resultantes por 0 para facilitar ordenações posteriores
df_clean["IS"] = df_clean["IS"].replace([np.inf, -np.inf], np.nan).fillna(0.0)

print("\n=== Amostra com IS (Índice de Saudabilidade) ===")
print(df_clean[["Company", "Category", "Product", "IS"]].head())

# 7) Ordenações e agrupamentos para gerar novos insights
# 7.1) Ranking de empresas por IS médio
is_mean_by_company = (
    df_clean.groupby("Company", as_index=False)["IS"]
    .mean()
    .sort_values("IS", ascending=False)
)
print("\n=== IS médio por empresa (desc) ===")
print(is_mean_by_company)

# 7.2) Top 10 itens mais saudáveis segundo o IS
top10_is = df_clean.sort_values("IS", ascending=False)[
    ["Company", "Category", "Product", "IS"]
].head(10)
print("\n=== Top 10 itens por IS (mais 'saudáveis') ===")
print(top10_is)

# 7.3) Itens com maior relação Sódio/Caloria (ex. útil p/ insights)
df_clean["Sodium_per_kCal"] = df_clean["Sodium (mg)"] / den
df_clean["Sodium_per_kCal"] = df_clean["Sodium_per_kCal"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
top_sodium_density = df_clean.sort_values("Sodium_per_kCal", ascending=False)[
    ["Company", "Category", "Product", "Sodium (mg)", "Energy (kCal)", "Sodium_per_kCal"]
].head(10)
print("\n=== Top 10 Sódio por kCal ===")
print(top_sodium_density)

# 8) Conclusão final: três insights automáticos a partir dos resultados
insights = []

# Insight 1: empresa mais calórica em média
if not calories_mean_by_company.empty:
    insights.append(
        f"1) A empresa com maior média de calorias é '{calories_mean_by_company.iloc[0]['Company']}' "
        f"({calories_mean_by_company.iloc[0]['Energy (kCal)']:.1f} kCal por item, em média)."
    )

# Insight 2: categoria com mais açúcar em média
if not sugar_by_category.empty:
    insights.append(
        f"2) A categoria com maior teor médio de açúcar é '{sugar_by_category.iloc[0]['Category']}' "
        f"({sugar_by_category.iloc[0]['Sugar (g)']:.1f} g, em média)."
    )

# Insight 3: relação proteína x gordura
insights.append(
    f"3) A correlação entre proteína e gordura total é {corr_protein_fat:.2f} "
    "(>0 sugere que itens mais proteicos tendem a vir com mais gordura; <0 seria o oposto)."
)

print("\n=== Conclusões (3 insights) ===")
for line in insights:
    print(line)
