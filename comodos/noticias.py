import feedparser
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
from pathlib import Path

def obter_nome_commodity(ticker):
    nomes_comodities = {
        "GC=F": "Ouro", "SI=F": "Prata", "CL=F": "Petróleo WTI",
        "BZ=F": "Petróleo Brent", "NG=F": "Gás Natural", "HG=F": "Cobre",
        "ZC=F": "Milho", "ZS=F": "Soja", "ZW=F": "Trigo",
        "SB=F": "Açúcar", "CT=F": "Algodão", "KC=F": "Café"
    }
    return nomes_comodities.get(ticker, ticker)

def salvar_cache(noticias, termo, cache_dir="comodos/cache"):
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    cache_file = Path(cache_dir) / f"noticias_{termo.lower().replace(' ', '_')}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False, indent=2)

def carregar_cache(termo, cache_dir="comodos/cache", max_age=24*60*60):
    cache_file = Path(cache_dir) / f"noticias_{termo.lower().replace(' ', '_')}.json"
    if not cache_file.exists():
        return None
    if (time.time() - cache_file.stat().st_mtime) > max_age:  # Cache expirado
        return None
    with open(cache_file, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_noticias_rss(termo, termo_ingles):
    feeds = [
        # Internacionais
        "https://www.reuters.com/arc/outboundfeeds/newsroom/commodities/?format=xml",
        "https://www.investing.com/rss/news_1.rss",
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "https://www.marketwatch.com/rss/commodities",
        "https://www.ft.com/markets?format=rss",
        "https://www.cnbc.com/id/10000664/device/rss",
        "https://www.thestreet.com/feed/markets",
        "https://www.bloomberg.com/feeds/markets.xml",
        "https://www.barchart.com/stocks/sectors/commodities/rss",
        "https://www.agriculture.com/news/rss",
        # Brasileiras
        "https://www.valor.com.br/empresas/agro/rss.xml",
        "https://www.estadao.com.br/economia/agronegocio/rss.xml",
        "https://www1.folha.uol.com.br/mercado/rss091.xml",
        "https://exame.com/brasil/agro/feed/",
        "https://globorural.globo.com/rss.xml",
        "https://www.canalrural.com.br/rss/",
        "https://www.noticiasagricolas.com.br/rss.xml",
        "https://g1.globo.com/economia/agronegocios/noticia/feed/",
        "https://www.ocafezinho.com/feed/"
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
        "https://www.investing.com/news/commodities-news",
        "https://www.reuters.com/markets/commodities/",
        "https://www.ft.com/commodities",
        "https://www.cnbc.com/commodities/",
        "https://www.thestreet.com/markets",
        "https://www.bloomberg.com/markets/commodities",
        "https://www.barchart.com/news/commodities",
        "https://www.agriculture.com/markets/commodities",
        # Brasileiras
        "https://www.valor.com.br/agro/",
        "https://www.estadao.com.br/economia/agronegocio/",
        "https://www1.folha.uol.com.br/mercado/",
        "https://exame.com/economia/agro/",
        "https://revistagloborural.globo.com/mercado/",
        "https://www.canalrural.com.br/noticias/mercado/",
        "https://www.noticiasagricolas.com.br/noticias/cafe/",
        "https://g1.globo.com/economia/agronegocios/",
        "https://www.ocafezinho.com/categoria/economia/"
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
            time.sleep(1)  # Delay para evitar bloqueios
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
        "Ouro": "gold", "Prata": "silver", "Petróleo WTI": "WTI oil",
        "Petróleo Brent": "Brent oil", "Gás Natural": "natural gas", "Cobre": "copper",
        "Milho": "corn", "Soja": "soybean", "Trigo": "wheat",
        "Açúcar": "sugar", "Algodão": "cotton", "Café": "coffee"
    }
    
    termo_ingles = termos_ingles.get(termo, termo.lower())
    
    # Verificar cache
    noticias_cache = carregar_cache(termo)
    if noticias_cache:
        print(f"Notícias carregadas do cache para {termo}")
        return noticias_cache
    
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
        salvar_cache(noticias_unicas[:5], termo)
        return noticias_unicas[:5]
    
    mensagem = {"mensagem": f"Nenhuma notícia relevante encontrada para {termo} via RSS ou scraping."}
    salvar_cache(mensagem, termo)
    return mensagem

if __name__ == "__main__":
    ticker = input("Digite o código da commodity (ex: KC=F para Café): ").strip().upper()
    nome_commodity = obter_nome_commodity(ticker)
    noticias = buscar_noticias(nome_commodity, ticker)

    print(f"\n### Últimas notícias sobre {nome_commodity} ###")
    if isinstance(noticias, dict) and "mensagem" in noticias:
        print(noticias["mensagem"])
    else:
        for noticia in noticias:
            print(f"- {noticia['titulo']}: {noticia['link']}")