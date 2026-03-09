"""
Test de escritura a Google Sheets desde terminal (sin Streamlit).
Ejecutar: python test_write_sheet.py
"""
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from sheets_helper import guardar_en_google_sheets

# Simula una respuesta real con columnas representativas de los módulos
COLUMNAS = [
    "email",
    "unesco_cuidado",
    "unesco_ley_primaria",
    "pais_incidentes_2025",
    "eutic_frecuencia_internet",
    "eutic_confianza_estado",
    "mck_areas_ia",
    "disp_ciberdelito_futuro",
    "disp_exposicion_personal",
    "perfil_dispositivos",
    "perfil_def_phishing",
]

respuestas_test = {col: "[TEST]" for col in COLUMNAS}
email_test = "test-write@ejemplo.com"

print("GOOGLE_SHEET_ID:", os.getenv("GOOGLE_SHEET_ID") or "(no definido)")
print("GOOGLE_CREDENTIALS_PATH:", os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"))
print("credentials.json existe:", os.path.exists("credentials.json"))
print()
print("Escribiendo fila de prueba en la Sheet...")

ok, msg = guardar_en_google_sheets(email_test, respuestas_test, COLUMNAS)

if ok:
    print("OK:", msg)
    sys.exit(0)
else:
    print("ERROR:", msg)
    sys.exit(1)
