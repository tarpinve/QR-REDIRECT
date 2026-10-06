import os
import json
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extraer el id de la URL (ej: /api/index?id=p001 o /r/p001)
        parsed_path = urlparse(self.path)
        path_parts = [p for p in parsed_path.path.split('/') if p]
        
        id_placa = None
        if len(path_parts) >= 2 and path_parts[0] == 'r':
            id_placa = path_parts[1]
        else:
            query_params = parse_qs(parsed_path.query)
            id_placa = query_params.get('id', [None])[0]

        if not id_placa:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Falta el parámetro id"}).encode())
            return

        if not SUPABASE_URL or not SUPABASE_KEY:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Faltan credenciales de Supabase"}).encode())
            return

        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            response = supabase.table("placas").select("url_destino").eq("id_placa", id_placa).execute()

            if response.data and len(response.data) > 0:
                url_final = response.data[0]["url_destino"]
                self.send_response(302)
                self.send_header('Location', url_final)
                self.end_headers()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Placa '{id_placa}' no encontrada"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
