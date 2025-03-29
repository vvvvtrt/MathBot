"""
Конфигурационный файл
"""
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TG_TOKEN')
admin_password = os.getenv('ADMIN_PASSWORD')

bot = Bot(token=token)
dp = Dispatcher()
