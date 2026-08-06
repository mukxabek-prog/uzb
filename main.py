import os
import asyncio
import logging
import urllib.parse
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from deep_translator import GoogleTranslator

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men AI Generator botman. 🎬\n\n"
        "Menga o'zbekcha yoki inglizcha matn yuboring, men sizga harakatlanuvchi GIF/video tayyorlab beraman!"
    )

@dp.message(F.text)
async def generate_animation_handler(message: types.Message):
    user_prompt = message.text
    status_msg = await message.answer("⏳ Prompt tarjima qilinib, GIF/Video tayyorlanmoqda...")

    try:
        # 1. O'zbekcha promptni ingliz tiliga o'girish
        translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)
        encoded_prompt = urllib.parse.quote(translated_prompt)
        
        # 2. Harakatlanuvchi (GIF/Video) model linki
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&private=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    file_path = "output.png"
                    
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)

                    photo_file = FSInputFile(file_path)
                    await message.answer_photo(
                        photo=photo_file, 
                        caption=f"✨ **Sizning prompt:** {user_prompt}\n🔤 **AI tushungan matn:** {translated_prompt}"
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
