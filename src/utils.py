# src/utils.py
"""
Funções utilitárias usadas no projeto de Credit Scoring.

Inclui:
- Métricas de performance (KS, AUC, Gini).
- Construção de tabelas por quantil de score.
- KS "seguro" para uso em groupby (ex.: por safra).
- Cálculo de PSI (Population Stability Index) por feature e por dataframe.
"""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# =========================
# MÉTRICAS
# =========================


def ks_score(y_true, y_proba) -> float:
    """
    Calcula o KS (Kolmogorov-Smirnov) entre bons (0) e maus (1)
    a partir das probabilidades previstas.

    Parâmetros
    ----------
    y_true : array-like
        Labels verdadeiros (0 = bom, 1 = mau).
    y_proba : array-like
        Probabilidades previstas de ser mau (1).

    Retorno
    -------
    float
        Valor do KS (entre 0 e 1).
    """
    data = (
        pd.DataFrame({"y": y_true, "score": y_proba})
        .sort_values("score", ascending=False)
    )

    total_bad = (data["y"] == 1).sum()
    total_good = (data["y"] == 0).sum()

    if total_bad == 0 or total_good == 0:
        return 0.0

    data["cum_bad"] = (data["y"] == 1).cumsum() / total_bad
    data["cum_good"] = (data["y"] == 0).cumsum() / total_good

    ks = (data["cum_bad"] - data["cum_good"]).abs().max()
    return float(ks)


def performance_metrics(y_true, y_proba):
    """
    Calcula KS, AUC e Gini a partir das probabilidades previstas.

    Parâmetros
    ----------
    y_true : array-like
        Labels verdadeiros (0/1).
    y_proba : array-like
        Probabilidades previstas de ser 1.

    Retorno
    -------
    tuple
        (ks, auc, gini)
    """
    y_true = np.array(y_true)
    y_proba = np.array(y_proba)

    auc = roc_auc_score(y_true, y_proba)
    ks = ks_score(y_true, y_proba)
    gini = 2 * auc - 1

    return float(ks), float(auc), float(gini)


def full_performance_metrics(y_true, y_proba, threshold: float = 0.5) -> dict:
    """
    Calcula um conjunto completo de métricas de classificação
    a partir das probabilidades previstas.

    Parâmetros
    ----------
    y_true : array-like
        Labels verdadeiros (0/1).
    y_proba : array-like
        Probabilidades previstas de ser 1.
    threshold : float, default=0.5
        Limiar para converter probabilidade em classe prevista.

    Retorno
    -------
    dict
        Dicionário com:
        - AUC, KS, Gini
        - Accuracy, Precision, Recall, F1
        - TP, TN, FP, FN
    """
    y_true = np.array(y_true)
    y_proba = np.array(y_proba)
    y_pred = (y_proba >= threshold).astype(int)

    # métricas de rankeamento
    auc = roc_auc_score(y_true, y_proba)
    ks = ks_score(y_true, y_proba)
    gini = 2 * auc - 1

    # métricas de classificação binária
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "AUC": float(auc),
        "KS": float(ks),
        "Gini": float(gini),
        "Accuracy": float(acc),
        "Precision": float(prec),
        "Recall": float(rec),
        "F1": float(f1),
        "TP": int(tp),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
    }


# =========================
# TABELAS POR QUANTIL
# =========================


def construct_metrics_table(
    df: pd.DataFrame,
    quantil_col: str,
    score_col: str,
    target_col: str,
    ordered_labels: List[str],
) -> pd.DataFrame:
    """
    Constrói tabela com volume, taxa de evento e faixa de score por quantil.

    Usada na análise de 'Taxa de Evento por Quantil'.

    Parâmetros
    ----------
    df : DataFrame
        DataFrame com as colunas de quantil, score e target.
    quantil_col : str
        Nome da coluna que identifica o quantil (ex.: 'quantil_score').
    score_col : str
        Nome da coluna de score/probabilidade.
    target_col : str
        Nome da coluna alvo (0/1).
    ordered_labels : list of str
        Lista de rótulos ordenados dos quantis (ex.: ['Quantil_1', ..., 'Quantil_10']).

    Retorno
    -------
    DataFrame
        Colunas:
        - quantil_col
        - volume
        - event_rate
        - score_min
        - score_max
    """
    tabela = (
        df.groupby(quantil_col)
        .agg(
            volume=(target_col, "size"),
            event_rate=(target_col, "mean"),
            score_min=(score_col, "min"),
            score_max=(score_col, "max"),
        )
        .reset_index()
    )

    # garantir ordem dos rótulos
    tabela[quantil_col] = pd.Categorical(
        tabela[quantil_col],
        categories=ordered_labels,
        ordered=True,
    )
    tabela = tabela.sort_values(quantil_col)

    return tabela


# =========================
# KS POR GRUPO
# =========================


def ks_safe(y_true, y_proba) -> float:
    """
    Versão do KS que retorna NaN quando não há pelo menos
    um bom e um mau. Útil para groupby por safra/segmento.

    Parâmetros
    ----------
    y_true : array-like
        Labels verdadeiros (0/1).
    y_proba : array-like
        Probabilidades previstas de ser 1.

    Retorno
    -------
    float
        KS calculado ou NaN se não há pelo menos um bom e um mau.
    """
    y_arr = np.array(y_true)
    if (y_arr == 1).sum() == 0 or (y_arr == 0).sum() == 0:
        return np.nan
    return ks_score(y_true, y_proba)


# =========================
# PSI (Population Stability Index)
# =========================


def psi_for_feature(
    train: pd.Series, test: pd.Series, n_bins: int = 10
) -> float:
    """
    Calcula o PSI de uma feature contínua/categorizada, usando bins baseados no treino.

    Parâmetros
    ----------
    train : Series
        Valores da feature no conjunto de treino.
    test : Series
        Valores da feature no conjunto de teste/validação.
    n_bins : int, default=10
        Número de bins (quantis) usados para o cálculo.

    Retorno
    -------
    float
        Valor do PSI para a feature.
    """
    # Remove NaN
    train = train.dropna()
    test = test.dropna()

    # Definir bins com base no treino (quantis)
    quantiles = np.linspace(0, 1, n_bins + 1)
    bin_edges = np.unique(np.quantile(train, quantiles))

    # Se der menos de 2 edges únicos, PSI = 0 (sem variação)
    if len(bin_edges) < 2:
        return 0.0

    train_bins = pd.cut(train, bins=bin_edges, include_lowest=True)
    test_bins = pd.cut(test, bins=bin_edges, include_lowest=True)

    train_dist = train_bins.value_counts(normalize=True).sort_index()
    test_dist = test_bins.value_counts(normalize=True).sort_index()

    # Alinha índices
    test_dist = test_dist.reindex(train_dist.index).fillna(0.0)

    # Evitar log(0)
    epsilon = 1e-6
    train_dist = train_dist.clip(epsilon, 1)
    test_dist = test_dist.clip(epsilon, 1)

    psi_values = (train_dist - test_dist) * np.log(train_dist / test_dist)
    return float(psi_values.sum())


def psi_for_dataframe(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    feature_cols: List[str],
    n_bins: int = 10,
) -> pd.Series:
    """
    Calcula o PSI para múltiplas colunas de um DataFrame.

    Parâmetros
    ----------
    df_train : DataFrame
        Conjunto de treino.
    df_test : DataFrame
        Conjunto de teste/validação.
    feature_cols : list of str
        Lista de colunas para calcular o PSI.
    n_bins : int, default=10
        Número de bins usados por feature.

    Retorno
    -------
    Series
        Série com PSI por coluna (ordenada descendentemente).
    """
    psi_dict = {}
    for col in feature_cols:
        psi_dict[col] = psi_for_feature(df_train[col], df_test[col], n_bins=n_bins)
    return pd.Series(psi_dict).sort_values(ascending=False)
