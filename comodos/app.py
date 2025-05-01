import streamlit as st
from noticias import obter_nome_commodity, buscar_noticias
from previsao import executar_previsao

st.set_page_config(page_title="Previsão de Commodities", layout="wide")

st.title("📊 Previsão e Notícias de Commodities")

# Dicionário de tickers válidos
TICKERS_VALIDOS = {
    "GC=F": "Ouro", "SI=F": "Prata", "CL=F": "Petróleo WTI",
    "BZ=F": "Petróleo Brent", "NG=F": "Gás Natural", "HG=F": "Cobre",
    "ZC=F": "Milho", "ZS=F": "Soja", "ZW=F": "Trigo",
    "SB=F": "Açúcar", "CT=F": "Algodão", "KC=F": "Café"
}

# Lista de commodities válidas
commodities = list(TICKERS_VALIDOS.values())

# Campo de texto para o usuário digitar a commodity
nome_commodity = st.text_input("Digite o nome da commodity (ex.: Café, Ouro, Soja):", value="Café")

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
    # Mensagem de erro com a lista de commodities válidas
    st.error(f"Valor inválido: '{nome_commodity}'. Por favor, escolha uma das seguintes commodities: {', '.join(commodities)}.")