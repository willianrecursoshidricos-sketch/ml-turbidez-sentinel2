"""
CorrelacaoTurbidez.py
-------------
Matriz de Dispersão entre Turbidez (NTU) e Bandas Espectrais do Sentinel-2,
incluindo Correlação de Pearson e Intervalo de Confiança de 95%.

Este script gera a figura:
- figures/matriz_dispersao_turbidez_bandas.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import math

# =====================================================
# CONFIGURAÇÕES
# =====================================================

DATA_PATH = "../data/dados_turbidez.xlsx"
OUTPUT_FIG = "../figures/matriz_dispersao_turbidez_bandas.png"

TARGET = "turbidez"

BANDAS = [
    "banda442", "banda492", "banda559", "banda665",
    "banda704", "banda739", "banda780",
    "banda833", "banda864", "banda1610", "banda2186"
]

# =====================================================
# FUNÇÃO: INTERVALO DE CONFIANÇA (FISHER Z)
# =====================================================

def pearson_ic95(r, n):
    if abs(r) >= 1:
        return r, r

    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    z_crit = 1.96

    lo = np.tanh(z - z_crit * se)
    hi = np.tanh(z + z_crit * se)

    return lo, hi

# =====================================================
# CARREGAR DADOS
# =====================================================

df = pd.read_excel(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()

# =====================================================
# CONFIGURAÇÃO DA FIGURA
# =====================================================

n_bandas = len(BANDAS)
cols = 4
rows = math.ceil(n_bandas / cols)

fig, axes = plt.subplots(rows, cols, figsize=(18, 4 * rows))
axes = axes.flatten()

# =====================================================
# LOOP DE DISPERSÃO + CORRELAÇÃO
# =====================================================

for i, banda in enumerate(BANDAS):
    ax = axes[i]

    x = df[banda]
    y = df[TARGET]

    mask = x.notna() & y.notna()
    x = x[mask]
    y = y[mask]

    r, _ = pearsonr(x, y)
    r_lo, r_hi = pearson_ic95(r, len(x))

    ax.scatter(x, y, alpha=0.7, s=20)
    ax.set_xlabel(banda)
    ax.set_ylabel("Turbidez (NTU)")

    ax.text(
        0.05, 0.95,
        f"r = {r:.2f}\nIC95% [{r_lo:.2f}, {r_hi:.2f}]",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

# Remover eixos vazios
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# =====================================================
# FINALIZAÇÃO
# =====================================================

fig.suptitle(
    "Matriz de Dispersão — Turbidez vs Bandas Espectrais\n"
    "Correlação de Pearson com Intervalo de Confiança de 95%",
    fontsize=16
)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(OUTPUT_FIG, dpi=300)
plt.close()

print(f"Figura gerada com sucesso: {OUTPUT_FIG}")
