# 5. 🚀 Validação do Modelo Final (LightGBM)

Esta fase consolida a **performance do modelo LightGBM tunado**, analisando em profundidade a separação de risco (ROC/KS), a distribuição do score (Taxa de Evento por Quantil) e a calibração da probabilidade de default no conjunto de Teste OOT.

---

## 5.1. 📊 Métricas de Desempenho Finais

O modelo final (LightGBM) foi avaliado em ambos os conjuntos.

| Base | AUC | KS | Gini | Accuracy | Precision | Recall | F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Teste (OOT)** | **0.708** | **0.314** | **0.417** | 0.694 | 0.589 | 0.159 | 0.250 |

---

## 5.2. 📊 Curvas de Ranqueamento

### 5.2.1. Curva ROC:

A Curva ROC no Teste OOT confirma o poder de ranqueamento, com um AUC de 0.708.

![](../images/image-3.png)


### 5.2.2. Curva KS:

O KS Score de 0.314 indica que a separação máxima entre a distribuição acumulada de Bons e Maus Pagadores é de 31.4%, um resultado satisfatório.

![](../images/image-5.png)

---

## 5.3. 📉 Taxa de Evento por Quantil (Lift Analysis)

A análise por quantis (decis) é a tradução mais direta do poder de ranqueamento para o negócio, mostrando a concentração de risco.

O gráfico de Taxa de Evento compara a frequência observada de default por faixas de score (quantis) no Treino e no Teste OOT.

![](../images/image-6.png)

O gráfico mostra que o modelo está conseguindo organizar bem a carteira em faixas de risco. A medida que vamos do quantil 1 para o quantil 10, tanto no treino quanto na validação a taxa de inadimplência aumenta, indicando que scores piores de fato concentram clientes mais problemáticos. As curvas de treino e validação não são idênticas, mas o padrão crescente se mantém.

---

## 5.4. ⚖️ Estabilidade Temporal do KS e Calibração

**KS por Safra**

A análise do KS mês a mês (por safra) é a verificação mais rigorosa da estabilidade preditiva ao longo do tempo.

![](../images/image-7.png)


O KS no Teste OOT (safras 10/2014 a 12/2014) mostra uma queda de performance na última safra (12/2014). Isso pode ser um sinal de mudança no mercado ou mudança de política de crédito.

**Curva de Calibração**

A curva de calibração verifica se a probabilidade prevista (P(Default)) corresponde à frequência real de default observada.

![](../images/image-8.png)

O modelo ranqueia bem e tem uma calibração aceitável nas faixas centrais, mas tende a subestimar a inadimplência tanto nos clientes de risco baixo (especialmente em validação) quanto, principalmente, nos de maior risco em treino. Faz sentido aplicar uma etapa extra de recalibração (Platt, isotônica ou ajuste por faixas de score).

## 5.5. PSI 

Na análise de estabilidade das variáveis entre o período de treino e o período de teste, utilizamos o Population Stability Index (PSI), calculado a partir da distribuição das features no conjunto de desenvolvimento (treino) em comparação com o conjunto de teste. Seguindo a prática de mercado, interpretamos os valores de PSI da seguinte forma:

PSI < 0,10 → variável estável;

0,10 ≤ PSI ≤ 0,25 → mudança moderada;

PSI > 0,25 → mudança severa na distribuição.

A maior parte das variáveis do modelo apresentou PSI baixo ou moderado, indicando comportamento relativamente estável entre os períodos. No entanto, duas variáveis chamaram atenção: VAR_53 e VAR_54, com PSI acima de 0,6, respectivamente, claramente acima do limiar de mudança severa.

Elas são reconhecidamente instáveis, sendo recomendável retirar elas do treinamento.