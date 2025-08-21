Atividade Prática: Python e Pandas com Dados Nutricionais

Explorando dados de fast food e desenvolvendo análise em notebook



Objetivo da Atividade:
Explorar, manipular e visualizar dados nutricionais de redes de fast food com Python e Pandas, desenvolvendo um notebook estruturado e interpretativo com foco em análise de dados para projetos de IA.


🗂️ Base de dados
📥 Disponível em anexo neste exercício.
Principais colunas:
Company (nome da rede)
Category (categoria do item)
Product (nome do item)
Valores nutricionais: Energy (kCal), Protein (g), Carbohydrates (g), Sugar (g), Fiber (g), Total Fat (g), Saturated Fat (g), Trans Fat (g), Cholesterol (mg), Sodium (mg)


📌 Tarefas obrigatórias


Importação de bibliotecas: pandas, numpy, matplotlib.pyplot, seaborn.

Leitura e análise inicial dos dados: uso de read_csv(), .head(), .info(), .describe()
Tratamento de dados ausentes: aplicar .dropna() nas colunas nutricionais essenciais.
Análise exploratória: responder com códigos e/ou gráficos:
Quais empresas têm os itens mais calóricos?
Quais os produtos com mais sódio?
Existe relação entre proteína e gordura?
Qual categoria tem mais açúcar?


Visualizações obrigatórias:
Gráfico de barras com calorias médias por empresa.
Scatterplot comparando proteína × gordura.
Histograma mostrando distribuição de açúcar.
Nova coluna: criar um índice de saudabilidade.
Exemplo de fórmula sugerida (IS):
        
        I S space equals space left parenthesis p r o t e í n a space plus space f i b r a space minus space a ç ú c a r space minus space g o r d u r a right parenthesis space divided by space c a l o r i a s
Quanto maior o valor de IS, mais “saudável” o item. Vocês podem ajustar a fórmula ou propor outros critérios, desde que justifiquem.
Ordenações e agrupamentos: utilizar .sort_values() ou .groupby() para gerar novos insights.
Conclusão final: descrever em texto três insights importantes obtidos a partir da análise.








Entrega
Formato: Notebook em Python (.ipynb) com códigos, gráficos e conclusões textuais integradas.
Data de entrega: 28/08/2025