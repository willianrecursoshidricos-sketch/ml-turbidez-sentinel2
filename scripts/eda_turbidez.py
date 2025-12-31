"""
eda_turbidez.py
----------------
Análise exploratória e estatísticas descritivas da turbidez da água
a partir de dados in situ associados ao Sentinel-2.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path("../data/dados_turbidez.xlsx")
FIGURES_PATH = Path("../figures")
FIGURES_PATH.mkdir(exist_ok=True)

def carregar_dados(caminho):
    df = pd.read_excel(caminho)
    df.columns = df.columns.str.strip().str.lower()
    df["date"] = pd.to_datetime(df["date"])
    df["ano"] = df["date"].dt.year
    return df

def estatisticas_descritivas(df):
    stats = df["turbidez"].describe()
    stats_extra = {
        "variancia": df["turbidez"].var(),
        "coef_var_%": (df["turbidez"].std() / df["turbidez"].mean()) * 100,
        "assimetria": df["turbidez"].skew(),
        "curtose": df["turbidez"].kurtosis()
    }
    return pd.concat([stats, pd.Series(stats_extra)])

def plot_histograma(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df["turbidez"], bins=20, kde=True)
    plt.xlabel("Turbidez (NTU)")
    plt.ylabel("Frequência")
    plt.title("Distribuição da Turbidez")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "histograma_turbidez.png", dpi=300)
    plt.close()

def plot_boxplot_por_ano(df):
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="ano", y="turbidez", data=df)
    plt.xlabel("Ano")
    plt.ylabel("Turbidez (NTU)")
    plt.title("Distribuição Anual da Turbidez")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "boxplot_turbidez_por_ano.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    dados = carregar_dados(DATA_PATH)
    stats = estatisticas_descritivas(dados)
    stats.to_csv(FIGURES_PATH / "estatisticas_descritivas_turbidez.csv")
    plot_histograma(dados)
    plot_boxplot_por_ano(dados)
    print("Análise exploratória concluída com sucesso.")
