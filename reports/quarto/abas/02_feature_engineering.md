# ⚙️ 2. Feature Engineering e Seleção de Variáveis

Esta seção detalha as **técnicas de pré-processamento e seleção** aplicadas para garantir um conjunto de features robusto e de alta qualidade para a modelagem. O objetivo é remover ruídos, redundâncias e variáveis instáveis.

---

## 2.1. 🧹 Filtragem Inicial (Missing, Constantes e IDs)

O primeiro passo foi remover variáveis que não agregam valor preditivo ou que apresentam alta incerteza devido à falta de dados.

**Critério de Descarte adotado para Missing Values:** Variáveis com mais de 60% de valores ausentes foram descartadas.

| Tipo de Variável Removida | Contagem | Exemplo | Justificativa |
| :--- | :---: | :--- | :--- |
| **Alto Missing** (>60%) | **19** | `VAR_62`, `VAR_70`, etc. | Alta incerteza e baixa confiabilidade estatística. |
| **Constante** | 0 | N/A | Não há variáveis com valor único. |
| **ID-Like** | 1 | `ID_COL` | Variáveis únicas por linha não carregam informação generalizável. |


**19 features foram removidas**, resultando em **62** features restantes para a análise (81 originais - 19 removidas).

---

## 2.2. 🗂️ Classificação de Variáveis (Categóricas vs. Numéricas)

A classificação correta das variáveis é uma **etapa essencial** para garantir que o pré-processamento subsequente seja aplicado de forma adequada (ex: One-Hot Encoding para categóricas, Scaling para numéricas).

### 2.2.1. Metodologia por Cardinalidade

Dada a **natureza mascarada das features**, a distinção entre variáveis contínuas e discretas foi feita utilizando a **Cardinalidade** (número de valores únicos) como critério principal.

**Threshold Definido:** Foi estabelecido um threshold de **25** valores únicos.

>**Variáveis Categóricas (CAT_VARS):** Features com até 25 valores únicos foram classificadas como categóricas, pois representam um conjunto discreto e gerenciável de classes.
>
>**Variáveis Numéricas (NUM_VARS):** Features com mais de 25 valores únicos foram classificadas como numéricas, indicando uma distribuição de dados contínua ou de alta variância.

### 2.2.2. Conversão de Tipo

Após a classificação, as features em **CAT_VARS** foram explicitamente convertidas para o tipo object (tipo Python para string ou categoria). Esta conversão é necessária para garantir que os pipelines de pré-processamento (como OneHotEncoder) as tratem corretamente, independentemente de seu tipo original.

---

## 2.3. 📉 Filtragem por Baixa Variância e Duplicatas

Variáveis com baixíssima variação (proximidade de valor constante) não distinguem bem os clientes e são removidas.

**Baixa Variância:** Foi definido um threshold de 0.001. Apenas **1** feature foi removida por ter variância muito próxima de zero.

A base não possui colunas duplicadas.

---

## 2.4. 🔗 Tratamento de Multicolinearidade (Alta Correlação)

A multicolinearidade entre features numéricas é **prejudicial** para a modelagem, pois torna os coeficientes do modelo instáveis e difíceis de interpretar.

**Critério de Descarte:** Manter apenas **uma** variável de cada par que apresentava correlação absoluta superior a 0.9 na base de Treino.

| var1 | var2 | corr |
| :--- | :--- | :---: |
| `VAR_19` | `VAR_22` | 0.975977 |
| `VAR_10` | `VAR_69` | 0.975103 |
| `VAR_24` | `VAR_58` | 0.974130 |
| `VAR_39` | `VAR_45` | 0.972208 |
| `VAR_14` | `VAR_26` | 0.954847 |


**5 features foram removidas** devido à alta correlação. O conjunto de dados final possui 56 features candidatas (61 restantes - 5 removidas).

---