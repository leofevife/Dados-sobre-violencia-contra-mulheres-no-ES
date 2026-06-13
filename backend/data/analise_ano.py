import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from app.db.client import SupabaseClient


def gerar_grafico_incidencias_ano() -> bytes:
    sb = SupabaseClient()
    dados = sb.get_view_all("vw_ocorrencias_por_ano")

    df = pd.DataFrame(dados)
    df.columns = [c.strip().lower() for c in df.columns]

    col_ano = "ano"
    col_qtd = "qtd_ocorrencias"

    df[col_ano] = pd.to_numeric(df[col_ano], errors="coerce")
    df[col_qtd] = pd.to_numeric(df[col_qtd], errors="coerce")
    df = df.dropna(subset=[col_ano, col_qtd])
    df = df.sort_values(col_ano)

    sns.set_theme(style="whitegrid", palette="muted")
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=df,
        x=col_ano,
        y=col_qtd,
        marker="o",
        linewidth=2.5,
        markersize=8,
        color="#7B2D8E",
        ax=ax,
    )

    ax.fill_between(df[col_ano], df[col_qtd], alpha=0.15, color="#7B2D8E")

    ax.set_xlabel("Ano", fontsize=13, fontweight="medium")
    ax.set_ylabel("Quantidade de Incidências", fontsize=13, fontweight="medium")

    anos = df[col_ano].astype(int).tolist()
    ax.set_xticks(anos)
    ax.set_xticklabels([str(a) for a in anos])
    ax.tick_params(axis="both", labelsize=11)

    for x_val, y_val in zip(df[col_ano], df[col_qtd]):
        ax.annotate(
            f"{int(y_val):,}".replace(",", "."),
            (x_val, y_val),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=10,
            fontweight="bold",
            color="#4A1A5E",
        )

    y_min, y_max = df[col_qtd].min(), df[col_qtd].max()
    padding = (y_max - y_min) * 0.15 if y_max > y_min else 1000
    ax.set_ylim(y_min - padding, y_max + padding)

    sns.despine(left=True, bottom=True)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def obter_anos_disponiveis() -> list:
    sb = SupabaseClient()
    dados = sb.get_view_all("vw_ocorrencias_por_ano_mes")
    if not dados:
        return []
        
    df = pd.DataFrame(dados)
    df.columns = [c.strip().lower() for c in df.columns]
    
    anos = df["ano"].dropna().unique().astype(int).tolist()
    return sorted(anos, reverse=True)


def gerar_grafico_incidencias_mes_ano(ano: int) -> bytes:
    sb = SupabaseClient()
    dados = sb.get_view_all("vw_ocorrencias_por_ano_mes")
    
    df = pd.DataFrame(dados)
    df.columns = [c.strip().lower() for c in df.columns]
    
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce")
    df["qtd_ocorrencias"] = pd.to_numeric(df["qtd_ocorrencias"], errors="coerce")
    
    df = df[df["ano"] == ano].copy()
    df = df.sort_values("mes")
    
    sns.set_theme(style="whitegrid", palette="muted")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.barplot(
        data=df,
        x="nome_mes",
        y="qtd_ocorrencias",
        color="#7B2D8E",
        ax=ax,
    )
    
    ax.set_xlabel("Mês", fontsize=13, fontweight="medium")
    ax.set_ylabel("Quantidade de Incidências", fontsize=13, fontweight="medium")
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
                color="#4A1A5E",
                xytext=(0, 4),
                textcoords="offset points",
            )
            
    # Ajustando o limite superior para não cortar os labels das barras
    y_max = df["qtd_ocorrencias"].max()
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
