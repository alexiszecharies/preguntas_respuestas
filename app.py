"""
Cyber Window - Encuesta multi-módulo
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
    page_title="Cyber Window · Encuesta",
    page_icon="🔐",
    layout="centered",
)

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
    # ── MÓDULO 0: Datos del respondente ──────────────────────────────────────
    {
        "titulo": "Datos de contacto",
        "descripcion": "Antes de comenzar, ingresá tu email.",
        "preguntas": [
            {
                "key": "email",
                "tipo": "text",
                "texto": "Email (obligatorio)",
                "placeholder": "tu@email.com",
            },
        ],
    },

    # ── MÓDULO 1: UNESCO ──────────────────────────────────────────────────────
    {
        "titulo": "Módulo UNESCO – Comparación Diálogo Político",
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
                "tipo": "vf",
                "texto": "Entre las nuevas palabras añadidas al Diccionario Oxford en 2024 se encontraban «doomscrolling» y «brain-rot». Ambas son símbolos de la omnipresencia del uso poco saludable de las redes sociales impulsado por algoritmos de inteligencia artificial.",
            },
            {
                "key": "unesco_vf_tecnologia_aprendizaje",
                "tipo": "vf",
                "texto": "Algunas tecnologías pueden favorecer el aprendizaje en algunos contextos, pero no cuando se usan en exceso o de forma inapropiada.",
            },
            {
                "key": "unesco_vf_celular_clase",
                "tipo": "vf",
                "texto": "Tener un teléfono inteligente en clase puede interrumpir el aprendizaje.",
            },
            {
                "key": "unesco_vf_notificaciones",
                "tipo": "vf",
                "texto": "Tener un teléfono móvil cerca con notificaciones es suficiente para que los estudiantes pierdan la atención de la tarea en cuestión.",
            },
            {
                "key": "unesco_vf_prohibicion_politica",
                "tipo": "vf",
                "texto": "Prohibir el teléfono en el colegio es una decisión política sobre las prioridades generales de la sociedad: pone al bienestar y la educación por encima de la conveniencia inmediata de la conectividad.",
            },
            {
                "key": "unesco_vf_refugio",
                "tipo": "vf",
                "texto": "Prohibir o limitar el uso de celular permite que la escuela recupere su papel como refugio de aprendizaje, libre (al menos por unas horas) de las distracciones del mundo exterior.",
            },
        ],
    },

    # ── MÓDULO 2: Diario El País ──────────────────────────────────────────────
    {
        "titulo": "Módulo Comparación con Diario El País",
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
        "titulo": "Módulo Comparación con EUTIC 2024",
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
        "titulo": "Módulo Comparación con McKinsey – IA en Organizaciones",
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
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Innovación",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_empleados",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Satisfacción de los empleados",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_competitiva",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Diferenciación competitiva",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_costos",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Costos",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_rentabilidad",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Rentabilidad",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_ingresos",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Ingresos orgánicos",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_talento",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Atracción y retención del talento",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_mercado",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Participación de mercado",
                "min": 1, "max": 5, "labels_min": "Nada", "labels_max": "Completamente",
            },
            {
                "key": "mck_ia_impacto_clientes",
                "tipo": "slider",
                "texto": "¿Hasta qué punto la IA impactó en los resultados del último año? – Satisfacción del cliente",
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
        "titulo": "Módulo – Disponibilidad Real para Aprender IA y CS",
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
        "titulo": "Módulo – Perfil de Riesgo del Usuario",
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
                "key": "perfil_menor_cargo",
                "tipo": "radio_si_no",
                "texto": "¿Es usted responsable de supervisar el uso de internet y dispositivos de algún menor de edad?",
            },
            {
                "key": "perfil_menor_rendimiento",
                "tipo": "radio_si_no",
                "texto": "¿Ha visto que el «tiempo de pantalla» afecta el rendimiento académico de los niños a su cargo?",
                "condicional": {
                    "trigger_key": "perfil_menor_cargo",
                    "trigger_values": ["Sí"],
                },
            },
            {
                "key": "perfil_menor_bienestar",
                "tipo": "radio_si_no",
                "texto": "¿Ha visto que el «tiempo de pantalla» afecta el bienestar emocional de los niños a su cargo?",
                "condicional": {
                    "trigger_key": "perfil_menor_cargo",
                    "trigger_values": ["Sí"],
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
]

# ─────────────────────────────────────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────────────────────────

def init_state():
    if "modulo_actual" not in st.session_state:
        st.session_state.modulo_actual = 0
    if "respuestas" not in st.session_state:
        st.session_state.respuestas = {}
    if "enviado" not in st.session_state:
        st.session_state.enviado = False

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
    texto = p["texto"]
    tipo = p["tipo"]

    if not check_condicional(p):
        return

    if tipo == "text":
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


def validar_modulo(modulo: dict) -> list[str]:
    """Devuelve lista de errores de validación del módulo actual."""
    errores = []
    for p in modulo["preguntas"]:
        if not check_condicional(p):
            continue
        key = p["key"]
        tipo = p["tipo"]
        val = st.session_state.respuestas.get(key)

        if tipo == "text" and key == "email":
            if not val or not val.strip():
                errores.append("El email es obligatorio.")
            elif "@" not in val:
                errores.append("El email no parece válido.")

        elif tipo in ("radio", "radio_si_no", "vf"):
            if val is None:
                errores.append(f"Falta responder: «{p['texto'][:60]}...»" if len(p['texto']) > 60 else f"Falta responder: «{p['texto']}»")

    return errores


# ─────────────────────────────────────────────────────────────────────────────
# PANTALLA FINAL
# ─────────────────────────────────────────────────────────────────────────────

def pantalla_final():
    st.title("🎉 ¡Muchas gracias!")
    st.success("Tus respuestas fueron guardadas correctamente en la planilla.")
    st.balloons()
    if st.button("Completar otra encuesta"):
        st.session_state.modulo_actual = 0
        st.session_state.respuestas = {}
        st.session_state.enviado = False
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ENVÍO FINAL
# ─────────────────────────────────────────────────────────────────────────────

def enviar_respuestas():
    """Aplana respuestas y las envía a Google Sheets."""
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
    columnas = list(respuestas_planas.keys())

    with st.spinner("Guardando respuestas en Google Sheets..."):
        ok, msg = guardar_en_google_sheets(email, respuestas_planas, columnas)

    if ok:
        st.session_state.enviado = True
        st.rerun()
    else:
        st.error(f"Error al guardar: {msg}")
        print(f"[app] Error al guardar: {msg}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# RENDER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.enviado:
    pantalla_final()
else:
    total = len(MODULOS)
    actual = st.session_state.modulo_actual
    modulo = MODULOS[actual]

    # Barra de progreso
    st.progress((actual) / total, text=f"Módulo {actual + 1} de {total}")

    st.title(f"🔐 {modulo['titulo']}")
    if modulo["descripcion"]:
        st.caption(modulo["descripcion"])

    st.divider()

    # Renderizar preguntas del módulo actual
    for p in modulo["preguntas"]:
        render_pregunta(p)
        st.write("")

    st.divider()

    # Botones de navegación
    col_prev, col_next = st.columns([1, 3])

    with col_prev:
        if actual > 0:
            if st.button("← Anterior", use_container_width=True):
                st.session_state.modulo_actual -= 1
                st.rerun()

    with col_next:
        es_ultimo = actual == total - 1
        label = "Enviar respuestas ✅" if es_ultimo else "Siguiente →"

        if st.button(label, type="primary", use_container_width=True):
            errores = validar_modulo(modulo)
            if errores:
                for e in errores:
                    st.error(e)
            else:
                if es_ultimo:
                    enviar_respuestas()
                else:
                    st.session_state.modulo_actual += 1
                    st.rerun()
