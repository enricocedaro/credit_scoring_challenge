# Credit Scoring Challenge

Este repositório contém a solução desenvolvida para um case técnico de **Ciência de Dados**, focado na construção de um modelo de **Credit Scoring**.  

---

## 🎯 Objetivo do Projeto

1. Desenvolver um modelo para predizer a variável target
2. Justificar o algoritmo e parâmetros utilizados
3. Apresentar métricas de performance do modelo
4. Explicar e apresentar os resultados

---

## 📁 Organização do Repositório

```
.
├── data/
│   ├── raw/           # Dados originais fornecidos no desafio
│   ├── processed/     # Bases tratadas e prontas para modelagem
├── models/            # Modelos treinados, artefatos e objetos serializados
├── notebooks/
│   ├── 01_ exploratory_data_analysis.ipynb # Exploração inicial dos dados
│   ├── 02_feature_engineering.ipynb # Criação/seleção de variáveis
│   ├── 03_model_training.ipynb         # Treino, tuning e comparação de modelos
│   └── 04_tunning.ipynb # Tunning do modelo
│   └── 05_tunning.ipynb # Análises finais e gráficos
├── reports/
│   ├── figures/       # Imagens e gráficos gerados
│   └── quarto/        # Ferramenta para visualização
├── src/               # utils.py e funções auxiliaress
├── requirements.txt   # Dependências do projeto
└── README.md
```

## ⚙️ Como Reproduzir o Projeto

### 1. Criar e ativar ambiente virtual
```bash
python -m venv venv
```

#### Linux / MacOS
```bash
source venv/bin/activate  # Linux/Mac
```

#### Windows
```bash
venv\Scripts\activate     # Windows
```


### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```


### 3. Executar o projeto

Rodar os notebooks presentes em _notebooks/_ na ordem indicada no início de cada arquivo

### 4. Relatório final

O relatório está presente no link https://enricocedaro.github.io/credit_scoring_challenge/

Obs.:_Não sera aplicada uma licença, qualquer reutilização deve preservar o contexto original do case e a autoria do código._