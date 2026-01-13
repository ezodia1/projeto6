import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Atribuição do DataFrame
df = pd.read_csv('games.csv')

# Transforma todas colunas em letras minúsculas
df.columns = df.columns.str.lower()

# Converte para os tipos primitivos corretos
df['year_of_release'] = df['year_of_release'].astype('Int64')
# O ano de lançamento estava como float desnecessariamente, então converti para inteiro

df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
# O valor estava como object, o que me impediria futuramente de realizar cálculos com ele, então converti para float

# Tratando Valores ausentes

df = df.dropna(subset=['name']) # 2 amostras
df = df.dropna(subset=['year_of_release']) # 244 amostras

#Preferi não mexer em user_score e critic_score, pois isso vai alterar um valor crucial que vai afetar os resultados finais e análise final, portanto como ele está NaN ele vai ser ignorado nessas análises

df['rating'] = df['rating'].fillna('Unknown')

df['total_sales'] = df['jp_sales'] + df['eu_sales'] + df['na_sales'] + df['other_sales']

#Lançamento de Jogos a cada ano:

#Ordena os jogos por ano de lançamento, do mais antigo ao mais novo e remove os duplicados para assim ter somente o ano original que o game lançou
df_unique = df.sort_values('year_of_release').drop_duplicates(subset='name', keep='first')
df_unique_gb = df_unique.groupby('year_of_release')['name'].count()

#print(df_unique_gb)

#Variaçao de vendas de plataforma pra plataforma ao longo dos anos

df_platform_sales_gb = df.groupby(['platform', 'year_of_release'])['total_sales'].sum()
#print(df_platform_sales_gb)

df_platform_sales = (
    df.groupby(['year_of_release', 'platform'])['total_sales']
      .sum()
      .reset_index()
)

df_platform_sales_peryear_gb = (
    df_platform_sales
      .sort_values(['year_of_release', 'total_sales'], ascending=[True, False])
      .groupby('year_of_release')
      .head(3)
)

df_platform_total = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False)

print(df_platform_total.head(10))

top_platforms = df_platform_total.head(5).index

df_top = df[df['platform'].isin(top_platforms)]

plt.figure(figsize=(12,6))
for p in top_platforms:
    data = df_platform_sales[df_platform_sales['platform'] == p]
    plt.plot(data['year_of_release'], data['total_sales'], label=p)

plt.title('Vendas Anuais das Principais Plataformas')
plt.xlabel('Ano de Lançamento')
plt.ylabel('Vendas Globais')
plt.legend()
plt.show()
