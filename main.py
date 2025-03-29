import asyncio
import logging

from config import dp, bot
from bot.handlers import student
from bot.handlers import teacher
from bot.handlers import start


logging.basicConfig(level=logging.DEBUG)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
