import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as st

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

#print(df_platform_total.head(10))

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
plt.savefig('Vendas Anuais das Principais Plataformas.png')
plt.close()

'''As plataformas com maiores vendas totais (PS2, X360, PS3, Wii e DS) apresentam um crescimento, ápice e queda bem claros. Algumas, como PS2 e Wii, foram muito fortes entre 2005 até 2010, mas desapareceram nos anos seguintes, mostrando que plataformas populares acabam sendo substituídas conforme novas gerações entram no mercado.'''

df_modern_platforms = df[df['year_of_release'] > 1995].sort_values('year_of_release')
df_modern_platforms = df_modern_platforms.groupby(['year_of_release', 'platform'])['total_sales'].sum().reset_index()
df_modern_platforms = df_modern_platforms[df_modern_platforms['total_sales'] > 20]

plt.title('Vendas Totais por Ano para todas as Plataformas')
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_modern_platforms, x='year_of_release', y='total_sales', hue='platform')
plt.xlabel('Ano de Lançamento')
plt.savefig('Vendas Totais por Ano para todas as Plataformas.png')
plt.close()

'''Ao analisar todas as plataformas após 1995, percebe-se que novas plataformas surgem aproximadamente a cada 5 a 7 anos, atingem ápice e depois são substituídas. Esse comportamento indica um ciclo natural do mercado, no qual plataformas antigas deixam de gerar vendas enquanto as novas assumem o protagonismo.'''

#BLOXPLOT

df_psxbox = ['PS4', 'XOne']
plt.figure(figsize=(14, 6))
sns.boxplot(data=df[df['platform'].isin(df_psxbox)],
            x='platform', y='total_sales')
plt.title('Vendas Globais por Plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Vendas Globais (em milhões)')
plt.xticks(rotation=45)
plt.savefig('Vendas Globais por Plataforma.png')
plt.close()

#avaliaçoes

df_ps2 = df[df['platform'] == 'PS2']

total = len(df_ps2)

nan_critic = df_ps2['critic_score'].isna().sum()
nan_user = df_ps2['user_score'].isna().sum()
nan_both = (df_ps2['critic_score'].isna() & df_ps2['user_score'].isna()).sum()

'''print(f"Total PS2: {total}")
print(f"NaN em critic_score: {nan_critic}")
print(f"NaN em user_score: {nan_user}")
print(f"NaN em ambos: {nan_both}") '''

df_ps2_dropna = df_ps2.dropna(subset=['critic_score', 'user_score', 'total_sales'])

plt.figure(figsize=(12,6))
sns.scatterplot(data=df_ps2_dropna, x='user_score', y='critic_score', size='total_sales', sizes=(20,200), alpha=0.6)
plt.xlabel('User Score')
plt.ylabel('Critic Score')
plt.title('Scores vs Vendas (cor = vendas)')
plt.savefig('user_critic.png')
plt.close()

#Ao analisar a diferença entre as vendas de jogos com avaliações altas pela crítica e vendas de jogos com avaliações altas pelos usuários, percebe-se que os games com notas altas pela crítica em sua maioria são um sucesso de venda, enquanto jogos com avaliações altas dos usuários não tem muita relação na venda total
 


'''Filtro para escolher 5 jogos que estejam para estas 5 principais plataformas ('PS3', 'X360', 'PS4', 'XOne', 'PC')''' 

#print(df.sort_values(by='total_sales', ascending=False)['name'].head(20))

#print(df[df['name'] == 'Grand Theft Auto V'])

df_gtav = df[df['name'] == 'Grand Theft Auto V']

games_platform = ['PS3', 'X360', 'PS4', 'XOne', 'PC']

df_same_games_platform = df[df['platform'].isin(games_platform)]

df_games_platform_merged = df_same_games_platform.groupby('name', as_index=False)['total_sales'].sum()

#print(df_games_platform_merged.sort_values(by='total_sales', ascending=False)['name'].head(20))

chosen_games = ['Grand Theft Auto V', 'Call of Duty: Black Ops 3', 'Call of Duty: Advanced Warfare', 'The Elder Scrolls V: Skyrim', 'FIFA 16']

df_chosen_games = df[df['name'].isin(chosen_games) & df['platform'].isin(games_platform)]


plt.figure(figsize=(12, 6))
sns.barplot(data=df_chosen_games, x='platform', y='total_sales', hue='name')
plt.xlabel(' ')
plt.ylabel('Vendas Globais')
plt.title('O mesmo jogo, vende diferente em outra plataforma?')
plt.savefig('vendas_games_plataforma.png')
plt.close()

#

#Venda de Jogos por Genero

df_games_genre_sales = df.groupby('genre', as_index=False)['total_sales'].sum()

df_games_unique = df.drop_duplicates(subset='name')

df_games_genre_count = df_games_unique.groupby('genre', as_index=False)['name'].count()

df_games_genre_merged = pd.merge(df_games_genre_count, df_games_genre_sales, on='genre')
df_games_genre_merged = df_games_genre_merged.rename(columns={'name': 'games_count'})

#print(df_games_genre_merged)

plt.figure(figsize=(12, 6))
sns.barplot(data=df_games_genre_merged, x='games_count', y='total_sales', hue='genre')
plt.savefig('Como a quantidade de jogos de um gênero influencia o total de vendas')
plt.close()

# Perfil de Usuário para cada região


#5 Plataformas que mais vendem em cada região:

#Japan
df_jp_platforms = df.groupby('platform')['jp_sales'].sum().sort_values(ascending=False).head(5)
df_jp_platforms_others = df.groupby('platform')['jp_sales'].sum().drop(df_jp_platforms.index).sum().round(2)
df_jp_platforms['others'] = df_jp_platforms_others

#North America
df_na_platforms = df.groupby('platform')['na_sales'].sum().sort_values(ascending=False).head(5)
df_na_platforms_others = df.groupby('platform')['na_sales'].sum().drop(df_na_platforms.index).sum().round(2)
df_na_platforms['others'] = df_na_platforms_others

#Europe
df_eu_platforms = df.groupby('platform')['eu_sales'].sum().sort_values(ascending=False).head(5)
df_eu_platforms_others = df.groupby('platform')['eu_sales'].sum().drop(df_eu_platforms.index).sum().round(2)
df_eu_platforms['others'] = df_eu_platforms_others

#Quotas de cada região

#Japan
quota_jp_platforms = ((df_jp_platforms / df['jp_sales'].sum()) * 100).round(2)

#North America
quota_na_platforms = ((df_na_platforms / df['na_sales'].sum()) * 100).round(2)

#Europe
quota_eu_platforms = ((df_eu_platforms / df['eu_sales'].sum()) * 100).round(2)

#print(quota_eu_platforms.map(lambda x: f"{x:.2f}%"))


#5 Gêneros que mais vendem em cada região:

#Japan
df_jp_genre = df.groupby('genre')['jp_sales'].sum().sort_values(ascending=False).head(5)
df_jp_genre_others = df.groupby('genre')['jp_sales'].sum().drop(df_jp_genre.index).sum().round(2)
df_jp_genre['others'] = df_jp_genre_others

#North America
df_na_genre = df.groupby('genre')['na_sales'].sum().sort_values(ascending=False).head(5)
df_na_genre_others = df.groupby('genre')['na_sales'].sum().drop(df_na_genre.index).sum().round(2)
df_na_genre['others'] = df_na_genre_others

#Europe
df_eu_genre = df.groupby('genre')['eu_sales'].sum().sort_values(ascending=False).head(5)
df_eu_genre_others = df.groupby('genre')['eu_sales'].sum().drop(df_eu_genre.index).sum().round(2)
df_eu_genre['others'] = df_eu_genre_others

#Quotas de cada região

#Japan
quota_jp_genre = ((df_jp_genre / df['jp_sales'].sum()) * 100).round(2)

#North America
quota_na_genre = ((df_na_genre / df['na_sales'].sum()) * 100).round(2)

#Europe
quota_eu_genre = ((df_eu_genre / df['eu_sales'].sum()) * 100).round(2)

#print(quota_eu_genre)


#5 Ratings que mais vendem em cada região: 

df_rating_dropna = df[df['rating'] != 'Unknown']


#Japan
df_jp_rating = df_rating_dropna.groupby('rating')['jp_sales'].sum().sort_values(ascending=False)

#North America
df_na_rating = df_rating_dropna.groupby('rating')['na_sales'].sum().sort_values(ascending=False)

#Europe
df_eu_rating = df_rating_dropna.groupby('rating')['eu_sales'].sum().sort_values(ascending=False)


#Gráficos 

#PLATFORM

plt.figure(figsize=(14,5))

# Japan
plt.subplot(1, 3, 1)
plt.pie(df_jp_platforms.values, labels=df_jp_platforms.index, autopct='%1.1f%%', startangle=90)
plt.title('Platform - Japan')

# North America
plt.subplot(1, 3, 2)
plt.pie(df_na_platforms.values, labels=df_na_platforms.index, autopct='%1.1f%%', startangle=90)
plt.title('Platform - North America')

# Europe
plt.subplot(1, 3, 3)
plt.pie(df_eu_platforms.values, labels=df_eu_platforms.index, autopct='%1.1f%%', startangle=90)
plt.title('Platform - Europe')

plt.tight_layout()
plt.savefig('platform_regions.png')
plt.close()

#GENRE

plt.figure(figsize=(14,5))

# Japan
plt.subplot(1, 3, 1)
plt.pie(df_jp_genre.values, labels=df_jp_genre.index, autopct='%1.1f%%', startangle=90)
plt.title('Genre - Japan')

# North America
plt.subplot(1, 3, 2)
plt.pie(df_na_genre.values, labels=df_na_genre.index, autopct='%1.1f%%', startangle=90)
plt.title('Genre - North America')

# Europe
plt.subplot(1, 3, 3)
plt.pie(df_eu_genre.values, labels=df_eu_genre.index, autopct='%1.1f%%', startangle=90)
plt.title('Genre - Europe')

plt.tight_layout()
plt.savefig('genre_regions.png')
plt.close()


#RATING

plt.figure(figsize=(14,5))

# Japan
plt.subplot(1, 3, 1)
plt.pie(df_jp_rating.values, labels=df_jp_rating.index, autopct='%1.1f%%', startangle=90)
plt.title('Rating - Japan')

# North America
plt.subplot(1, 3, 2)
plt.pie(df_na_rating.values, labels=df_na_rating.index, autopct='%1.1f%%', startangle=90)
plt.title('Rating - North America')

# Europe
plt.subplot(1, 3, 3)
plt.pie(df_eu_rating.values, labels=df_eu_rating.index, autopct='%1.1f%%', startangle=90)
plt.title('Rating - Europe')

plt.tight_layout()
plt.savefig('rating_regions.png')
plt.close()

#TESTES DE HIPOTESE
df_user_dropna = df[df['user_score'].notna()]

df_user_pc = df_user_dropna[df_user_dropna['platform'] == 'PC']['user_score']
df_user_xone = df_user_dropna[df_user_dropna['platform'] == 'XOne']['user_score']

alpha = 0.05

platform_user_score_results = st.ttest_ind(df_user_pc, df_user_xone)

print(f'valor-p: {platform_user_score_results.pvalue}')

if platform_user_score_results.pvalue < alpha: 
    print("Rejeitamos a hipótese nula")
    print("Conclusão: As médias SÃO diferentes")
else:
    print("Não podemos rejeitar a hipótese nula")
    print("Conclusão: As médias PODEM SER iguais")

#GENEROS

df_user_action = df_user_dropna[df_user_dropna['genre'] == 'Action']['user_score']
df_user_sports = df_user_dropna[df_user_dropna['genre'] == 'Sports']['user_score']

alpha = 0.05

genre_user_score_results = st.ttest_ind(df_user_action, df_user_sports)

print(f'valor-p: {genre_user_score_results.pvalue}')

if genre_user_score_results.pvalue < alpha: 
    print("Rejeitamos a hipótese nula")
    print("Conclusão: As médias são estatisticamente diferentes")
else:
    print("Não podemos rejeitar a hipótese nula")
    print("Conclusão: Não há evidência estatística de diferença entre as médias")


# Teste 1: Utilizei dos valores fornecidos para testar a hipótese nula (As classificações médias dos usuários das plataformas Xbox One e PC são as mesmas) e a hipótese alternativa (As classificações médias dos usuários das plataformas Xbox One e PC são diferentes). Com isso concluí que, mesmo sendo plataformas com experiências de jogabilidade distintas entre console e computador, as avaliações dos usuários apresentam diferença estatisticamente significativa. Com isso rejeitamos a hipótese nula.

# Teste 2: Utilizei os dados disponíveis para testar a hipótese nula (As classificações médias dos usuários para os gêneros Action e Sports são iguais) e a hipótese alternativa (As classificações médias dos usuários para os gêneros Action e Sports são diferentes). A partir da análise, verifiquei que mesmo sendo gêneros distintos e com públicos diferentes, as avaliações dos usuários não apresentam diferença estatisticamente significativa entre eles. Portanto, não podemos rejeitar a hipótese nula.

#Para estes testes de hipótese utilizei a significância de 5%, tendo em vista que se está sendo analisado dados referentes a compra de videogames e jogos, o quem infere que há algumas variáveis tais como games com múltiplos gêneros, gêneros de jogos que costumam vir acompanhados (como ação e aventura), pessoas que compram consoles por causa de exclusivos ou por fator nostalgia. Como há algumas variáveis que não se tem como calcular com exatidão e o resultado dessa hipótese não coloca a vida de ninguém em risco eu utilizei uma significância de 5%.