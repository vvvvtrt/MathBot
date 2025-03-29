import os

from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение реквизитов из переменных окружения
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

# Формирование строки подключения
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"\
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
