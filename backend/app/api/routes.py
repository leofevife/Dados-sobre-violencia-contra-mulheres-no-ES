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
