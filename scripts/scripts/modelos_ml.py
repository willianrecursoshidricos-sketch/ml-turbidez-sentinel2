"""
modelos_ml.py
-------------
Treinamento e avaliação de modelos de Machine Learning
para estimativa da turbidez da água (NTU) usando Sentinel-2.
"""

import pandas as pd
import numpy as np
import itertools
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from scipy.stats import zscore

# ======================================================
# CONFIGURAÇÕES
# ======================================================

DATA_PATH = Path("../data/dados_turbidez.xlsx")
RESULTS_PATH = Path("../results")
RESULTS_PATH.mkdir(exist_ok=True)

TARGET = "turbidez"

BANDAS = [
    "banda442", "banda492", "banda559", "banda665", "banda704",
    "banda739", "banda780", "banda833", "banda864",
    "banda1610", "banda2186"
]

MODELOS = {
    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42
    ),
    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),
    "SVM": SVR(kernel="linear")
}

# ======================================================
# FUNÇÕES
# ======================================================

def carregar_dados():
    df = pd.read_excel(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    return df


def gerar_razoes_bandas(df, bandas):
    ratios = {}
    for b1, b2 in itertools.combinations(bandas, 2):
        nome = f"{b1}/{b2}"
        ratios[nome] = df[b1] / df[b2]
    return pd.DataFrame(ratios)


def calcular_metricas(y_true, y_pred):
    r = np.corrcoef(y_true, y_pred)[0, 1]
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return r, rmse, mape


def avaliar_modelo(X, y, modelo, nome_feature, nome_modelo, scenario):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    r, rmse, mape = calcular_metricas(y_test, y_pred)

    return {
        "Feature": nome_feature,
        "Modelo": nome_modelo,
        "Scenario": scenario,
        "Pearson_r": r,
        "RMSE": rmse,
        "MAPE": mape
    }

# ======================================================
# EXECUÇÃO PRINCIPAL
# ======================================================

if __name__ == "__main__":

    df = carregar_dados()

    # ---------- COM OUTLIERS ----------
    resultados = []

    ratios = gerar_razoes_bandas(df, BANDAS)
    df_all = pd.concat([df, ratios], axis=1)

    y = df[TARGET]

    # Bandas individuais
    for banda in BANDAS:
        X = df[[banda]].values
        for nome, modelo in MODELOS.items():
            resultados.append(
                avaliar_modelo(X, y, modelo, banda, nome, "Com Outliers")
            )

    # Razões de bandas
    for ratio in ratios.columns:
        X = ratios[[ratio]].values
        for nome, modelo in MODELOS.items():
            resultados.append(
                avaliar_modelo(X, y, modelo, ratio, nome, "Com Outliers")
            )

    # Todas as bandas
    X_all = df_all[BANDAS + list(ratios.columns)].values
    for nome, modelo in MODELOS.items():
        resultados.append(
            avaliar_modelo(X_all, y, modelo, "Todas Bandas", nome, "Com Outliers")
        )

    # ---------- SEM OUTLIERS ----------
    z = zscore(df[TARGET])
    df_filt = df[np.abs(z) <= 3]

    ratios_filt = gerar_razoes_bandas(df_filt, BANDAS)
    df_all_filt = pd.concat([df_filt, ratios_filt], axis=1)

    y_f = df_filt[TARGET]

    for banda in BANDAS:
        X = df_filt[[banda]].values
        for nome, modelo in MODELOS.items():
            resultados.append(
                avaliar_modelo(X, y_f, modelo, banda, nome, "Sem Outliers")
            )

    for ratio in ratios_filt.columns:
        X = ratios_filt[[ratio]].values
        for nome, modelo in MODELOS.items():
            resultados.append(
                avaliar_modelo(X, y_f, modelo, ratio, nome, "Sem Outliers")
            )

    X_all_f = df_all_filt[BANDAS + list(ratios_filt.columns)].values
    for nome, modelo in MODELOS.items():
        resultados.append(
            avaliar_modelo(X_all_f, y_f, modelo, "Todas Bandas", nome, "Sem Outliers")
        )

    # ======================================================
    # SALVAR RESULTADOS
    # ======================================================

    resultados_df = pd.DataFrame(resultados)

    resultados_df.to_excel(
        RESULTS_PATH / "resultados_modelos.xlsx",
        index=False
    )

    top10 = resultados_df.sort_values("RMSE").head(10)
    top10.to_excel(
        RESULTS_PATH / "top10_modelos.xlsx",
        index=False
    )

    print("Modelagem finalizada com sucesso.")
