import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from common.bot_cmd_lst import private

from handlers.user_private import user_private_router
from handlers.whereami import whereami_router
from handlers.commission import commission_router
from handlers.dormitory import dormitory_router
from handlers.help_chat import send_to_group_router, group_adm_router

from handlers.update_db_key_ans import update_db_key_ans_router
from database.engine import create_db, drop_db, session_maker


from middlewares.db import DataBaseSession

bot = Bot(token=os.getenv("TOKEN"), parse_mode=ParseMode.HTML)


dp = Dispatcher()


dp.include_router(user_private_router)
dp.include_router(whereami_router)
dp.include_router(commission_router)
dp.include_router(dormitory_router)
dp.include_router(send_to_group_router)
dp.include_router(group_adm_router)
dp.include_router(update_db_key_ans_router)


async def on_startup(bot):
    await bot.send_message(1772168991, text="Бот запущен!")
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    await bot.send_message(1772168991, text="Бот остановлен!")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)



    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=private, scope=types.BotCommandScopeAllPrivateChats()
    )
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
