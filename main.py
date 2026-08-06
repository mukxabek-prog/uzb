import os
import asyncio
import logging
import urllib.parse
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Telegram Bot Token (Render Environment Variables'dan olinadi)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men AI Generator botman. 🎬🎨\n\n"
        "Menga ingliz tilida matn (prompt) yuboring, men sizga rasmli animatsiya yaratib beraman!\n\n"
        "Masalan: *A cool cat walking on the beach with sunglasses*"
    )

@dp.message(F.text)
async def generate_media_handler(message: types.Message):
    prompt = message.text
    status_msg = await message.answer("⏳ Genratsiya jarayoni ketmoqda, kuting...")

    try:
        # Promptni URL formatiga o'tkazish
        encoded_prompt = urllib.parse.quote(prompt)
        # Bepul Pollinations AI generator manzili
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&seed=42"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    file_path = "output.jpg"
                    
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)

                    # Natijani Telegram'ga yuborish
                    photo_file = FSInputFile(file_path)
                    await message.answer_photo(
                        photo=photo_file, 
                        caption=f"✨ **Prompt:** {prompt}"
                    )
                    await status_msg.delete()
                else:
                    await status_msg.edit_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await status_msg.edit_text("❌ Serverda xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
