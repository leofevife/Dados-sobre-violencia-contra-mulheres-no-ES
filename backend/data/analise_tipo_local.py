import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import squarify

from app.db.client import SupabaseClient


def gerar_treemap_tipo_local() -> bytes:
    sb = SupabaseClient()
    dados = sb.get_view_all("VW_INCIDENCIAS_POR_TIPO_LOCAL")

    df = pd.DataFrame(dados)
    df.columns = [c.strip().lower() for c in df.columns]

    col_local = None
    col_qtd = None
    for c in df.columns:
        if "local" in c or "tipo" in c or "nome" in c:
            col_local = c
        if "qtd" in c or "quantidade" in c or "total" in c or "incidencia" in c or "count" in c:
            col_qtd = c

    if col_local is None or col_qtd is None:
        colunas = list(df.columns)
        col_local = colunas[0]
        col_qtd = colunas[1]

    df[col_qtd] = pd.to_numeric(df[col_qtd], errors="coerce")
    df = df.dropna(subset=[col_qtd])
    df = df.sort_values(col_qtd, ascending=False).head(10)

    labels = [
        f"{row[col_local].replace('/', '\n')}\n{int(row[col_qtd]):,}".replace(",", ".")
        for _, row in df.iterrows()
    ]
    sizes = df[col_qtd].tolist()

    min_val = min(sizes)
    max_val = max(sizes)
    val_range = max_val - min_val if max_val > min_val else 1
    cores = [plt.cm.Purples(0.4 + 0.5 * ((val - min_val) / val_range)) for val in sizes]


    fig, ax = plt.subplots(figsize=(14, 8))

    squarify.plot(
        sizes=sizes,
        label=labels,
        color=cores[:len(sizes)],
        alpha=0.85,
        ax=ax,
        text_kwargs={
            "fontsize": 11,
            "fontweight": "bold",
            "color": "white",
            "wrap": True,
        },
        pad=3,
    )

    ax.set_title(
        "Top 10 Locais com Mais Incidências",
        fontsize=18,
        fontweight="bold",
        pad=15,
    )
    ax.axis("off")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
