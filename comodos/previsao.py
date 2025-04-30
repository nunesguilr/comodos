import numpy as np
import pandas as pd
import yfinance as yf
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pathlib import Path
import time

# Função para calcular RSI
def compute_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(method='ffill')

# Função para calcular MACD
def compute_macd(data, short=12, long=26, signal=9):
    exp1 = data.ewm(span=short, adjust=False).mean()
    exp2 = data.ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - signal_line
    return macd_hist.fillna(method='ffill')

# Modelo LSTM
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size=128, num_layers=2, output_size=1, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

# Funções de Cache
def salvar_cache_dados(data, ticker, cache_dir="comodos/cache"):
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    cache_file = Path(cache_dir) / f"dados_{ticker.lower().replace('=', '_')}.csv"
    data.to_csv(cache_file)

def carregar_cache_dados(ticker, cache_dir="comodos/cache", max_age=24*60*60):
    cache_file = Path(cache_dir) / f"dados_{ticker.lower().replace('=', '_')}.csv"
    if not cache_file.exists():
        return None
    if (time.time() - cache_file.stat().st_mtime) > max_age:  # Cache expirado
        return None
    return pd.read_csv(cache_file, index_col=0, parse_dates=True)

# Preprocessamento
def preprocessar_dados(data, seq_length=45):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(seq_length, len(scaled_data)):
        X.append(scaled_data[i-seq_length:i])
        y.append(scaled_data[i, 0])

    return np.array(X), np.array(y).reshape(-1, 1), scaler

# Obter dados
def obter_dados(ticker, start_date="2023-01-01"):
    # Verificar cache
    cached_data = carregar_cache_dados(ticker)
    if cached_data is not None:
        print(f"Dados carregados do cache para {ticker}")
        return cached_data

    hoje = datetime.now().date()
    data = yf.download(ticker, start=start_date, end=hoje.strftime("%Y-%m-%d"), auto_adjust=False)
    if data.empty or len(data) < 100:
        raise ValueError("Dados insuficientes ou ticker inválido.")

    data['Close_MA'] = data['Close'].rolling(window=7).mean()
    data['RSI'] = compute_rsi(data['Close'])
    data['MACD'] = compute_macd(data['Close'])
    data['Volatility'] = data['Close'].rolling(window=14).std()
    data['Volume'] = data['Volume']

    try:
        dollar_data = yf.download("DX-Y.NYB", start=start_date, end=hoje.strftime("%Y-%m-%d"))
        data['Dollar'] = dollar_data['Close'].reindex(data.index, method='ffill')
    except:
        data['Dollar'] = data['Close'].mean()  # Fallback: média do preço de fechamento

    data = data[['Close', 'Close_MA', 'RSI', 'MACD', 'Volatility', 'Volume', 'Dollar']].dropna()
    salvar_cache_dados(data, ticker)
    return data

def plot_predictions(y_test, predicted_prices, scaler, data, ticker, predicted_next):
    y_test_inv = scaler.inverse_transform(
        np.concatenate([y_test, np.zeros((y_test.shape[0], data.shape[1]-1))], axis=1)
    )[:, 0]
    predicted_inv = scaler.inverse_transform(
        np.concatenate([predicted_prices, np.zeros((predicted_prices.shape[0], data.shape[1]-1))], axis=1)
    )[:, 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(len(y_test_inv)), y_test_inv, label="Real")
    ax.plot(range(len(predicted_inv)), predicted_inv, label="Previsto")
    ax.axvline(x=len(y_test_inv)-1, color='r', linestyle='--', label="Último Dia")
    ax.plot([len(y_test_inv)-1, len(y_test_inv)], [y_test_inv[-1], predicted_next], 'go-', label="Previsão Amanhã")
    ax.set_xlim(len(y_test_inv)-60, len(y_test_inv)+1)
    ax.set_title(f"Previsões para {ticker}")
    ax.set_xlabel("Dias")
    ax.set_ylabel("Preço (USD)")
    ax.legend()
    fig.savefig(f"{ticker}_predictions.png")
    plt.close(fig)
    return fig

def direction_accuracy(y_true, y_pred):
    y_true_diff = np.diff(y_true.flatten())
    y_pred_diff = np.diff(y_pred.flatten())
    correct = np.sum((y_true_diff > 0) == (y_pred_diff > 0))
    return correct / (len(y_true_diff) - 1) if len(y_true_diff) > 1 else 0.0

def executar_previsao(ticker, exibir_log=True):
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        data = obter_dados(ticker)

        X, y, scaler = preprocessar_dados(data.values)
        train_size = int(len(X) * 0.7)
        val_size = int(len(X) * 0.15)

        X_train, X_val, X_test = X[:train_size], X[train_size:train_size+val_size], X[train_size+val_size:]
        y_train, y_val, y_test = y[:train_size], y[train_size:train_size+val_size], y[train_size+val_size:]

        X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
        X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
        y_val_tensor = torch.tensor(y_val, dtype=torch.float32)
        X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

        model = LSTMModel(input_size=X.shape[2], hidden_size=128, num_layers=2, output_size=1, dropout=0.2).to(device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.0003)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.8)

        epochs = 25
        best_val_loss = float('inf')
        patience, trigger = 7, 0
        best_model = None

        for epoch in range(epochs):
            model.train()
            epoch_loss = 0
            for xb, yb in train_loader:
                xb, yb = xb.to(device), yb.to(device)
                optimizer.zero_grad()
                out = model(xb)
                loss = criterion(out, yb)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            scheduler.step()

            model.eval()
            with torch.no_grad():
                val_out = model(X_val_tensor.to(device)).cpu().numpy()
                val_loss = mean_squared_error(y_val, val_out)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                trigger = 0
                best_model = model.state_dict()
            else:
                trigger += 1
                if trigger >= patience:
                    break

            if exibir_log and epoch % 5 == 0:
                print(f"Epoch {epoch}, Train Loss: {epoch_loss/len(train_loader):.4f}, Val Loss: {val_loss:.4f}")

        model.load_state_dict(best_model)
        model.eval()
        with torch.no_grad():
            predicted_prices = model(X_test_tensor.to(device)).cpu().numpy()
            mse = mean_squared_error(y_test, predicted_prices)
            rmse = np.sqrt(mse)
            dir_acc = direction_accuracy(y_test, predicted_prices)

            last_sequence = torch.tensor(X[-1].reshape(1, X.shape[1], X.shape[2]), dtype=torch.float32).to(device)
            predicted_next_scaled = model(last_sequence).cpu().numpy()
            predicted_next = scaler.inverse_transform(
                np.concatenate([predicted_next_scaled, np.zeros((1, X.shape[2]-1))], axis=1)
            )[0][0]

        preco_atual = float(data['Close'].iloc[-1])
        fig = plot_predictions(y_test, predicted_prices, scaler, data, ticker, predicted_next)

        return {
            "preco_atual": preco_atual,
            "previsao_amanha": predicted_next,
            "rmse": rmse,
            "acuracia": dir_acc,
            "grafico": fig
        }

    except Exception as e:
        raise RuntimeError(f"Erro: {e}")