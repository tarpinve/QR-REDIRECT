import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from supabase import create_client, Client

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@app.get("/")
@app.get("/api/index")
@app.get("/api/index.py")
@app.get("/r/{id_placa}")
def redirigir(id_placa: str = None):
    if not id_placa:
        raise HTTPException(status_code=400, detail="Falta el ID de la placa")
        
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Faltan las credenciales de Supabase en Vercel")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table("placas").select("url_destino").eq("id_placa", id_placa).execute()

    if response.data and len(response.data) > 0:
        url_final = response.data[0]["url_destino"]
        return RedirectResponse(url=url_final, status_code=302)
    else:
        raise HTTPException(status_code=404, detail=f"Placa '{id_placa}' no encontrada")
