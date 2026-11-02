import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Render port talab qilgani uchun kichik fon serveri
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Fon rejimida serverni ishga tushirish
threading.Thread(target=run_web_server, daemon=True).start()
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import yt_dlp

# Loggingni yoqish
logging.basicConfig(level=logging.INFO)

# @BotFather'dan olgan tokeningizni quyidagi 'SIZNING_TOKENINGIZ' o'rniga yozasiz
TOKEN = "8870625481:AAG_4LPvShRx1d_L3MOK281vo1uiKb-jZWQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Salom! Men All-in-One Media Yuklovchi botman.\n\n"
        "Menga Instagram, TikTok yoki YouTube havolasini (linkini) yuboring, men sizga videoni yuklab beraman!"
    )

@dp.message(F.text.startswith("http"))
async def download_media(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Video yuklab olinmoqda, biroz kuting...")

    # yt-dlp sozlamalari
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Videoni foydalanuvchiga yuborish
        video = types.FSInputFile("downloaded_video.mp4")
        await message.answer_video(video, caption="Marhamat, siz so'ragan video! 📥")
        
        # Serverda faylni tozalash
        if os.path.exists("downloaded_video.mp4"):
            os.remove("downloaded_video.mp4")
            
    except Exception as e:
        await message.answer(f"❌ Kechirasiz, videoni yuklab bo'lmadi. Havola to'g'riligiga ishonch hosil qiling.\nXatolik: {str(e)}")
        if os.path.exists("downloaded_video.mp4"):
            os.remove("downloaded_video.mp4")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
