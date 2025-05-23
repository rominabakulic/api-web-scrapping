# Xepelin Blog Scraper API

Este proyecto expone una API desarrollada con FastAPI que permite scrapear artículos del blog de Xepelin por categoría o por todas las categorías automáticamente (usando el sitemap). Los datos se almacenan en un Google Spreadsheet y se notifica a un webhook con el resultado.


## Endpoints disponibles

### 1. /scrape

Scrapea todos los artículos de una categoría específica del blog.
- Método: POST
- Body:
```
{
  "categoria": "corporativos",
  "webhook": "https://hooks.zapier.com/hooks/catch/..."
}
```
- Respuesta:
```
{
  "message": "Scrape exitoso.",
  "total": 15,
  "gsheet": "https://docs.google.com/spreadsheets/...",
  "posts_data": [...]
}
```


### 2. /scrape/all

Scrapea todas las categorías detectadas en el sitemap del sitio.
- Método: POST
- Body:
```
{
  "webhook": "https://hooks.zapier.com/hooks/catch/..."
}
```
 - Respuesta:
```
{
  "message": "Scrape de todas las categorías completado.",
  "categorias_detectadas": [...],
  "posts_totales": 80,
  "gsheet": "https://docs.google.com/spreadsheets/..."
}
```


### Datos extraídos

Por cada artículo, se extraen los siguientes campos:
- Titular
- Categoría
- Autor
- Tiempo de lectura
- Fecha de modificación (desde el sitemap)
- URL del artículo

Todos los datos se almacenan en un Google Spreadsheet accesible mediante link público.

### Requisitos
- Python 3.10+
- Playwright
- FastAPI
- Google Cloud credentials con acceso a Google Sheets API

Instalación local
```
pip install -r requirements.txt
playwright install chromium
```
Variables necesarias
- credentials.json (archivo de servicio de Google API)
- El archivo debe compartirse con el Google Sheet que se utilizará


Docker (opcional)
```
docker build -t xepelin-scraper .
docker run -p 8080:8080 xepelin-scraper
```


Ejemplo curl
```
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"categoria": "corporativos", "webhook": "https://hooks.zapier.com/hooks/catch/..."}'
```

⸻

Créditos

Desarrollado por Romina Bakulic como prueba técnica para Xepelin.

