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

df['rating'] = df['rating'].fillna('Unknown')

# Valores ausentes em critic_score e user_score foram imputados utilizando a mediana para preservar a distribuição e reduzir impacto de outliers. Além disso, foram criadas variáveis indicadoras de ausência para preservar a informação de missingness.

df['critic_score_missing'] = df['critic_score'].isna()
df['user_score_missing'] = df['user_score'].isna()

df['critic_score'] = df['critic_score'].fillna(df['critic_score'].median())
df['user_score'] = df['user_score'].fillna(df['user_score'].median())

df.info()
print(df.sample(15))

df['total_sales'] = df['jp_sales'] + df['eu_sales'] + df['na_sales'] + df['other_sales']

