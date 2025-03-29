"""
Клавиатуры для ученика
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def student_kb():
    buttons = [
        [InlineKeyboardButton(text="Посмотреть задания",
                              callback_data="student_exercises")],
        [InlineKeyboardButton(text="Посмотреть узоры",
                              callback_data="look_patterns")],
        [InlineKeyboardButton(text="Назад", callback_data="start")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
