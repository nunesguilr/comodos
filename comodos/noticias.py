import feedparser
import requests
from bs4 import BeautifulSoup
import re
import time

def obter_nome_commodity(ticker):
    nomes_comodities = {
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
        "OJ=F": "Suco de Laranja", "LBS=F": "Madeira",
        # Outros
        "DX=F": "Índice Dólar", "ES=F": "S&P 500 Futuros", "NQ=F": "Nasdaq 100 Futuros"
    }
    return nomes_comodities.get(ticker, ticker)

def buscar_noticias_rss(termo, termo_ingles):
    feeds = [
        # Internacionais
        "https://www.reuters.com/arc/outboundfeeds/newsroom/commodities/?format=xml",  # Reuters Commodities
        "https://www.investing.com/rss/news_1.rss",  # Investing.com Commodities
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",  # WSJ Markets
        "https://www.marketwatch.com/rss/commodities",  # MarketWatch Commodities
        "https://www.ft.com/markets?format=rss",  # Financial Times Markets
        "https://www.cnbc.com/id/10000664/device/rss",  # CNBC Markets
        "https://www.thestreet.com/feed/markets",  # TheStreet Markets
        "https://www.bloomberg.com/feeds/markets.xml",  # Bloomberg Markets
        "https://www.barchart.com/stocks/sectors/commodities/rss",  # Barchart Commodities
        "https://www.agriculture.com/news/rss",  # Agriculture.com
        # Brasileiras
        "https://www.valor.com.br/empresas/agro/rss.xml",  # Valor Econômico Agro
        "https://www.estadao.com.br/economia/agronegocio/rss.xml",  # Estadão Agronegócio
        "https://www1.folha.uol.com.br/mercado/rss091.xml",  # Folha Mercado
        "https://exame.com/brasil/agro/feed/",  # Exame Agronegócio
        "https://globorural.globo.com/rss.xml",  # Globo Rural
        "https://www.canalrural.com.br/rss/",  # Canal Rural
        "https://www.noticiasagricolas.com.br/rss.xml",  # Notícias Agrícolas
        "https://g1.globo.com/economia/agronegocios/noticia/feed/",  # G1 Agronegócio
        "https://www.ocafezinho.com/feed/"  # O Cafezinho
    ]
    
    noticias = []
    palavras_relevantes = [
        "price", "market", "futures", "export", "production", "supply", "demand", "commodity", "tariff",
        "preço", "mercado", "exportação", "produção", "oferta", "demanda", "safra", "clima", "arábica",
        "robusta", "cotação", "bolsa", "commodities"
    ]
    palavras_ignorar = [
        "recipe", "cooking", "culinary", "lifestyle", "health", "diet", "consumer", "receita", "culinária",
        "estilo de vida", "saúde", "dieta", "café da manhã", "barista", "promoção", "loja"
    ]
    
    for feed_url in feeds: 
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                summary = entry.get("summary", "")
                
                content = (title + " " + summary).lower()
                if (termo.lower() in content or termo_ingles.lower() in content) and \
                   any(palavra in content for palavra in palavras_relevantes) and \
                   not any(palavra in content for palavra in palavras_ignorar):
                    noticias.append({"titulo": title, "link": link})
        except Exception as e:
            print(f"Aviso: Erro ao acessar feed {feed_url}: {e}")
    
    return noticias[:5] if noticias else []

def buscar_noticias_scraping(termo, termo_ingles):
    urls = [
        # Internacionais
        "https://www.investing.com/news/commodities-news",  # Investing.com Commodities
        "https://www.reuters.com/markets/commodities/",  # Reuters Commodities
        "https://www.ft.com/commodities",  # Financial Times Commodities
        "https://www.cnbc.com/commodities/",  # CNBC Commodities
        "https://www.thestreet.com/markets",  # TheStreet Markets
        "https://www.bloomberg.com/markets/commodities",  # Bloomberg Commodities
        "https://www.barchart.com/news/commodities",  # Barchart News
        "https://www.agriculture.com/markets/commodities",  #
        # Brasileiras
        "https://www.valor.com.br/agro/",  # Valor Econômico Agro
        "https://www.estadao.com.br/economia/agronegocio/",  # Estadão Agronegócio
        "https://www1.folha.uol.com.br/mercado/",  # Folha Mercado
        "https://exame.com/economia/agro/",  # Exame Agronegócio
        "https://revistagloborural.globo.com/mercado/",  # Globo Rural Mercado
        "https://www.canalrural.com.br/noticias/mercado/",  # Canal Rural Mercado
        "https://www.noticiasagricolas.com.br/noticias/cafe/",  # Notícias Agrícolas Café
        "https://g1.globo.com/economia/agronegocios/",  # G1 Agronegócio
        "https://www.ocafezinho.com/categoria/economia/"  # O Cafezinho Economia
    ]
    
    noticias = []
    palavras_relevantes = [
        "price", "market", "futures", "export", "production", "supply", "demand", "commodity", "tariff",
        "preço", "mercado", "exportação", "produção", "oferta", "demanda", "safra", "clima", "arábica",
        "robusta", "cotação", "bolsa", "commodities"
    ]
    palavras_ignorar = [
        "recipe", "cooking", "culinary", "lifestyle", "health", "diet", "consumer", "receita", "culinária",
        "estilo de vida", "saúde", "dieta", "café da manhã", "barista", "promoção", "loja"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }
    
    for url in urls:
        try:
            time.sleep(1)  
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            if response.status_code != 200:
                print(f"Aviso: Erro HTTP {response.status_code} ao acessar {url}")
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            if "investing.com" in url:
                articles = soup.select("article a.title, a.js-article-title, h3 a")
            elif "reuters.com" in url:
                articles = soup.select("article a[data-testid='Heading'], h3 a, a.story-title")
            elif "ft.com" in url:
                articles = soup.select("a.js-teaser-heading-link, h3 a")
            elif "cnbc.com" in url:
                articles = soup.select("div.Card-title a, h3 a")
            elif "thestreet.com" in url:
                articles = soup.select("h3 a, a.article-title")
            elif "bloomberg.com" in url:
                articles = soup.select("article a.headline, h3 a")
            elif "barchart.com" in url:
                articles = soup.select("h4 a, a.news-title")
            elif "agriculture.com" in url:
                articles = soup.select("h3 a, a.article-title")
            elif "valor.com.br" in url:
                articles = soup.select("h2.teaser__title a, h3 a")
            elif "estadao.com.br" in url:
                articles = soup.select("h3 a, a.article-title")
            elif "folha.uol.com.br" in url:
                articles = soup.select("h2.c-headline__title a, h3 a")
            elif "exame.com" in url:
                articles = soup.select("h3 a, a.post-title")
            elif "globorural.globo.com" in url:
                articles = soup.select("h2.post-title a, h3 a")
            elif "canalrural.com.br" in url:
                articles = soup.select("h2 a, a.post-title")
            elif "noticiasagricolas.com.br" in url:
                articles = soup.select("h3 a, a.news-title")
            elif "g1.globo.com" in url:
                articles = soup.select("h2 a, a.post-title")
            elif "ocafezinho.com" in url:
                articles = soup.select("h2 a, a.entry-title")
            else:
                articles = []
            
            for article in articles:
                title = article.text.strip()
                link = article.get("href", "")
                if not link.startswith("http"):
                    base_url = url.split("/")[0] + "//" + url.split("/")[2]
                    link = base_url + link
                
                content = title.lower()
                if (termo.lower() in content or termo_ingles.lower() in content) and \
                   any(palavra in content for palavra in palavras_relevantes) and \
                   not any(palavra in content for palavra in palavras_ignorar):
                    noticias.append({"titulo": title, "link": link})
        
        except Exception as e:
            print(f"Aviso: Erro ao fazer scraping em {url}: {e}")
    
    return noticias[:5] if noticias else []

def buscar_noticias(termo, ticker):
    termos_ingles = {
        # Metais
        "Ouro": "gold", "Prata": "silver", "Platina": "platinum", "Paládio": "palladium", "Cobre": "copper",
        # Energia
        "Petróleo WTI": "WTI oil", "Petróleo Brent": "Brent oil", "Gás Natural": "natural gas",
        "Gasolina RBOB": "gasoline", "Óleo de Aquecimento": "heating oil",
        # Grãos e Agricultura
        "Milho": "corn", "Soja": "soybean", "Trigo": "wheat", "Trigo Vermelho": "red wheat",
        "Farelo de Soja": "soybean meal", "Óleo de Soja": "soybean oil", "Aveia": "oats",
        # Carnes
        "Gado Vivo": "live cattle", "Carne de Porco": "lean hogs", "Gado de Corte": "feeder cattle",
        # Soft Commodities
        "Açúcar": "sugar", "Cacau": "cocoa", "Café Arábica": "coffee", "Algodão": "cotton",
        "Suco de Laranja": "orange juice", "Madeira": "lumber",
        # Outros
        "Índice Dólar": "dollar index"
    }
    termo_ingles = termos_ingles.get(termo, termo.lower())
    
    noticias_rss = buscar_noticias_rss(termo, termo_ingles)
    noticias_scraping = buscar_noticias_scraping(termo, termo_ingles)
    
    noticias = noticias_rss + noticias_scraping
    noticias_unicas = []
    links_vistos = set()
    for noticia in noticias:
        if noticia["link"] not in links_vistos:
            noticias_unicas.append(noticia)
            links_vistos.add(noticia["link"])
    
    if noticias_unicas:
        return noticias_unicas[:5]
    
    return {"mensagem": f"Nenhuma notícia relevante encontrada para {termo} via RSS ou scraping."}

if __name__ == "__main__":
    ticker = input("Digite o código da commodity (ex: KC=F para Café): ").strip().upper()
    nome_commodity = obter_nome_commodity(ticker)
    noticias = buscar_noticias(nome_commodity, ticker)

    print(f"\n### Últimas notícias sobre {nome_commodity} ###")
    if isinstance(noticias, dict) and ("erro" in noticias or "mensagem" in noticias):
        print(noticias.get("erro", noticias.get("mensagem")))
    else:
        for noticia in noticias:
            print(f"- {noticia['titulo']}: {noticia['link']}")