import gspread
from typing import List
import google.auth            #



def guardar_en_gsheet(posts_data: List[dict]) -> str:

    spreadsheet_id = "1-NQtPvk6Knd7CHH7XjyCWxeSmxltc5-lCg4SWF__RcI"

    SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

    creds, _ = google.auth.default(scopes=SCOPES)

    client = gspread.authorize(creds)

    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.sheet1

    ws.clear()

    # Encabezados
    rows = [["Titular", "Categoría", "Autor",
                "Tiempo de lectura", "Fecha de modificación", "URL"]]

    # Agregar datos
    for post in posts_data:
            rows.append([
                post.get("titular"),
                post.get("categoria"),
                post.get("autor"),
                post.get("tiempo_lectura"),
                post.get("fecha_publicacion"),
                post.get("url"),
            ])

    # Cargar todos los datos en una sola llamada
    ws.update(f"A1:F{len(rows)}", rows)

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"