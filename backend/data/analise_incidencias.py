import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from app.db.client import SupabaseClient


def gerar_grafico_incidencias_hora() -> bytes:
    sb = SupabaseClient()
    dados = sb.get_view_all("view_incidencias_hora")

    df = pd.DataFrame(dados)

    df.columns = [c.strip().lower() for c in df.columns]

    col_hora = None
    col_qtd = None
    for c in df.columns:
        if "hora" in c:
            col_hora = c
        if "qtd" in c or "quantidade" in c or "total" in c or "incidencia" in c or "count" in c:
            col_qtd = c

    if col_hora is None or col_qtd is None:
        colunas = list(df.columns)
        col_hora = colunas[0]
        col_qtd = colunas[1]

    df[col_hora] = pd.to_numeric(df[col_hora], errors="coerce")
    df[col_qtd] = pd.to_numeric(df[col_qtd], errors="coerce")
    df = df.dropna(subset=[col_hora, col_qtd])
    df = df.sort_values(col_hora)

    sns.set_theme(style="whitegrid", palette="muted")
    fig, ax = plt.subplots(figsize=(14, 6))

    sns.lineplot(
        data=df,
        x=col_hora,
        y=col_qtd,
        marker="o",
        linewidth=2.5,
        markersize=8,
        color="#7B2D8E",
        ax=ax,
    )

    ax.fill_between(df[col_hora], df[col_qtd], alpha=0.15, color="#7B2D8E")

    ax.set_title("Incidências em determinada hora", fontsize=18, fontweight="bold", pad=15)
    ax.set_xlabel("Hora do Dia", fontsize=13, fontweight="medium")
    ax.set_ylabel("Quantidade de Incidências", fontsize=13, fontweight="medium")

    ax.set_xticks(range(int(df[col_hora].min()), int(df[col_hora].max()) + 1))
    ax.tick_params(axis="both", labelsize=11)

    for x_val, y_val in zip(df[col_hora], df[col_qtd]):
        ax.annotate(
            f"{int(y_val)}",
            (x_val, y_val),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=9,
            fontweight="bold",
            color="#4A1A5E",
        )

    sns.despine(left=True, bottom=True)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
