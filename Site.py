import streamlit as st
import pandas as pd

# Título da sua página
st.title("Relatório de Presença")

# Aqui, vamos usar dados de mentira.
# Quando você tiver a "chave", é aqui que você colocaria o código para ler seu arquivo do Google Drive.
dados = {
    'Domingo': ['Dia 1', 'Dia 2', 'Dia 3', 'Dia 4', 'Dia 5'],
    'Presença': [15, 20, 18, 25, 22]
}

# Criamos uma tabela (dataframe) com os dados
df = pd.DataFrame(dados)

# Criamos o gráfico de barras com a tabela
st.header("Quantidade de Irmãozinhos por Domingo")
st.bar_chart(df, x='Domingo', y='Presença')

# Você pode adicionar mais gráficos aqui!
# Por exemplo, para mostrar os recitativos ou a idade.
