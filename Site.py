# --- Carregar e Processar os Dados (função com cache) ---
@st.cache_data(ttl=5) # Cache os dados por 5 segundos
def load_data():
    try:
        # Carrega o arquivo de cadastro
        df_cadastro = pd.read_excel(URL_CADASTRO, engine='openpyxl')
        df_cadastro = df_cadastro.dropna(how='all') # Remove linhas vazias

        # Carrega o arquivo de presença/recitativos
        df_presenca = pd.read_excel(URL_PRESENCA, engine='openpyxl')
        df_presenca = df_presenca.dropna(how='all') # Remove linhas vazias
        
        # Converte a coluna de data para o formato correto
        df_presenca['Data'] = pd.to_datetime(df_presenca['Data'], format='%d/%m/%Y', errors='coerce')
        
        # Pega a última data de atualização da planilha de presença
        ultima_data_atualizacao = df_presenca['Data'].max().strftime('%d/%m/%Y')
        
        return df_cadastro, df_presenca, ultima_data_atualizacao
    except Exception as e:
        st.error(f"❌ Erro ao carregar os dados do Google Drive. Verifique se os links estão públicos ou se o formato é 'xlsx'/'xls'. Erro: {e}")
        return None, None, None
