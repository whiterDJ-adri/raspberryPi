import os
from discord_webhook import DiscordWebhook

# Reemplaza 'TU_URL_DEL_WEBHOOK' con la URL que copiaste de Discord
def send_message(data):
    webhook = DiscordWebhook(
        url= os.getenv("WEBHOOK_DISCORD"),
        content=f"¡Nueva foto capturada! \n Hora: {data['date']}",
    )
    resp = webhook.execute()
    status = getattr(resp, "status_code", 200)
    if status not in (200, 204):
        raise RuntimeError(f"Error enviando a Discord: {status}")
    return {"msg": "Mensaje enviado a Discord", "status": status}
