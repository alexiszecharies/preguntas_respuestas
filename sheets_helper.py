"""
Helper para guardar respuestas en Google Sheets.
Si no hay credenciales configuradas, se puede usar guardado local en CSV.
"""
from __future__ import annotations

import os
from pathlib import Path

def guardar_en_google_sheets(
    email: str, respuestas: dict, preguntas: list[str]
) -> tuple[bool, str]:
    """
    Guarda las respuestas en una hoja de Google Sheets.
    email: correo de quien responde
    respuestas: dict pregunta -> respuesta
    preguntas: lista de textos de preguntas (orden de columnas)
    Escribe columnas: Email, preguntas..., Fecha/Hora
    Returns: (éxito, mensaje)
    """
    import sys
    
    print("[sheets_helper] Inicio de guardar_en_google_sheets", file=sys.stderr)
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

    if not sheet_id or not Path(creds_path).exists():
        return False, "No configurado: añade GOOGLE_SHEET_ID y credentials.json (ver README)."

    try:
        print("[sheets_helper] Importando gspread...", file=sys.stderr)
        import gspread
        from google.oauth2.service_account import Credentials
        import socket

        # Timeout global de socket: 10 segundos para evitar que se cuelgue infinito
        socket.setdefaulttimeout(10.0)

        print("[sheets_helper] Creando credenciales...", file=sys.stderr)
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        
        print("[sheets_helper] Autorizando con gspread...", file=sys.stderr)
        gc = gspread.authorize(creds)
        
        print(f"[sheets_helper] Abriendo sheet {sheet_id}...", file=sys.stderr)
        sh = gc.open_by_key(sheet_id)
        
        print("[sheets_helper] Accediendo a sheet1...", file=sys.stderr)
        worksheet = sh.sheet1

        from datetime import datetime

        print("[sheets_helper] Preparando datos...", file=sys.stderr)
        headers = ["Email"] + list(preguntas) + ["Fecha/Hora"]
        try:
            print("[sheets_helper] Leyendo fila 1 (headers)...", file=sys.stderr)
            existing = worksheet.row_values(1)
        except Exception as e:
            print(f"[sheets_helper] No hay headers (error: {e})", file=sys.stderr)
            existing = []
        if not existing:
            print("[sheets_helper] Escribiendo headers...", file=sys.stderr)
            worksheet.append_row(headers)

        print("[sheets_helper] Escribiendo fila de respuestas...", file=sys.stderr)
        row = [email] + [respuestas.get(p, "") for p in preguntas] + [datetime.now().isoformat()]
        worksheet.append_row(row)
        
        print("[sheets_helper] Éxito!", file=sys.stderr)
        return True, "Respuestas guardadas en Google Sheets."
    except socket.timeout:
        print("[sheets_helper] Timeout en la conexión a Google Sheets", file=sys.stderr)
        return False, "Timeout: La conexión con Google Sheets tardó demasiado. Revisá tu conexión a internet o firewall."
    except Exception as e:
        print(f"[sheets_helper] Excepción: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False, str(e)


def guardar_en_csv(
    email: str, respuestas: dict, preguntas: list[str], archivo: str = "respuestas.csv"
) -> str:
    """Guarda respuestas en un CSV local (fallback si no hay Google). Columnas: Email, preguntas..., Fecha/Hora."""
    import csv
    from datetime import datetime

    filepath = Path(archivo)
    existe = filepath.exists()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["Email"] + preguntas + ["Fecha/Hora"])
        row = [email] + [respuestas.get(p, "") for p in preguntas] + [datetime.now().isoformat()]
        writer.writerow(row)
    return f"Guardado en {archivo}"
