"""
Конфигурационный файл
"""
import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv


load_dotenv()
token = "6998740889:AAECC8AcxxqlWVHBgIjuu3LQYS8Qj_LujKY"# os.getenv()
admin_password = "1"# os.getenv()

bot = Bot(token=token)
dp = Dispatcher()