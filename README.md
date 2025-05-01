## Lousa: Sistema de Previsão de Preços de Commodities - Commodos

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/release/python-3133/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.38.0+-red.svg)](https://streamlit.io/)

## Visão Geral

O **Commodos** é um sistema baseado em aprendizado de máquina que prevê preços de commodities, como café (KC=F), petróleo bruto (CL=F) e soja (ZS=F), utilizando dados históricos. Ele combina um modelo LSTM (Long Short-Term Memory), implementado com TensorFlow ou PyTorch, para previsão de preços, um módulo de coleta de notícias para fornecer contexto de mercado, e uma interface web interativa construída com Streamlit para visualização de previsões e notícias. Todas as funcionalidades (download, treinamento, scraping e interface) são gerenciadas pelo script `app.py`. O Commodos foca em previsões precisas de preços em USD, com possibilidade de conversão para BRL, e na correlação entre eventos de mercado e tendências de preços.

## Funcionalidades

- **Previsão de Preços**: Utiliza um modelo LSTM (via TensorFlow ou PyTorch) com possibilidade de integrar um mecanismo de Attention para prever preços de commodities com base em dados históricos do Yahoo Finance (yfinance).
- **Coleta de Notícias**: Realiza scraping e coleta de notícias de feeds RSS e sites (ex.: Bloomberg, Reuters, CafePoint) para contextualizar os movimentos de preços.
- **Interface Interativa**: Um painel Streamlit exibe previsões de preços, indicadores técnicos e notícias relevantes, com um menu dropdown para selecionar commodities.
- **Enriquecimento de Dados**: Inclui indicadores técnicos (ex.: médias móveis, RSI) para aumentar a precisão das previsões.
- **Tratamento de Erros**: Possui scraping robusto com mecanismos de fallback para erros HTTP (404, 403) e validação de dados para lidar com valores ausentes ou inconsistentes.

## Estrutura do Projeto

```
COMODOS/
├── comodos/                 # Código-fonte
│   ├── cache/              # Dados em cache (ex.: preços baixados, notícias coletadas)
│   ├── __init__.py         # Torna 'comodos' um pacote Python
│   ├── app.py             # Aplicação Streamlit (download, treinamento, scraping e interface)
│   ├── tests/             # Testes unitários
│   │   ├── __init__.py    # Torna 'tests' um pacote Python
├── .gitignore             # Ignora arquivos desnecessários
├── poetry.lock            # Arquivo de bloqueio de dependências do Poetry
├── pyproject.toml         # Configuração do projeto e dependências
├── README.md              # Documentação do projeto
```

## Instalação

### 1. Clonar o Repositório:

```bash
git clone git@github.com:nunesguilr/comodos.git
cd COMODOS
```

### 2. Instalar o Poetry (caso ainda não tenha):

```bash
pip install poetry
```

### 3. Instalar as Dependências:

```bash
poetry install
```

### 4. Ativar o Ambiente Virtual:

```bash
poetry shell
```

## Execução

### Rodar a aplicação Streamlit:

```bash
poetry run start-app
```

Ou diretamente:

```bash
poetry run streamlit run comodos/app.py
```

Acesse via navegador: [http://localhost:8501](http://localhost:8501)

## Exemplo de Uso

Ao selecionar "Café (KC=F)" na interface:
- Visualize gráficos com preços históricos e previsões futuras (com intervalos de confiança).
- Consulte indicadores técnicos (RSI, médias móveis).
- Leia notícias recentes relacionadas à commodity.

*Recomendação:* Adicione imagens/screeenshots da interface para melhor documentação.

## Arquitetura

- **Previsão**: LSTM via PyTorch ou TensorFlow, com dados via yfinance.
- **Scraping**: RSS e HTML com `feedparser`, `beautifulsoup4`, `requests`.
- **Painel Web**: Streamlit.

## Dependências (definidas em `pyproject.toml`)

- `streamlit`
- `tensorflow`, `torch`, `torchvision`, `torchaudio`
- `yfinance`, `pandas`, `numpy`, `scikit-learn`
- `matplotlib`, `plotly`
- `feedparser`, `beautifulsoup4`, `requests`, `python-dotenv`

## Melhoria Contínua

- Adicionar Attention ao modelo LSTM
- Sistema de relevância para notícias
- Gráficos interativos com Plotly
- Conversão cambial via API externa
- Suporte para mais commodities

## Contribuição

1. Fork e branch
2. Commit e push
3. Pull Request para `main`

*Use PEP8, escreva testes, e use `poetry run pytest` para testar.*

## Licença

MIT. Consulte o arquivo LICENSE.

## Contato

Dúvidas/sugestões: [guermenunes2@gmail.com](mailto:guermenunes2@gmail.com)

## Solução de Problemas

- `fetch-data` não reconhecido: use a interface.
- `app.py` não encontrado: execute do diretório correto.
- Porta 8501 ocupada: feche outros processos.
- Problemas com `.env`: verifique variáveis e `.gitignore`.
- Falha no scraping: veja `comodos/cache/`.
- Streamlit desatualizado: atualize com `poetry add streamlit@latest`.