# Configurar secretos en Streamlit Cloud

## ⚠️ NUNCA subas `credentials.json` a GitHub

El archivo `credentials.json` contiene credenciales privadas y ya está en `.gitignore`. **No lo subas al repositorio.**

## Pasos para deployar en Streamlit Cloud

### 1. Subí tu código a GitHub (sin `credentials.json`)

```bash
git add .
git commit -m "Configurar app para Streamlit Cloud"
git push
```

### 2. Deployá en Streamlit Cloud

1. Entrá a [share.streamlit.io](https://share.streamlit.io)
2. Conectá tu cuenta de GitHub
3. Seleccioná tu repositorio: `preguntas_respuestas`
4. Archivo principal: `app.py`
5. Clic en **Deploy**

### 3. Configurá los Secrets

1. En tu app deployada, clic en **⚙️ Settings** (esquina superior derecha)
2. En el menú lateral: **Secrets**
3. Pegá esto (reemplazando con tus valores reales de `credentials.json`):

```toml
# ID de tu Google Sheet (está en la URL)
GOOGLE_SHEET_ID = "16DUuD1JT3RxTZGKbt3lN7uX0CQypD14N80e0zfvsuj4"

# Credenciales de tu cuenta de servicio
[gcp_service_account]
type = "service_account"
project_id = "gen-lang-client-0371741674"
private_key_id = "tu-private-key-id-aqui"
private_key = "-----BEGIN PRIVATE KEY-----\nTU-CLAVE-PRIVADA-COMPLETA-AQUI\n-----END PRIVATE KEY-----\n"
client_email = "kaiden@gen-lang-client-0371741674.iam.gserviceaccount.com"
client_id = "tu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "tu-cert-url"
universe_domain = "googleapis.com"
```

**Importante:**
- Copiá los valores exactos de tu `credentials.json`
- La `private_key` debe incluir `\n` para los saltos de línea (Streamlit los convierte automáticamente)
- Guardá los secrets

### 4. Reiniciá la app

Después de guardar los secrets, la app se reiniciará automáticamente y podrá escribir en tu Google Sheet.

---

## Verificar que funcione

1. Abrí tu app en Streamlit Cloud
2. Completá el formulario con tu email
3. Enviá las respuestas
4. Verificá en tu Google Sheet que aparezca la nueva fila

## Troubleshooting

**Si da error de credenciales:**
- Verificá que copiaste todos los campos correctamente
- Asegurate de que la `private_key` empiece con `"-----BEGIN PRIVATE KEY-----\n` y termine con `\n-----END PRIVATE KEY-----\n"`
- La cuenta de servicio (`client_email`) debe tener permiso de **Editor** en la Google Sheet

**Si da timeout:**
- En Streamlit Cloud no debería haber problemas de red (a diferencia de local)
- Verificá que el `GOOGLE_SHEET_ID` sea correcto
