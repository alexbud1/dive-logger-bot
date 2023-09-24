import asyncio
import logging
import os
import sys
from os.path import dirname, join

from aiogram import Bot, Dispatcher, F, Router, types
from dotenv import load_dotenv
from handlers import commands, fill_profile
from callbacks import callbacks

# .env adjustments
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


async def main() -> None:
    API_TOKEN = os.environ.get("API_TOKEN")
    bot = Bot(token=API_TOKEN, parse_mode="HTML")

    dp = Dispatcher()
    # Include routers from handlers/ they will be entered as A -> B -> C
    dp.include_routers(commands.router, callbacks.router, fill_profile.router)

    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
