import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from deep_translator import GoogleTranslator
from gradio_client import Client

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men AI Video Generator botman. 🎬\n\n"
        "Menga o'zbekcha matn yuboring, men sizga **haqiqiy MP4 video** tayyorlab beraman!\n\n"
        "Masalan: *Suv ostida suzib yurgan rang-barang baliqlar*"
    )

@dp.message(F.text)
async def generate_video_handler(message: types.Message):
    user_prompt = message.text
    status_msg = await message.answer("⏳ Prompt tarjima qilinib, video generatsiya bo'lmoqda (1-2 daqiqa kuting)...")

    try:
        # 1. O'zbekcha promptni ingliz tiliga tarjima qilish
        translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)

        # 2. AI Video modelga so'rov yuborish (Async thread ichida)
        loop = asyncio.get_running_loop()
        
        def call_video_ai():
            # Bepul va ochiq video generator model
            client = Client("ZeroScope/ZeroScope_v2_XL")
            result = client.predict(
                translated_prompt,
                api_name="/predict"
            )
            return result

        # Video yo'lini olish
        video_path = await loop.run_in_executor(None, call_video_ai)

        if video_path and os.path.exists(video_path):
            # 3. Videoni Telegram'ga .mp4 formatda yuborish
            video_file = FSInputFile(video_path)
            await message.answer_video(
                video=video_file, 
                caption=f"🎬 **Prompt:** {user_prompt}\n🔤 **AI o'qigan matn:** {translated_prompt}"
            )
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Videoni yaratishda xatolik yuz berdi.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await status_msg.edit_text("❌ Server band yoki xatolik yuz berdi. Qaytadan urinib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
