"""
App Streamlit: preguntas de opción múltiple en código; respuestas a Google Sheets.
Actualizá la lista PREGUNTAS acá cuando quieras cambiar las preguntas (ej. cada semana).
"""
import os
import sys
import traceback
from pathlib import Path

# Fijar directorio del proyecto para que .env y credentials.json se encuentren
_DIR = Path(__file__).resolve().parent
os.chdir(_DIR)

import streamlit as st
from dotenv import load_dotenv

from sheets_helper import guardar_en_google_sheets

load_dotenv(_DIR / ".env")

st.set_page_config(page_title="Preguntas semanales", page_icon="📋", layout="centered")

# --- Preguntas fijas en código (actualizá esta lista cuando quieras) ---
PREGUNTAS = [
    {
        "pregunta": "¿Con qué frecuencia usás este servicio?",
        "opciones": ["Todos los días", "Algunas veces por semana", "Rara vez", "Es la primera vez"],
    },
    {
        "pregunta": "¿Qué tan satisfecho estás con la atención?",
        "opciones": ["Muy satisfecho", "Satisfecho", "Neutral", "Insatisfecho"],
    },
    {
        "pregunta": "¿Qué aspecto te gustaría que mejoremos primero?",
        "opciones": ["Velocidad de respuesta", "Claridad de la información", "Facilidad de uso", "Nada, está bien así"],
    },
    {
        "pregunta": "¿Recomendarías este servicio a otra persona?",
        "opciones": ["Sí, sin dudas", "Probablemente sí", "No estoy seguro", "No"],
    },
]

# --- Formulario ---
st.title("📋 Preguntas semanales")
st.caption("Elegí una opción por pregunta. Las respuestas se registran en la planilla con tu email y la fecha/hora.")

with st.form("form_respuestas"):
    email = st.text_input("Email (obligatorio)", type="default", placeholder="tu@email.com", key="email")
    respuestas = {}
    for i, item in enumerate(PREGUNTAS):
        texto = item["pregunta"]
        opciones = item["opciones"]
        elegida = st.radio(texto, opciones, key=f"resp_{i}", horizontal=False)
        respuestas[texto] = elegida
    enviar = st.form_submit_button("Enviar respuestas")

if enviar:
    email = (email or "").strip()
    if not email:
        st.error("El email es obligatorio. Ingresá tu correo para enviar las respuestas.")
    else:
        lista_preguntas = [p["pregunta"] for p in PREGUNTAS]
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
        
        # Debug: mostrar info de configuración en consola
        print("=" * 60, file=sys.stderr)
        print(f"GOOGLE_SHEET_ID: {sheet_id}", file=sys.stderr)
        print(f"GOOGLE_CREDENTIALS_PATH: {creds_path}", file=sys.stderr)
        print(f"credentials.json existe: {Path(creds_path).exists()}", file=sys.stderr)
        print(f"Working directory: {os.getcwd()}", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

        if not sheet_id:
            st.error("No se configuró GOOGLE_SHEET_ID en el archivo .env")
            st.stop()
        
        if not Path(creds_path).exists():
            st.error(f"No se encontró el archivo de credenciales: {creds_path}")
            st.stop()

        try:
            with st.spinner("Guardando respuestas en Google Sheets..."):
                print(f"Llamando a guardar_en_google_sheets con email={email}", file=sys.stderr)
                ok, msg = guardar_en_google_sheets(email, respuestas, lista_preguntas)
                print(f"Resultado: ok={ok}, msg={msg}", file=sys.stderr)
                
            if ok:
                st.success(msg)
                st.balloons()
            else:
                st.error(f"Error al guardar: {msg}")
        except Exception as e:
            st.error("Error al guardar las respuestas.")
            st.code(traceback.format_exc(), language=None)
            print(traceback.format_exc(), file=sys.stderr)
