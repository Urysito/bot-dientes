import os
import asyncio
import random
from datetime import datetime
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- CONFIGURACIÓN ---
TOKEN   = os.environ.get("TELEGRAM_TOKEN")   # pon tu token aquí si no usas variables de entorno
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") # pon tu chat_id aquí si no usas variables de entorno

# Mensajes aleatorios para que no sea siempre igual
MENSAJES_TARDE = [
    "🦷 ¡Hora de lavarse los dientes! No lo dejes para luego.",
    "🪥 Recuerda: 2 minutos de cepillado, toda la tarde protegida.",
    "😁 ¡Dientes limpios, sonrisa feliz! Toca cepillarse.",
    "🦷 Tu yo del futuro te lo agradecerá. ¡A lavarse los dientes!",
]

MENSAJES_NOCHE = [
    "🌙 Antes de dormir... ¡los dientes! No te olvides.",
    "😴 Último recordatorio del día: cepíllate los dientes.",
    "🦷 No te vayas a la cama sin lavarte los dientes. ¡Venga!",
    "🌛 Buenas noches (después de cepillarte, claro 😄).",
]

async def enviar_recordatorio(mensajes: list):
    bot = Bot(token=TOKEN)
    mensaje = random.choice(mensajes)
    await bot.send_message(chat_id=CHAT_ID, text=mensaje)
    print(f"[{datetime.now().strftime('%H:%M')}] Mensaje enviado: {mensaje}")

async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Madrid")

    # Recordatorio tarde: hora aleatoria entre 15:00 y 15:59
    minuto_tarde = random.randint(0, 59)
    scheduler.add_job(
        enviar_recordatorio,
        "cron",
        hour=15,
        minute=minuto_tarde,
        args=[MENSAJES_TARDE],
    )

    # Recordatorio noche: hora aleatoria entre 00:00 y 00:59
    minuto_noche = random.randint(0, 59)
    scheduler.add_job(
        enviar_recordatorio,
        "cron",
        hour=0,
        minute=minuto_noche,
        args=[MENSAJES_NOCHE],
    )

    scheduler.start()
    print(f"✅ Bot arrancado. Recordatorio tarde: 15:{minuto_tarde:02d} | Noche: 00:{minuto_noche:02d}")

    # Mantener el proceso vivo
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
