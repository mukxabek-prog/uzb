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
        "Menga matn yuboring, men sizga media tayyorlab beraman!"
    )

@dp.message(F.text)
async def generate_media_handler(message: types.Message):
    user_prompt = message.text
    status_msg = await message.answer("⏳ Generatsiya jarayoni ketmoqda...")

    # 1. Tarjimani xavfsiz qilish (Xatolik bo'lsa, asl textni oladi)
    try:
        translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)
        # Agar tarjima xato javob qaytarsa yoki ichida "Error" so'zi bo'lsa:
        if not translated_prompt or "Error 500" in translated_prompt or "There was an error" in translated_prompt:
            translated_prompt = user_prompt
    except Exception as t_err:
        logging.error(f"Tarjima xatosi: {t_err}")
        translated_prompt = user_prompt

    try:
        # 2. Promptni URL formatiga o'tkazish
        encoded_prompt = urllib.parse.quote(translated_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&private=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    media_bytes = await response.read()
                    file_path = "output.jpg"
                    
                    with open(file_path, "wb") as f:
                        f.write(media_bytes)

                    photo_file = FSInputFile(file_path)
                    
                    await message.answer_photo(
                        photo=photo_file, 
                        caption=f"✨ **Siz yuborgan matn:** {user_prompt}\n🔤 **AI tayyorlagan prompt:** {translated_prompt}"
                    )
                    await status_msg.delete()
                else:
                    await status_msg.edit_text("❌ Serverdan javob olishda xatolik yuz berdi.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await status_msg.edit_text("❌ Xatolik yuz berdi, qaytadan urinib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
