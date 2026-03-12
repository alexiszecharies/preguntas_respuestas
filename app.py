"""
Ciber Window
Wizard paso a paso, un módulo por pantalla.
Para actualizar preguntas: editá los MODULOS más abajo.
"""
import os
import sys
import traceback
from pathlib import Path

_DIR = Path(__file__).resolve().parent
os.chdir(_DIR)

import streamlit as st
from dotenv import load_dotenv
from sheets_helper import guardar_en_google_sheets

load_dotenv(_DIR / ".env")

st.set_page_config(
    page_title="Ciber Window · Encuesta",
    page_icon="🔐",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTILOS – identidad visual de kaidenteam.com
# Paleta real: fondo #f0f4f8 (gris-azul claro), texto #0d1b2a (navy),
#              acento teal #1ab5c8, azul marino #1a2f6e
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Override Streamlit primary color (evita el rojo en sliders, focus, etc.) ── */
:root {
    --primary-color: #1ab5c8 !important;
    --secondary-background-color: #ffffff !important;
    --text-color: #0d1b2a !important;
}

/* ── Fondo animado con formas flotantes ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 15% 20%, rgba(26,181,200,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 75%, rgba(26,100,180,0.10) 0%, transparent 50%),
        linear-gradient(160deg, #e8f4f8 0%, #f0f4f8 50%, #eaf0f8 100%);
}

.floating-shapes {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}
.shape {
    position: absolute;
    border: 2px solid rgba(26, 181, 200, 0.25);
    border-radius: 6px;
    animation: floatShape linear infinite;
    opacity: 0;
}
.shape.circle { border-radius: 50%; }

/* Diferentes tamaños, posiciones y duraciones */
.shape:nth-child(1)  { width:55px;  height:55px;  left:5%;   top:15%; animation-duration:14s; animation-delay:0s;   }
.shape:nth-child(2)  { width:35px;  height:35px;  left:88%;  top:8%;  animation-duration:18s; animation-delay:2s;   }
.shape:nth-child(3)  { width:70px;  height:70px;  left:75%;  top:60%; animation-duration:20s; animation-delay:1s;   }
.shape:nth-child(4)  { width:28px;  height:28px;  left:20%;  top:72%; animation-duration:16s; animation-delay:4s;   }
.shape:nth-child(5)  { width:45px;  height:45px;  left:50%;  top:85%; animation-duration:22s; animation-delay:0.5s; }
.shape:nth-child(6)  { width:20px;  height:20px;  left:93%;  top:40%; animation-duration:12s; animation-delay:3s;   }
.shape:nth-child(7)  { width:60px;  height:60px;  left:35%;  top:5%;  animation-duration:25s; animation-delay:6s;   }
.shape:nth-child(8)  { width:38px;  height:38px;  left:62%;  top:30%; animation-duration:17s; animation-delay:1.5s; }
.shape:nth-child(9)  { width:22px;  height:22px;  left:8%;   top:50%; animation-duration:19s; animation-delay:5s;   }
.shape:nth-child(10) { width:50px;  height:50px;  left:78%;  top:88%; animation-duration:23s; animation-delay:2.5s; }

@keyframes floatShape {
    0%   { transform: translateY(0px)   rotate(0deg);   opacity: 0;    }
    10%  { opacity: 0.8; }
    90%  { opacity: 0.8; }
    100% { transform: translateY(-80px) rotate(25deg);  opacity: 0;    }
}

/* Hacer que el contenido quede por encima de las formas */
[data-testid="stMainBlockContainer"],
[data-testid="stMain"] > div {
    position: relative;
    z-index: 1;
}
</style>

<div class="floating-shapes">
  <div class="shape"></div>
  <div class="shape circle"></div>
  <div class="shape"></div>
  <div class="shape circle"></div>
  <div class="shape"></div>
  <div class="shape circle"></div>
  <div class="shape"></div>
  <div class="shape circle"></div>
  <div class="shape"></div>
  <div class="shape circle"></div>
</div>

<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #f0f4f8 !important;
    color: #0d1b2a !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background-color: #ffffff !important; border-bottom: 1px solid #dce4ed; }
[data-testid="stMainBlockContainer"] { background-color: #f0f4f8 !important; padding-top: 1.5rem; }

/* ── Títulos ── */
h1 {
    color: #0d1b2a !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
h1 em { color: #1ab5c8; font-style: normal; }
h2, h3 { color: #0d1b2a !important; font-weight: 700 !important; }

/* ── Header de marca ── */
.kaiden-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 0.75rem 0 1.25rem 0;
    border-bottom: 1px solid #dce4ed;
    margin-bottom: 1.75rem;
}
.kaiden-subtext {
    font-size: 0.72rem;
    color: #6b8099;
    font-weight: 400;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Tarjeta blanca que envuelve el formulario ── */
[data-testid="stForm"], .block-container {
    background-color: #f0f4f8 !important;
}

/* ── Etiquetas ── */
label, [data-testid="stWidgetLabel"] p,
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #0d1b2a !important;
    font-size: 0.96rem !important;
}

/* ── Inputs de texto ── */
input[type="text"], textarea {
    background-color: #ffffff !important;
    color: #0d1b2a !important;
    border: 1.5px solid #c8d6e5 !important;
    border-radius: 8px !important;
}
input[type="text"]:focus, textarea:focus {
    border-color: #1ab5c8 !important;
    box-shadow: 0 0 0 3px rgba(26, 181, 200, 0.15) !important;
}

/* ── Radio buttons (opciones con fondo blanco, pregunta sin) ── */
[data-testid="stRadio"] > div { gap: 0.35rem; }
[data-testid="stRadio"] label {
    background-color: #ffffff;
    border: 1.5px solid #c8d6e5;
    border-radius: 8px;
    padding: 7px 14px !important;
    transition: all 0.15s;
    color: #0d1b2a !important;
}
[data-testid="stRadio"] [data-testid="stWidgetLabel"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label div,
[data-testid="stRadio"] label span {
    color: #0d1b2a !important;
}
[data-testid="stRadio"] label:hover {
    border-color: #1ab5c8 !important;
    background-color: #e8f8fa !important;
}
[data-testid="stRadio"] label:hover p,
[data-testid="stRadio"] label:hover div,
[data-testid="stRadio"] label:hover span {
    color: #0d1b2a !important;
}

/* ── Checkboxes ── */
[data-testid="stCheckbox"] label {
    background-color: #ffffff;
    border: 1.5px solid #c8d6e5;
    border-radius: 8px;
    padding: 6px 12px !important;
    margin-bottom: 4px;
    color: #0d1b2a !important;
}
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label div,
[data-testid="stCheckbox"] label span {
    color: #0d1b2a !important;
}
[data-testid="stCheckbox"] label:hover {
    border-color: #1ab5c8 !important;
    background-color: #e8f8fa !important;
}
[data-testid="stCheckbox"] label:hover p,
[data-testid="stCheckbox"] label:hover span {
    color: #0d1b2a !important;
}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] > div > div {
    background-color: #ffffff !important;
    border: 1.5px solid #c8d6e5 !important;
    border-radius: 8px !important;
    color: #0d1b2a !important;
}
span[data-baseweb="tag"] {
    background-color: #d0f0f5 !important;
    color: #0d7a8a !important;
    border: 1px solid #1ab5c8 !important;
    border-radius: 4px !important;
}

/* ── Selectbox (ranking) ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #ffffff !important;
    border: 1.5px solid #c8d6e5 !important;
    color: #0d1b2a !important;
    border-radius: 8px !important;
}

/* ── Slider ── */
/* Track completo (fondo gris) */
[data-testid="stSlider"] [data-testid="stSliderTrack"] {
    background-color: #c8d6e5 !important;
}
/* Parte activa del track (izquierda del thumb) */
[data-testid="stSlider"] [data-testid="stSliderTrack"] > div,
[data-testid="stSlider"] [data-testid="stSliderTrack"] > div:first-child {
    background-color: #1ab5c8 !important;
}
/* Thumb (círculo) */
[data-testid="stSlider"] [role="slider"] {
    background-color: #1ab5c8 !important;
    border: 3px solid #ffffff !important;
    box-shadow: 0 0 0 2px #1ab5c8 !important;
    width: 20px !important;
    height: 20px !important;
}
[data-testid="stSlider"] [role="slider"]:focus {
    box-shadow: 0 0 0 3px rgba(26, 181, 200, 0.35) !important;
}
/* Número del valor actual encima del thumb */
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"],
[data-testid="stSlider"] div[data-testid="stThumbValue"] {
    color: #1ab5c8 !important;
    font-weight: 600 !important;
}
/* Eliminar el color rojo heredado del theme de Streamlit */
[data-testid="stSlider"] * {
    --slider-color: #1ab5c8 !important;
    accent-color: #1ab5c8 !important;
}

/* ── Botón primario ── */
[data-testid="stButton"] > button[kind="primary"] {
    background-color: #1ab5c8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1.8rem !important;
    transition: background-color 0.2s, transform 0.1s;
    letter-spacing: 0.3px;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #159eb0 !important;
    transform: translateY(-1px);
}

/* ── Botón secundario ── */
[data-testid="stButton"] > button:not([kind="primary"]) {
    background-color: transparent !important;
    color: #6b8099 !important;
    border: 1.5px solid #c8d6e5 !important;
    border-radius: 50px !important;
    font-weight: 500 !important;
}
[data-testid="stButton"] > button:not([kind="primary"]):hover {
    border-color: #1ab5c8 !important;
    color: #1ab5c8 !important;
}

/* ── Barra de progreso ── */
[data-testid="stProgressBar"] > div > div { background-color: #1ab5c8 !important; }
[data-testid="stProgressBar"] > div { background-color: #c8d6e5 !important; border-radius: 4px; }

/* ── Divider ── */
hr { border-color: #dce4ed !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 8px !important; }

/* ── Caption ── */
[data-testid="stCaptionContainer"] p, small, .stCaption { color: #6b8099 !important; }

/* ── Forzar texto oscuro en todos los widgets ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stWidgetLabel"] div,
[data-baseweb="radio"] span,
[data-baseweb="checkbox"] span,
[data-baseweb="radio"] p,
[data-baseweb="checkbox"] p {
    color: #0d1b2a !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f4f8; }
::-webkit-scrollbar-thumb { background: #c8d6e5; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #1ab5c8; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DEFINICIÓN DE MÓDULOS Y PREGUNTAS
# Tipos soportados:
#   radio        → opciones, index=None (sin default)
#   radio_si_no  → Sí / No
#   vf           → Verdadero / Falso
#   checkboxes   → selección múltiple (lista corta)
#   multiselect  → selección múltiple (lista larga)
#   slider       → escala numérica (min, max, labels_min, labels_max)
#   ranking      → ordenar opciones con 4 dropdowns
#   text         → campo de texto libre
#   conditional  → muestra sub-preguntas si la respuesta a trigger_key está en trigger_values
# ─────────────────────────────────────────────────────────────────────────────

MODULOS = [
    # ── MÓDULO 0: Datos del participante ─────────────────────────────────────
    {
        "titulo": "Datos del participante",
        "descripcion": "Antes de comenzar, ingresá tu email y aceptá el consentimiento.",
        "preguntas": [
            {
                "key": "email",
                "tipo": "text",
                "texto": "Email (obligatorio)",
                "placeholder": "tu@email.com",
            },
            {
                "key": "consentimiento",
                "tipo": "consent",
                "texto": "Acepto participar voluntariamente en esta encuesta y autorizo el uso de mis respuestas con fines de investigación. Mis datos serán tratados de forma confidencial.",
            },
        ],
    },

    # ── MÓDULO 1: UNESCO ──────────────────────────────────────────────────────
    {
        "titulo": "Mirada 1",
        "descripcion": "",
        "preguntas": [
            {
                "key": "unesco_cuidado",
                "tipo": "checkboxes",
                "texto": "¿Tiene personas a su cargo en lo que refiere al cuidado frente a riesgos de uso problemático de celular?",
                "opciones": [
                    "Sí, niñ@s de 6 a 12 años",
                    "Sí, adolescentes de 12 a 18 años",
                    "Sí, jóvenes mayores de 18 años",
                    "Sí, adultos mayores",
                    "No tengo personas a cargo",
                ],
            },
            {
                "key": "unesco_restricciones_escuela",
                "tipo": "radio",
                "texto": "Los niñ@s y adolescentes que tiene a su cuidado, ¿concurren a un centro educativo que tiene restricciones en el uso del celular?",
                "opciones": [
                    "Sí, prohíben completamente el uso de celulares durante el horario escolar, con excepciones mínimas como salud, discapacidad y uso pedagógico autorizado.",
                    "Sí, se permite el uso limitado, sólo en ciertos momentos: recreos, fuera de clase, o en ciertos niveles educativos.",
                    "No hay prohibición general, pero se regula el uso con fines pedagógicos o bajo supervisión docente.",
                ],
                "condicional": {
                    "trigger_key": "unesco_cuidado",
                    "trigger_values": ["Sí, niñ@s de 6 a 12 años", "Sí, adolescentes de 12 a 18 años"],
                },
            },
            {
                "key": "unesco_escuela_impacto",
                "tipo": "radio",
                "texto": "En el centro educativo al que concurren los niñ@s y adolescentes que tiene a su cuidado:",
                "opciones": [
                    "La tecnología ha exacerbado las normas o estereotipos de género negativos.",
                    "El uso de las redes sociales ha afectado el bienestar y la autoestima de las niñas más que de los varones.",
                    "Se ha amplificado el ciberacoso por el uso de dispositivos en línea en el entorno escolar y por el diseño sesgado de los algoritmos de inteligencia artificial.",
                ],
                "condicional": {
                    "trigger_key": "unesco_cuidado",
                    "trigger_values": ["Sí, niñ@s de 6 a 12 años", "Sí, adolescentes de 12 a 18 años"],
                },
            },
            {
                "key": "unesco_ley_primaria",
                "tipo": "radio_si_no",
                "texto": "Si hubiese una votación general, ¿apoyaría la creación de leyes que prohíban el uso de teléfonos inteligentes en la escuela primaria?",
            },
            {
                "key": "unesco_ley_secundaria",
                "tipo": "radio_si_no",
                "texto": "Si hubiese una votación general, ¿apoyaría la creación de leyes que prohíban el uso de teléfonos inteligentes en secundaria/liceo?",
            },
            {
                "key": "unesco_ley_educacion_riesgos",
                "tipo": "radio_si_no",
                "texto": "Si hubiese una votación general, ¿apoyaría leyes que obliguen a los centros educativos a enseñar los riesgos y oportunidades de la tecnología y redes sociales?",
            },
            {
                "key": "unesco_vf_doomscrolling",
                "tipo": "likert",
                "texto": "Entre las nuevas palabras añadidas al Diccionario Oxford en 2024 se encontraban «doomscrolling» y «brain-rot». Ambas son símbolos de la omnipresencia del uso poco saludable de las redes sociales impulsado por algoritmos de inteligencia artificial.",
            },
            {
                "key": "unesco_vf_tecnologia_aprendizaje",
                "tipo": "likert",
                "texto": "Algunas tecnologías pueden favorecer el aprendizaje en algunos contextos, pero no cuando se usan en exceso o de forma inapropiada.",
            },
            {
                "key": "unesco_vf_celular_clase",
                "tipo": "likert",
                "texto": "Tener un teléfono inteligente en clase puede interrumpir el aprendizaje.",
            },
            {
                "key": "unesco_vf_notificaciones",
                "tipo": "likert",
                "texto": "Tener un teléfono móvil cerca con notificaciones es suficiente para que los estudiantes pierdan la atención de la tarea en cuestión.",
            },
            {
                "key": "unesco_vf_prohibicion_politica",
                "tipo": "likert",
                "texto": "Prohibir el teléfono en el colegio es una decisión política sobre las prioridades generales de la sociedad: pone al bienestar y la educación por encima de la conveniencia inmediata de la conectividad.",
            },
            {
                "key": "unesco_vf_refugio",
                "tipo": "likert",
                "texto": "Prohibir o limitar el uso de celular permite que la escuela recupere su papel como refugio de aprendizaje, libre (al menos por unas horas) de las distracciones del mundo exterior.",
            },
        ],
    },

    # ── MÓDULO 2: Diario El País ──────────────────────────────────────────────
    {
        "titulo": "Mirada 2",
        "descripcion": "",
        "preguntas": [
            {
                "key": "pais_instituciones",
                "tipo": "multiselect",
                "texto": "¿Cuál de las siguientes instituciones/iniciativas existe en nuestro país?",
                "opciones": [
                    "Dirección General de Cibercrimen del Ministerio del Interior",
                    "Organización nacional para la ciudadanía digital (sin fines de lucro)",
                    "Unidad Especializada en Cibercriminalidad de la Fiscalía General de la Nación",
                    "CERT - Centro Nacional de Respuesta a Incidentes de Seguridad Informática",
                    "Departamento de Delitos Sexuales (Cibercrimen) – monitoreo de material de abuso sexual infantil",
                    "Estrategia Nacional de Ciberseguridad 2024-2030",
                    "SOC - Centro de monitoreo de seguridad de la información",
                    "AGESIC - Agencia de Gobierno Electrónico y Sociedad de la Información",
                    "Cámara Uruguaya Fintech (CUF)",
                ],
            },
            {
                "key": "pais_denuncia",
                "tipo": "checkboxes",
                "texto": "Para denunciar un ciber delito, ¿qué corresponde hacer?",
                "opciones": [
                    "Contactar a la liga de defensa del consumidor si compró un producto y la empresa no existe",
                    "No modificar los dispositivos electrónicos donde tenga mensajes del ciber delito, para preservar la evidencia",
                    "Dirigirse al servicio técnico y pedirles que corran un anti virus",
                    "Formular la denuncia en cualquier seccional policial en forma presencial",
                    "Denunciar por el teléfono 2030 4625",
                ],
            },
            {
                "key": "pais_incidentes_2025",
                "tipo": "radio",
                "texto": "En el año 2025, ¿cuántos incidentes de seguridad de la información se detectaron y respondieron?",
                "opciones": [
                    "Aproximadamente 12 mil",
                    "Aproximadamente 22 mil",
                    "Aproximadamente 42 mil",
                    "Aproximadamente 62 mil",
                ],
            },
            {
                "key": "pais_pct_datos_personales",
                "tipo": "radio",
                "texto": "¿Qué porcentaje de los incidentes de ciberseguridad estuvo vinculado a la recolección de datos personales de los afectados?",
                "opciones": [
                    "Más del 20%",
                    "Más del 50%",
                    "Más del 70%",
                    "Más del 95%",
                ],
            },
            {
                "key": "pais_estafador_vivencias",
                "tipo": "checkboxes",
                "texto": "¿Qué vivencias activa el estafador para condicionarnos a entregar información o transferir dinero?",
                "opciones": [
                    "La codicia, la avaricia, el deseo de hacer plata fácil",
                    "El miedo, el pánico de que ocurra algo terrible que debemos impedir",
                    "La sensación de que hemos tenido suerte 'por una vez en la vida' y que hemos salido sorteados en un premio",
                    "El respeto a la autoridad de alguien que nos indica cómo proceder en tono firme y claro",
                ],
            },
            {
                "key": "pais_bps_phishing",
                "tipo": "radio",
                "texto": "Cuando una persona recibe el mensaje de un correo @bps.gub.uy diciendo «Tiene un subsidio social pendiente de cobro. Complete la información pertinente y recíbalo en un plazo de 24 horas», lo que está ocurriendo es:",
                "opciones": [
                    "El BPS está enviando un recordatorio a quienes no han ido a cobrar a la red de cobranza",
                    "El BPS quiere acelerar la entrega del subsidio para que la persona lo reciba lo más pronto posible",
                    "Es seguro que se está haciendo un simulacro para evaluar si el usuario sabe cómo reaccionar ante un phishing",
                    "Es seguro que es un phishing sencillo",
                    "Son estudiantes de ingeniería social que hacen una pasantía para mejorar el servicio del BPS a los jubilados",
                ],
            },
        ],
    },

    # ── MÓDULO 3: EUTIC 2024 ─────────────────────────────────────────────────
    {
        "titulo": "Mirada 3",
        "descripcion": "",
        "preguntas": [
            {
                "key": "eutic_frecuencia_internet",
                "tipo": "radio",
                "texto": "¿Utilizó alguna vez Internet? ¿Con qué frecuencia?",
                "opciones": [
                    "Diariamente",
                    "Una vez por semana",
                    "Tres veces por semana",
                    "Una vez por mes",
                    "Casi nunca o nunca",
                ],
            },
            {
                "key": "eutic_tramites_digitales",
                "tipo": "checkboxes",
                "texto": "En el último mes, ¿en cuáles de los siguientes realizó trámites digitales, gestiones en línea o compras?",
                "opciones": [
                    "Organismos del Estado",
                    "Intendencia departamental",
                    "Prestador de servicio de salud",
                    "Banco (caja de ahorro o cuenta corriente)",
                    "Mercado Libre, Temu, Amazon u otro e-commerce",
                    "Comidas en PedidosYa u otra app de delivery",
                ],
            },
            {
                "key": "eutic_confianza_estado",
                "tipo": "slider",
                "texto": "¿Confía en la seguridad de los servicios digitales del Estado?",
                "min": 1,
                "max": 5,
                "labels_min": "Nada",
                "labels_max": "Totalmente",
            },
            {
                "key": "eutic_confianza_banco",
                "tipo": "slider",
                "texto": "¿Confía en la seguridad de los servicios digitales de su banco personal?",
                "min": 1,
                "max": 5,
                "labels_min": "Nada",
                "labels_max": "Totalmente",
            },
            {
                "key": "eutic_practicas_info",
                "tipo": "checkboxes",
                "texto": "¿Cuáles de las siguientes actividades ha realizado últimamente (últimos 3 meses)?",
                "opciones": [
                    "Buscar información explicativa e instructiva sobre un tema",
                    "Ver noticias y novedades de prensa nacional e internacional",
                    "Seguir noticias deportivas",
                    "Ver videos educativos sobre algún tema de interés",
                    "Buscar información de salud, enfermedades, medicación y tratamiento",
                ],
            },
            {
                "key": "eutic_ia",
                "tipo": "checkboxes",
                "texto": "¿Ha utilizado herramientas de inteligencia artificial últimamente (en los últimos 3 meses)?",
                "opciones": [
                    "No",
                    "Sí, ChatGPT",
                    "Sí, Claude",
                    "Sí, Gemini o Copilot",
                    "Sí, Deepseek",
                    "Sí, otras",
                ],
            },
            {
                "key": "eutic_actividades_3meses",
                "tipo": "checkboxes",
                "texto": "En los últimos 3 meses, ¿cuáles de estas actividades realizó?",
                "opciones": [
                    "Almacenó imágenes, videos o documentos en la nube (Dropbox, Google Drive, iCloud, etc.)",
                    "Consultó sitios para obtener información sobre alguna temática",
                    "Buscó información sobre bienes y servicios",
                    "Buscó información sobre la actualidad o leyó noticias",
                    "Buscó direcciones o utilizó mapas para ubicarse",
                ],
            },
            {
                "key": "eutic_teletrabajo_3meses",
                "tipo": "checkboxes",
                "texto": "En los últimos 3 meses (relacionado al trabajo):",
                "opciones": [
                    "Respondió a un mail o mensaje laboral fuera del horario de trabajo",
                    "Realizó teletrabajo desde su hogar a través de internet",
                    "Realizó un curso a distancia en la computadora laboral",
                ],
            },
            {
                "key": "eutic_redes_diario",
                "tipo": "checkboxes",
                "texto": "¿Cuáles de las siguientes utiliza diariamente?",
                "opciones": [
                    "WhatsApp",
                    "Facebook",
                    "Instagram",
                    "YouTube",
                    "Spotify",
                    "Twitter / X",
                    "TikTok",
                ],
            },
            {
                "key": "eutic_redes_conducta",
                "tipo": "checkboxes",
                "texto": "En las redes sociales, ¿qué hace habitualmente?",
                "opciones": [
                    "Mira publicaciones de otros (amigos, influencers, artistas, marcas)",
                    "Publica contenido (fotos, videos, texto)",
                    "Comparte o repostea contenidos de otros",
                ],
            },
            {
                "key": "eutic_actividades_sociales",
                "tipo": "checkboxes",
                "texto": "En los últimos 3 meses:",
                "opciones": [
                    "Realizó llamadas o videollamadas",
                    "Envió, chequeó o recibió mails",
                    "Leyó o descargó noticias, diarios, revistas o libros por Internet",
                    "Participó, votó o firmó en campañas o votaciones en Internet",
                    "Utilizó sitios o apps para conocer gente y salir",
                ],
            },
            {
                "key": "eutic_entretenimiento",
                "tipo": "multiselect",
                "texto": "¿Para qué utiliza internet para su entretenimiento?",
                "opciones": [
                    "Contenidos de belleza y cuidado de la piel",
                    "Contenidos deportivos, fitness, gimnasio",
                    "Fútbol",
                    "Ver y descargar música",
                    "Ver y descargar series o películas",
                    "Escuchar la radio en línea",
                    "Jugar videojuegos",
                    "Ver contenido subido por conocidos",
                    "Ver noticias y actualidad",
                    "Ver humor o bromas",
                    "Ver gastronomía o cocina",
                ],
            },
            {
                "key": "eutic_nivel_usuario",
                "tipo": "radio",
                "texto": "Usted diría que es un usuario de estas tecnologías en un nivel:",
                "opciones": [
                    "Básico",
                    "Avanzado",
                    "No soy usuario realmente",
                ],
            },
            {
                "key": "eutic_seg_compra",
                "tipo": "radio_si_no",
                "texto": "En los últimos 12 meses: ¿Dejó de comprar algún producto o servicio por Internet por preocupaciones de seguridad?",
            },
            {
                "key": "eutic_seg_fraude_tarjeta",
                "tipo": "radio_si_no",
                "texto": "En los últimos 12 meses: ¿Perdió dinero por fraude de tarjetas de crédito por Internet?",
            },
            {
                "key": "eutic_seg_acoso",
                "tipo": "radio_si_no",
                "texto": "En los últimos 12 meses: ¿Lo acosaron u hostigaron por Internet (ciberbullying o chantaje)?",
            },
            {
                "key": "eutic_seg_hackeo",
                "tipo": "radio_si_no",
                "texto": "En los últimos 12 meses: ¿Le hackearon su correo electrónico o sus cuentas en redes sociales?",
            },
            {
                "key": "eutic_seg_privacidad",
                "tipo": "radio_si_no",
                "texto": "En los últimos 12 meses: ¿Invadieron su privacidad (fotos, videos o información personal)?",
            },
            {
                "key": "eutic_seg_virus",
                "tipo": "radio_si_no",
                "texto": "En los últimos 12 meses: ¿Perdió información debido a un virus u otra infección informática?",
            },
        ],
    },

    # ── MÓDULO 4: McKinsey ───────────────────────────────────────────────────
    {
        "titulo": "Mirada 4",
        "descripcion": "",
        "preguntas": [
            {
                "key": "mck_areas_ia",
                "tipo": "multiselect",
                "texto": "¿En qué áreas de su organización se utilizan Agentes de IA?",
                "opciones": [
                    "IT",
                    "Marketing y Ventas",
                    "Operaciones",
                    "Desarrollo de productos o servicios",
                    "Ingeniería de Software",
                    "Riesgo, cumplimiento, legales",
                    "Recursos Humanos",
                    "Estrategia y finanzas corporativas",
                    "Cadena de suministros y gestión de stocks/inventarios",
                    "Producción",
                    "No se utilizan",
                ],
            },
            {
                "key": "mck_ia_impacto_innovacion",
                "tipo": "slider",
                "texto": "INNOVACIÓN · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_empleados",
                "tipo": "slider",
                "texto": "SATISFACCIÓN DE LOS EMPLEADOS · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_competitiva",
                "tipo": "slider",
                "texto": "DIFERENCIACIÓN COMPETITIVA · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_costos",
                "tipo": "slider",
                "texto": "COSTOS · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_rentabilidad",
                "tipo": "slider",
                "texto": "RENTABILIDAD · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_ingresos",
                "tipo": "slider",
                "texto": "INGRESOS ORGÁNICOS · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_talento",
                "tipo": "slider",
                "texto": "ATRACCIÓN Y RETENCIÓN DEL TALENTO · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_mercado",
                "tipo": "slider",
                "texto": "PARTICIPACIÓN DE MERCADO · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_clientes",
                "tipo": "slider",
                "texto": "SATISFACCIÓN DEL CLIENTE · ¿Hasta qué punto la IA impactó en los resultados del último año en este aspecto?",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_areas_reduccion_costos",
                "tipo": "multiselect",
                "texto": "¿En qué áreas cree que hay reducciones de costos al implementar IA?",
                "opciones": [
                    "IT", "Marketing y Ventas", "Operaciones",
                    "Desarrollo de productos o servicios", "Ingeniería de Software",
                    "Riesgo, cumplimiento, legales", "Recursos Humanos",
                    "Estrategia y finanzas corporativas",
                    "Cadena de suministros y gestión de stocks/inventarios", "Producción",
                ],
            },
            {
                "key": "mck_indicadores_transformacion",
                "tipo": "checkboxes",
                "texto": "Al incorporar nueva tecnología, ¿los planes de su organización incluyen indicadores de:",
                "opciones": ["Eficiencia", "Crecimiento", "Innovación"],
            },
        ],
    },

    # ── MÓDULO 5: Disponibilidad para aprender IA y CS ───────────────────────
    {
        "titulo": "Mirada 5",
        "descripcion": "",
        "preguntas": [
            {
                "key": "disp_ciberdelito_futuro",
                "tipo": "radio",
                "texto": "¿Cree que el ciberdelito:",
                "opciones": [
                    "Irá disminuyendo porque las personas y las empresas se preparan cada vez más y mejor",
                    "Crecerá en todo el mundo con tasas incrementales brutales",
                    "Ganará la carrera a la ciberseguridad; es esperable una crisis asimilable a lo que fue la pandemia",
                ],
            },
            {
                "key": "disp_exposicion_personal",
                "tipo": "slider",
                "texto": "¿Qué tan expuesto a sufrir un incidente de ciberseguridad considera que está? – En su vida personal",
                "min": 1, "max": 5, "labels_min": "Nada expuesto", "labels_max": "Muy expuesto",
            },
            {
                "key": "disp_exposicion_profesional",
                "tipo": "slider",
                "texto": "¿Qué tan expuesto considera que está? – En su rol profesional",
                "min": 1, "max": 5, "labels_min": "Nada expuesto", "labels_max": "Muy expuesto",
            },
            {
                "key": "disp_exposicion_familiar",
                "tipo": "slider",
                "texto": "¿Qué tan expuesto considera que está? – Su entorno familiar",
                "min": 1, "max": 5, "labels_min": "Nada expuesto", "labels_max": "Muy expuesto",
            },
            {
                "key": "disp_exposicion_trabajo",
                "tipo": "slider",
                "texto": "¿Qué tan expuesto considera que está? – Su lugar de trabajo",
                "min": 1, "max": 5, "labels_min": "Nada expuesto", "labels_max": "Muy expuesto",
            },
            {
                "key": "disp_exposicion_pais",
                "tipo": "slider",
                "texto": "¿Qué tan expuesto considera que está? – Su país a nivel general",
                "min": 1, "max": 5, "labels_min": "Nada expuesto", "labels_max": "Muy expuesto",
            },
            {
                "key": "disp_foco_vida",
                "tipo": "radio",
                "texto": "¿Cree que en el día a día sus actividades y su tiempo están enfocando sus esfuerzos en las cosas más importantes de la vida?",
                "opciones": [
                    "Sí, todo está bajo control",
                    "A veces sí, a veces los esfuerzos no van hacia lo verdaderamente importante",
                    "En general el esfuerzo impacta en las cosas importantes",
                    "Uno hace muchas cosas, pero el resultado no se puede controlar, siempre pasan cosas",
                ],
            },
            {
                "key": "disp_eventos_12m",
                "tipo": "checkboxes",
                "texto": "¿Cómo lo encuentra el comienzo del año? ¿Qué cosas le han pasado en los últimos 12 meses?",
                "opciones": [
                    "Muerte de un miembro cercano de su familia o amigo cercano",
                    "Ha tenido alguna enfermedad incapacitante",
                    "Ha requerido hospitalización",
                    "Algún pariente cercano con enfermedad grave",
                    "Se incrementaron sus responsabilidades laborales o fue asignado a un nuevo puesto",
                    "Ingresó a laborar en una nueva empresa",
                    "Aumentó la cantidad de viajes por trabajo",
                    "Fue despedido o suspendido de su trabajo",
                    "Ha tenido dificultades económicas",
                    "Compra de vivienda",
                    "Mudanza a otra ciudad",
                    "Adquirió un nuevo préstamo",
                    "Contrajo matrimonio o unión libre",
                    "Divorcio o terminación de relación de pareja",
                    "Nacimiento de un hijo",
                    "Ha tenido conflictos de pareja",
                    "Ha tenido problemas legales",
                    "Ha sufrido accidente de tránsito o accidente laboral",
                    "Ninguno de los anteriores",
                ],
            },
            {
                "key": "disp_preoc_robo_identidad",
                "tipo": "radio",
                "texto": "¿Qué nivel de preocupación le genera el robo de identidad?",
                "opciones": ["Ninguno", "Bajo", "Medio", "Alto", "Muy Alto"],
            },
            {
                "key": "disp_preoc_vaciamiento",
                "tipo": "radio",
                "texto": "¿Qué nivel de preocupación le genera el vaciamiento de cuentas bancarias?",
                "opciones": ["Ninguno", "Bajo", "Medio", "Alto", "Muy Alto"],
            },
            {
                "key": "disp_preoc_datos_delitos",
                "tipo": "radio",
                "texto": "¿Qué nivel de preocupación le genera el uso de sus datos para delitos?",
                "opciones": ["Ninguno", "Bajo", "Medio", "Alto", "Muy Alto"],
            },
            {
                "key": "disp_preoc_fotos_privadas",
                "tipo": "radio",
                "texto": "¿Qué nivel de preocupación le genera la exposición de fotos o información privada?",
                "opciones": ["Ninguno", "Bajo", "Medio", "Alto", "Muy Alto"],
            },
            {
                "key": "disp_preoc_infraestructura",
                "tipo": "radio",
                "texto": "¿Qué nivel de preocupación le generan los ataques a infraestructuras críticas?",
                "opciones": ["Ninguno", "Bajo", "Medio", "Alto", "Muy Alto"],
            },
            {
                "key": "disp_puede_ocurrir",
                "tipo": "radio",
                "texto": "Pensando en estas situaciones, ¿cuál le parece que puede ocurrir este año?",
                "opciones": [
                    "Que le hackeen su cuenta de mail personal",
                    "Que hackeen a su banco y alguien opere sus cuentas",
                    "Que haga una compra online y el producto nunca se reciba",
                    "Todas por igual",
                    "Ninguna de todas",
                ],
            },
            {
                "key": "disp_tec_mejora_laboral",
                "tipo": "slider",
                "texto": "¿Cuál es su idea sobre la tecnología? – Creo que puede mejorar mi desempeño laboral",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_aprender_sencillo",
                "tipo": "slider",
                "texto": "Creo que aprender a usar tecnología es generalmente sencillo",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_confianza_digital",
                "tipo": "slider",
                "texto": "Confío en mi capacidad para dominar nuevas herramientas digitales",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_apoyo_equipo",
                "tipo": "slider",
                "texto": "Mi equipo y superiores me apoyarían en el proceso de adopción de nuevas tecnologías",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_exp_positiva",
                "tipo": "slider",
                "texto": "He tenido experiencias positivas con la adopción de nuevas tecnologías",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_innovacion_valorada",
                "tipo": "slider",
                "texto": "En lo que yo hago se valora la innovación y el aprendizaje digital",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_preocupa_sustitucion",
                "tipo": "slider",
                "texto": "Me preocupa que la tecnología sustituya parte de mis tareas",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_beneficio_clientes",
                "tipo": "slider",
                "texto": "El uso de esta tecnología beneficia a todos, especialmente a clientes o usuarios",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_recursos_tiempo",
                "tipo": "slider",
                "texto": "Tengo recursos y tiempo para aprender a usar tecnología",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tec_probar_mas",
                "tipo": "slider",
                "texto": "Me gustaría probar y utilizar más la tecnología en mi trabajo",
                "min": 1, "max": 5, "labels_min": "Muy en desacuerdo", "labels_max": "Muy de acuerdo",
            },
            {
                "key": "disp_tendencias_2026",
                "tipo": "checkboxes",
                "texto": "¿Qué tendencias cree que marcarán el panorama de ciberseguridad en Uruguay 2026?",
                "opciones": [
                    "Cibercrimen como servicio",
                    "Mayor profesionalización del ataque",
                    "Reducción de phishing",
                    "Más filtraciones de datos públicos",
                ],
            },
            {
                "key": "disp_ranking_ciberseg",
                "tipo": "ranking",
                "texto": "Ordene las siguientes entidades de mayor a menor nivel de cuidado de la ciberseguridad:",
                "opciones": [
                    "La legislación del país",
                    "AGESIC",
                    "La educación media",
                    "Los responsables de informática",
                ],
            },
            {
                "key": "disp_efectivo_reducir_riesgo",
                "tipo": "multiselect",
                "texto": "¿Qué considera más efectivo para reducir los ciber riesgos? (máx. 3)",
                "opciones": [
                    "Educación Digital",
                    "Legislación más estricta",
                    "Mayor responsabilidad de empresas tecnológicas",
                    "Seguros contra ciber riesgos",
                    "Herramientas de protección más simples",
                    "Conciencia individual y buenos hábitos digitales",
                ],
            },
            {
                "key": "disp_leyes_apoyaria",
                "tipo": "checkboxes",
                "texto": "¿Cuál/es de las siguientes leyes apoyaría?",
                "opciones": [
                    "Clases de ciudadanía digital en escuelas, con énfasis en el uso de dispositivos inteligentes",
                    "Clases de ciudadanía digital en liceos para las relaciones virtuales en redes sociales",
                    "Clases de ciudadanía digital en los lugares de trabajo para prevención de ciberataques",
                ],
            },
            {
                "key": "disp_linea_emergencia",
                "tipo": "radio_si_no",
                "texto": "¿Considera útil y/o necesario contar con una línea telefónica de emergencias de ciberseguridad disponible fuera del horario laboral?",
            },
            {
                "key": "disp_portal_reporte",
                "tipo": "radio_si_no",
                "texto": "En caso de detectar una amenaza, ¿utilizaría un portal web o formulario en línea confiable para reportarlo?",
            },
            {
                "key": "disp_seguro_empresa",
                "tipo": "radio",
                "texto": "¿Su empresa tiene un seguro contra ciberataques?",
                "opciones": ["Sí", "No", "No sé / No estoy seguro"],
            },
            {
                "key": "disp_seguro_cobertura",
                "tipo": "radio",
                "texto": "Si tiene seguro, ¿cubre lucro cesante, pago de rescate, consultoría de TI y campañas de reputación?",
                "opciones": ["Sí", "No", "No sé / No estoy seguro"],
                "condicional": {
                    "trigger_key": "disp_seguro_empresa",
                    "trigger_values": ["Sí"],
                },
            },
            {
                "key": "disp_simulacros_empresa",
                "tipo": "radio",
                "texto": "En su lugar de trabajo, ¿ya han realizado simulacros de ciberataques?",
                "opciones": ["Sí", "No", "No sé / No estoy seguro"],
            },
            {
                "key": "disp_simulacros_tipo",
                "tipo": "checkboxes",
                "texto": "Si realizaron simulacros, ¿qué tipo de situaciones se simularon?",
                "opciones": [
                    "Le roban el celular",
                    "Le hackearon su email",
                    "Le hackearon WhatsApp",
                    "No sé / No estoy seguro",
                ],
                "condicional": {
                    "trigger_key": "disp_simulacros_empresa",
                    "trigger_values": ["Sí"],
                },
            },
            {
                "key": "disp_simulacro_imaginario",
                "tipo": "radio",
                "texto": "¿Usted ha hecho un simulacro aunque sea imaginario?",
                "opciones": ["Sí", "No", "No sé / No estoy seguro"],
            },
        ],
    },

    # ── MÓDULO 6: Perfil de riesgo del usuario ────────────────────────────────
    {
        "titulo": "Mirada 6",
        "descripcion": "",
        "preguntas": [
            {
                "key": "perfil_dispositivos",
                "tipo": "checkboxes",
                "texto": "Seleccione los dispositivos electrónicos que utiliza habitualmente:",
                "opciones": ["Smartphone", "Tablet", "Laptop", "PC de escritorio", "Otro"],
            },
            {
                "key": "perfil_cuentas_email",
                "tipo": "radio",
                "texto": "¿Cuántas cuentas/casillas de correo electrónico utiliza (sumando laboral, educativo, social y personal)?",
                "opciones": ["1", "2", "3", "4 o más"],
            },
            {
                "key": "perfil_contrasenas",
                "tipo": "radio",
                "texto": "¿Cuántas contraseñas distintas estima que tiene «dentro de su cabeza»?",
                "opciones": ["Menos de 5", "Entre 5 y 10", "Entre 11 y 20", "Más de 20"],
            },
            {
                "key": "perfil_so_celular",
                "tipo": "radio",
                "texto": "¿Cuál es el sistema operativo de su celular?",
                "opciones": ["iOS", "Android", "Otro / No sabe"],
            },
            {
                "key": "perfil_mails_dia",
                "tipo": "radio",
                "texto": "¿Cuántos mails envías y recibes por día?",
                "opciones": [
                    "Entre 0 y 20 correos",
                    "Entre 20 y 50 correos",
                    "Entre 50 y 100 correos",
                    "Más de 100 correos cada día",
                ],
            },
            {
                "key": "perfil_dias_teletrabajo",
                "tipo": "radio",
                "texto": "¿Cuántos días por semana teletrabaja en forma remota?",
                "opciones": ["1", "2", "3", "4", "5", "No teletrabajo"],
            },
            {
                "key": "perfil_vpn",
                "tipo": "radio",
                "texto": "¿Tiene VPN para conectarse en forma segura a internet cuando teletrabaja?",
                "opciones": ["Sí", "No", "No sé"],
            },
            {
                "key": "perfil_apps_transporte",
                "tipo": "radio",
                "texto": "Apps de transporte (Uber, Cabify, etc.) – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_apps_comidas",
                "tipo": "radio",
                "texto": "Apps de comidas (PedidosYa, Rappi, etc.) – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_apps_entretenimiento",
                "tipo": "radio",
                "texto": "Apps de entretenimiento (Netflix, Prime Video, etc.) – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_linkedin",
                "tipo": "radio",
                "texto": "Redes sociales profesionales (LinkedIn) – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_boletines",
                "tipo": "radio",
                "texto": "¿Está suscrito a boletines informativos o medios digitales?",
                "opciones": ["No estoy suscrito", "Entre 1 y 3", "4 o más"],
            },
            {
                "key": "perfil_redes_noticias",
                "tipo": "radio",
                "texto": "¿Usa redes de noticias como X (Twitter), Threads, Facebook o similares?",
                "opciones": ["Sí, activamente", "Sí, ocasionalmente", "No"],
            },
            {
                "key": "perfil_instagram_uso",
                "tipo": "radio",
                "texto": "Instagram – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_facebook_uso",
                "tipo": "radio",
                "texto": "Facebook – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_tiktok_uso",
                "tipo": "radio",
                "texto": "TikTok – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_youtube_uso",
                "tipo": "radio",
                "texto": "YouTube – intensidad de uso:",
                "opciones": ["A diario", "Una vez por semana", "Muy esporádica", "Nunca"],
            },
            {
                "key": "perfil_horas_pantalla",
                "tipo": "radio",
                "texto": "¿Cuántas horas por día dedica al entretenimiento en pantalla?",
                "opciones": [
                    "Aproximadamente 1 hora diaria",
                    "Entre 2 y 3 horas diarias",
                    "Aproximadamente 4 horas diarias",
                    "Más de 5 horas diarias",
                ],
            },
            {
                "key": "perfil_alteraciones_sueño",
                "tipo": "radio_si_no",
                "texto": "En el último año, ¿ha experimentado alteraciones en el sueño y/o insomnio?",
            },
            {
                "key": "perfil_adiccion_celular",
                "tipo": "radio_si_no",
                "texto": "En el último año, ¿ha experimentado adicción comportamental al celular?",
            },
            {
                "key": "perfil_multitarea_habito",
                "tipo": "radio",
                "texto": "¿Cuál de las siguientes describe mejor su forma de trabajar?",
                "opciones": [
                    "Ordeno las tareas a realizar y las hago una a la vez",
                    "Hago varias cosas a la vez, especialmente cuando falta tiempo",
                    "Siempre estoy haciendo y pensando varias cosas a la vez",
                ],
            },
            {
                "key": "perfil_dos_pantallas",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia utiliza dos o más pantallas al mismo tiempo mientras trabaja o estudia?",
                "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_revisa_notif_concentracion",
                "tipo": "radio",
                "texto": "Mientras realiza una tarea que requiere concentración, ¿con qué frecuencia revisa mensajes o redes sociales antes de terminar?",
                "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_cognitivo_multitarea",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia realiza varias tareas cognitivas al mismo tiempo (escribir un informe mientras responde mensajes o participa en una reunión)?",
                "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_tareas_automaticas",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia realiza tareas rutinarias (ordenar la casa, cocinar) mientras lee y responde mensajes?",
                "opciones": ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_conduccion",
                "tipo": "radio",
                "texto": "Cuando conduce un vehículo, ¿con qué frecuencia revisa mensajes, redes sociales o correos?",
                "opciones": ["Nunca", "Ocasionalmente", "Frecuentemente", "Siempre", "No conduzco"],
            },
            {
                "key": "perfil_menor_rendimiento",
                "tipo": "radio_si_no",
                "texto": "¿Ha visto que el «tiempo de pantalla» afecta el rendimiento académico de los niños a su cargo?",
                "condicional": {
                    "trigger_key": "unesco_cuidado",
                    "trigger_values": ["Sí, niñ@s de 6 a 12 años", "Sí, adolescentes de 12 a 18 años"],
                },
            },
            {
                "key": "perfil_menor_bienestar",
                "tipo": "radio_si_no",
                "texto": "¿Ha visto que el «tiempo de pantalla» afecta el bienestar emocional de los niños a su cargo?",
                "condicional": {
                    "trigger_key": "unesco_cuidado",
                    "trigger_values": ["Sí, niñ@s de 6 a 12 años", "Sí, adolescentes de 12 a 18 años"],
                },
            },
            {
                "key": "perfil_conoce_uso_problematico",
                "tipo": "radio_si_no",
                "texto": "¿Conoce a alguien que tenga un uso problemático del celular?",
            },
            {
                "key": "perfil_intento_reducir",
                "tipo": "radio_si_no",
                "texto": "¿Ha intentado reducir el tiempo de uso del celular y se ha sentido incapaz de lograrlo?",
            },
            {
                "key": "perfil_ansioso_sin_celular",
                "tipo": "radio_si_no",
                "texto": "¿Se siente nervioso, irritable o ansioso si pasa tiempo sin consultar sus mensajes o si no está localizable?",
            },
            {
                "key": "perfil_descuida_actividades",
                "tipo": "radio_si_no",
                "texto": "¿El uso del celular lo ha llevado a dejar de hacer actividades importantes (estudio, trabajo, sueño) o a descuidar relaciones personales?",
            },
            {
                "key": "perfil_sentimiento_hackeos",
                "tipo": "radio",
                "texto": "¿Cuál de las siguientes palabras expresa mejor sus sentimientos hacia los hackeos y los ciberataques?",
                "opciones": [
                    "No sé", "Indiferencia", "Distancia", "Alivio", "Incertidumbre",
                    "Tranquilidad", "Expectativa", "Esperanza", "Miedo", "Orgullo",
                ],
            },
            {
                "key": "perfil_informacion_ciberataques",
                "tipo": "radio",
                "texto": "¿Qué tan informado está sobre casos de ciberataque a empresas y organismos del Estado?",
                "opciones": [
                    "Muy informado",
                    "Tengo cierta información",
                    "Tengo poca información, pero gran preocupación",
                    "No tengo información y no sigo el tema",
                ],
            },
            {
                "key": "perfil_habitos_cyberseg",
                "tipo": "radio",
                "texto": "¿Cuál de las siguientes palabras expresa mejor sus hábitos personales en lo que refiere a ciberseguridad?",
                "opciones": [
                    "No sé", "Débiles e insuficientes", "Ni buenos ni malos",
                    "Mejorando rápidamente", "Fuertes y defensivos",
                ],
            },
            {
                "key": "perfil_ultima_radio",
                "tipo": "radio",
                "texto": "¿Cuándo fue la última vez que escuchó un informativo en radio?",
                "opciones": [
                    "Hoy", "En la última semana", "En el último mes",
                    "Hace más de un mes", "No recuerdo / Nunca",
                ],
            },
            {
                "key": "perfil_ultima_tv",
                "tipo": "radio",
                "texto": "¿Cuándo fue la última vez que vio un informativo en la TV?",
                "opciones": [
                    "Hoy", "En la última semana", "En el último mes",
                    "Hace más de un mes", "No recuerdo / Nunca",
                ],
            },
            {
                "key": "perfil_ultimo_diario",
                "tipo": "radio",
                "texto": "¿Cuándo fue la última vez que leyó un diario o portal de noticias online?",
                "opciones": [
                    "Hoy", "En la última semana", "En el último mes",
                    "Hace más de un mes", "No recuerdo / Nunca",
                ],
            },
            {
                "key": "perfil_igual_info_transito",
                "tipo": "radio",
                "texto": "¿Entiende que está igualmente informado de accidentes de ciberseguridad que de accidentes de tránsito?",
                "opciones": [
                    "Estoy informado de los accidentes de tránsito más importantes, pero no me entero de los ciberataques",
                    "Sí, estoy muy bien informado de accidentes de tránsito y de ciberataques",
                    "No estoy informado de accidentes de tránsito ni de ciberataques",
                ],
            },
            {
                "key": "perfil_info_suficiente_ciberataques",
                "tipo": "radio_si_no",
                "texto": "¿Considera que la información actual sobre ciberataques es suficiente y útil para tomar acciones de cuidado?",
            },
            {
                "key": "perfil_def_phishing",
                "tipo": "radio",
                "texto": "Un ciberataque donde los delincuentes suplantan a entidades de confianza mediante correos o mensajes falsos para robar contraseñas o datos bancarios. Esto es:",
                "opciones": ["Ransomware", "Phishing", "Malware", "Encriptación"],
            },
            {
                "key": "perfil_def_ransomware",
                "tipo": "radio",
                "texto": "Un software malicioso que bloquea el acceso a los datos críticos de una víctima, los destruye o los publica a menos que se pague un rescate. Esto es:",
                "opciones": ["Ransomware", "Phishing", "Malware", "Encriptación"],
            },
            {
                "key": "perfil_def_ingenieria_social",
                "tipo": "radio",
                "texto": "La ingeniería social es:",
                "opciones": [
                    "Una rama de la ingeniería que se especializa en la construcción de espacios públicos y viviendas sociales",
                    "Una táctica de manipular, influenciar o engañar a una víctima para obtener el control de un sistema informático o robar información personal y financiera",
                    "Una especialidad de ingeniería telemática que desarrolla programas de antivirus para proteger a los usuarios de redes sociales",
                ],
            },
            {
                "key": "perfil_def_2fa",
                "tipo": "radio",
                "texto": "La autenticación de dos factores es:",
                "opciones": [
                    "La clave especial que tienen los ingenieros informáticos para hacer cambios en los sistemas como administradores",
                    "Lo que se usa para hacer transferencias bancarias con doble firma, para que dos personas de la empresa hagan los pagos",
                    "Un método de seguridad que requiere dos formas distintas de verificación: además de saber la contraseña, hay que recibir un código por mail o SMS",
                ],
            },
            {
                "key": "perfil_frec_actualiza_dispositivos",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia actualiza sus dispositivos?",
                "opciones": ["Nunca", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_frec_contrasenas_distintas",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia usa contraseñas diferentes para distintas cuentas?",
                "opciones": ["Nunca", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_frec_2fa",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia activa la autenticación de 2 factores/pasos?",
                "opciones": ["Nunca", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_frec_permisos_apps",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia revisa permisos de Apps?",
                "opciones": ["Nunca", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_frec_copias_seguridad",
                "tipo": "radio",
                "texto": "¿Con qué frecuencia hace copias de seguridad?",
                "opciones": ["Nunca", "A veces", "Frecuentemente", "Siempre"],
            },
            {
                "key": "perfil_practicas_diarias",
                "tipo": "checkboxes",
                "texto": "¿Cuál/es de estas prácticas está aplicando diariamente?",
                "opciones": [
                    "Activar autenticación en dos pasos",
                    "Aceptar inmediatamente todas las solicitudes de amistad",
                    "Evitar compartir ubicación en tiempo real",
                    "Usar contraseñas distintas para cada cuenta",
                ],
            },
            {
                "key": "perfil_qr",
                "tipo": "radio",
                "texto": "Antes de escanear un código QR:",
                "opciones": [
                    "Veo la URL a la que apunta y solo ingreso si es HTTPS",
                    "Verifico que la URL no esté acortada ni parezca sospechosa y entonces ingreso",
                    "Entro directamente, no suelo revisar nada",
                    "Ninguna de las anteriores",
                ],
            },
            {
                "key": "perfil_barreras_ciberseg",
                "tipo": "multiselect",
                "texto": "¿Por qué se hace 'cuesta arriba' estar actualizado en hábitos personales de ciberseguridad? (Seleccioná todas las que apliquen)",
                "opciones": [
                    "Porque uno siente temor a ser juzgado o parecer desactualizado si hace preguntas básicas",
                    "Porque uno se siente culpable de haber hecho algo malo sin mala intención",
                    "Porque en realidad es un tema de personas muy importantes a las que quieren ventilarles escándalos",
                    "Porque las empresas grandes son las que se encargan de estos temas, no es algo que me tenga que preocupar a mí",
                    "Por falta de tiempo para más procedimientos y controles",
                    "No percibo ninguna barrera",
                ],
            },
        ],
    },

    # ── MÓDULO 7: Dato fundamental – CI ──────────────────────────────────────
    {
        "titulo": "Mirada 7",
        "descripcion": "Datos socioeconómicos y demográficos del participante.",
        "preguntas": [
            # ── Año de nacimiento ────────────────────────────────────────────
            {
                "key": "ci_anio_nacimiento",
                "tipo": "selectbox",
                "texto": "¿En qué año nació?",
                "opciones": [str(a) for a in range(2008, 1939, -1)],
            },
            # ── Sexo al nacer ────────────────────────────────────────────────
            {
                "key": "ci_sexo",
                "tipo": "radio",
                "texto": "Sexo al nacer",
                "opciones": ["Hombre", "Mujer"],
            },
            # ── Grado de educación ───────────────────────────────────────────
            {
                "key": "ci_educacion",
                "tipo": "radio",
                "texto": "Grado de educación alcanzado hasta el momento",
                "opciones": [
                    "Ciclo básico de educación secundaria, técnica o militar incompleta",
                    "Ciclo básico de educación secundaria, técnica o militar completa",
                    "Bachillerato de educación secundaria, técnica o militar incompleta",
                    "Bachillerato de educación secundaria, técnica o militar completa",
                    "Educación terciaria incompleta (Universidad, Magisterio, Profesorado)",
                    "Educación terciaria completa (Universidad, Magisterio, Profesorado)",
                    "Maestría o Doctorado completo",
                ],
            },
            # ── Situación laboral ────────────────────────────────────────────
            {
                "key": "ci_situacion_laboral",
                "tipo": "radio",
                "texto": "¿Cuál de estas situaciones describe mejor su situación laboral?",
                "opciones": [
                    "Estudiando o capacitándose",
                    "Empleado (asalariado público o privado) que depende de un superior que está en Uruguay",
                    "Empleado (asalariado público o privado) que depende de un superior que está fuera del país",
                    "Empleado (asalariado público o privado) con un equipo de colaboradores a cargo que está en Uruguay",
                    "Empleado (asalariado público o privado) con un equipo de colaboradores que está total o parcialmente fuera de Uruguay",
                    "Cuenta propia con local",
                    "Profesional independiente",
                    "Ayudando a un miembro de la familia en un emprendimiento familiar",
                    "Desempleado (sin empleo o buscando trabajo)",
                    "Jubilado o pensionista",
                    "En el servicio militar",
                    "Se dedica a las tareas del hogar",
                    "Enfermo o incapacitado por largo tiempo o de manera permanente",
                    "Otra situación",
                ],
            },
            # ── Región con la que trabaja (condicional) ──────────────────────
            {
                "key": "ci_region_trabajo",
                "tipo": "selectbox",
                "texto": "¿Con qué región trabaja su superior / equipo fuera del país?",
                "opciones": [
                    "Estados Unidos: Costa Este",
                    "Estados Unidos: Costa Oeste",
                    "América Latina y Caribe",
                    "Europa",
                    "China",
                    "India",
                    "Otros",
                ],
                "condicional": {
                    "trigger_key": "ci_situacion_laboral",
                    "trigger_values": [
                        "Empleado (asalariado público o privado) que depende de un superior que está fuera del país",
                        "Empleado (asalariado público o privado) con un equipo de colaboradores que está total o parcialmente fuera de Uruguay",
                    ],
                },
            },
            # ── Personas en el hogar ─────────────────────────────────────────
            {
                "key": "ci_personas_hogar",
                "tipo": "selectbox",
                "texto": "¿Cuántas personas viven habitualmente en su hogar?",
                "opciones": [str(n) for n in range(1, 16)],
            },
            {
                "key": "ci_menores_14",
                "tipo": "selectbox",
                "texto": "Indique cuántas personas que viven en su hogar tienen menos de 14 años",
                "opciones": [str(n) for n in range(0, 16)],
            },
            {
                "key": "ci_mayores_65",
                "tipo": "selectbox",
                "texto": "Indique cuántas personas que viven en su hogar tienen 65 años o más",
                "opciones": [str(n) for n in range(0, 16)],
            },
            # ── Rol en el hogar ──────────────────────────────────────────────
            {
                "key": "ci_rol_hogar",
                "tipo": "radio",
                "texto": "¿Cuál es la respuesta que mejor define su rol en el hogar?",
                "opciones": [
                    "Jefe/Jefa de hogar",
                    "Comparten la Jefatura del Hogar",
                    "Cónyuge del Jefe/Jefa",
                    "Hijo/Hija",
                    "Abuelo/Abuela",
                    "Otro",
                ],
            },
            # ── Baños y habitaciones ─────────────────────────────────────────
            {
                "key": "ci_total_banios",
                "tipo": "selectbox",
                "texto": "¿Cuál es el total de baños que tiene su hogar?",
                "opciones": [str(n) for n in range(0, 11)],
            },
            {
                "key": "ci_total_habitaciones",
                "tipo": "selectbox",
                "texto": "¿Cuál es el total de habitaciones que utiliza en su hogar, sin ser baño y cocina?",
                "opciones": [str(n) for n in range(0, 16)],
            },
            # ── Servicio doméstico ───────────────────────────────────────────
            {
                "key": "ci_servicio_domestico",
                "tipo": "radio",
                "texto": "¿Su hogar paga (en dinero o de otra forma) a personas para que limpien la vivienda, cuiden niños o ancianos o realicen alguna tarea doméstica?",
                "opciones": ["Sí", "No"],
            },
            # ── Lugar donde nació ────────────────────────────────────────────
            {
                "key": "ci_lugar_nacimiento",
                "tipo": "radio",
                "texto": "Lugar donde nació y vivió su infancia",
                "opciones": ["Uruguay", "En el exterior"],
            },
            {
                "key": "ci_nacimiento_pais",
                "tipo": "selectbox",
                "texto": "¿En qué país nació?",
                "opciones": [
                    "Argentina", "Bolivia", "Brasil", "Chile", "Colombia",
                    "Costa Rica", "Cuba", "Ecuador", "El Salvador",
                    "España", "Estados Unidos", "Guatemala", "Honduras",
                    "México", "Nicaragua", "Panamá", "Paraguay", "Perú",
                    "Portugal", "Puerto Rico", "República Dominicana",
                    "Venezuela", "Otro",
                ],
                "condicional": {
                    "trigger_key": "ci_lugar_nacimiento",
                    "trigger_values": ["En el exterior"],
                },
            },
            # ── Lugar donde vive actualmente ─────────────────────────────────
            {
                "key": "ci_lugar_residencia",
                "tipo": "radio",
                "texto": "Lugar en donde hoy vive",
                "opciones": ["Uruguay", "En el exterior"],
            },
            {
                "key": "ci_residencia_departamento",
                "tipo": "selectbox",
                "texto": "¿En qué departamento vive?",
                "opciones": [
                    "Artigas", "Canelones", "Cerro Largo", "Colonia",
                    "Durazno", "Flores", "Florida", "Lavalleja",
                    "Maldonado", "Montevideo", "Paysandú", "Río Negro",
                    "Rivera", "Rocha", "Salto", "San José",
                    "Soriano", "Tacuarembó", "Treinta y Tres",
                ],
                "condicional": {
                    "trigger_key": "ci_lugar_residencia",
                    "trigger_values": ["Uruguay"],
                },
            },
            {
                "key": "ci_residencia_pais",
                "tipo": "selectbox",
                "texto": "¿En qué país vive?",
                "opciones": [
                    "Argentina", "Bolivia", "Brasil", "Chile", "Colombia",
                    "Costa Rica", "Cuba", "Ecuador", "El Salvador",
                    "España", "Estados Unidos", "Guatemala", "Honduras",
                    "México", "Nicaragua", "Panamá", "Paraguay", "Perú",
                    "Portugal", "Puerto Rico", "República Dominicana",
                    "Venezuela", "Otro",
                ],
                "condicional": {
                    "trigger_key": "ci_lugar_residencia",
                    "trigger_values": ["En el exterior"],
                },
            },
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────────────────────────

def scroll_to_top():
    """Marca el flag para que al inicio del próximo render se haga scroll al top."""
    st.session_state["_scroll_top"] = True

def init_state():
    if "modulo_actual" not in st.session_state:
        st.session_state.modulo_actual = 0
    if "respuestas" not in st.session_state:
        st.session_state.respuestas = {}
    if "enviado" not in st.session_state:
        st.session_state.enviado = False
    if "_error_keys" not in st.session_state:
        st.session_state._error_keys = set()

init_state()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def check_condicional(pregunta: dict) -> bool:
    """Devuelve True si la pregunta debe mostrarse (no tiene condicional o se cumple)."""
    cond = pregunta.get("condicional")
    if not cond:
        return True
    trigger_key = cond["trigger_key"]
    trigger_values = cond["trigger_values"]
    valor_actual = st.session_state.respuestas.get(trigger_key)
    if valor_actual is None:
        return False
    if isinstance(valor_actual, list):
        return any(v in valor_actual for v in trigger_values)
    return valor_actual in trigger_values


def render_pregunta(p: dict):
    """Renderiza una pregunta y guarda la respuesta en session_state."""
    key = p["key"]
    tipo = p["tipo"]

    if not check_condicional(p):
        return

    error_keys = st.session_state.get("_error_keys", set())
    has_error = key in error_keys

    if has_error:
        st.markdown(
            "<div style='border-left: 4px solid #e74c3c; padding-left: 12px; "
            "background: rgba(231,76,60,0.06); border-radius: 4px; padding-top: 8px; "
            "padding-bottom: 4px; margin-bottom: 4px;'>",
            unsafe_allow_html=True,
        )

    _etiquetas = {
        "checkboxes":  " *(selección múltiple)*",
        "multiselect": " *(selección múltiple)*",
        "radio":       " *(opción única)*",
        "selectbox":   "",
        "radio_si_no": "",
        "vf":          "",
        "likert":      "",
        "slider":      "",
        "ranking":     "",
        "text":        "",
        "consent":     "",
    }
    texto = p["texto"] + _etiquetas.get(tipo, "")

    if tipo == "consent":
        current = st.session_state.respuestas.get(key, False)
        val = st.checkbox(texto, value=current, key=f"widget_{key}")
        st.session_state.respuestas[key] = val

    elif tipo == "text":
        val = st.text_input(
            texto,
            value=st.session_state.respuestas.get(key, ""),
            placeholder=p.get("placeholder", ""),
            key=f"widget_{key}",
        )
        st.session_state.respuestas[key] = val

    elif tipo == "radio":
        opciones = p["opciones"]
        current = st.session_state.respuestas.get(key)
        idx = opciones.index(current) if current in opciones else None
        val = st.radio(texto, opciones, index=idx, key=f"widget_{key}")
        st.session_state.respuestas[key] = val

    elif tipo == "selectbox":
        opciones = p["opciones"]
        current = st.session_state.respuestas.get(key)
        options_with_placeholder = ["Seleccionar..."] + opciones
        idx = options_with_placeholder.index(current) if current in options_with_placeholder else 0
        val = st.selectbox(texto, options_with_placeholder, index=idx, key=f"widget_{key}")
        st.session_state.respuestas[key] = val if val != "Seleccionar..." else None

    elif tipo == "radio_si_no":
        opciones = ["Sí", "No"]
        current = st.session_state.respuestas.get(key)
        idx = opciones.index(current) if current in opciones else None
        val = st.radio(texto, opciones, index=idx, horizontal=True, key=f"widget_{key}")
        st.session_state.respuestas[key] = val

    elif tipo == "vf":
        opciones = ["Verdadero", "Falso"]
        current = st.session_state.respuestas.get(key)
        idx = opciones.index(current) if current in opciones else None
        val = st.radio(texto, opciones, index=idx, horizontal=True, key=f"widget_{key}")
        st.session_state.respuestas[key] = val

    elif tipo == "likert":
        opciones = [
            "Muy de acuerdo", "De acuerdo",
            "Ni de acuerdo ni en desacuerdo",
            "En desacuerdo", "Muy en desacuerdo",
        ]
        current = st.session_state.respuestas.get(key)
        idx = opciones.index(current) if current in opciones else None
        val = st.radio(texto, opciones, index=idx, key=f"widget_{key}")
        st.session_state.respuestas[key] = val

    elif tipo == "checkboxes":
        st.write(f"**{texto}**")
        opciones = p["opciones"]
        current = st.session_state.respuestas.get(key, [])
        seleccionadas = []
        for op in opciones:
            checked = st.checkbox(op, value=(op in current), key=f"widget_{key}_{op}")
            if checked:
                seleccionadas.append(op)
        st.session_state.respuestas[key] = seleccionadas

    elif tipo == "multiselect":
        current = st.session_state.respuestas.get(key, [])
        val = st.multiselect(texto, p["opciones"], default=current, key=f"widget_{key}")
        st.session_state.respuestas[key] = val

    elif tipo == "slider":
        current = st.session_state.respuestas.get(key, p["min"])
        val = st.slider(
            f"{texto}  \n_{p['labels_min']} → {p['labels_max']}_",
            min_value=p["min"],
            max_value=p["max"],
            value=current,
            key=f"widget_{key}",
        )
        st.session_state.respuestas[key] = val

    elif tipo == "ranking":
        opciones = p["opciones"]
        st.write(f"**{texto}**")
        st.caption("Seleccioná cada opción en el lugar que corresponde (1 = mayor cuidado).")
        current = st.session_state.respuestas.get(key, {})
        lugares = ["1er lugar", "2do lugar", "3er lugar", "4to lugar"]
        ranking_result = {}
        for lugar in lugares[:len(opciones)]:
            prev = current.get(lugar, opciones[0])
            if prev not in opciones:
                prev = opciones[0]
            sel = st.selectbox(lugar, opciones, index=opciones.index(prev), key=f"widget_{key}_{lugar}")
            ranking_result[lugar] = sel
        st.session_state.respuestas[key] = ranking_result

    if has_error:
        st.markdown(
            "<span style='color:#e74c3c; font-size:0.85rem;'>⚠ Esta pregunta es obligatoria</span>"
            "</div>",
            unsafe_allow_html=True,
        )


def validar_modulo(modulo: dict) -> tuple[list[str], set[str]]:
    """Devuelve (lista de mensajes de error, set de keys con error)."""
    errores = []
    keys_error = set()
    for p in modulo["preguntas"]:
        if not check_condicional(p):
            continue
        key = p["key"]
        tipo = p["tipo"]
        val = st.session_state.respuestas.get(key)

        if tipo == "consent":
            if not val:
                errores.append("Debés aceptar el consentimiento para continuar.")
                keys_error.add(key)
            continue

        if tipo == "text" and key == "email":
            if not val or not val.strip():
                errores.append("El email es obligatorio.")
                keys_error.add(key)
            elif "@" not in val:
                errores.append("El email no parece válido.")
                keys_error.add(key)

        elif tipo in ("radio", "radio_si_no", "vf", "likert", "selectbox"):
            if val is None:
                label = p["texto"][:60] + "..." if len(p["texto"]) > 60 else p["texto"]
                errores.append(f"Falta responder: «{label}»")
                keys_error.add(key)

    return errores, keys_error


# ─────────────────────────────────────────────────────────────────────────────
# PANTALLA FINAL
# ─────────────────────────────────────────────────────────────────────────────

def pantalla_final():
    col_logo, _ = st.columns([1, 4])
    with col_logo:
        st.image("logo_kaiden.png", width=160)
    st.markdown("<div class='kaiden-subtext'>Ciber Window</div>", unsafe_allow_html=True)
    st.divider()
    st.title("¡Muchas gracias!")
    st.markdown(
        "<p style='color:#7a9bb5; font-size:1.05rem;'>Tus respuestas fueron guardadas correctamente. "
        "Tu participación nos ayuda a construir una ciudadanía digital más fuerte.</p>",
        unsafe_allow_html=True,
    )
    st.success("Respuestas registradas.")
    st.balloons()
    if st.button("Completar otra encuesta"):
        st.session_state.modulo_actual = 0
        st.session_state.respuestas = {}
        st.session_state.enviado = False
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ENVÍO FINAL
# ─────────────────────────────────────────────────────────────────────────────

def _build_master_columns() -> list[str]:
    """
    Genera la lista canónica de columnas en el orden exacto del formulario,
    expandiendo las preguntas tipo 'ranking' en sus sub-columnas.
    Siempre incluye todas las preguntas, independientemente de condicionales.
    """
    cols = []
    for modulo in MODULOS:
        for p in modulo["preguntas"]:
            if p["tipo"] == "ranking":
                for i in range(1, len(p["opciones"]) + 1):
                    lugar = ["1er lugar", "2do lugar", "3er lugar", "4to lugar"][i - 1]
                    cols.append(f"{p['key']}_{lugar}")
            else:
                cols.append(p["key"])
    return cols

MASTER_COLUMNS = _build_master_columns()


def enviar_respuestas():
    """Aplana respuestas y las envía a Google Sheets usando columnas fijas."""
    # Aplanar todo a strings
    respuestas_planas = {}
    for key, val in st.session_state.respuestas.items():
        if isinstance(val, list):
            respuestas_planas[key] = " | ".join(val)
        elif isinstance(val, dict):
            for subkey, subval in val.items():
                respuestas_planas[f"{key}_{subkey}"] = subval
        else:
            respuestas_planas[key] = val

    email = st.session_state.respuestas.get("email", "")

    with st.spinner("Guardando respuestas ..."):
        ok, msg = guardar_en_google_sheets(email, respuestas_planas, MASTER_COLUMNS)

    if ok:
        st.session_state.enviado = True
        st.rerun()
    else:
        st.error(f"Error al guardar: {msg}")
        print(f"[app] Error al guardar: {msg}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# RENDER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

# Scroll al top si viene de navegación entre módulos
if st.session_state.pop("_scroll_top", False):
    st.components.v1.html(
        """<script>
        setTimeout(function() {
            const targets = [
                window.parent.document.querySelector('[data-testid="stMainBlockContainer"]'),
                window.parent.document.querySelector('[data-testid="stMain"]'),
                window.parent.document.querySelector('.main'),
                window.parent.document.body,
            ];
            targets.forEach(el => { if (el) el.scrollTop = 0; });
            window.parent.scrollTo(0, 0);
        }, 50);
        </script>""",
        height=0,
    )

# Header de marca con logo real
st.markdown("<div style='padding-top: 1.5rem;'></div>", unsafe_allow_html=True)
col_logo, _ = st.columns([1, 4])
with col_logo:
    st.image("logo_kaiden.png", width=160)
st.markdown("<div class='kaiden-subtext'>Ciber Window</div>", unsafe_allow_html=True)
st.divider()

if st.session_state.enviado:
    pantalla_final()
else:
    total = len(MODULOS)
    actual = st.session_state.modulo_actual
    modulo = MODULOS[actual]

    # Barra de progreso
    total_miradas = total - 1  # module 0 is data collection, not a "Mirada"
    if actual == 0:
        progress_text = "Datos del participante"
    else:
        progress_text = f"Mirada {actual}/{total_miradas}"
    st.progress((actual) / total, text=progress_text)

    st.title(f"{modulo['titulo']}")
    if modulo["descripcion"]:
        st.caption(modulo["descripcion"])

    # Banner de errores si hay preguntas sin contestar
    if st.session_state._error_keys:
        n = len(st.session_state._error_keys)
        st.error(f"Hay {n} pregunta{'s' if n > 1 else ''} sin contestar. Están marcadas en rojo.")

    st.divider()

    # Renderizar preguntas del módulo actual
    for p in modulo["preguntas"]:
        render_pregunta(p)
        st.write("")

    st.divider()

    # Botones de navegación
    es_ultimo = actual == total - 1
    label = "Enviar respuestas ✅" if es_ultimo else "Siguiente →"

    def _handle_siguiente():
        errores, keys_error = validar_modulo(modulo)
        if errores:
            st.session_state._error_keys = keys_error
            scroll_to_top()
            st.rerun()
        else:
            st.session_state._error_keys = set()
            if es_ultimo:
                enviar_respuestas()
            else:
                st.session_state.modulo_actual += 1
                scroll_to_top()
                st.rerun()

    if actual > 0:
        col_prev, col_mid, col_next = st.columns([2, 1, 2])
        with col_prev:
            if st.button("← Anterior", use_container_width=True):
                st.session_state._error_keys = set()
                st.session_state.modulo_actual -= 1
                scroll_to_top()
                st.rerun()
        with col_next:
            if st.button(label, type="primary", use_container_width=True):
                _handle_siguiente()
    else:
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            if st.button(label, type="primary", use_container_width=True):
                _handle_siguiente()
