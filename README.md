# Preguntas y respuestas (Streamlit + planilla)

App en Streamlit para subir preguntas, que la gente responda y que las respuestas se registren en una planilla (Google Sheets o CSV local).

## Qué hace

- **Preguntas en código**: las preguntas y sus opciones están en `app.py` en la lista `PREGUNTAS`. Las actualizás cuando quieras (ej. cada semana).
- **Formulario**: la gente responde con opción múltiple (una opción por pregunta).
- **Guardado**: las respuestas se registran en Google Sheets (si está configurado) o en `respuestas.csv` en la carpeta del proyecto.

## Requisitos

- **Python 3.10+** (3.10, 3.11 o 3.12). Streamlit ya no soporta 3.8. Si usas pyenv: en la carpeta del proyecto `.python-version` fija 3.10; con `pyenv install 3.10` ya tenés una versión compatible.

## Cómo ejecutarlo

```bash
cd preguntas_kaiden
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Abre en el navegador la URL que muestre Streamlit (por defecto http://localhost:8501).

## Cómo conseguir credenciales de Google (paso a paso)

### 1. Ir a Google Cloud Console

- Abre **[console.cloud.google.com](https://console.cloud.google.com/)** e inicia sesión con tu cuenta de Google.

### 2. Crear un proyecto (o usar uno existente)

- Arriba a la izquierda, junto a “Google Cloud”, haz clic en el selector de proyectos.
- “Nuevo proyecto” → pon un nombre (ej. “Preguntas Kaiden”) → Crear.
- Asegúrate de tener ese proyecto seleccionado.

### 3. Activar las APIs necesarias

- Menú ☰ → **APIs y servicios** → **Biblioteca**.
- Busca **“Google Sheets API”** → entra → **Activar**.
- Vuelve a Biblioteca, busca **“Google Drive API”** → entra → **Activar**.

### 4. Crear la cuenta de servicio y descargar el JSON (las “credenciales”)

- Menú ☰ → **APIs y servicios** → **Credenciales**.
- Arriba: **+ Crear credenciales** → **Cuenta de servicio**.
- Nombre: por ejemplo “streamlit-sheets”. Puedes dejar el resto por defecto → **Crear y continuar**.
- Rol: no es obligatorio para nuestro uso; puedes saltar o poner “Editor” si te lo pide → **Listo**.
- En la tabla de cuentas de servicio, haz clic en la que acabas de crear.
- Pestaña **Claves** → **Añadir clave** → **Crear clave**.
- Elige **JSON** → **Crear**. Se descargará un archivo `.json`.
- **Mueve ese archivo** a la carpeta del proyecto (`preguntas_kaiden`) y **renómbralo a `credentials.json`**.  
  (Ese archivo ya está en `.gitignore`, no lo subas a GitHub.)

### 5. Crear la hoja de cálculo y compartirla

- Entra en **[sheets.google.com](https://sheets.google.com)** y crea una hoja nueva (o usa una existente).
- Copia el **ID de la hoja** desde la URL:
  ```
  https://docs.google.com/spreadsheets/d/1ABC123xyz.../edit
                                      ^^^^^^^^^^^^^^^^
                                      este es el ID
  ```
- Abre el archivo `credentials.json` que descargaste. Busca la línea `"client_email"`. Verás algo como:
  `"client_email": "algo@nombre-del-proyecto.iam.gserviceaccount.com"`
- En Google Sheets, botón **Compartir** → en “Añadir personas”, pega ese **email** (el de `client_email`) → permiso **Editor** → Enviar.

### 6. Configurar el proyecto

- En la carpeta del proyecto, copia el ejemplo de variables de entorno:
  ```bash
  cp .env.example .env
  ```
- Edita `.env` y deja algo así (con tu ID real de la hoja):
  ```
  GOOGLE_CREDENTIALS_PATH=credentials.json
  GOOGLE_SHEET_ID=1ABC123xyz...
  ```

Con esto, al enviar respuestas en la app se guardarán en esa hoja de Google. Si no configuras Google, las respuestas se guardan en `respuestas.csv` en la carpeta del proyecto.

## Cómo cambiar las preguntas

Editá la lista `PREGUNTAS` en `app.py`. Cada elemento es un diccionario con `"pregunta"` y `"opciones"`:

```python
PREGUNTAS = [
    {
        "pregunta": "¿Tu pregunta?",
        "opciones": ["Opción A", "Opción B", "Opción C"],
    },
    # ...
]
```

## Estructura del proyecto

- `app.py` – App Streamlit (subir preguntas + formulario de respuestas).
- `sheets_helper.py` – Guardado en Google Sheets y CSV.
- `requirements.txt` – Dependencias.
- `.env.example` – Ejemplo de variables para Google (copiar a `.env`).
