# Inicio.py

import streamlit as st
from datetime import datetime

# Configurações iniciais da página
st.set_page_config(page_title="Fantasy World: A Jornada Mágica", layout="wide")

# Informações do jogo
nome_jogo = "Fantasy World: A Jornada Mágica"
descricao = """
**Bem-vindo a Fantasy World: A Jornada Mágica!**

Prepare-se para embarcar em uma aventura épica onde a magia, a coragem e a amizade serão suas maiores armas.
Neste mundo encantado, você criará seu próprio herói, escolherá habilidades únicas, explorará reinos misteriosos 
e enfrentará criaturas lendárias.

**A história começa** em uma terra esquecida pelo tempo, onde uma antiga profecia fala sobre um escolhido
capaz de restaurar o equilíbrio entre a luz e a escuridão. Seu personagem será guiado por mestres sábios, enfrentará dilemas difíceis,
e terá o destino do mundo em suas mãos.

Você poderá:
- Explorar vastos mapas abertos cheios de segredos.
- Forjar alianças com clãs mágicos e guerreiros lendários.
- Conquistar artefatos antigos para aumentar seus poderes.
- Personalizar habilidades e equipamentos para criar sua estratégia única.
- Viver uma história onde cada decisão molda o futuro do mundo.

**Fantasy World** promete trazer uma experiência única de imersão, aventura e emoção!

---
"""

data_lancamento = datetime(2025, 12, 20)

# Calculando o tempo restante para o lançamento
hoje = datetime.now()
tempo_restante = data_lancamento - hoje
dias_restantes = tempo_restante.days

# Layout da página
col1, col2 = st.columns([2, 1])

with col1:
    st.title(f"🎮 {nome_jogo}")
    
    st.subheader("🌟 Sobre o jogo:")
    st.markdown(descricao)

    st.subheader("📅 Data de Lançamento:")
    st.write(f"**{data_lancamento.strftime('%d/%m/%Y')}**")

    st.subheader("⏳ Tempo até o lançamento:")
    if dias_restantes > 0:
        st.success(f"🚀 Faltam **{dias_restantes} dias** para o grande lançamento!")
    else:
        st.warning("O jogo já foi lançado!")

    st.markdown("---")
    st.info("⚙️ No momento, o jogo está em fase de manutenção e ajustes finais. Acreditamos que, em breve, ele será lançado para todos os aventureiros!")
    
with col2:
    st.write("## 🔐 Acesso Rápido")
    st.write("---")
    if st.button("🔑 Login"):
        st.switch_page("Login.py")
    if st.button("📝 Cadastro"):
        st.switch_page("Cadastro.py")

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>© 2025 Fantasy World Studios. Todos os direitos reservados.</p>",
    unsafe_allow_html=True
)
