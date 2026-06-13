import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

from app.db.client import SupabaseClient


def train_model():
    sb = SupabaseClient()
    dados = sb.get_view_all("vw_ocorrencias_por_ano_mes")
    
    if not dados:
        raise ValueError("Sem dados para treinar o modelo.")
        
    df = pd.DataFrame(dados)
    df.columns = [c.strip().lower() for c in df.columns]
    
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce")
    df["qtd_ocorrencias"] = pd.to_numeric(df["qtd_ocorrencias"], errors="coerce")
    df = df.dropna(subset=["ano", "mes", "qtd_ocorrencias"])
    
    df_encoded = pd.get_dummies(df, columns=["mes"], drop_first=False)
    
    feature_cols = ["ano"] + [c for c in df_encoded.columns if c.startswith("mes_")]
    X = df_encoded[feature_cols]
    y = df_encoded["qtd_ocorrencias"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model, feature_cols


def prever_incidencias_ano(ano_futuro: int) -> dict:
    model, feature_cols = train_model()
    
    meses = list(range(1, 13))
    anos = [ano_futuro] * 12
    
    df_test = pd.DataFrame({"ano": anos, "mes": meses})
    X_pred_encoded = pd.get_dummies(df_test, columns=["mes"], drop_first=False)
    
    for col in feature_cols:
        if col not in X_pred_encoded.columns:
            X_pred_encoded[col] = 0
            
    X_pred_encoded = X_pred_encoded[feature_cols]
    
    y_pred = model.predict(X_pred_encoded)
    
    y_pred = [max(0, int(round(val))) for val in y_pred]
    
    total_previsto = sum(y_pred)
    
    return {
        "ano": ano_futuro,
        "total_previsto": total_previsto,
        "previsoes_mensais": y_pred
    }


def gerar_grafico_previsao_mes_ano(ano_futuro: int) -> bytes:
    dados_previsao = prever_incidencias_ano(ano_futuro)
    y_pred = dados_previsao["previsoes_mensais"]
    
    nomes_meses = [
        "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
        "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
    ]
    
    df_pred = pd.DataFrame({
        "nome_mes": nomes_meses,
        "qtd_prevista": y_pred
    })
    
    sns.set_theme(style="whitegrid", palette="muted")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.barplot(
        data=df_pred,
        x="nome_mes",
        y="qtd_prevista",
        color="#D49A89",
        ax=ax,
    )
    
    for patch in ax.patches:
        patch.set_facecolor("#A569BD")
        patch.set_edgecolor("#7B2D8E")
    
    ax.set_xlabel("Mês", fontsize=13, fontweight="medium")
    ax.set_ylabel("Previsão de Incidências", fontsize=13, fontweight="medium")
    ax.set_title(f"Previsão de Incidências por Mês - Ano Hipotético: {ano_futuro}", fontsize=14, fontweight="bold", pad=20, color="black")
    ax.tick_params(axis="both", labelsize=11)
    
    for p in ax.patches:
        height = p.get_height()
        if pd.notna(height) and height > 0:
            ax.annotate(
                f"{int(height):,}".replace(",", "."),
                (p.get_x() + p.get_width() / 2., height),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color="black",
                xytext=(0, 4),
                textcoords="offset points",
            )
            
    y_max = df_pred["qtd_prevista"].max()
    if pd.notna(y_max):
        padding = y_max * 0.15 if y_max > 0 else 100
        ax.set_ylim(0, y_max + padding)
            
    sns.despine(left=True, bottom=True)
    fig.tight_layout()
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
