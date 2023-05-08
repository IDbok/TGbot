import asyncio
import logging

# from aiogram.contrib.fsm_storage.redis import MemoryStorege
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data.config import load_config

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# from my_functions import message_processing
# from db2 import db_function



# # Функция по чтению и отправки сообщения
# @dp.message_handler()
# async def get_message(message: types.Message):
#
#     # message_info = [message.chat.id, message.chat.username, message.chat.first_name, message.text, '05.05.2023']
#     message_info = [message.chat.id, message.chat.username, message.chat.first_name, message.text, message.date]
#     text_to_send = 'test'
#     print(f'входящее сообщение от {message.chat.username}(id:{message.chat.id}):\n"{message.text}"')
#
#
#     # Формирование текста для ответа
#     message_processed = message_processing(message_info)
#     print(f'Результат выполнения функции message_processing: {message_processed}')
#
#     if message_processed[1]== '': # Значит нет ошибок
#
#         list_to_db = message_processed[0]
#         text_to_send = db_function(message_info,list_to_db)[1]
#         print(f'Отправляемое сообщение:\n"{text_to_send}"')
#
#     else:
#         text_to_send = message_processed[1]
#
#     # выполняю подключение к БД и загружаю туда данные, если connection_db = 1
#
#     sent_message = await bot.send_message(chat_id=message_info[0], text=text_to_send)
#     # print(sent_message.to_python())
#
# executor.start_polling(dp)

logger = logging.getLogger(__name__) # __name__ - по идее это название файла в котором производится код, т.е. сейча это bot.py

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config('.env')

    bot = Bot(token=config.tg_bot.token ) # , parse_mode='HTML'
    # storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorege
    dp = Dispatcher(bot) # , storage = storage

    try:
        await dp.start_polling()
    finally:
        # await dp.storage.close()
        # await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Бот завершил работу')