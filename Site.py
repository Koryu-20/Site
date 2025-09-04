import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Título do aplicativo
st.set_page_config(page_title="Dashboard da Paróquia", layout="wide")
st.title("Dashboard de Informações da Paróquia")
st.markdown("---")

# Função para carregar e processar os dados
# ATENÇÃO: A lógica para ler o Google Sheets (usando a API)
# precisaria ser inserida aqui. Este exemplo usa um DataFrame de demonstração.
def get_data():
    # Simulando os dados do Google Sheets
    # Substitua esta parte pelo código real da API para buscar seus dados
    data = {
        'Domingo': ['01-09', '08-09', '15-09', '22-09', '29-09'],
        'Irmãozinhos': [15, 18, 22, 25, 20],
        'Recitativos_Totais': [5, 6, 8, 7, 9],
        'Idade': ['10-15', '16-20', '21-25', '10-15', '16-20'],
        'Quantidade': [30, 45, 20, 35, 50]
    }
    df = pd.DataFrame(data)
    
    # Criando um DataFrame para o gráfico de idade
    df_idade = df.groupby('Idade')['Quantidade'].sum().reset_index()
    return df, df_idade

# Loop de atualização (simulando a atualização a cada 5 segundos)
while True:
    df, df_idade = get_data()

    # Layout com colunas para organizar os gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.header("Presença de Irmãozinhos por Domingo")
        fig1 = px.bar(df, x='Domingo', y='Irmãozinhos', title="Número de Irmãozinhos por Domingo")
        st.plotly_chart(fig1, use_container_width=True)

        st.header("Recitativos Totais")
        fig2 = px.line(df, x='Domingo', y='Recitativos_Totais', title="Número de Recitativos Totais")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.header("Jovens e Irmãozinhos por Faixa Etária")
        fig3 = px.pie(df_idade, values='Quantidade', names='Idade', title="Distribuição por Faixa Etária")
        st.plotly_chart(fig3, use_container_width=True)

    # Mensagem de rodapé com a última atualização
    st.markdown(f"Última atualização: {time.strftime('%H:%M:%S', time.localtime())}")
    st.markdown("---")

    # Espera 5 segundos antes de recarregar
    time.sleep(5)
    st.experimental_rerun()
