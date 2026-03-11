"""
Helper para guardar respuestas en Google Sheets.
Soporta autenticación desde st.secrets (Streamlit Cloud) o desde .env + credentials.json (local).
"""
from __future__ import annotations

import os
from pathlib import Path


def guardar_en_google_sheets(
    email: str, respuestas: dict, preguntas: list[str]
) -> tuple[bool, str]:
    """
    Guarda las respuestas en una hoja de Google Sheets.
    - email: correo de quien responde
    - respuestas: dict {columna: valor} (ya aplanado)
    - preguntas: lista de claves en el orden deseado de columnas
    Añade columna Fecha/Hora al final.
    Returns: (éxito, mensaje)
    """
    import sys

    # Resolver GOOGLE_SHEET_ID y credenciales: Streamlit Secrets > .env
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GOOGLE_SHEET_ID" in st.secrets:
            sheet_id = st.secrets["GOOGLE_SHEET_ID"]
            use_streamlit_secrets = True
        else:
            sheet_id = os.getenv("GOOGLE_SHEET_ID")
            use_streamlit_secrets = False
    except Exception:
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        use_streamlit_secrets = False

    if not sheet_id:
        return False, "No configurado: añadí GOOGLE_SHEET_ID en .env o en Streamlit Secrets."

    try:
        import gspread
        from google.oauth2.service_account import Credentials
        import socket
        from datetime import datetime

        socket.setdefaulttimeout(15.0)

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        if use_streamlit_secrets:
            import streamlit as st
            creds = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=scopes,
            )
        else:
            creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
            if not Path(creds_path).exists():
                return False, f"No se encontró {creds_path}. Revisá el README para configurar las credenciales."
            creds = Credentials.from_service_account_file(creds_path, scopes=scopes)

        gc = gspread.authorize(creds)
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.sheet1

        headers = list(preguntas) + ["Fecha/Hora"]

        try:
            existing_headers = worksheet.row_values(1)
        except Exception:
            existing_headers = []

        if not existing_headers:
            worksheet.append_row(headers)

        # Siempre escribir todas las columnas en orden fijo (vacío si no hay valor)
        row = [str(respuestas.get(p, "")) for p in preguntas] + [datetime.now().isoformat()]
        worksheet.append_row(row)

        return True, "Respuestas guardadas correctamente en Google Sheets."

    except socket.timeout:
        return False, "Timeout: la conexión con Google Sheets tardó demasiado. Revisá tu conexión a internet."
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False, str(e)
