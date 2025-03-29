"""
Обработчики для учителя
"""
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import config
from bot.keyboards.start import start_kb
from bot.keyboards.teacher import teacher_kb, teacher_login_kb, return_to_login_kb, return_to_menu_kb, \
    look_or_add_patterns_kb
from config import bot, dp
from aiogram.types import CallbackQuery, Message


class AuthState(StatesGroup):
    wait = State()


class PatternState(StatesGroup):
    wait = State()


@dp.callback_query(F.data == "teacher_login")
async def teacher_login(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Для начала вам нужно войти.\nКак вы бы хотели это сделать?",
        reply_markup=teacher_login_kb()
    )


@dp.callback_query(F.data == "check_device")
async def teacher_login_by_id(callback: CallbackQuery):
    db_admin_id = 1  # todo вставить проверку айдишника из бд
    if db_admin_id == callback.from_user.id:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Добро пожаловать!\nЭто ваша домашняя страница тут вы можете...",
            reply_markup=teacher_kb()
        )
    else:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Зачем врать? =(",
            reply_markup=return_to_login_kb()
        )


@dp.callback_query(F.data == "password")
async def teacher_login_by_password(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Введите пароль",
        reply_markup=return_to_login_kb()
    )
    await state.update_data(call=callback)
    await state.set_state(AuthState.wait)


@dp.message(StateFilter(AuthState.wait))
async def password_typing(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.delete()
    await validate_password(state)


async def validate_password(state: FSMContext):
    data = await state.get_data()
    password = data["password"]
    call = data["call"]

    # todo достать пароли из бд (желательно все, потому что вход по паролю для того и нужен, что у тя нет конкретного айдишника)
    db_password = config.admin_password
    if password == db_password:  # должно быть if password in db_passwords
        await call.message.edit_text(
            text="Добро пожаловать!\nЭто ваша домашняя страница тут вы можете...",
            reply_markup=teacher_kb()
        )
    else:
        await call.message.edit_text(
            text="Пароль неверный =(",
            reply_markup=return_to_login_kb()
        )


@dp.callback_query(F.data == "teacher")
async def teacher(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Это ваша домашняя страница тут вы можете...",
        reply_markup=teacher_kb()
    )


@dp.callback_query(F.data == "look_or_add_patterns")
async def look_or_add_patterns(callback: CallbackQuery, state: FSMContext):
    await state.update_data(call=callback)
    await display_patterns(state)


async def display_patterns(state: FSMContext):
    data = await state.get_data()
    call = data["call"]
    new_pattern = data.get("new_pattern", "")

    if new_pattern == "":
        # todo запрос из бд на все добавленные рисунки
        db_request = ["Хохма", "Хохма", "Хохма", "Хохма"]
        patterns_str = "\n".join([i for i in db_request])
        await call.message.edit_text(
            text="Ваши узоры: \n" + patterns_str,
            reply_markup=look_or_add_patterns_kb()
        )
    else:
        # todo запись нового паттерна в бд мб
        # db_request = [] #с возвратом всех паттернов если хотим сразу и отображать после добавления
        # patterns_str = "\n".join([i for i in db_request])
        await call.message.edit_text(
            text="Новый узор успешно добавлен\n\n",
            reply_markup=return_to_menu_kb()
        )
    await state.clear()


@dp.callback_query(F.data == "add_pattern")
async def add_pattern(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Введите новый паттерн",
        reply_markup=return_to_menu_kb()
    )
    await state.update_data(call=callback)
    await state.set_state(PatternState.wait)


@dp.message(StateFilter(PatternState.wait))
async def pattern_typing(message: Message, state: FSMContext):
    await state.update_data(new_pattern=message.text)
    await message.delete()
    await display_patterns(state)


@dp.callback_query(F.data == "home_tasks")
async def home_tasks(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Напишите по каким узорам дать дз",
        reply_markup=return_to_menu_kb()
    )
