"""
Test de escritura a Google Sheets desde terminal (sin Streamlit).
Ejecutar: python test_write_sheet.py
"""
import os
import sys

# Asegurar que se carga .env desde la carpeta del proyecto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from sheets_helper import guardar_en_google_sheets

# Datos de prueba (mismas preguntas que en app.py)
PREGUNTAS_TEXTO = [
    "¿Con qué frecuencia usás este servicio?",
    "¿Qué tan satisfecho estás con la atención?",
    "¿Qué aspecto te gustaría que mejoremos primero?",
    "¿Recomendarías este servicio a otra persona?",
]
respuestas_test = {p: "[TEST]" for p in PREGUNTAS_TEXTO}
email_test = "test-write@ejemplo.com"

print("GOOGLE_SHEET_ID:", os.getenv("GOOGLE_SHEET_ID") or "(no definido)")
print("GOOGLE_CREDENTIALS_PATH:", os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"))
print("credentials.json existe:", os.path.exists("credentials.json"))
print()
print("Escribiendo fila de prueba en la Sheet...")

ok, msg = guardar_en_google_sheets(email_test, respuestas_test, PREGUNTAS_TEXTO)

if ok:
    print("OK:", msg)
    sys.exit(0)
else:
    print("ERROR:", msg)
    sys.exit(1)
