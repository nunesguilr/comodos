import streamlit as st
from noticias import obter_nome_commodity, buscar_noticias
from previsao import executar_previsao

st.set_page_config(page_title="Previsão de Commodities", layout="wide")

st.title("📊 Previsão e Notícias de Commodities")

# Dicionário completo de tickers válidos
TICKERS_VALIDOS = {
    # Metais
    "GC=F": "Ouro", "SI=F": "Prata", "PL=F": "Platina", "PA=F": "Paládio", "HG=F": "Cobre",
    # Energia
    "CL=F": "Petróleo WTI", "BZ=F": "Petróleo Brent", "NG=F": "Gás Natural",
    "RB=F": "Gasolina RBOB", "HO=F": "Óleo de Aquecimento",
    # Grãos e Agricultura
    "ZC=F": "Milho", "ZS=F": "Soja", "ZW=F": "Trigo", "KE=F": "Trigo Vermelho",
    "ZM=F": "Farelo de Soja", "ZL=F": "Óleo de Soja", "ZO=F": "Aveia",
    # Carnes
    "LE=F": "Gado Vivo", "HE=F": "Carne de Porco", "GF=F": "Gado de Corte",
    # Soft Commodities
    "SB=F": "Açúcar", "CC=F": "Cacau", "KC=F": "Café Arábica", "CT=F": "Algodão",
    "OJ=F": "Suco de Laranja", "LBS=F": "Madeira"
}

# Lista de commodities válidas em ordem alfabética
commodities = sorted(list(TICKERS_VALIDOS.values()))

# Campo de seleção para o usuário escolher a commodity
nome_commodity = st.selectbox(
    "Selecione ou digite o nome da commodity:",
    options=commodities,
    index=commodities.index("Café Arábica") if "Café Arábica" in commodities else 0
)

# Validar a entrada
if nome_commodity in commodities:
    # Mapear o nome da commodity para o ticker
    ticker = [k for k, v in TICKERS_VALIDOS.items() if v == nome_commodity][0]

    if ticker:
        nome = obter_nome_commodity(ticker)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"🔮 Previsão de Preço - {nome}")
            try:
                resultado = executar_previsao(ticker, exibir_log=False)

                st.image(f"{ticker}_predictions.png", use_container_width=True)

                st.markdown(f"""
                    ### 📊 Resultado da Previsão – {nome}
                    - **Preço Atual:** USD {resultado['preco_atual']:.2f}  
                    - **Previsão para Amanhã:** USD {resultado['previsao_amanha']:.2f}  
                    - **RMSE (Raiz Erro Quadrático Médio):** {resultado['rmse']:.4f}  
                    - **Acurácia de Direção:** {resultado['acuracia']:.2%}  
                """)
            except Exception as e:
                st.error(f"Erro ao gerar previsão: {e}")

        with col2:
            st.subheader(f"📰 Notícias Recentes - {nome}")
            noticias = buscar_noticias(nome, ticker)
            if isinstance(noticias, list):
                for n in noticias:
                    st.markdown(f"- [{n['titulo']}]({n['link']})")
            else:
                st.info(noticias.get("mensagem", "Nenhuma notícia encontrada."))
else:
    st.error(f"Valor inválido: '{nome_commodity}'. Por favor, escolha uma das seguintes commodities: {', '.join(commodities)}.")

# Adicionando informações adicionais na sidebar
st.sidebar.markdown("""
### ℹ️ Sobre esta aplicação
Esta ferramenta combina:
- Previsão de preços usando modelos de machine learning
- Notícias em tempo real sobre commodities

**Como usar:**
1. Selecione uma commodity na lista
2. Veja a previsão de preço e notícias relacionadas
3. Para commodities agrícolas, as notícias incluem dados sobre safras e clima

**Commodities disponíveis:**
- Metais preciosos e industriais
- Energia e petróleo
- Grãos e agrícolas
- Carnes e soft commodities
""")