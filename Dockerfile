# Dockerfile
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instalar playwright + dependencias de Chromium
RUN pip install playwright && playwright install chromium

# Crear y moverse al directorio de la app
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto expuesto por uvicorn
EXPOSE 8080

# Comando para ejecutar FastAPI en Cloud Run
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]