import os
import httpx
import schedule
import time
from fastapi import FastAPI
from telegram import Bot
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
app = FastAPI()

products = [
    {"name": "منتج 1", "url": "ضع_رابط_المنتج_هنا"},
]

async def check_prices():
    async with httpx.AsyncClient() as client:
        for p in products:
            try:
                r = await client.get(p["url"], timeout=20)
                soup = BeautifulSoup(r.text, "html.parser")
                price = soup.find("span", class_="price").text.strip()
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{p['name']}: {price}")
            except Exception as e:
                print(f"Error: {e}")

def job():
    import asyncio
    asyncio.run(check_prices())

schedule.every().day.at("09:00").do(job)

@app.get("/")
def read_root():
    return {"status": "Monitor Masr is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
