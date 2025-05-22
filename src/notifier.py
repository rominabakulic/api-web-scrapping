import requests

def enviar_webhook(webhook_url: str, gsheet_url: str, email: str):
    body = {
        "email": email,
        "link": gsheet_url
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=body, headers=headers)
    print("Respuesta webhook:", response.text)