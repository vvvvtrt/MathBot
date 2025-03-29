"""
Обработчики для ученика
"""
from aiogram import F
from aiogram.types import CallbackQuery

from bot.keyboards.student import student_kb
from config import bot, dp


@dp.callback_query(F.data == "student")
async def student(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Это твоя домашняя страница тут ты можешь...",
        reply_markup=student_kb()
    )

# todo добавить получение узоров и их вывод в цикле


@dp.callback_query(F.data == "look_patterns")
async def look_patterns(callback: CallbackQuery):
    # todo добавить получение узоров и их вывод в цикле
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Доступные темы/узоры:",
        reply_markup=student_kb()
    )

# @dp.callback_query_handler(F.data == "student_exercises")
# async def student_exercises(callback: CallbackQuery):
#     #TODO добавить вывод картинок с заданиями
