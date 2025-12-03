# 4. 🔬 Tunning e Modelo de Regressão Logística Final

Nesta etapa, o modelo de Regressão Logística escolhido na Etapa 3 é **otimizado** usando pesquisa de hiperparâmetros e, em seguida, validado no conjunto de Teste Out-of-Time (OOT).

---

## 4.1. ⚙️ Estratégia de Otimização

O modelo foi otimizado utilizando o **RandomizedSearchCV**, buscando maximizar o KS Score, uma métrica crítica para separação de risco

O processo de tunning focou na regularização do modelo para evitar overfitting e garantir a robustez.

**Melhores Parâmetros Encontrados:**

| Parâmetro | Valor Otimizado |
| :--- | :---: |
| **`n_estimators`** | 800 |
| **`learning_rate`** | 0.01 |
| **`subsample`** | 0.7 |
| **`reg_alpha` / `reg_lambda`** | 0.0 / 0.0 |

---

## 4.2. 🎯 Performance Final do LightGBM (Teste OOT)

O modelo otimizado foi treinado na base completa de Treino e avaliado no conjunto de Teste OOT, confirmando seu potencial máximo.

| Métrica | Valor |
| :--- | :---: |
| **KS** | 0.313688 |
| **AUC** | 0.708333 |
| **Gini** | 0.416665 |

Após o tunning, o LightGBM alcançou o melhor desempenho absoluto no Teste OOT, com **AUC** de **0.708** e **Gini** de **0.417**. Este resultado supera o modelo de Regressão Logística (AUC 0.701) e confirma o **LightGBM como o modelo mais preditivo para o modelo.**