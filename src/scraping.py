from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from typing import List, Optional
import asyncio


async def load_all_posts(page, url) -> str:
    await page.goto(url, timeout=30000)
    selector = "main > div:last-child > div:first-child > div:last-child > button"

    while True:
        try:
            await page.wait_for_selector(selector, timeout=5000)
            await page.click(selector)
            await page.wait_for_timeout(1500)
        except PlaywrightTimeoutError:
            break

    return await page.content()


def get_urls(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for div in soup.find_all("div", class_="BlogArticle_box__JyD1X BlogArticle_boxSimple__KiPW6"):
        a_tag = div.find("a", href=True)
        if a_tag:
            urls.append(a_tag["href"])
    return urls


def get_post_data(html: str, fecha_publicacion: Optional[str]) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    if html:
        title = soup.find("h1", class_="ArticleSingle_title__0DNjm")
        category = soup.select_one(".ArticleSingle_wrapper__I9R7j > div:first-child > div:first-child > a")

        author = None
        author_container = soup.find("div", class_="ArticleSingle_authorImage__8FILj")
        if author_container and author_container.find_parent():
            siblings = author_container.find_parent().find_all("div", recursive=False)
            if len(siblings) >= 2:
                author_tag = siblings[1].find("div")
                author = author_tag.text.strip() if author_tag else None

        time_tag = soup.find("div", class_="Text_body__snVk8")
        time_to_read = time_tag.get_text(strip=True) if time_tag else None
        if time_to_read and "min" in time_to_read:
            parts = time_to_read.split("min")
            time_to_read = parts[0].strip() + " min"

        return {
            "titular": title.text.strip() if title else None,
            "categoria": category.text.strip() if category else None,
            "autor": author,
            "tiempo_lectura": time_to_read,
            "fecha_publicacion": fecha_publicacion,
        }
    
    return {
        "titular": "No se pudo obtener el título",
        "categoria": "No se pudo obtener la categoría",
        "autor": "No se pudo obtener el autor",
        "tiempo_lectura": "No se pudo obtener el tiempo de lectura",
        "fecha_publicacion": "No se pudo obtener la fecha de publicación",
    }


async def get_post_html(context, url: str) -> Optional[str]:
    for intento in range(3):
        try:
            page = await context.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=20000*(intento + 1))
            await page.wait_for_timeout(1500)
            html = await page.content()
            await page.close()
            return html
        except Exception as e:
            print(f"Intento {intento + 1}/3 fallido al procesar {url}: {e}")
            try:
                await page.close()
            except:
                pass  
            await asyncio.sleep(1)
    return None


async def get_all_posts_data(blog_url: str, url_to_lastmod: dict) -> List[dict]:
    posts_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        html = await load_all_posts(page, blog_url)
        urls = get_urls(html)
        await page.close()

        tasks = []
        for url in urls:
            tasks.append(get_post_html(context, url))

        html_results = await asyncio.gather(*tasks)
        print(f"Procesando {len(html_results)} posts...")

        for html, url in zip(html_results, urls):
            if html:
                fecha = url_to_lastmod.get(url, "N/D")
                post_data = get_post_data(html, fecha_publicacion=fecha)
                post_data["url"] = url
                posts_data.append(post_data)
            else:
                unknown_post_data = {
                    "titular": "No se pudo obtener el título",
                    "categoria": "No se pudo obtener la categoría",
                    "autor": "No se pudo obtener el autor",
                    "tiempo_lectura": "No se pudo obtener el tiempo de lectura",
                    "fecha_publicacion": "No se pudo obtener la fecha de publicación",
                    "url": url,
                }
                posts_data.append(unknown_post_data)

        print(f"Se procesaron {len(posts_data)} posts.")

        await browser.close()

    return posts_data