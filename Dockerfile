# ───────────────────────────────────────────────────────────────
# Imagen base con Python 3.10, Playwright y Chromium instalados
# ───────────────────────────────────────────────────────────────
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Crea directorio de trabajo
WORKDIR /app

# Copia el resto del proyecto
COPY . .

# Instala dependencias de Python de tu proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Puerto obligatorio para Cloud Run
EXPOSE 8080

# Lanza la API FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]