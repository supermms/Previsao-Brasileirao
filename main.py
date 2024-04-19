import streamlit as st
import numpy as np
import pandas as pd
import csv
import re
from datetime import datetime
import random
import seaborn as sns


#Estilos
st.markdown(
"""
<style>
section[data-testid="stFileUploadDropzone"] > button {
    color: #A5D8FF
}
</style>
""", unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)



st.markdown("<h1 style='text-align: center;'>Previsão Brasileirão</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Estudo utilizando IA para previsão da Série A do Campeonato Brasileiro</p>", unsafe_allow_html=True)
st.markdown("""<p class="show-on-cel" style='text-align: center; display:none; color:#FC8181;"'>Esta aplicação não é responsiva para celulares. Selecione a versão para computador para ter uma melhor experiência.</p>""", unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center;'>Tabela Atual</h2>", unsafe_allow_html=True)

tabela_atual = pd.read_csv("./classificacao.csv", sep=';')
st.dataframe(tabela_atual[['#','Equipe', 'J','V', 'P']].set_index('#'), use_container_width=True)#.style.hide())

tabela_partidas = pd.read_csv("./partidas.csv", sep=';')
powerRanking = pd.read_csv("./powerranking.csv", sep=';')


for index, row in tabela_partidas.iterrows():
    hometeam = tabela_partidas.loc[index, 'Home']
    awayteam = tabela_partidas.loc[index, 'Away']
    PRHome = powerRanking[powerRanking['Equipe'] == hometeam][['PowerRanking']].iloc[0,0]
    PRAway = powerRanking[powerRanking['Equipe'] == awayteam][['PowerRanking']].iloc[0,0]
    tabela_partidas.loc[index, 'OddH'] = 0.465 - (PRHome - PRAway)*0.035
    tabela_partidas.loc[index, 'OddD'] = 0.3 - ((tabela_partidas.loc[index, 'OddH']-0.33)/6)
    tabela_partidas.loc[index, 'OddA'] = 1 - tabela_partidas.loc[index, 'OddH'] - tabela_partidas.loc[index, 'OddD']


tabela_partidas[tabela_partidas['Jogado'] == 'Não']['Res'] = ''

for index, row in tabela_partidas.iterrows():
    if row['Jogado'] == 'Não':
        n = random.randint(1,1000)/1000
        if n < row['OddH']:
            tabela_partidas.loc[index, 'Res'] = 'H'
        elif n < (row['OddH'] + row['OddD']):
            tabela_partidas.loc[index, 'Res'] = 'D'
        else:
            tabela_partidas.loc[index, 'Res'] = 'A'

dict_posicoes = {"Athlético-PR":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Atlético-MG": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Atlético-GO": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Bahia":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Botafogo": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Bragantino": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Corinthians": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Criciúma":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Cruzeiro": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Cuiabá":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Flamengo": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Fluminense":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Fortaleza": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Grêmio":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Internacional": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Juventude":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Palmeiras": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "São Paulo": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Vasco": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 "Vitória": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                 }

n_sims = 1000
for x in range(n_sims):
    st.write(x)
    tabela_partidas[tabela_partidas['Jogado'] == 'Não']['Res'] = ''
    for index, row in tabela_partidas.iterrows():
        if row['Jogado'] == 'Não':
            n = random.randint(1,1000)/1000
            if n < row['OddH']:
                tabela_partidas.loc[index, 'Res'] = 'H'
            elif n < (row['OddH'] + row['OddD']):
                tabela_partidas.loc[index, 'Res'] = 'D'
            else:
                tabela_partidas.loc[index, 'Res'] = 'A'

    tabela_previsao = tabela_atual
    for index, row in tabela_previsao.iterrows():
        team = tabela_previsao.loc[index, 'Equipe']
        vitorias = tabela_partidas[tabela_partidas['Home'] == team][tabela_partidas['Res'] == 'H'].shape[0] + tabela_partidas[tabela_partidas['Away'] == team][tabela_partidas['Res'] == 'A'].shape[0]
        empates = tabela_partidas[tabela_partidas['Home'] == team][tabela_partidas['Res'] == 'D'].shape[0] + tabela_partidas[tabela_partidas['Away'] == team][tabela_partidas['Res'] == 'D'].shape[0]
        partidas = tabela_partidas[tabela_partidas['Home'] == team].shape[0] + tabela_partidas[tabela_partidas['Away'] == team].shape[0]
        tabela_previsao.loc[index, 'J'] = partidas
        tabela_previsao.loc[index, 'P'] = vitorias*3 + empates
        tabela_previsao.loc[index, 'V'] = vitorias

    tabela_previsao.sort_values(['P', 'V'], ascending=False, inplace=True)

    i = 1
    for index, row in tabela_previsao.iterrows():
        tabela_previsao.loc[index, '#'] = i
        i = i+1
    
    for index, row in tabela_previsao.iterrows():
        #st.write(f"{row['Equipe']} ficou em {row['#']}")
        dict_posicoes[row['Equipe']][row['#']-1] += 1

dict_posicoes_rel = {}
for key in dict_posicoes:
    dict_posicoes_rel[key] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(dict_posicoes[key])):
        dict_posicoes_rel[key][i] = dict_posicoes[key][i]/sum(dict_posicoes[key])



#Criar dataframe por posições
df_prev_posicoes = pd.DataFrame(dict_posicoes).T
# Divide each row by the number of simulations to get probabilities
df_prev_posicoes = df_prev_posicoes.div(n_sims)
df_prev_posicoes.rename(columns={0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10,
                                 10:11, 11:12, 12:13, 13:14, 14:15, 15:16, 16:17,
                                 17:18, 18:19, 19:20}, inplace=True)

st.markdown("<h2 style='text-align: center;'>Previsões</h2>", unsafe_allow_html=True)
st.write("")
st.markdown("<h3 style='text-align: center;'>Previsão por posição</h3>", unsafe_allow_html=True)

cm = sns.light_palette("green", as_cmap=True)

df_prev_posicoes = df_prev_posicoes.sort_values(20, ascending=True)
df_prev_posicoes = df_prev_posicoes.sort_values(1, ascending=False)

#df_percentages = df_prev_posicoes.style.background_gradient(cmap=cm)

df_percentages = df_prev_posicoes.applymap(lambda x: '{:.2%}'.format(x))

# Display the formatted DataFrame
st.dataframe(df_percentages)

