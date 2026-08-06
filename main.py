import os
import asyncio
import logging
import urllib.parse
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from deep_translator import GoogleTranslator

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men AI Video Generator botman. 🎬\n\n"
        "Menga o'zbekcha matn yuboring, men sizga harakatlanuvchi **GIF / Video** tayyorlab beraman!"
    )

@dp.message(F.text)
async def generate_video_handler(message: types.Message):
    user_prompt = message.text
    status_msg = await message.answer("⏳ Video tayyorlanmoqda, iltimos kuting...")

    try:
        # 1. O'zbekcha promptni ingliz tiliga tarjima qilamiz
        translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)
        encoded_prompt = urllib.parse.quote(translated_prompt)
        
        # 2. Bepul ochiq Video API'ga so'rov yuboramiz (mp4/gif video qaytaradi)
        video_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&nologo=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status == 200:
                    video_bytes = await response.read()
                    file_path = "output.mp4"
                    
                    with open(file_path, "wb") as f:
                        f.write(video_bytes)

                    video_file = FSInputFile(file_path)
                    
                    # 3. Videoni Telegram'ga yuborish
                    await message.answer_animation(
                        animation=video_file,
                        caption=f"🎬 **Prompt:** {user_prompt}\n🔤 **AI o'qigan matn:** {translated_prompt}"
                    )
                    await status_msg.delete()
                else:
                    await status_msg.edit_text("❌ Serverdan video olishda xatolik yuz berdi.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await status_msg.edit_text("❌ Videoni yaratishda xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
