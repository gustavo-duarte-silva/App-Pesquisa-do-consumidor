import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Gustavo.app')
st.header('Resultado da Pesquisa do Consumidor 2021')

#DATAFRAME - HEADERS - LINHA DA COLUNA NO EXCEL - INICIANDO EM ZERO
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file, 
                    sheet_name=sheet_name,
                    usecols='B:D',
                    header=3)

df_participants = pd.read_excel(excel_file, 
                    sheet_name=sheet_name,
                    usecols='F:G',
                    header=3)     

df_participants.dropna(inplace=True)                                  

department_names = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()
age_selection = st.slider('Intervalo de Idade', min_value=min(ages), max_value=max(ages), value = (min(ages), max(ages)))
department_selection = st.multiselect('Departamentos', department_names, default=department_names)

filter = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))

df_grouped = df[filter].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()

if department_selection:
    bar_chart = px.bar(df_grouped,
                    x='Rating',
                    y='Votes',
                    text='Votes')

    st.plotly_chart(bar_chart)
else:
    st.error("Escolha um Valor!")

pie_chart = px.pie(df_participants,
                title='Numero de Participantes',
                values='Participants',
                names='Departments')

st.plotly_chart(pie_chart)