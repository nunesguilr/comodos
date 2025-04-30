# Sistema de Previsão de Preços de Commodities - Commodos

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
├── poetry.lock             # Arquivo de bloqueio de dependências do Poetry
├── pyproject.toml          # Configuração do projeto e dependências
├── README.md               # Documentação do projeto
```

## Pré-requisitos

- Python 3.13 ou superior ([Python Downloads](https://www.python.org/downloads/release/python-3133/))
- Poetry (para gerenciamento de dependências) ([Poetry Installation](https://python-poetry.org/docs/#installation))
- Streamlit 1.38.0 ou superior ([Streamlit Documentation](https://streamlit.io/))
- Git (para clonagem do repositório) ([Git SCM Downloads](https://git-scm.com/downloads))

## Instalação

1. **Clonar o Repositório via SSH**:

   ```bash
   git clone git@github.com:<your-username>/comodos.git
   cd COMODOS
   ```

   *Nota*: Substitua `<your-username>` pelo seu usuário ou organização no GitHub. Certifique-se de ter configurado uma chave SSH em [GitHub > Settings > SSH and GPG keys](https://github.com/settings/keys).

2. **Instalar o Poetry**:

   Caso o Poetry não esteja instalado, instale-o com:

   ```bash
   pip install poetry
   ```

3. **Instalar as Dependências**:

   Use o Poetry para instalar as dependências do projeto:

   ```bash
   poetry install
   ```

4. **Ativar o Ambiente Virtual**:

   O Poetry cria automaticamente um ambiente virtual. Ative-o com:

   ```bash
   poetry shell
   ```

## Uso

Todas as funcionalidades do Commodos (download de dados, treinamento do modelo, coleta de notícias e visualização) são gerenciadas pela interface Streamlit. Para iniciar:

1. **Iniciar a Interface do Commodos**:

   Execute o aplicativo Streamlit:

   ```bash
   poetry run start-app
   ```

   Ou, alternativamente:

   ```bash
   poetry run streamlit run comodos/app.py
   ```

   Acesse o painel em `http://localhost:8501`. Use o menu dropdown para selecionar uma commodity e realizar as seguintes ações:
   - Baixar dados históricos via yfinance.
   - Treinar o modelo LSTM.
   - Coletar notícias de sites como Bloomberg, Reuters, e CafePoint.
   - Visualizar previsões, indicadores técnicos e notícias.

   *Nota*: Certifique-se de que `app.py` está configurado para executar todas essas tarefas. Consulte os logs em `comodos/cache/` para erros. Configure variáveis de ambiente em um arquivo `.env` (ex.: chaves de API), se necessário.

## Exemplo

Ao selecionar "Café (KC=F)" no painel do Commodos, você verá:
- Um gráfico com preços históricos e previsões para os próximos 30 dias, incluindo intervalos de confiança.
- Indicadores técnicos, como RSI e médias móveis, para análise de tendências.
- Uma seção de notícias com artigos recentes sobre produção de café ou políticas comerciais.

*Sugestão*: Adicione screenshots da interface Streamlit aqui para ilustrar a experiência do usuário.

## Como Funciona

### Previsão de Preços
O sistema utiliza uma rede neural LSTM (via TensorFlow ou PyTorch) treinada com dados históricos de preços obtidos via [yfinance](https://pypi.org/project/yfinance/). O modelo analisa padrões temporais para prever preços futuros, com possibilidade de integrar mecanismos de Attention para maior precisão. Tudo é gerenciado via `app.py`.

### Coleta de Notícias
Notícias são coletadas de feeds RSS e sites como [Bloomberg](https://www.bloomberg.com/), [Reuters](https://www.reuters.com/), e [CafePoint](https://www.cafepoint.com.br/) usando as bibliotecas `feedparser` e `beautifulsoup4` dentro de `app.py`. Essas notícias contextualizam eventos que podem impactar os preços.

### Interface Interativa
Construída com [Streamlit](https://streamlit.io/), a interface, implementada em `app.py`, permite selecionar commodities via dropdown, visualizar previsões, indicadores técnicos e notícias em um painel interativo.

## Fontes de Dados

- **Dados Históricos de Preços**: Yahoo Finance, acessado via [yfinance](https://pypi.org/project/yfinance/).
- **Notícias**: Feeds RSS e sites, incluindo [Bloomberg](https://www.bloomberg.com/), [Reuters](https://www.reuters.com/), e [CafePoint](https://www.cafepoint.com.br/).

*Nota*: O scraping de notícias deve respeitar os termos de serviço dos sites. Verifique as políticas de cada fonte.

## Métricas de Desempenho

[Adicione métricas como Erro Absoluto Médio (MAE) ou Raiz do Erro Quadrático Médio (RMSE), se disponíveis, para demonstrar a precisão do modelo.]

## Possíveis Melhorias

- **Aprimorar o Modelo**: Adicionar camadas de Attention ao LSTM e testar métodos ensemble.
- **Filtragem de Notícias**: Implementar pontuação de relevância baseada em palavras-chave.
- **Melhorar a Interface**: Incluir gráficos interativos com [Plotly](https://plotly.com/python/).
- **Conversão de Moedas**: Integrar uma API como [ExchangeRate-API](https://www.exchangerate-api.com/) para conversão USD-BRL.
- **Expandir Commodities**: Suporte para ouro (GC=F), milho (ZC=F), entre outros.

## Requisitos

As dependências são gerenciadas pelo Poetry e definidas no `pyproject.toml`. As principais incluem:

- `yfinance`: Obtenção de dados históricos.
- `tensorflow`, `torch`, `torchvision`, `torchaudio`: Construção e treinamento do modelo LSTM.
- `streamlit`: Interface web (versão 1.38.0 ou superior recomendada).
- `pandas`, `numpy`, `scikit-learn`: Manipulação de dados e aprendizado de máquina.
- `matplotlib`, `plotly`: Visualização.
- `feedparser`, `beautifulsoup4`: Coleta de notícias.
- `requests`, `python-dotenv`: Requisições HTTP e gerenciamento de variáveis de ambiente.

### Streamlit
O Streamlit é usado para criar a interface interativa. Para verificar a versão instalada:

```bash
poetry run pip show streamlit
```

Se necessário, atualize com:

```bash
poetry add streamlit@latest
```

Consulte o arquivo `pyproject.toml` para a lista completa de dependências.

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b nome-da-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona feature'`).
4. Envie a branch para o repositório remoto (`git push origin nome-da-feature`).
5. Abra um pull request contra a branch `main`.

*Nota*: Siga as convenções de código PEP8 e inclua testes, se aplicável. Execute `poetry run pytest` para rodar testes, se disponíveis.

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT). Veja o arquivo `LICENSE` para detalhes.

## Contato

Para perguntas ou sugestões, abra uma issue no repositório ou contate os mantenedores em [guermenunes2@gmail.com](mailto:guermenunes2@gmail.com).

## Solução de Problemas

- **Erro: "'fetch-data' não é reconhecido"**: O comando `fetch-data` não está definido. Use a interface Streamlit (`poetry run start-app`) para baixar dados.
- **Erro: "File does not exist: comodos/app.py"**: Execute `poetry run start-app` ou `poetry run streamlit run comodos/app.py` a partir do diretório `COMODOS/`, onde `app.py` está em `comodos/`.
- **Interface não carrega em `http://localhost:8501`**: Confirme que `poetry run start-app` foi executado e que a porta 8501 está livre. Verifique os logs do Streamlit.
- **Erro de versão do Streamlit**: Certifique-se de que a versão do Streamlit é 1.38.0 ou superior. Atualize com `poetry add streamlit@latest`.
- **Dados ausentes ou inconsistentes**: Verifique os logs em `comodos/cache/` para detalhes sobre erros de download ou scraping.
- **Erro com variáveis de ambiente**: Configure o arquivo `.env` com as chaves necessárias (ex.: chaves de API) e garanta que ele esteja no `.gitignore`.