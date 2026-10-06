import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from supabase import create_client, Client

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/api/index")
@app.get("/r/{id_placa}")
def redirigir(id_placa: str = None):
    if not id_placa:
        raise HTTPException(status_code=400, detail="Falta el ID de la placa")
        
    response = supabase.table("placas").select("url_destino").eq("id_placa", id_placa).execute()
    
    if response.data and len(response.data) > 0:
        url_final = response.data[0]["url_destino"]
        return RedirectResponse(url=url_final, status_code=302)
    else:
        raise HTTPException(status_code=404, detail="Placa no encontrada")

