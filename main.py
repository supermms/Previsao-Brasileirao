import streamlit as st
import numpy as np
import pandas as pd
import csv
import re
from datetime import datetime
import random
import seaborn as sns


apply_update = False

def checkH2H(t1, t2, df_prev_posicoes):
    sum_pct_t1 = 0.00
    sum_pct_t2 = 0.00 
    for i in range(20):
        p1 = df_prev_posicoes.loc[t1, i+1]
        p2 = sum(df_prev_posicoes.loc[t2, i+2:])
        sum_pct_t1 += p1*p2

        p1 = sum(df_prev_posicoes.loc[t1, i+2:])
        p2 = df_prev_posicoes.loc[t2, i+1]
        sum_pct_t2 += p1*p2

    sum_pct_t1_new = (sum_pct_t1)/(sum_pct_t1+sum_pct_t2)
    sum_pct_t2_new = (sum_pct_t2)/(sum_pct_t1+sum_pct_t2)

    return (sum_pct_t1_new, sum_pct_t2_new)

def checkG4(team, df_prev_posicoes):
    probs = sum([p for p in df_prev_posicoes.loc[team, 1:4]])
    return probs

def checkG6(team, df_prev_posicoes):
    probs = sum([p for p in df_prev_posicoes.loc[team, 1:6]])
    return probs

def checkZ4(team, df_prev_posicoes):
    probs = sum([p for p in df_prev_posicoes.loc[team, 17:]])
    return probs



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
#st.markdown("""<p class="show-on-cel" style='text-align: center; display:none; color:#FC8181;"'>Esta aplicação não é responsiva para celulares. Selecione a versão para computador para ter uma melhor experiência.</p>""", unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center;'>Tabela Atual</h2>", unsafe_allow_html=True)

tabela_atual = pd.read_csv("./classificacao.csv", sep=';')
st.dataframe(tabela_atual[['#','Equipe', 'P', 'J','V', 'SG', 'GP']].set_index('#'), use_container_width=True)#.style.hide())

st.divider()

st.markdown("<h2 style='text-align: center;'>Previsões</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Previsão por Posição</h3>", unsafe_allow_html=True)


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

if apply_update:
    n_sims = 10000
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
    df_prev_posicoes.to_csv('prev_posicoes.csv')
else:
    df_prev_posicoes = pd.read_csv('prev_posicoes.csv', index_col=0)
    df_prev_posicoes.columns = df_prev_posicoes.columns.astype(int)

#df_percentages = df_prev_posicoes.style.background_gradient(cmap=cm)
df_percentages = df_prev_posicoes.applymap(lambda x: '{:.2%}'.format(x))

# Display the formatted DataFrame
st.dataframe(df_percentages)

st.divider()

st.markdown("<h3 style='text-align: center;'>Campeão</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Verifique a probabilidade de uma equipe ser campeã</p>", unsafe_allow_html=True)

equipes = [e for e in df_prev_posicoes.index.to_list()]
team1_camp = st.selectbox('Selecione a Equipe:', equipes, key='sbteam1camp')
p1 = df_prev_posicoes.loc[team1_camp, 1]

st.markdown(f"<p style='text-align: center;'>A probabilidade do <b>{team1_camp}</b> ser campeão é de {p1*100:.2f}%</p>", unsafe_allow_html=True)
if p1 > 0.00:
    st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_camp}</b> ser campeão é de {1/p1:.2f}</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_camp}</b> ser campeão é de infinito</p>", unsafe_allow_html=True)
st.write('')

st.divider()

st.markdown("<h3 style='text-align: center;'>Head-to-Head</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Verifique a probabilidade de uma equipe terminar acima da outra</p>", unsafe_allow_html=True)

equipes = [e for e in df_prev_posicoes.index.to_list()]
col1, col2 = st.columns(2)
team1_h2h = col1.selectbox('Selecione a Equipe 1:', equipes, key='sbteam1g4')
team2_h2h = col2.selectbox('Selecione a Equipe 2:', equipes, key='sbteam2g4')
p1, p2 = checkH2H(team1_h2h, team2_h2h, df_prev_posicoes)

st.markdown(f"<p style='text-align: center;'>A probabilidade do <b>{team1_h2h}</b> terminar acima do <b>{team2_h2h}</b> é de {p1*100:.2f}%</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_h2h}</b> terminar acima do <b>{team2_h2h}</b> é de {1/p1:.2f}</p>", unsafe_allow_html=True)
st.write('')
st.markdown(f"<p style='text-align: center;'>A probabilidade do <b>{team2_h2h}</b> terminar acima do <b>{team1_h2h}</b> é de {p2*100:.2f}%</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team2_h2h}</b> terminar acima do <b>{team1_h2h}</b> é de {1/p2:.2f}</p>", unsafe_allow_html=True)

st.divider()

st.markdown("<h3 style='text-align: center;'>G4 e G6</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Verifique a probabilidade de uma equipe terminar entre as 4 ou 6 primeiras</p>", unsafe_allow_html=True)

team1_g4g6 = st.selectbox('Selecione a Equipe:', equipes)
g4_prob = checkG4(team1_g4g6, df_prev_posicoes)
g6_prob = checkG6(team1_g4g6, df_prev_posicoes)
st.markdown(f"<p style='text-align: center;'>A probabilidade do <b>{team1_g4g6}</b> terminar no G4 é de <b>{g4_prob*100:.2f}%</b></p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_g4g6}</b> terminar no G4 é de  <b>{1/g4_prob:.2f}</b></p>", unsafe_allow_html=True)
st.write('')
st.markdown(f"<p style='text-align: center;'>A probabilidade do <b>{team1_g4g6}</b> terminar no G6 é de <b>{g6_prob*100:.2f}%</b></p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_g4g6}</b> terminar no G6 é de  <b>{1/g6_prob:.2f}</b></p>", unsafe_allow_html=True)

st.divider()

st.markdown("<h3 style='text-align: center;'>Z4</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Verifique a probabilidade de uma equipe terminar entre as 4 últimas posições</p>", unsafe_allow_html=True)

team1_z4 = st.selectbox('Selecione a Equipe:', equipes, key='sbz4')
z4_prob = checkZ4(team1_z4, df_prev_posicoes)

st.markdown(f"<p style='text-align: center;'>A probabilidade do <b>{team1_z4}</b> terminar no Z4 é de <b>{z4_prob*100:.2f}%</b></p>", unsafe_allow_html=True)
if z4_prob > 0.00:
    st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_z4}</b> terminar no Z4 é de <b>{1/z4_prob:.2f}</b></p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='text-align: center;'>A cotação justa para o <b>{team1_z4}</b> terminar no Z4 é de infinito</b></p>", unsafe_allow_html=True)


st.divider()
st.markdown("""<p style='text-align: center;'>Desenvolvido por <a href='https://linkedin.com/in/matheusmsa'>Matheus Sá</a></p>""", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center;'>Quer ajudar o projeto? Considere apoiar o desenvolvimento me pagando um cafézinho <a href='https://nubank.com.br/pagar/30c23/Xvbp895w2O'>via Pix</a></p>""", unsafe_allow_html=True)
st.markdown("""<a id="copy-code" class="copy-button copy-icon db tc no-underline br3 fw6 ttu ttn-ns" data-clipboard-text="00020126950014BR.GOV.BCB.PIX0136e8ef6f0c-2db5-4008-af3a-17f38c81c85c0233Obrigado por apoiar meu trabalho!5204000053039865802BR5917MATHEUS MORENO SA6009SAO PAULO61080540900062240520o9bsntFvnPHTXlX30c236304594C">Copiar código do QR Code</a>""", unsafe_allow_html=True)


