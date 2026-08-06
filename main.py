import os
import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

# Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
SMM_API_KEY = os.getenv("SMM_API_KEY")  # SMM Panel API Key
SMM_API_URL = "https://justanotherpanel.com/api/v2"  # O'zingiz ishlatadigan SMM Panel API linki

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Asosiy tugmalar (Menu)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Buyurtma berish"), KeyboardButton(text="💰 Balansim")],
        [KeyboardButton(text="📊 Xizmatlar narxi"), KeyboardButton(text="👨‍💻 Qo'llab-quvvatlash")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Salom, **{message.from_user.first_name}**! 👋\n"
        "**Nakrutka Bot**ga xush kelibsiz. Kanal va profillaringizni osongina rivojlantiring!",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )

# SMM Panelga API so'rov yuboruvchi funksiya
async def create_smm_order(service_id: int, link: str, quantity: int):
    payload = {
        'key': SMM_API_KEY,
        'action': 'add',
        'service': service_id,
        'link': link,
        'quantity': quantity
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(SMM_API_URL, data=payload) as resp:
            return await resp.json()

# Buyurtma berish tugmasi bosilganda
@dp.message(F.text == "🚀 Buyurtma berish")
async def order_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Telegram Obunachi", callback_data="serv_tg_sub")],
        [InlineKeyboardButton(text="👁 Telegram Ko'rishlar (Views)", callback_data="serv_tg_view")],
        [InlineKeyboardButton(text="❤️ Instagram Layklar", callback_data="serv_insta_like")]
    ])
    await message.answer("Kerakli xizmat turini tanlang:", reply_markup=kb)

# Balansni ko'rish
@dp.message(F.text == "💰 Balansim")
async def show_balance(message: types.Message):
    # Bu yerda ma'lumotlar bazasidan (Database) foydalanuvchi balansini chiqarasiz
    user_balance = 0  # Misol uchun 0 so'm
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Balansni to'ldirish", callback_data="top_up")]
    ])
    await message.answer(f"💵 Sizning balansingiz: **{user_balance} so'm**", reply_markup=kb, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
