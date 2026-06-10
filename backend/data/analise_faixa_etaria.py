import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from app.db.client import SupabaseClient


def gerar_grafico_faixa_etaria() -> bytes:
    sb = SupabaseClient()
    dados = sb.get_view_all("VW_INCIDENCIAS_POR_FAIXA_ETARIA")

    df = pd.DataFrame(dados)
    df.columns = [c.strip().lower() for c in df.columns]

    col_faixa = None
    col_qtd = None
    for c in df.columns:
        if "faixa" in c or "etaria" in c or "idade" in c:
            col_faixa = c
        if "qtd" in c or "quantidade" in c or "total" in c or "incidencia" in c or "count" in c:
            col_qtd = c

    if col_faixa is None or col_qtd is None:
        colunas = list(df.columns)
        col_faixa = colunas[0]
        col_qtd = colunas[1]

    df[col_qtd] = pd.to_numeric(df[col_qtd], errors="coerce")
    df = df.dropna(subset=[col_qtd])
    df = df.sort_values(col_qtd, ascending=False)

    labels = df[col_faixa].tolist()
    sizes = df[col_qtd].tolist()
    total = sum(sizes)

    palette = ["#7B2D8E", "#A855F7", "#C084FC", "#D8B4FE", "#9CA3AF"]

    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%",
        startangle=140,
        colors=palette[:len(sizes)],
        pctdistance=0.75,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2.5),
        textprops=dict(fontsize=12, fontweight="bold"),
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")

    legend_labels = [
        f"{label}  ({int(size):,})"
        .replace(",", ".")
        for label, size in zip(labels, sizes)
    ]

    legend = ax.legend(
        wedges,
        legend_labels,
        title="Faixa Etária",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=12,
        title_fontsize=13,
        frameon=True,
        fancybox=True,
        shadow=True,
    )
    legend.get_title().set_fontweight("bold")

    ax.set_title(
        "Incidências por Faixa Etária",
        fontsize=20,
        fontweight="bold",
        pad=25,
        color="#4A1A5E",
    )

    centre_circle = plt.Circle((0, 0), 0.35, fc="white")
    ax.add_artist(centre_circle)

    ax.text(
        0, 0,
        f"{total:,}".replace(",", "."),
        ha="center", va="center",
        fontsize=22, fontweight="bold",
        color="#4A1A5E",
    )
    ax.text(
        0, -0.08,
        "Total",
        ha="center", va="center",
        fontsize=11, fontweight="medium",
        color="#7B2D8E",
    )

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
