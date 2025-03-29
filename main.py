import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import questions, different_types
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(questions.router, different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
