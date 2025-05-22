from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from .scraping import get_all_posts_data
from .notifier import enviar_webhook
from .gsheet import guardar_en_gsheet

app = FastAPI()

class ScrapeRequest(BaseModel):
    categoria: str
    webhook: str

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    if not request.categoria:
        return {"error": "No se recibió una categoría"}

    try:
        url = f"https://xepelin.com/blog/{request.categoria.lower().replace(' ', '-')}"
        posts_data = await get_all_posts_data(url)
        gsheet_url = guardar_en_gsheet(posts_data)
        enviar_webhook(request.webhook, gsheet_url, "rominabakulic@gmail.com")

        return { 
            "message": "Scrape exitoso.",
            "total": len(posts_data),
            "posts_data": posts_data
        }
    except Exception as e:
        return {"error": str(e)}
    
# https://hooks.zapier.com/hooks/catch/11217441/bfemddr