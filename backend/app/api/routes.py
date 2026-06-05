from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.db.client import SupabaseClient

router = APIRouter()
sb_client = SupabaseClient()


@router.get("/status")
def status():
    return {
        "status": "ok",
        "database": "supabase",
        "supabase_url": sb_client.url,
    }


@router.get("/supabase/health")
def supabase_health():
    try:
        rows = sb_client.get_view("view_incidencias_hora", limit=1)
        return {
            "success": True,
            "message": "Conexão com Supabase verificada com sucesso.",
            "sample": rows,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "error": str(exc),
                "hint": "Verifique se a SUPABASE_KEY e SUPABASE_URL estão corretos.",
            },
        )


@router.get("/supabase/view/incidencias_hora")
def get_view_incidencias_hora():
    try:
        rows = sb_client.get_view_all("view_incidencias_hora")
        return {"success": True, "rows": rows}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/analise/incidencias-hora")
def grafico_incidencias_hora():
    try:
        from data.analise_incidencias import gerar_grafico_incidencias_hora
        img_bytes = gerar_grafico_incidencias_hora()
        return Response(content=img_bytes, media_type="image/png")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/analise/treemap-tipo-local")
def grafico_treemap_tipo_local():
    try:
        from data.analise_tipo_local import gerar_treemap_tipo_local
        img_bytes = gerar_treemap_tipo_local()
        return Response(content=img_bytes, media_type="image/png")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/analise/locais-disponiveis")
def obter_locais_disponiveis():
    try:
        rows = sb_client.get_view_all("VW_INCIDENCIAS_HORA_TOP10")
        locais = {}
        for r in rows:
            tipo_local = r.get("tipo_local", r.get("TIPO_LOCAL"))
            bloco_hora = r.get("bloco_hora", r.get("BLOCO_HORA"))
            qtd = int(r.get("qtd_incidencias", r.get("QTD_INCIDENCIAS", 0)))
            
            if tipo_local not in locais:
                locais[tipo_local] = {"ni_count": 0}
            
            if bloco_hora == "N/I":
                locais[tipo_local]["ni_count"] = qtd
                
        resultado = [{"local": k, "ni_count": v["ni_count"]} for k, v in locais.items()]
        resultado.sort(key=lambda x: x["local"])
        return {"success": True, "locais": resultado}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/analise/incidencias-hora-local")
def grafico_incidencias_hora_local(local: str):
    try:
        from data.analise_incidencias import gerar_grafico_incidencias_hora_local
        img_bytes = gerar_grafico_incidencias_hora_local(local)
        return Response(content=img_bytes, media_type="image/png")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
