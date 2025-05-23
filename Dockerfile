FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para Chromium
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libatk1.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 \
    libxcomposite1 libxdamage1 libxrandr2 libxext6 libxfixes3 libx11-6 \
    libx11-xcb1 libxcb1 libxrender1 libxkbcommon0 libdbus-1-3 libexpat1 \
    libatspi2.0-0 libglib2.0-0 libgobject-2.0-0 libnspr4 libnss3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y Chromium
RUN pip install playwright && playwright install chromium

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar FastAPI en Cloud Run
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]