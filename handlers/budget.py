import asyncio

from data.config import load_config

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from handlers.echo import register_echo
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from handlers.my_functions import message_processing
from handlers.db import db_function


async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]

    await message.answer('\n'.join(text))


# Функция по чтению и отправки сообщения
async def get_message(message: types.Message):

    message_info = [message.chat.id, message.chat.username, message.chat.first_name, message.text, message.date]

    print(f'входящее сообщение от {message.chat.username}(id:{message.chat.id}):\n"{message.text}"')

    # Формирование текста для ответа
    message_processed = message_processing(message_info)
    print(f'Результат выполнения функции message_processing: {message_processed}')

    if message_processed[1]== '': # Значит нет ошибок

        list_to_db = message_processed[0]
        text_to_send = db_function(message_info,list_to_db)[1]
        print(f'Отправляемое сообщение:\n"{text_to_send}"')

    else:
        text_to_send = message_processed[1]

    # выполняю подключение к БД и загружаю туда данные, если connection_db = 1
    await message.answer(text_to_send)

def register_budget(dp: Dispatcher):
    dp.register_message_handler(get_message)
