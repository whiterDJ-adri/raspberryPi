import os
from discord_webhook import DiscordWebhook
from datetime import datetime
from zoneinfo import ZoneInfo


def send_message(data):
    
    # Parsear la fecha que llega en data['date']
    
    # Ejemplo: si tu 'date' viene como string ISO "2025-10-09T15:30:00"
    data_time_formateada = datetime.fromisoformat(data["date"])

    
    # Convertir a hora de Madrid
    hora_madrid = data_time_formateada.astimezone(ZoneInfo("Europe/Madrid"))
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
