# Estimativa da Turbidez da Água com Sentinel-2 e Machine Learning

Este projeto apresenta o desenvolvimento de modelos de Machine Learning para estimar a turbidez da água (NTU)
a partir de bandas espectrais do satélite Sentinel-2.

## Objetivo
Avaliar o potencial de bandas espectrais individuais, combinações de bandas e razões espectrais
na predição da turbidez da água, com aplicação em ambientes aquáticos continentais.

## Base de Dados
- Dados in situ de qualidade da água (turbidez, clorofila-a, feofitina, SST, ST, SDT e cor verdadeira)
- Bandas espectrais do satélite Sentinel-2

## Metodologia
- Análise exploratória dos dados (EDA)
- Estatísticas descritivas da turbidez
- Análise de correlação entre parâmetros ambientais e bandas espectrais
- Modelagem preditiva utilizando:
  - Random Forest
  - Support Vector Machine (SVM)
  - Decision Tree
- Avaliação dos modelos com:
  - RMSE
  - MAPE
  - Correlação de Pearson
- Geração de mapas espaciais de turbidez

## Tecnologias Utilizadas
- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- Sensoriamento Remoto (Sentinel-2)

## Autor
**Willian Geraldo da Silva**  
Engenheiro Ambiental e Sanitarista  
Ciência de Dados e Machine Learning Aplicado a Recursos Hídricos
