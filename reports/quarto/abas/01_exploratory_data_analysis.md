# 1. 📄 Análise Exploratória de Dados (EDA)

Este capítulo apresenta a **exploração da base de dados**, a definição da **separação de teste e treino** e as análises iniciais de qualidade e distribuição de risco.  

---

## 1.1. 🎯 Definição do Target e Distribuição da Amostra

A base de dados bruta contém **10.738 observações** e **81 colunas** (incluindo id, safra e features).

**Definição da Variável Alvo (y)** - não tem nulos

>y = 1 (Mau Pagador): **Inadimplência (default)**
>
>y = 0 (Bom Pagador): **Não-inadimplência**

A Taxa de **Inadimplência Global** da amostra é de **29,13%**.

| Classe | Contagem Absoluta | Proporção |
| :--- | :--- | :--- |
| 0 (Bom Pagador) | 7.610 | 70,87% |
| 1 (Mau Pagador) | 3.128 | 29,13% |

---

## 1.2. 📈 Estabilidade Temporal da Inadimplência (Análise por Safra)

A análise do risco ao longo do tempo (safra) é crucial em crédito. A base abrange **12 meses**, de 01/2014 a 12/2014.

O gráfico abaixo mostra a variação da taxa de inadimplência (média de y) em cada safra.

![](../images/image-1.png)

A taxa de inadimplência demonstra uma **tendência de aumento nas safras finais** (11/2014 e 12/2014), atingindo o pico de **35,24%** na última safra. Este pico é significativamente maior do que a média da amostra (29,13%), sugerindo uma possível instabilidade temporal ou uma mudança no perfil de risco dos clientes mais recentes.

---

## 1.3. 📈 Estabilidade das Variáveis por Safra

Para garantir que o modelo de Credit Scoring seja robusto ao longo do tempo, é essencial monitorar as features mais preditivas e verificar se suas distribuições se mantêm estáveis ao longo das safras.

Gráfico de estabilidade da **VAR_1**:

![](../images/image-4.png)

---

## 1.4. 🛠️ Qualidade e Saúde dos Dados (Valores Ausentes)

A qualidade dos dados foi avaliada, com foco na presença de valores ausentes (Missing Values).

**Total de Features Analisadas:** 78
**Amostra Total:** 10.738 linhas

![](../images/image.png)

**Conclusão e Próxima Etapa:** Há uma grande quantidade de variáveis com uma alta percentagem de valores ausentes (mais de 50%). Na fase 02_feature_engineering.ipynb, será necessário definir um limite de corte para descarte de variáveis.

---

## 1.5. 🛠️ Seleção da base (treino e teste)

**Separação temporal entre treino e teste:**

Embora a base permita uma divisão aleatória entre treino e teste, optei por utilizar a variável safra para construir um cenário mais próximo do uso real do modelo em produção.

Além disso foi considerado a inadimplência das safras, com as últimas sendo "piores".

Treino: safra <= 2024-09 (28% de default médio)

Teste out-of-time: safra > 2024-09 (32% de default médio)

---