"""
Конфигурационный файл
"""
import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv


load_dotenv()
token = "6854770104:AAHuY8IwSJy4-dOsWFdNjT9LvJZgq858oNM"# os.getenv()
admin_password = "1"# os.getenv()

bot = Bot(token=token)
dp = Dispatcher()