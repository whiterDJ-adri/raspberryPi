import os
from discord_webhook import DiscordWebhook
from datetime import datetime
import pytz 


def send_message(data):
    zona_madrid = pytz.timezone("Europe/Madrid")
    data_time_formateada = datetime.fromisoformat(data["date"])

    hora_madrid = data_time_formateada.astimezone(zona_madrid)
    hora_formateada = hora_madrid.strftime("%d/%m/%Y %H:%M:%S")

    webhook = DiscordWebhook(
        url=os.getenv("WEBHOOK_DISCORD"),
        content=f"¡Nueva foto capturada! \n Hora: {hora_formateada} Filename: {data['filename']}",
    )

    resp = webhook.execute()
    status = getattr(resp, "status_code", 200)
    if status not in (200, 204):
        raise RuntimeError(f"Error enviando a Discord: {status}")
    return {"msg": "Mensaje enviado a Discord", "status": status}
