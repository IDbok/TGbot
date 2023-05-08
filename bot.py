import asyncio

from data.config import load_config

from aiogram import Bot, Dispatcher, types
# from aiogram.utils import executor

# from handlers.echo import register_echo
from handlers.budget import register_budget

def register_all_handlers(dp):
     # register_echo(dp)
     register_budget(dp)


async def main():
    config = load_config('.env')

    bot = Bot(token=config.tg_bot.token) # , parse_mode='HTML'
    dp = Dispatcher(bot)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        # await dp.storage.close()
        # await dp.storage.wait_closed()
        # await bot.session.close()
        # await bot.get_session().close()
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
        # logger.error('Бот завершил работу')
