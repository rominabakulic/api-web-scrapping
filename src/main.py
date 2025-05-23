from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

import requests
from xml.etree import ElementTree

from .scraping import get_all_posts_data
from .notifier import enviar_webhook
from .gsheet import guardar_en_gsheet

app = FastAPI()

class ScrapeRequest(BaseModel):
    categoria: str
    webhook: str


class ScrapeAllRequest(BaseModel):
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
    
@app.post("/scrape/all")
async def scrape_all(request: ScrapeAllRequest):
    sitemap_url = "https://xepelin.com/sitemap.xml"

    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        sitemap_xml = response.text

        root = ElementTree.fromstring(sitemap_xml)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall(".//ns:loc", ns)]

        categorias = set()
        for url in urls:
            if "xepelin.com/blog/" in url:
                parts = url.split("/")
                idx = parts.index("blog")
                if idx + 1 < len(parts):
                    categorias.add(parts[idx + 1])

        all_posts = []
        for categoria in categorias:
            url = f"https://xepelin.com/blog/{categoria}"
            try:
                posts = await get_all_posts_data(url)
                all_posts.extend(posts)
            except Exception as e:
                print(f"Error scrapeando {categoria}: {e}")

        gsheet_url = guardar_en_gsheet(all_posts)

        enviar_webhook(request.webhook, gsheet_url, "rominabakulic@gmail.com")

        return {
            "message": "Scrape de todas las categorías completado.",
            "categorias_detectadas": list(categorias),
            "posts_totales": len(all_posts),
            "gsheet": gsheet_url
        }

    except Exception as e:
        return {"error": str(e)}