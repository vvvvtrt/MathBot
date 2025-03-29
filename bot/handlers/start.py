"""
Начальный блок
"""
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.start import start_kb
from config import dp, bot


@dp.callback_query(F.data == "start")
async def callback_start(callback_query: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите вашу роль:",
        reply_markup=start_kb()
    )


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Выберите вашу роль:", reply_markup=start_kb())
