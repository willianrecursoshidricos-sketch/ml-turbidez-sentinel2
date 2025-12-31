"""
correlacao.py
-------------
Análise de correlação entre turbidez, parâmetros ambientais
e bandas espectrais do Sentinel-2.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from itertools import product
from pathlib import Path

DATA_PATH = Path("../data/dados_turbidez.xlsx")
FIGURES_PATH = Path("../figures")
FIGURES_PATH.mkdir(exist_ok=True)

PARAMETROS = [
    "chla", "feofitina", "sst", "st", "sdt", "turbidez", "cor verdadeira"
]

BANDAS = [
    "banda442", "banda492", "banda559", "banda665", "banda704",
    "banda739", "banda780", "banda833", "banda864",
    "banda1610", "banda2186"
]

def carregar_dados():
    df = pd.read_excel(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    return df

def pearson_ic(x, y, alpha=0.05):
    r, _ = pearsonr(x, y)
    n = len(x)
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    z_crit = 1.96
    lo = np.tanh(z - z_crit * se)
    hi = np.tanh(z + z_crit * se)
    return r, lo, hi

def matriz_dispersao(df):
    resultados = []

    for param, banda in product(PARAMETROS, BANDAS):
        dados = df[[param, banda]].dropna()
        if len(dados) < 10:
            continue

        r, lo, hi = pearson_ic(dados[param], dados[banda])
        resultados.append({
            "Parametro": param,
            "Banda": banda,
            "Pearson_r": r,
            "IC_inf": lo,
            "IC_sup": hi
        })

        plt.figure(figsize=(4, 4))
        plt.scatter(dados[banda], dados[param], alpha=0.7)
        plt.xlabel(banda)
        plt.ylabel(param)
        plt.title(
            f"{param} vs {banda}\n"
            f"r = {r:.2f} | IC95% [{lo:.2f}, {hi:.2f}]"
        )
        plt.tight_layout()
        plt.savefig(
            FIGURES_PATH / f"disp_{param}_{banda}.png",
            dpi=300
        )
        plt.close()

    return pd.DataFrame(resultados)

if __name__ == "__main__":
    df = carregar_dados()
    tabela_corr = matriz_dispersao(df)
    tabela_corr.to_excel(
        FIGURES_PATH / "correlacao_parametros_bandas.xlsx",
        index=False
    )
    print("Análise de correlação finalizada com sucesso.")
